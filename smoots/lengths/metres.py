from vinculum import Rational

from smoots.lengths.length import Length


class Metres(Length):
    """
    A length in metres.
    """

    @classmethod
    def metres_per_unit(cls) -> Rational:
        """
        Gets the number of metres per metre.
        """

        return Rational(1)
