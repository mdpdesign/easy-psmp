from ecmd import EasyCommand


class EasySCP(EasyCommand):

    def __init__(self) -> None:
        self.binary: str = "scp"
        self.arguments: list = [
            "-o UserKnownHostsFile=/dev/null",
            "-o StrictHostKeyChecking=no",
        ]

    def get_binary(self):
        return self.binary

    def get_arguments(self) -> list:
        return self.arguments
