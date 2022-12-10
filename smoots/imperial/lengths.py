from smoots.imperial.imperial import Imperial
from smoots.imperial.units import FootUnit, InchUnit, MileUnit, YardUnit


class Inches(InchUnit, Imperial):
    """
    A length in inches.
    """


class Feet(FootUnit, Imperial):
    """
    A length in feet.
    """


class Yards(YardUnit, Imperial):
    """
    A length in yards.
    """


class Miles(MileUnit, Imperial):
    """
    A length in miles.
    """
