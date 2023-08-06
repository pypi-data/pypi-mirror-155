from typing import Iterable, Generator
from .point_charge import PointCharge
from .positioned import Positioned
from .vector import Vector


class ElectrostaticField:
    def __init__(self,
                 charges: Iterable[PointCharge],
                 k: float | int = 8.99E+9):
        self._charges: list[PointCharge] = list(charges)
        self._k: float = float(k)

    @property
    def k(self) -> float:
        return self._k

    def get_charges(self) -> Generator[PointCharge, None, None]:
        for charge in self._charges:
            yield charge

    def get_potential(self, position: Positioned) -> float:
        inf_p = float("inf")
        inf_n = float("-inf")

        result = 0
        for charge in self._charges:
            if charge.charge != 0:
                d = charge.get_distance_between(position)
                if d == 0:
                    return inf_p if charge.charge > 0 else inf_n
                result += self.k * charge.charge / d
        return result

    def get_intensity(self, position: Positioned) -> Vector:
        nan = float("nan")

        result_x = 0
        result_y = 0
        for charge in self._charges:
            if charge.charge != 0:
                d = charge.get_distance_between(position)
                if d == 0:
                    return Vector(nan, nan)
                result_divided_by_d = self.k * charge.charge / d ** 3
                result_x += result_divided_by_d * (position.x - charge.x)
                result_y += result_divided_by_d * (position.y - charge.y)
        return Vector(result_x, result_y)
