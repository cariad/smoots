from __future__ import annotations

from vinculum import Fraction

from smoots.unit import Unit


class CentimetreUnit(Unit):
    """
    Metric centimetre.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        return Fraction(1, 100)


class MetreUnit(Unit):
    """
    Metric metre.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        return Fraction(1)
