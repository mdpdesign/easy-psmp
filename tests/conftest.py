import os
import pathlib
from typing import Any, Generator, TextIO

import pyotp
import pytest
import yaml


@pytest.fixture(scope="session", autouse=True)
def set_env_variables() -> None:
    os.environ["EPSMP_PSW"] = "vagrant"
    os.environ["EPSMP_TOTP_SECRET"] = pyotp.random_base32()


@pytest.fixture
def create_test_config() -> Generator[TextIO, Any, None]:
    # create file
    test_config: dict = {
        "ssh": {
            "binary": "./tests/test_psmp.sh",
        },
        "scp": {
            "binary": "./tests/test_psmp.sh",
        },
    }

    with open("epsmpcfg.yaml", "w", encoding="utf-8") as file:
        file.write(yaml.dump(test_config))

    yield file

    # cleanup file
    pathlib.Path("epsmpcfg.yaml").unlink()
