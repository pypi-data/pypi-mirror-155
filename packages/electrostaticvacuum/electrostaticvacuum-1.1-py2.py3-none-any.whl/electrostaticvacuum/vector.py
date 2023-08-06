import math
from .positioned import Positioned


class Vector(Positioned):
    def __init__(self, x: float | int, y: float | int):
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @staticmethod
    def create_point_with_polar(r: float | int, theta: float | int) -> 'Vector':
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return Vector(x, y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other: 'Vector'):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __bool__(self):
        return self.x == 0 and self.y == 0
