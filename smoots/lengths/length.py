from __future__ import annotations

from abc import ABC, abstractmethod
from logging import DEBUG
from typing import Any, Dict, Type, TypeVar

from vinculum import Fraction

from smoots.log import log


class Length(ABC):
    """
    Length.
    """

    def __init__(self, length: float | Fraction | int) -> None:
        # "length" is in the derived class' units (i.e. inches, lightyears,
        # etc) but we always record metres internally.
        self._total_metres = length * self.metres_per_unit()

    def __add__(self: LengthT, other: Any) -> LengthT:
        if isinstance(other, (float, Fraction, int)):
            other = self.__class__(other)

        if isinstance(other, Length):
            total_metres = self._total_metres + other._total_metres
            return self.__class__.from_metres(total_metres)

        raise TypeError(
            f"Cannot add {other.__class__.__name__} ({repr(other)}) to "
            f"{self.__class__.__name__}"
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, (float, int)):
            return float(self) == other

        if isinstance(other, Length):
            return self._total_metres == other._total_metres

        raise TypeError(
            f"Cannot compare {self.__class__.__name__} with "
            f"{other.__class__.__name__} ({repr(other)})"
        )

    def __float__(self) -> float:
        return float(self.length)

    def __int__(self) -> int:
        return self.integral

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({(float(self))})"

    def breakout(self, *lengths: LengthTT) -> Dict[LengthTT, Length]:
        """
        Breaks this length into `lengths`.

        Returns a dictionary of length types and values.

        The smallest unit will be returned as a fraction if needed for
        precision; all previous lengths will be integral.
        """

        final_length_index = len(lengths) - 1
        metres_remaining = self._total_metres
        result: Dict[LengthTT, Length] = {}

        ordered_length_types = sorted(
            lengths,
            key=lambda length: length.metres_per_unit(),
            reverse=True,
        )

        for index, length_type in enumerate(ordered_length_types):
            metres_per_unit = length_type.metres_per_unit()
            unit_length = metres_remaining / metres_per_unit
            length = length_type(unit_length)
            metres_remaining -= unit_length.integral * metres_per_unit

            if index == final_length_index:
                result[length_type] = length
            else:
                result[length_type] = length_type(length.integral)

        return result

    @classmethod
    def from_metres(
        cls: Type[LengthT],
        metres: float | Fraction | int,
    ) -> LengthT:
        """
        Creates a new instance of this length `metres` long.
        """

        unit_length = metres / cls.metres_per_unit()

        if log.isEnabledFor(DEBUG):  # pragma: no cover
            # Check first because `.decimal()` is expensive.
            log.debug(
                "Creating a new %s with unit length %s (%s m)",
                cls.__name__,
                unit_length.decimal(),
                metres.decimal() if isinstance(metres, Fraction) else metres,
            )

        return cls(unit_length)

    @property
    def integral(self) -> int:
        """
        Gets the integral part of this length.
        """

        return self.length.integral

    @property
    def length(self) -> Fraction:
        """
        Gets the length of this length.
        """

        return self._total_metres / self.metres_per_unit()

    @classmethod
    @abstractmethod
    def metres_per_unit(cls) -> Fraction:
        """
        Gets the number of metres per unit length.
        """

    def to(self, length: Type[LengthT]) -> LengthT:
        """
        Converts this length to `length`.
        """

        unit_length = self._total_metres / length.metres_per_unit()
        return length(unit_length)


LengthT = TypeVar("LengthT", bound=Length)
LengthTT = TypeVar("LengthTT", bound=Type[Length])
