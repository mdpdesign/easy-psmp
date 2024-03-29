import argparse
import fcntl
import logging
import os
import signal
import struct
import sys
import termios
from logging import Logger
from typing import Any, Callable

import pexpect
import pyotp
from dotenv import load_dotenv

from ecmd import EasyCommand
from escp import EasySCP
from essh import EasySSH


def get_terminal_size() -> tuple:
    """Get current terminal size

    Returns:
        tuple: rows, cols for current terminal size
    """
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack("hhhh", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
    return a[0], a[1]


def main(cmd: str, ecmd: EasyCommand, argv: list) -> int:
    """Performs non-interactive SSH/SCP login command to PSMP that requires
    providing interactively password, OTP and reason for login

    Args:
        ecmd (EasyCommand): Specific command implementation to execute
        argv (list): Arguments passed to SSH/SCP command

    Returns:
        int: Exit code: 0 OK, 1 Error
    """

    # This function is inside the "main" to have access to "child" object that otherwise
    # would have to be a "global" object and we could have difficulties with context manager
    # pylint: disable=unused-argument
    def sigwinch_passthrough(sig: int, data: Any) -> None:
        if not child.closed:
            child.setwinsize(*get_terminal_size())

    logger: Logger = logging.getLogger("epsmp-logger")
    binary: str = ecmd.get_binary()
    opts: list = ecmd.get_arguments()

    try:
        with pexpect.spawn(binary, opts + argv, encoding="utf-8") as child:

            logger.debug("Using '%s' binary, with arguments: %s", binary, opts + argv)
            logger.debug("Setting child size %s and SIGWINCH", get_terminal_size())

            child.logfile_read = sys.stdout
            child.setwinsize(*get_terminal_size())
            signal.signal(signal.SIGWINCH, sigwinch_passthrough)

            logger.debug("Starting expect")

            # Beware of patterns to match:
            # If you pass a list of patterns and more than one matches, the first match in the stream is chosen.
            # https://pexpect.readthedocs.io/en/stable/api/pexpect.html#pexpect.spawn.expect
            expected_answers: dict = {
                "[Pp]assword:": lambda: child.sendline(os.getenv("EPSMP_PSW")),
                "[Mm]ulti-factor authentication is required.": lambda: child.sendline(
                    pyotp.TOTP(
                        os.getenv("EPSMP_TOTP_SECRET", ""), digits=6, interval=30
                    ).now()
                ),
                "[Rr]eason for this operation:": lambda: child.sendline("BAU"),
                # Special cases:
                # SSH Logged in - don't check other patterns
                "[#\\$] ": lambda: None,
                # SCP copying file
                "ETA": lambda: None,
                # Command finished/closed
                pexpect.EOF: lambda: None,
            }

            expected_answers_keys: list = list(expected_answers.keys())

            # This allows to "unblock" the prompt even if some expected prompts don't match
            for _ in expected_answers:
                try:
                    index: int = child.expect(expected_answers_keys)

                    if index >= 0:
                        the_key: Any = expected_answers_keys[index]

                        logger.debug("Matched expected: '%s'", the_key)

                        # Handle special cases - not the prettiest but it works 😅
                        # if command already finished - EOF
                        # if SSH is already logged in
                        # if SCP started copying file
                        # don't check other matches, break the loop
                        if the_key == pexpect.EOF:
                            logger.debug("Command '%s' closed - EOF", cmd)
                            break

                        if cmd == "ssh" and the_key == "[#\\$] ":
                            logger.debug("SSH logged in")
                            break

                        if cmd == "scp" and the_key == "ETA":
                            logger.debug("SCP logged in, copying..")
                            break

                        fn: Callable = expected_answers[the_key]
                        fn()
                except pexpect.exceptions.TIMEOUT:
                    logger.debug(
                        "=== Failed to execute expect, didn't match any of: %s, exiting!",
                        list(expected_answers.keys()),
                        exc_info=True,
                    )
                    child.close()
                    return 1

            logger.debug("Expect interact")
            child.logfile_read = None
            child.interact()

        logger.debug(
            "=== Finished expect, '%s' command exit code: %s", cmd, child.exitstatus
        )
        return child.exitstatus

    # pylint: disable=broad-exception-caught
    except Exception:
        logger.debug("=== Failed to execute expect, exiting!", exc_info=True)
        return 1


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cmd",
        help="Specify command to run, possible choices: %(choices)s",
        choices=["ssh", "scp"],
    )
    parser.add_argument(
        "--debug", help="Enable debug logging to local log file", action="store_true"
    )
    args, args_other = parser.parse_known_args()

    load_dotenv()

    # Note that setting EPSMP_DEBUG ENV var to any non-empty value will enable debug log
    debug: bool = any([args.debug, os.getenv("EPSMP_DEBUG")])

    logger: Logger = logging.getLogger("epsmp-logger")
    logging.basicConfig(
        filename="epsmp-dbglog.log" if debug else None,
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    )

    logger.debug("=== Starting '%s' script", sys.argv[0])

    ecmd: EasyCommand

    match args.cmd:
        case "ssh":
            ecmd = EasySSH()
        case "scp":
            ecmd = EasySCP()
        case _:
            raise AttributeError("Command not implemented")

    sys.exit(main(args.cmd, ecmd, args_other))
