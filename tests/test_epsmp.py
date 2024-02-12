import pty
import re
import subprocess
import traceback
from subprocess import CompletedProcess

import pexpect
import pytest
from pytest import MonkeyPatch

from ecmd import EasyCommand
from epsmp import main


class EasySSHMock(EasyCommand):
    def __init__(self, binary: str = "cat") -> None:
        self.binary = binary

    def get_binary(self) -> str:
        return self.binary

    def get_arguments(self) -> list:
        return []


class SpawnMock:
    def __init__(self, *args, **kwargs) -> None:
        self.index = kwargs.get("index")
        self.exitstatus = kwargs.get("exitstatus")
        self.raise_timeout = kwargs.get("raise_timeout")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

    def setwinsize(self, *args, **kwargs):
        pass

    def expect(self, *args, **kwargs):
        if self.raise_timeout:
            raise pexpect.exceptions.TIMEOUT("Raising TIMEOUT")

        return self.index

    def sendline(self, *args, **kwargs):
        pass

    def interact(self):
        pass

    def close(self):
        pass


def test_if_psmp_main_ssh_logs_in(monkeypatch: MonkeyPatch) -> None:

    def mock_get(*args, **kwargs) -> SpawnMock:
        return SpawnMock(index=3, exitstatus=0)

    monkeypatch.setattr("epsmp.get_terminal_size", lambda: (100, 20))
    monkeypatch.setattr("pexpect.spawn", mock_get)

    ssh_obj = EasySSHMock()
    ec: int = main("ssh", ssh_obj, [])

    assert ec == 0


def test_if_psmp_main_scp_start_copy(monkeypatch: MonkeyPatch) -> None:

    def mock_get(*args, **kwargs) -> SpawnMock:
        return SpawnMock(index=4, exitstatus=0)

    monkeypatch.setattr("epsmp.get_terminal_size", lambda: (100, 20))
    monkeypatch.setattr("pexpect.spawn", mock_get)

    ssh_obj = EasySSHMock()
    ec: int = main("scp", ssh_obj, [])

    assert ec == 0


def test_if_psmp_main_exits_on_EOF(monkeypatch: MonkeyPatch) -> None:

    def mock_get(*args, **kwargs) -> SpawnMock:
        return SpawnMock(index=5, exitstatus=0)

    monkeypatch.setattr("epsmp.get_terminal_size", lambda: (100, 20))
    monkeypatch.setattr("pexpect.spawn", mock_get)

    ssh_obj = EasySSHMock()
    ec: int = main("ssh", ssh_obj, [])

    assert ec == 0


def test_if_psmp_main_exits_on_TIMEOUT(monkeypatch: MonkeyPatch) -> None:

    def mock_get(*args, **kwargs) -> SpawnMock:
        return SpawnMock(raise_timeout=True)

    monkeypatch.setattr("epsmp.get_terminal_size", lambda: (100, 20))
    monkeypatch.setattr("pexpect.spawn", mock_get)

    ssh_obj = EasySSHMock()
    ec: int = main("ssh", ssh_obj, [])

    assert ec == 1


def test_if_psmp_main_raise_exception_and_exits_with_1(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr("epsmp.get_terminal_size", lambda: (100, 20))

    ssh_obj = EasySSHMock("nocommand")
    ec: int = main("ssh", ssh_obj, ["host"])

    assert ec == 1


@pytest.mark.parametrize("cmd", ["ssh", "scp"])
def test_func_if_epsmp_provides_correct_input(cmd: str, create_test_config) -> None:
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


def test_func_if_epsmp_shows_usage_with_incorrect_arguments(create_test_config) -> None:
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

    regex = (
        r"^usage: epsmp.py.*argument cmd: invalid choice.*\(choose from 'ssh', 'scp'\)$"
    )
    assert re.search(regex, process.stderr, re.S | re.M)
