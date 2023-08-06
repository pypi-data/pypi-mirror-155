from abc import ABC, abstractmethod


class MessageListener(ABC):
    @abstractmethod
    def start_listening(self):
        pass

    @abstractmethod
    def stop_listening(self):
        pass
