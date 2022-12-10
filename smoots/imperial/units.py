from __future__ import annotations

from vinculum import Fraction

from smoots.unit import Unit


class InchUnit(Unit):
    """
    Imperial inch.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        return FootUnit.metres_per_unit() / 12


class FootUnit(Unit):
    """
    Imperial foot.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        return YardUnit.metres_per_unit() / 3


class YardUnit(Unit):
    """
    Imperial yard.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        """
        Gets the number of meters per yard.

        The yard was defined as exactly 0.9144 meters by the international yard
        and pound agreement of 1959.

        https://usma.org/laws-and-bills/refinement-of-values-for-the-yard-and-the-pound
        """

        return Fraction(9_144, 10_000)


class MileUnit(Unit):
    """
    Imperial mile.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        return FootUnit.metres_per_unit() * 5_280
