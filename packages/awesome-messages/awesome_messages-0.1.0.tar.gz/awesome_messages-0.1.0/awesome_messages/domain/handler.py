from abc import ABC, abstractmethod


class MessageHandler(ABC):
    @abstractmethod
    def on_msg(self, message: dict):
        pass
