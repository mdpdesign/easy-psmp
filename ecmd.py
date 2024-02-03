from abc import ABC, abstractmethod


class EasyCommand(ABC):

    @abstractmethod
    def get_binary(self) -> str:
        pass

    @abstractmethod
    def get_arguments(self) -> list:
        pass
