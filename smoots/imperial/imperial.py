from typing import Type

from vinculum import Fraction

from smoots.imperial.units import FootUnit, InchUnit, MileUnit, YardUnit
from smoots.length import Length
from smoots.unit import Unit


class Imperial(Length):
    """
    A length in imperial units.
    """

    @classmethod
    def units(cls) -> tuple[Type[Unit], ...]:
        """
        Gets the units of this length.
        """

        return (MileUnit, YardUnit, FootUnit, InchUnit)

    @property
    def inches(self) -> int:
        """
        Integral inches in this length.
        """

        return self.get_integral(InchUnit)

    @property
    def feet(self) -> int:
        """
        Integral feet in this length.
        """

        return self.get_integral(FootUnit)

    @property
    def yards(self) -> int:
        """
        Integral yards in this length.
        """

        return self.get_integral(YardUnit)

    @property
    def miles(self) -> int:
        """
        Integral miles in this length.
        """

        return self.get_integral(MileUnit)

    @property
    def to_feet(self) -> Fraction:
        """
        Length in feet.
        """

        return self.to(FootUnit)
