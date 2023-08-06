import numpy
from .electrostatic_field import ElectrostaticField
from .point_charge import PointCharge
from .positioned import Positioned
from .vector import Vector


class Field:
    @staticmethod
    def of_x_poles(x: int, r: float | int = 1, start_angle: float | int = 0,
                   charge: float | int = 1, k: float | int = 8.99E+9):
        if x == 0:
            return ElectrostaticField([], k=k)

        if x < 0:
            x = -x

        def generate_charges():
            charge_inner = charge
            angle_list = list(numpy.linspace(start_angle, 2 * numpy.pi + start_angle, x + 1))
            del angle_list[-1]
            for angle in angle_list:
                position = Vector.create_point_with_polar(r, angle)
                yield PointCharge(position, charge_inner)
                charge_inner = -charge_inner

        return ElectrostaticField(generate_charges(), k=k)

    @staticmethod
    def from_charge_map(
            charge_map: list[list[float | int]],
            start: Positioned,
            step_x: float | int,
            step_y: float | int,
            k: float | int = 8.99E+9):

        def range_endless(start_value: float | int, step_value: float | int):
            value = start_value
            yield value
            while True:
                value += step_value
                yield value

        result = (
            PointCharge(Vector(x, y), item)
            for line, y in zip(charge_map, range_endless(start.y, step_y))
            for item, x in zip(line, range_endless(start.x, step_x))
            if item != 0
        )

        return ElectrostaticField(result, k=k)
