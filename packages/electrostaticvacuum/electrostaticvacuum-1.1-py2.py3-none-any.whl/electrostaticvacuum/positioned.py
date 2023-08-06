import abc
import math


class Positioned(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def x(self) -> float:
        pass

    @property
    @abc.abstractmethod
    def y(self) -> float:
        pass

    def get_distance_between(self, another: 'Positioned') -> float:
        dx = self.x - another.x
        dy = self.y - another.y
        return math.sqrt(dx * dx + dy * dy)
