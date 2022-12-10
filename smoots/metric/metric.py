from typing import Type

from smoots.length import Length
from smoots.metric.units import CentimetreUnit, MetreUnit
from smoots.unit import Unit


class Metric(Length):
    """
    A length in metric units.
    """

    @classmethod
    def units(cls) -> tuple[Type[Unit], ...]:
        """
        Gets the units of this length.
        """

        return (MetreUnit, CentimetreUnit)

    @property
    def centimetres(self) -> int:
        """
        Integral centimetres in this length.
        """

        return self.get_integral(CentimetreUnit)

    @property
    def metres(self) -> int:
        """
        Integral metres in this length.
        """

        return self.get_integral(MetreUnit)
