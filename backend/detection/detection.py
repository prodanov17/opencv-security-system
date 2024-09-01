from abc import ABC, abstractmethod


class Detection(ABC):
    @abstractmethod
    def detect(self, frame):
        pass

    @abstractmethod
    def get_short_name(self):
        pass
