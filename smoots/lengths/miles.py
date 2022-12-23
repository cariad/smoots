from vinculum import Rational

from smoots.lengths.feet import Feet
from smoots.lengths.length import Length


class Miles(Length):
    """
    A length in miles.
    """

    @classmethod
    def metres_per_unit(cls) -> Rational:
        """
        Gets the number of metres per mile.
        """

        return Feet.metres_per_unit() * 5_280
