import pty
import subprocess
from subprocess import CompletedProcess

import pytest


@pytest.mark.parametrize("cmd", ["ssh", "scp"])
def test_if_epsmp_provides_correct_input(cmd: str):
    """Test if epsmp works properly when asked for input"""

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
        check=False,
    )

    assert process.returncode == 0


def test_if_epsmp_shows_usage_with_incorrect_arguments():
    """Test if epsmp exits with error and shows usage
    when passed incorrect command argument"""

    cmd_str: str = """
        /usr/bin/env bash -c '
            source .venv/bin/activate;
            python epsmp.py nocommand --debug dummyhost
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
        check=False,
    )

    assert process.returncode == 2
    assert "usage: epsmp.py [-h] [--debug] {ssh,scp}" in process.stderr
    assert "(choose from 'ssh', 'scp')" in process.stderr
