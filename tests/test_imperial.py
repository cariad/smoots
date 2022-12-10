from pytest import mark
from vinculum import Fraction

from smoots.imperial import Feet, Imperial, Inches, Miles, Yards


@mark.parametrize(
    "i, miles, yards, feet, inches",
    [
        (Inches(25), 0, 0, 2, 1),
        (Feet(2.5), 0, 0, 2, 6),
        (Yards(Fraction(7, 3)), 0, 2, 1, 0),
        (Miles(1.5), 1, 880, 0, 0),
    ],
)
def test(i: Imperial, miles: int, yards: int, feet: int, inches: int) -> None:
    assert i.miles == miles
    assert i.yards == yards
    assert i.feet == feet
    assert i.inches == inches


def test__addition() -> None:
    result = Feet(5) + Inches(7)
    assert result.yards == 1
    assert result.feet == 2
    assert result.inches == 7


def test__to_feet() -> None:
    result = Feet(5) + Inches(7)
    assert result.to_feet.integral == 5
    assert result.inches == 7
