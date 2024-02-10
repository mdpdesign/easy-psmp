import logging
from abc import ABC, abstractmethod
from logging import Logger
from pathlib import Path, PosixPath

import yaml


class EasyCommand(ABC):
    """Abstract class/interface for Easy-PSMP commands"""

    # pylint: disable=missing-function-docstring
    @abstractmethod
    def get_binary(self) -> str:
        raise NotImplementedError

    # pylint: disable=missing-function-docstring
    @abstractmethod
    def get_arguments(self) -> list:
        raise NotImplementedError


def load_config() -> dict:
    """Loads Easy-PSMP configuration file 'epsmpcfg.y*ml' and returns it as dictionary

    Returns:
        dict: dictionary with configuration settings, or empty dict when config file can't be loaded
    """

    logger: Logger = logging.getLogger("epsmp-logger")

    try:
        logger.debug("Try to load Yaml configuration")

        p: Path = Path(".")
        cfg_file: PosixPath = list(p.glob("epsmpcfg.y*ml"))[0]

        with open(cfg_file.resolve().as_posix(), "r", encoding="utf-8") as file:
            config: dict = yaml.safe_load(file)

            logger.debug("Loading Yaml configuration successful")
            return config

    # pylint: disable=broad-exception-caught
    except Exception:
        logger.debug(
            "Loading Yaml configuration failed, will use defaults - this is OK if config file doesn't exist"
        )
        return {}
