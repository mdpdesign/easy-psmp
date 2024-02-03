from ecmd import EasyCommand


class EasySSH(EasyCommand):

    def __init__(self) -> None:
        self.binary: str = "ssh"
        self.arguments: list = [
            "-o UserKnownHostsFile=/dev/null",
            "-o StrictHostKeyChecking=no",
        ]

    def get_binary(self) -> str:
        return self.binary

    def get_arguments(self) -> list:
        return self.arguments
