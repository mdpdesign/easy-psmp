import yaml
from pathlib import Path, PosixPath
from ecmd import EasyCommand


class EasySSH(EasyCommand):

    def __init__(self) -> None:

        default_binary: str = "ssh"
        default_arguments: list = [
            "-o UserKnownHostsFile=/dev/null",
            "-o StrictHostKeyChecking=no",
        ]

        try:
            p: Path = Path(".")
            cfg_file: PosixPath = list(p.glob("epsmpcfg.y*ml"))[0]

            with open(cfg_file.resolve().as_posix(), "r") as file:
                config: dict = yaml.safe_load(file)
                self.binary = config.get("ssh", {}).get("binary", default_binary)
                self.arguments = config.get("ssh", {}).get(
                    "arguments", default_arguments
                )
        except:
            self.binary = default_binary
            self.arguments = default_arguments

    def get_binary(self) -> str:
        return self.binary

    def get_arguments(self) -> list:
        return self.arguments
