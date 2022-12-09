from __future__ import annotations

from io import StringIO
from time import perf_counter
from typing import Any, List, Optional

from smoots.log import log


class VeryPreciseNumber:
    def __init__(self, numerator: int, denominator: int = 1) -> None:
        self._numerator = numerator
        self._denominator = denominator

        if self._denominator < 0:
            self._denominator = abs(self._denominator)
            self._numerator = self._numerator * -1

    @staticmethod
    def greatest_common_factor(a: int, b: int) -> int:
        # Set up a division problem where a is larger than b.
        biggest = max(a, b)
        smallest = min(a, b)

        if smallest in (0, biggest):
            return smallest

        while True:
            remainder = biggest % smallest

            if remainder == 0:
                return smallest

            biggest = smallest
            smallest = remainder

    @property
    def reduced(self) -> VeryPreciseNumber:
        gcf = self.greatest_common_factor(self.numerator, self.denominator)
        if gcf in (0, 1):
            return self
        return VeryPreciseNumber(
            self.numerator // gcf, self.denominator // gcf
        )

    @staticmethod
    def same_denominator(
        a: VeryPreciseNumber,
        b: VeryPreciseNumber,
    ) -> tuple[VeryPreciseNumber, VeryPreciseNumber]:
        x = a
        y = b

        if a.denominator != b.denominator:
            x = VeryPreciseNumber(
                a.numerator * b.denominator,
                a.denominator * b.denominator,
            )
            y = VeryPreciseNumber(
                b.numerator * a.denominator,
                b.denominator * a.denominator,
            )

        return x, y

    def __add__(self, other: Any) -> VeryPreciseNumber:
        if isinstance(other, VeryPreciseNumber):
            a, b = self.same_denominator(self, other)
            return VeryPreciseNumber(
                a.numerator + b.numerator, a.denominator
            ).reduced

        raise TypeError(
            f"Cannot add {other} ({other.__class__.__name__}) to "
            f"{self.__class__.__name__}"
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, VeryPreciseNumber):
            if self.numerator == 0 and other.numerator == 0:
                return True

            return (
                self.numerator == other.numerator
                and self.denominator == other.denominator
            )

        log.warning(
            "Cannot compare %s (%s) to %s",
            other,
            other.__class__.__name__,
            self.__class__.__name__,
        )

        return False

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, VeryPreciseNumber):
            a, b = self.same_denominator(self, other)
            return a.numerator > b.numerator

        raise TypeError(
            f"Cannot check {self.__class__.__name__} > {other} "
            f"({other.__class__.__name__})"
        )

    def __mul__(self, other: Any) -> VeryPreciseNumber:
        if isinstance(other, VeryPreciseNumber):
            result = VeryPreciseNumber(
                self.numerator * other.numerator,
                self.denominator * other.denominator,
            ).reduced
            # log.debug("%s * %s = %s", self, other, result)
            return result

        raise TypeError(
            f"Cannot multiply {self.__class__.__name__} by {other} "
            f"({other.__class__.__name__})"
        )

    def __repr__(self) -> str:
        return f"{self._numerator}/{self._denominator}"

    def __sub__(self, other: Any) -> VeryPreciseNumber:
        if isinstance(other, VeryPreciseNumber):
            other = VeryPreciseNumber(other.numerator * -1, other.denominator)
            return self + other

        raise TypeError(
            f"Cannot add {other} ({other.__class__.__name__}) to "
            f"{self.__class__.__name__}"
        )

    @property
    def reciprocal(self) -> VeryPreciseNumber:
        return VeryPreciseNumber(self.denominator, self.numerator)

    def __truediv__(self, other: Any) -> VeryPreciseNumber:
        if isinstance(other, VeryPreciseNumber):
            return self * other.reciprocal

        if isinstance(other, int):
            return self * VeryPreciseNumber(1, other)

        raise TypeError(
            f"Cannot divide (true) {self.__class__.__name__} by {other} "
            f"({other.__class__.__name__})"
        )

    def decimal(self, decimals: int = 100, recursion: bool = True) -> str:
        result = StringIO()

        integral = self._numerator // self._denominator

        # Be aware of CVE-2020-10735:
        # https://github.com/python/cpython/issues/95778

        integral_length = self.length(integral)

        if integral_length == 0:
            result.write("0")
        else:
            for e in range(integral_length - 1, -1, -1):
                result.write(str(self.at_exponent(integral, e)))

        result.write(".")

        remainder = (self._numerator % self._denominator) * 10

        recursion_track: Optional[List[int]] = [] if recursion else None

        fractional = 0
        recurring_count = 0
        decimal_places = 0

        while True:
            i = remainder // self._denominator
            remainder = (remainder % self._denominator) * 10

            if recursion_track is not None and (remainder in recursion_track):
                recurring_count = len(recursion_track) - recursion_track.index(
                    remainder
                )
                break

            fractional *= 10
            fractional += i
            decimal_places += 1

            if remainder == 0 or decimal_places >= decimals:
                break

            if recursion_track is not None:
                recursion_track.append(remainder)

        fractional_length = self.length(fractional)

        if fractional_length == 0:
            result.write("0")
        else:
            for index, e in enumerate(range(fractional_length - 1, -1, -1)):
                if index >= fractional_length - recurring_count:
                    result.write("\u0305")
                result.write(str(self.at_exponent(fractional, e)))

        return result.getvalue()

    @property
    def denominator(self) -> int:
        return self._denominator

    @property
    def numerator(self) -> int:
        return self._numerator

    @staticmethod
    def at_exponent(number: int, exponent: int) -> int:
        return int(number // 10**exponent) % 10

    @staticmethod
    def string_to_int(s: str) -> int:
        result = 0
        for index, digit in enumerate(s):
            e = len(s) - (index + 1)
            result += int(digit) * (10**e)
        return result

    @classmethod
    def from_string(cls, s: str) -> VeryPreciseNumber:
        # Be aware of CVE-2020-10735:
        # https://github.com/python/cpython/issues/95778

        s = s.strip()

        if "/" in s:
            index = s.index("/")
            return VeryPreciseNumber(
                VeryPreciseNumber.string_to_int(s[:index]),
                VeryPreciseNumber.string_to_int(s[index + 1 :]),  # noqa: E203
            )

        numerator = 0
        denominator = 1
        is_fraction = False

        for char in s:
            if char == ".":
                is_fraction = True
                continue

            numerator *= 10
            numerator += int(char)
            if is_fraction:
                denominator *= 10

        return VeryPreciseNumber(numerator, denominator).reduced

    @staticmethod
    def pi(iterations: int = 2000) -> VeryPreciseNumber:
        """
        Leibniz's formula
        """

        start = perf_counter()

        denominator = 1
        p = VeryPreciseNumber(0)

        for i in range(iterations):
            curr = VeryPreciseNumber(4) / denominator
            p = p + curr if i % 2 == 0 else p - curr
            denominator += 2

        end = perf_counter()
        log.debug("%s iterations took %s seconds", iterations, end - start)

        return p

    @staticmethod
    def length(number: int) -> int:
        count = 0
        while number > 0:
            count += 1
            number //= 10

        return count
