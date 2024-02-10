from ecmd import EasyCommand, load_config


class EasySSH(EasyCommand):
    """A class to represent SSH command"""

    def __init__(self) -> None:

        default_binary: str = "ssh"
        default_arguments: list = [
            "-o UserKnownHostsFile=/dev/null",
            "-o StrictHostKeyChecking=no",
        ]

        config: dict = load_config()
        self.binary = (config.get("ssh") or {}).get("binary") or default_binary
        self.arguments = (config.get("ssh") or {}).get("arguments") or default_arguments

    def get_binary(self) -> str:
        """Returns binary path or name

        Returns:
            str: Path to binary or its name
        """
        return self.binary

    def get_arguments(self) -> list:
        """Returns list of arguments for binary

        Returns:
            list: list of configured arguments or defaults
        """
        return self.arguments
