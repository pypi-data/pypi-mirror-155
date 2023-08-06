from .positioned import Positioned


class PointCharge(Positioned):
    def __init__(self, position: Positioned, charge: float | int):
        self._x = position.x
        self._y = position.y
        self._charge = float(charge)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def charge(self) -> float:
        return self._charge

    def __str__(self):
        return f"<a point charge at ({self.x}, {self.y}) with {self.charge} unit quantities>"
