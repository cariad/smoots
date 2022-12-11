from vinculum import Fraction

from smoots.lengths.length import Length
from smoots.lengths.yards import Yards


class Feet(Length):
    """
    A length in feet.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        """
        Gets the number of metres per foot.
        """

        return Yards.metres_per_unit() / 3
