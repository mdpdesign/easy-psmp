import fcntl
import os
import signal
import struct
import sys
import termios

import pexpect
import pyotp
from dotenv import load_dotenv


def get_terminal_size() -> tuple:
    """Get current terminal size

    Returns:
        tuple: rows, cols for current terminal size
    """
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack("hhhh", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
    return a[0], a[1]


def main(args: any) -> int:
    """Performs non-interactive SSH login command to PSMP that requires
    providing interactively password, OTP and reason for login

    Args:
        args (any): Arguments passed to SSH command

    Returns:
        int: Exit code: 0 OK, 1 Error
    """

    # This function is inside the "main" to have access to "child" object that otherwise
    # would have to be a "global" object and we would have difficulties with context manager
    def sigwinch_passthrough(sig: int, data: any) -> None:
        if not child.closed:
            child.setwinsize(*get_terminal_size())

    ssh_bin: str = "ssh"
    ssh_opts: list = ["-o UserKnownHostsFile=/dev/null", "-o StrictHostKeyChecking=no"]

    try:
        load_dotenv()

        with pexpect.spawn(ssh_bin, ssh_opts + args[1:], encoding="utf-8") as child:
            child.logfile_read = sys.stdout
            child.setwinsize(*get_terminal_size())
            signal.signal(signal.SIGWINCH, sigwinch_passthrough)

            child.expect_exact("Vault Password:")
            child.sendline(os.getenv("ESSH_PSW"))
            child.expect_exact("RADIUS challenge:")
            child.sendline(
                pyotp.TOTP(os.getenv("ESSH_TOTP_SECRET"), digits=6, interval=30).now()
            )

            child.expect_exact("reason for this operation:")
            child.sendline("BAU")

            child.logfile_read = None
            child.interact()

        return 0
    except Exception as e:
        print(f"Exception:\n{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
