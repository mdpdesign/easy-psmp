import pytest

import escp
from escp import EasySCP


@pytest.mark.parametrize(
    "attr,expected",
    [
        ("binary", "scp"),
        (
            "arguments",
            [
                "-o UserKnownHostsFile=/dev/null",
                "-o StrictHostKeyChecking=no",
            ],
        ),
    ],
)
def test_escp_default_arguments(attr: str, expected: list, monkeypatch) -> None:
    monkeypatch.setattr(escp, "load_config", lambda: {})

    essh_obj: EasySCP = EasySCP()
    assert getattr(essh_obj, attr) == expected


@pytest.mark.parametrize(
    "attr,expected",
    [
        ("binary", "/path/to/binary/scp"),
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
        escp,
        "load_config",
        lambda: {
            "scp": {
                "binary": "/path/to/binary/scp",
                "arguments": [
                    "argument one",
                    "argument two",
                ],
            }
        },
    )

    essh_obj: EasySCP = EasySCP()
    assert getattr(essh_obj, attr) == expected
