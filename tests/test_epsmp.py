import os
import pathlib
import pty
import re
import subprocess
from subprocess import CompletedProcess

import pyotp
import pytest
import yaml

from epsmp import main
from essh import EasySSH


@pytest.fixture(scope="function")
def create_test_config():
    # create file
    test_config = {
        "ssh": {
            "binary": "./tests/test_psmp.sh",
        },
        "scp": {
            "binary": "./tests/test_psmp.sh",
        },
    }
    file = open("epsmpcfg.yaml", "w", encoding="utf-8")
    file.write(yaml.dump(test_config))
    file.close()

    yield file

    # cleanup file
    pathlib.Path("epsmpcfg.yaml").unlink()


def test_if_psmp_main_exit_with_1_with_incorrect_host(create_test_config) -> None:
    _ = create_test_config
    os.environ["EPSMP_PSW"] = "vagrant"
    os.environ["EPSMP_TOTP_SECRET"] = pyotp.random_base32()

    ssh_obj = EasySSH()
    ec: int = main("ssh", ssh_obj, ["host"])

    assert ec == 1


@pytest.mark.parametrize("cmd", ["ssh", "scp"])
def test_if_epsmp_provides_correct_input(cmd: str, create_test_config):
    """Test if epsmp works properly when asked for input"""

    _ = create_test_config
    os.environ["EPSMP_PSW"] = "vagrant"
    os.environ["EPSMP_TOTP_SECRET"] = pyotp.random_base32()

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


def test_if_epsmp_shows_usage_with_incorrect_arguments(create_test_config):
    """Test if epsmp exits with error and shows usage
    when passed incorrect command argument"""

    _ = create_test_config
    os.environ["EPSMP_PSW"] = "vagrant"
    os.environ["EPSMP_TOTP_SECRET"] = pyotp.random_base32()

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

    regex = (
        r"^usage: epsmp.py.*argument cmd: invalid choice.*\(choose from 'ssh', 'scp'\)$"
    )
    assert re.search(regex, process.stderr, re.S | re.M)
