from vinculum import Fraction

from smoots.lengths.length import Length


class Metres(Length):
    """
    A length in metres.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        """
        Gets the number of metres per metre.
        """

        return Fraction(1)
