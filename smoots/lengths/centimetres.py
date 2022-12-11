from vinculum import Fraction

from smoots.lengths.length import Length


class Centimetres(Length):
    """
    A length in centimetres.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        """
        Gets the number of metres per centimetre.
        """

        return Fraction(1, 100)
