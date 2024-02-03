from ecmd import EasyCommand, load_config


class EasySSH(EasyCommand):

    def __init__(self) -> None:

        default_binary: str = "ssh"
        default_arguments: list = [
            "-o UserKnownHostsFile=/dev/null",
            "-o StrictHostKeyChecking=no",
        ]

        config: dict = load_config()
        self.binary = config.get("ssh", {}).get("binary", default_binary)
        self.arguments = config.get("ssh", {}).get("arguments", default_arguments)

    def get_binary(self) -> str:
        return self.binary

    def get_arguments(self) -> list:
        return self.arguments