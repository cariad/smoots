from vinculum import Rational

from smoots.lengths.length import Length


class Centimetres(Length):
    """
    A length in centimetres.
    """

    @classmethod
    def metres_per_unit(cls) -> Rational:
        """
        Gets the number of metres per centimetre.
        """

        return Rational(1, 100)
