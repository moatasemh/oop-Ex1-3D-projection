from abc import ABC, abstractmethod
import numpy as np


class VideoWriter(ABC):
    @abstractmethod
    def add_frame(self, frame: np.ndarray):
        pass

    @abstractmethod
    def release(self):
        pass