from vinculum import Fraction

from smoots.lengths.length import Length


class Yards(Length):
    """
    A length in yards.
    """

    @classmethod
    def metres_per_unit(cls) -> Fraction:
        """
        Gets the number of metres per yard.

        The yard was defined as exactly 0.9144 metres by the international yard
        and pound agreement of 1959.

        https://usma.org/laws-and-bills/refinement-of-values-for-the-yard-and-the-pound
        """

        return Fraction(9_144, 10_000)
