from vinculum import Fraction

from smoots.lengths.feet import Feet
from smoots.lengths.length import Length


class Inches(Length):
    """
    A length in inches.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        """
        Gets the number of metres per inch.
        """

        return Feet.metres_per_unit() / 12
