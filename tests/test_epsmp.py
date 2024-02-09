import pty
import subprocess
from subprocess import CompletedProcess

import pytest


@pytest.mark.parametrize("cmd", ["ssh", "scp"])
def test_epsmp(cmd: str):

    cmd_str: str = f"""
        /usr/bin/env bash -c '
            source .venv/bin/activate;
            python epsmp.py {cmd} --debug dummyhost
        '
    """

    _, child_fd = pty.openpty()
    process: CompletedProcess = subprocess.run(
        cmd_str,
        stdin=child_fd,
        stdout=child_fd,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )

    assert process.returncode == 0
