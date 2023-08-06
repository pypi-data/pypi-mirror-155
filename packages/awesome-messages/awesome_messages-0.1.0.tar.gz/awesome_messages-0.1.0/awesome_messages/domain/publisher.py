from abc import ABC, abstractmethod


class MessagePublisher(ABC):
    @abstractmethod
    def publish(self, message: dict):
        pass

    @abstractmethod
    def stop_publishing(self):
        pass
