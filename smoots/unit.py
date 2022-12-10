from abc import ABC, abstractmethod

from vinculum import Fraction


class Unit(ABC):
    """
    A unit of length.
    """

    @classmethod
    @abstractmethod
    def metres_per_unit(cls) -> Fraction:
        """
        Gets the number of meters per unit.
        """
