from ecmd import EasyCommand, load_config


class EasySCP(EasyCommand):

    def __init__(self) -> None:

        default_binary: str = "scp"
        default_arguments: list = [
            "-o UserKnownHostsFile=/dev/null",
            "-o StrictHostKeyChecking=no",
        ]

        config: dict = load_config()
        self.binary = (config.get("scp") or {}).get("binary") or default_binary
        self.arguments = (config.get("scp") or {}).get("arguments") or default_arguments

    def get_binary(self) -> str:
        return self.binary

    def get_arguments(self) -> list:
        return self.arguments
