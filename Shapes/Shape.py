from abc import ABC, abstractmethod
import random

class Shape(ABC):
    def __init__(self):
        self.BLOCK_SIZE = 2
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.rotation = random.randint(0, 3)
        self.shape = None
        self._build_shape()

    @abstractmethod
    def _build_shape(self):
        pass

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        self._build_shape()

    def get_shape(self):
        return self.shape
    
    def get_color(self):
        return self.color