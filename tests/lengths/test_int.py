from pytest import mark

from smoots import Feet, Inches, Length


@mark.parametrize(
    "length, expect",
    [
        (Feet(7), 7),
        (Inches(6), 6),
        (Feet(5) + Inches(6), 5),
        (Feet(5) + Inches(13), 6),
    ],
)
def test(length: Length, expect: int) -> None:
    a = int(length)
    assert a == expect
