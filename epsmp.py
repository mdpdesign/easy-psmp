import argparse
import fcntl
import logging
import os
import signal
import struct
import sys
import termios

from typing import Any

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


def main(ecmd: EasyCommand, argv: list) -> int:
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
    def sigwinch_passthrough(sig: int, data: Any) -> None:
        if not child.closed:
            child.setwinsize(*get_terminal_size())

    logger = logging.getLogger("epsmp-logger")
    binary: str = ecmd.get_binary()
    opts: list = ecmd.get_arguments()

    try:
        with pexpect.spawn(binary, opts + argv, encoding="utf-8") as child:

            logger.debug(f"Using {binary} binary, with arguments: {opts + argv}")
            logger.debug(f"Setting child size {get_terminal_size()} and SIGWINCH")

            child.logfile_read = sys.stdout
            child.setwinsize(*get_terminal_size())
            signal.signal(signal.SIGWINCH, sigwinch_passthrough)

            logger.debug(f"Starting expect")

            child.expect("[Pp]assword:")
            child.sendline(os.getenv("EPSMP_PSW"))

            child.expect_exact("RADIUS challenge:")
            child.sendline(
                pyotp.TOTP(os.getenv("EPSMP_TOTP_SECRET"), digits=6, interval=30).now()
            )

            child.expect_exact("reason for this operation:")
            child.sendline("BAU")

            child.logfile_read = None
            child.interact()

        logger.debug("Finished expect, everything OK")
        return 0
    except:
        logger.debug("Failed to execute expect", exc_info=True)
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
    debug: bool = any([args.debug, os.getenv("EPSMP_DEBUG", False)])

    logger = logging.getLogger("epsmp-logger")
    logging.basicConfig(
        filename="epsmp-dbglog.log" if debug else None,
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    )

    ecmd: EasyCommand

    match args.cmd:
        case "ssh":
            ecmd = EasySSH()
        case "scp":
            ecmd = EasySCP()
        case _:
            raise AttributeError("Command not implemented")

    exit(main(ecmd, args_other))
