from pathlib import Path

from pytest import MonkeyPatch

import ecmd
from ecmd import load_config


def test_load_config_exception(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(ecmd, "Path", lambda: Path("doesnotexist"))

    config: dict = load_config()
    assert config == {}
