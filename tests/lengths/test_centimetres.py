from pytest import mark

from smoots import Centimetres, Feet, Inches, Length, Metres, Miles, Yards


@mark.parametrize(
    "length, expect",
    [
        (Centimetres(7), 7),
        (Feet(0.5), 15.24),
        (Feet(1), 30.48),
        (Feet(3.28084), 100.0000032),
        (Inches(0.5), 1.27),
        (Inches(1), 2.54),
        (Inches(4), 10.16),
        (Metres(0.9), 90),
        (Metres(1.0), 100),
        (Metres(1.1), 110),
        (Metres(1.15), 115),
        (Miles(0.000001), 0.1609344),
        (Miles(0.000621371), 99.9999690624),
        (Miles(1), 160934.4),
        (Yards(1), 91.44),
        (Yards(1.09361), 99.99969839999998),
        (Yards(17), 1554.48),
    ],
)
def test_to_centimetres(length: Length, expect: float) -> None:
    a = length.to(Centimetres)
    assert a == expect
