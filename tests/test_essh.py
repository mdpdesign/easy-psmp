from ast import arguments

import pytest

import essh
from essh import EasySSH


@pytest.mark.parametrize(
    "attr,expected",
    [
        ("binary", "ssh"),
        (
            "arguments",
            [
                "-o UserKnownHostsFile=/dev/null",
                "-o StrictHostKeyChecking=no",
            ],
        ),
    ],
)
def test_essh_default_arguments(attr: str, expected: list, monkeypatch) -> None:
    monkeypatch.setattr(essh, "load_config", lambda: {})

    essh_obj: EasySSH = EasySSH()
    assert getattr(essh_obj, attr) == expected


@pytest.mark.parametrize(
    "attr,expected",
    [
        ("binary", "/path/to/binary/ssh"),
        (
            "arguments",
            [
                "argument one",
                "argument two",
            ],
        ),
    ],
)
def test_essh_non_default_arguments(attr: str, expected: list, monkeypatch) -> None:
    monkeypatch.setattr(
        essh,
        "load_config",
        lambda: {
            "ssh": {
                "binary": "/path/to/binary/ssh",
                "arguments": [
                    "argument one",
                    "argument two",
                ],
            }
        },
    )

    essh_obj: EasySSH = EasySSH()
    assert getattr(essh_obj, attr) == expected
