from __future__ import annotations
from logging import getLogger
from math import modf
from typing import Any, Dict, List, Optional
from math import log10, floor, pow
from smoots.log import log

pi_log = getLogger("smoots.pi")


class VeryPreciseNumber:
    def __init__(
        self,
        significand: int,
        e: int = 0,
        repeating: Optional[int] = None,
    ) -> None:
        self._exponent = e
        self._significand = significand
        self._repeating = repeating

    def __add__(self, other: Any) -> VeryPreciseNumber:
        if isinstance(other, VeryPreciseNumber):
            most_significant_exponent = max(
                self.most_significant_exponent,
                other.most_significant_exponent,
            )

            least_significant_exponent = min(
                self.least_significant_exponent,
                other.least_significant_exponent,
            )

            exponent_offset = (
                0 - least_significant_exponent if least_significant_exponent < 0 else 0
            )

            exponent = least_significant_exponent
            result = 0
            carry = 0

            while True:
                self_value = self.at_exponent(exponent)
                other_value = other.at_exponent(exponent)

                summed = self_value + other_value

                result += summed * (10 ** (exponent + exponent_offset))

                exponent += 1
                if exponent > most_significant_exponent and carry == 0:
                    break

            vpn = VeryPreciseNumber(result, e=-exponent_offset)
            log.debug("%s + %s = %s", self, other, vpn)
            return vpn

        raise TypeError(
            f"Cannot add {other} ({other.__class__.__name__}) to "
            f"{self.__class__.__name__}"
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, VeryPreciseNumber):
            self_integral = self.integral
            other_integral = other.integral

            if self_integral != other_integral:
                log.debug(
                    "This integral %s != other %s",
                    self_integral,
                    other_integral,
                )
                return False

            if self.repeating != other.repeating:
                log.debug(
                    "This number's repeating sequence %s != other's %s",
                    self.repeating,
                    other.repeating,
                )
                return False

            self_fractional = self.normal_fractional
            other_fractional = other.normal_fractional

            if self_fractional[0] != other_fractional[0]:
                log.debug(
                    "This fractional significand %s != other %s",
                    self_fractional[0],
                    other_fractional[0],
                )
                return False

            if self_fractional[1] != other_fractional[1]:
                log.debug(
                    "This fractional exponent %s != other %s",
                    self_fractional[1],
                    other_fractional[1],
                )
                return False

            return True

        log.warning(
            "Cannot compare %s (%s) to %s",
            other,
            other.__class__.__name__,
            self.__class__.__name__,
        )

        return False

    def __repr__(self) -> str:
        f, e = self.normal_fractional
        e = abs(e)

        fraction_str = str(f)
        padding = "0" * (e - len(fraction_str))

        return f"{self.integral}.{padding}{fraction_str}"

    def __sub__(self, other: Any) -> VeryPreciseNumber:
        if isinstance(other, VeryPreciseNumber):
            log.debug("Calculating %s - %s", self, other)
            most_significant_exponent = max(
                self.most_significant_exponent,
                other.most_significant_exponent,
            )

            least_significant_exponent = min(
                self.least_significant_exponent,
                other.least_significant_exponent,
            )

            exponent_offset = (
                0 - least_significant_exponent if least_significant_exponent < 0 else 0
            )

            exponent = least_significant_exponent
            result = 0
            ten_from_next = False

            while True:
                self_value = self.at_exponent(exponent)
                other_value = other.at_exponent(exponent)

                if ten_from_next:
                    if self_value > 0:
                        self_value -= 1
                        ten_from_next = False
                    else:
                        self_value = 9
                        ten_from_next = True

                if self_value < other_value:
                    self_value += 10
                    ten_from_next = True

                subbed = self_value - other_value

                result += subbed * (10 ** (exponent + exponent_offset))

                exponent += 1
                if exponent > most_significant_exponent and not ten_from_next:
                    break

            vpn = VeryPreciseNumber(result, e=-exponent_offset)
            log.debug("%s - %s = %s", self, other, vpn)
            return vpn

        raise TypeError(
            f"Cannot subtract {other} ({other.__class__.__name__}) from "
            f"{self.__class__.__name__}"
        )

    def __truediv__(self, other: Any) -> VeryPreciseNumber:
        if isinstance(other, int):
            carry = 0
            exponent = self.most_significant_exponent
            result = 0
            result_exponent = self._exponent

            # value, carry and their result
            recursion_track: List[tuple[int, int, int]] = []
            repeating: Optional[int] = None

            while True:
                value = carry + self.at_exponent(exponent)

                if exponent < 0:
                    mult = 1
                    result *= 10
                else:
                    mult = 10**exponent

                this_result = (value // other) * mult

                carry = (value % other) * 10
                exponent -= 1

                if exponent < self._exponent:
                    if carry == 0:
                        result += this_result
                        break

                    this_recursion_info = (value, carry, this_result)

                    start_index = (
                        recursion_track.index(this_recursion_info)
                        if this_recursion_info in recursion_track
                        else None
                    )

                    if start_index is not None:
                        log.debug("Recursion detected at track index %s", start_index)

                        for index in range(
                            len(recursion_track) - 1, start_index - 1, -1
                        ):
                            repeating = int(
                                str(recursion_track[index][2]) + str(repeating or "")
                            )

                        break

                    recursion_track.append(this_recursion_info)

                    result_exponent -= 1

                result += this_result

            vpn = VeryPreciseNumber(result, e=result_exponent, repeating=repeating)

            log.debug("%s / %s = %s", self, other, vpn)

            return vpn

        raise TypeError(
            f"Cannot divide {self.__class__.__name__} by {other} "
            f"({other.__class__.__name__})"
        )

    def at_exponent(self, exponent: int) -> int:
        """
        Gets the value at `exponent`.

        For example, the value at exponent 3 of 12345 is 2 because
        2,000 == 2 * 10**3.
        """

        index = exponent - self._exponent

        if index < 0:
            return 0

        return int(self._significand // 10**index) % 10

    @classmethod
    def from_string(cls, s: str) -> VeryPreciseNumber:
        # Be aware of CVE-2020-10735: https://github.com/python/cpython/issues/95778

        s = s.strip()

        exponent = 0

        if "." in s:
            exponent = s.index(".") - (len(s) - 1)

        significand = 0

        for char in s:
            if char == ".":
                continue
            significand *= 10
            significand += int(char)

        log.debug(
            'Lazily converted "%s" to significand %s and exponent %s',
            s,
            significand,
            exponent,
        )

        while significand > 0 and significand % 10 == 0:
            significand //= 10
            exponent += 1
            log.debug(
                "Collapsed to significand %s and exponent %s",
                significand,
                exponent,
            )

        log.debug(
            '"%s" converted to significand %s and exponent %s',
            s,
            significand,
            exponent,
        )

        return VeryPreciseNumber(significand, e=exponent)

    @property
    def integral(self) -> int:
        max_exponent = self.most_significant_exponent
        result = 0

        for exponent in range(max_exponent + 1):
            result += self.at_exponent(exponent) * (10**exponent)

        return result

    @property
    def least_significant_exponent(self) -> int:
        """
        Gets the most least exponent of the number.
        """

        return self._exponent

    @property
    def most_significant_exponent(self) -> int:
        """
        Gets the most significant exponent of the number.

        For example, the most significant exponent of "32" is "1" because
        30 == 10**1.
        """

        significand_length = self.length(self._significand)

        if significand_length == 0:
            return 0

        return significand_length + self._exponent - 1

    @property
    def normal_fractional(self) -> tuple[int, int]:
        min_exponent = self.least_significant_exponent
        result = 0
        start_exponent = 0

        for exponent in range(-1, min_exponent - 1, -1):
            result *= 10
            if v := self.at_exponent(exponent):
                start_exponent = min(start_exponent, exponent)
                result += v

        while result > 0 and result % 10 == 0:
            result //= 10

        return result, start_exponent

    @staticmethod
    def pi(iterations: int = 1_000_000) -> VeryPreciseNumber:
        """
        Leibniz's formula
        """

        denominator = 1
        p = VeryPreciseNumber(0)

        for i in range(iterations):
            curr = VeryPreciseNumber(4) / denominator
            p = p + curr if i % 2 == 0 else p - curr
            denominator += 2
            pi_log.debug("Pi estimation after %s iterations: %s", i, p)

        return p

    @property
    def repeating(self) -> Optional[int]:
        return self._repeating

    @property
    def scale(self) -> VeryPreciseNumber:
        if self._exponent == 0:
            return VeryPreciseNumber(self._exponent)

        if self._exponent > 0:
            s = int(pow(10, self._exponent))
            return VeryPreciseNumber(s)

        raise NotImplementedError()

    # class VeryPreciseNumber:
    #     def __init__(self, integral: int, fractional: int, shift: int = 0) -> None:
    #         self._integral = integral
    #         self._fractional = fractional

    #     @staticmethod
    #     def reverse(number: int) -> int:
    #         number_len = VeryPreciseNumber.length(number)
    #         result = 0
    #         for index in range(number_len):
    #             power = number_len - index - 1
    #             src = VeryPreciseNumber.nth(number, index)

    #             result += (src * (10**power))

    #         return result

    #     def __eq__(self, other: Any) -> bool:
    #         if isinstance(other, VeryPreciseNumber):
    #             return self.integral == other._integral and self._fractional == other._fractional

    #         log.warning(
    #             "Cannot compare %s (%s) to %s",
    #             other, other.__class__.__name__, self.__class__.__name__,
    #         )

    #         return False

    #     def __repr__(self) -> str:
    #         return f"{self._integral}.{self._fractional}"

    #     # @staticmethod
    #     # def divide(dividend: int, divisor: int, carry: int = 0, no_remainder: bool = False) -> tuple[int, int]:
    #     #     """
    #     #     Returns the integer result of the division and the remainder.
    #     #     """

    #     #     dividend_length = VeryPreciseNumber.length(dividend)
    #     #     result = 0
    #     #     remainder = carry

    #     #     power = 0

    #     #     while True:

    #     #     # for power in range(0, dividend_length):
    #     #         n = (remainder * 10) + VeryPreciseNumber.nth(dividend, power)

    #     #         tenth = (10 ** -power) if no_remainder else (10 ** power)
    #     #         result += (n // divisor) * tenth
    #     #         remainder = n % divisor

    #     #         power += 1

    #     #         if power >= dividend_length and ((not no_remainder) or (remainder == 0)):
    #     #             break

    #     #     log.debug("%s r %s / %s = %s r %s", dividend, carry, divisor, result, remainder)
    #     #     return result, remainder

    @staticmethod
    def length(number: int) -> int:
        count = 0
        while number > 0:
            count += 1
            number //= 10

        return count

    #     @staticmethod
    #     def length(number: int) -> int:
    #         return floor(log10(number) + 1) if number else 0

    #     @staticmethod
    #     def nth(number: int, index: int) -> int:
    #         n = int(number / (10 ** (index - 0)) % 10)
    #         log.debug("%s[%s] == %s", number, index, n)
    #         return n

    @staticmethod
    def nth(number: int, index: int) -> int:
        n = number // (10 ** (index - 0)) % 10
        log.debug("%s[%s] == %s", number, index, n)
        return n


#     @classmethod
#     def new(cls, value: float | int) -> VeryPreciseNumber:
#         if isinstance(value, int):
#             return VeryPreciseNumber(value, 0)

#         f, i = modf(value)
#         fraction_len = len(str(f)) - 2
#         return VeryPreciseNumber(int(i), int(f * (10**fraction_len)))

#     @property
#     def integral(self) -> int:
#         return self._integral

#     @property
#     def fractional(self) -> VeryPreciseNumber:
#         return VeryPreciseNumber(0, self._fractional)
