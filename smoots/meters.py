# from __future__ import annotations

# from abc import ABC, abstractmethod

# # from dataclasses import dataclass
# from math import modf
# from typing import Any, Optional, Type, TypeVar


# class Length(ABC):
#     pass
#     # @classmethod
#     # @abstractmethod
#     # def from_meters(cls: Type[LengthT], meters: Meters) -> LengthT:
#     #     """ """

#     # @abstractmethod
#     # def to_meters(self) -> Meters:
#     #     """ """

#     # def __add__(self: LengthT, other: Any) -> LengthT:
#     #     if isinstance(other, Length):
#     #         other_length = other.to_meters()
#     #     else:
#     #         other_length = Meters.from_float(float(other))

#     #     length = Meters.add(self.to_meters(), other_length)
#     #     return self.from_meters(length)

#     # def to(self, t: Type[LengthT]) -> LengthT:
#     #     return t.from_meters(self.to_meters())


# LengthT = TypeVar("LengthT", bound=Length)


# # class Inches(Length):
# #     def __init__(self, inches: float) -> None:
# #         f, i = modf(inches)

# #         self._inches = int(i)
# #         self._eighths = int(f * 8)

# #     @property
# #     def inches(self) -> int:
# #         return self._inches

# #     @classmethod
# #     def from_meters(cls, meters: Meters) -> Inches:
# #         return Inches(meters.meters * 39.3701)

# #     def to_meters(self) -> Meters:
# #         return Meters(self._inches / 39.3701)


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


# class Meters(Length):
#     def __init__(self, meters: VeryPreciseNumber) -> None:
#         self._meters = meters.integral
#         self._centimeters = Centimeters(meters.fractional * 100)

#     # @classmethod
#     # def add(cls, a: Meters, b: Meters) -> Meters:
#     #     return Meters(99)

#     # @classmethod
#     # def from_float(cls, f: float) -> Meters:
#     #     return Meters(99)

#     # @classmethod
#     # def from_meters(cls, meters: Meters) -> Meters:
#     #     return meters

#     @property
#     def meters(self) -> int:
#         return self._meters

#     # def to_meters(self) -> Meters:
#     #     return self
