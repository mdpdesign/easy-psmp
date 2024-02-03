import fcntl
import os
import signal
import struct
import sys
import termios
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

    binary: str = ecmd.get_binary()
    opts: list = ecmd.get_arguments()

    try:
        load_dotenv()

        with pexpect.spawn(binary, opts + args[2:], encoding="utf-8") as child:

            pprint(opts + args[2:])

            child.logfile_read = sys.stdout
            child.setwinsize(*get_terminal_size())
            signal.signal(signal.SIGWINCH, sigwinch_passthrough)

            child.expect("[Pp]assword:")
            child.sendline(os.getenv("ESSH_PSW"))

            # child.expect_exact("RADIUS challenge:")
            # child.sendline(
            #     pyotp.TOTP(os.getenv("ESSH_TOTP_SECRET"), digits=6, interval=30).now()
            # )

            # child.expect_exact("reason for this operation:")
            # child.sendline("BAU")

            child.logfile_read = None
            child.interact()

        return 0
    except Exception as e:
        print(f"Exception:\n{e}")
        return 1


if __name__ == "__main__":

    ecmd: EasyCommand

    match sys.argv[1]:
        case "ssh":
            ecmd = EasySSH()
        case "scp":
            ecmd = EasySCP()
        case _:
            raise NotImplementedError("This command is not implemented")

    sys.exit(main(ecmd, sys.argv))
