from abc import ABC, abstractmethod


class Detection(ABC):
    @abstractmethod
    def detect(self, frame):
        pass
