import fcntl
import os
import signal
import struct
import sys
import termios
import logging
from pprint import pprint

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


def main(ecmd: EasyCommand, args: list) -> int:
    """Performs non-interactive SSH/SCP login command to PSMP that requires
    providing interactively password, OTP and reason for login

    Args:
        args (any): Arguments passed to SSH/SCP command

    Returns:
        int: Exit code: 0 OK, 1 Error
    """

    # This function is inside the "main" to have access to "child" object that otherwise
    # would have to be a "global" object and we would have difficulties with context manager
    def sigwinch_passthrough(sig: int, data: any) -> None:
        if not child.closed:
            child.setwinsize(*get_terminal_size())

    logger = logging.getLogger("epsmp-logger")
    binary: str = ecmd.get_binary()
    opts: list = ecmd.get_arguments()

    try:
        with pexpect.spawn(binary, opts + args[2:], encoding="utf-8") as child:

            logger.debug(f"Using {binary} binary, with arguments: {opts + args[2:]}")
            logger.debug(f"Setting child size {get_terminal_size()} and SIGWINCH")

            child.logfile_read = sys.stdout
            child.setwinsize(*get_terminal_size())
            signal.signal(signal.SIGWINCH, sigwinch_passthrough)

            logger.debug(f"Starting expect")

            child.expect("[Pp]assword:")
            child.sendline(os.getenv("EPSMP_PSW"))

            # child.expect_exact("RADIUS challenge:")
            # child.sendline(
            #     pyotp.TOTP(os.getenv("EPSMP_TOTP_SECRET"), digits=6, interval=30).now()
            # )

            # child.expect_exact("reason for this operation:")
            # child.sendline("BAU")

            child.logfile_read = None
            child.interact()

        logger.debug("Finished expect, everything OK")
        return 0
    except:
        logger.debug("Failed to execute expect", exc_info=True)
        return 1


if __name__ == "__main__":

    load_dotenv()

    debug: bool = os.getenv("EPSMP_DEBUG", False)
    logger = logging.getLogger("epsmp-logger")
    logging.basicConfig(
        filename="epsmp-dbglog.log" if debug else None,
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    )

    ecmd: EasyCommand

    # TODO: Possibly use argparse module for this...
    match sys.argv[1]:
        case "ssh":
            ecmd = EasySSH()
        case "scp":
            ecmd = EasySCP()
        case _:
            raise NotImplementedError(
                "Missing argument 'ssh' or 'scp', or this command is not implemented"
            )

    sys.exit(main(ecmd, sys.argv))
