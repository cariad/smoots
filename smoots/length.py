from __future__ import annotations

from abc import ABC, abstractmethod
from logging import DEBUG
from typing import Any, Dict, Type, TypeVar

from vinculum import Fraction

from smoots.log import log
from smoots.unit import Unit


class Length(ABC):
    """
    Abstract base length.

    `length` describes the number of units that the derived class represents.
    """

    def __init__(self, length: float | Fraction | int) -> None:
        self._total_metres = length * self.metres_per_unit()

        if log.isEnabledFor(DEBUG):  # pragma: no cover
            # Check first because `.decimal()` is expensive.
            log.debug(
                "Breaking out a new %s with length %s (%s m)",
                self.__class__.__name__,
                length.decimal() if isinstance(length, Fraction) else length,
                self._total_metres.decimal(),
            )

        metres_remaining = self._total_metres
        self._lengths: Dict[Type[Unit], Fraction] = {}

        for unit in self.units():
            fraction = metres_remaining / unit.metres_per_unit()
            if log.isEnabledFor(DEBUG):  # pragma: no cover
                # Check first because `.decimal()` is expensive.
                log.debug(
                    "%s claimed %s",
                    unit.__name__,
                    fraction.integral,
                )

            self._lengths[unit] = fraction
            metres_remaining -= fraction.integral * unit.metres_per_unit()

    def __add__(self: LengthT, other: Any) -> LengthT:
        if isinstance(other, Length):
            total_metres = self._total_metres + other._total_metres
            return self.__class__.from_metres(total_metres)

        raise TypeError(
            f"Cannot add {other.__class__.__name__} ({repr(other)}) to "
            f"{self.__class__.__name__}"
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return int(self) == other

        if isinstance(other, float):
            return float(self) == other

        if isinstance(other, Length):
            return self._total_metres == other._total_metres

        raise TypeError(
            f"Cannot compare {self.__class__.__name__} with "
            f"{other.__class__.__name__} ({repr(other)})"
        )

    def __float__(self) -> float:
        return float(self.total)

    def __int__(self) -> int:
        return self.integral

    def get_integral(self, unit: Type[Unit]) -> int:
        """
        Gets the integral value of `unit`.
        """

        return self._lengths[unit].integral

    @classmethod
    def from_metres(cls: Type[LengthT], m: float | Fraction | int) -> LengthT:
        unit_length = m / cls.metres_per_unit()

        if log.isEnabledFor(DEBUG):  # pragma: no cover
            # Check first because `.decimal()` is expensive.
            log.debug(
                "Creating a new %s with unit length %s (%s m)",
                cls.__name__,
                unit_length.decimal(),
                m.decimal() if isinstance(m, Fraction) else m,
            )

        return cls(unit_length)

    @property
    def integral(self) -> int:
        return (self._total_metres / self.metres_per_unit()).integral

    @classmethod
    @abstractmethod
    def metres_per_unit(cls) -> Fraction:
        """
        Gets the number of metres per unit length.
        """

    def to(self, unit: Type[Unit]) -> Fraction:
        """
        Converts this length to `unit`.
        """

        return self._total_metres / unit.metres_per_unit()

    @property
    def total(self) -> Fraction:
        return self._total_metres / self.metres_per_unit()

    @classmethod
    @abstractmethod
    def units(cls) -> tuple[Type[Unit], ...]:
        """
        Gets the units of this length.
        """


LengthT = TypeVar("LengthT", bound=Length)
