from __future__ import annotations

from abc import ABC, abstractmethod

# # from dataclasses import dataclass
# from math import modf
from typing import Any, Optional, Type, TypeVar
from smoots.very_precise_number import VeryPreciseNumber
from smoots.log import log

class Length(ABC):
    @classmethod
    @abstractmethod
    def from_meters(cls: Type[LengthT], meters: VeryPreciseNumber) -> LengthT:
        """ """

    @abstractmethod
    def to_meters(self) -> VeryPreciseNumber:
        """ """

    # def __add__(self: LengthT, other: Any) -> LengthT:
    #     if isinstance(other, Length):
    #         other_length = other.to_meters()
    #     else:
    #         other_length = Meters.from_float(float(other))

    #     length = Meters.add(self.to_meters(), other_length)
    #     return self.from_meters(length)

    def to(self, t: Type[LengthT]) -> LengthT:
        return t.from_meters(self.to_meters())


LengthT = TypeVar("LengthT", bound=Length)


class Inches(Length):
    def __init__(self, inches: VeryPreciseNumber) -> None:
        self._inches = inches

# #         f, i = modf(inches)

# #         self._inches = int(i)
# #         self._eighths = int(f * 8)

    @property
    def inches(self) -> int:
        return self._inches.integral

    @classmethod
    def from_meters(cls, meters: VeryPreciseNumber) -> Inches:
        # 1 m = 39.370079 in
        inches_per_meter = 39.370079

        as_inches = meters * inches_per_meter
        log.debug("%s * %s = %s", meters, inches_per_meter, as_inches.decimal())
        return Inches(as_inches)

    def to_meters(self) -> VeryPreciseNumber:
        return self._inches / 39.3701


# class Centimeters(Length):
#     def __init__(self, centimeters: VeryPreciseNumber) -> None:
#         self._centimeters = centimeters.integral
#         # self.millimeters = centimeters + (f * 10)

#     # @classmethod
#     # def from_meters(cls, meters: Meters) -> Centimeters:
#     #     return Centimeters(meters.meters * 100)

#     @property
#     def centimeters(self) -> int:
#         return self._centimeters

#     # def to_meters(self) -> Meters:
#     #     return Meters(0, self)


class Meters(Length):
    def __init__(self, meters: VeryPreciseNumber) -> None:
        self._meters = meters

    @property
    def metres(self) -> int:
        return self._meters.integral

    @property
    def centimetres(self) -> int:
        return (self._meters.fractional * 100).integral

    @classmethod
    def from_meters(cls, meters: VeryPreciseNumber) -> Meters:
        return Meters(meters)

    def to_meters(self) -> VeryPreciseNumber:
        return self._meters
