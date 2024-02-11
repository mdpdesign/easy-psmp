from pathlib import Path

from pytest import MonkeyPatch

import ecmd
from ecmd import load_config


def test_load_config_returns_yaml_dict(create_test_config) -> None:
    config: dict = load_config()
    assert config == {
        "ssh": {
            "binary": "./tests/test_psmp.sh",
        },
        "scp": {
            "binary": "./tests/test_psmp.sh",
        },
    }


def test_load_config_returns_default_empty_dict(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(ecmd, "Path", lambda: Path("doesnotexist"))

    config: dict = load_config()
    assert config == {}
