from pytest import mark

from smoots import Centimetres, Feet, Inches, Length, Metres, Miles, Yards


@mark.parametrize(
    "length, expect",
    [
        (Centimetres(99), 0.99),
        (Centimetres(100), 1),
        (Centimetres(101), 1.01),
        (Feet(2), 0.6096),
        (Feet(3.28084), 1.000000032),
        (Feet(7), 2.1336),
        (Inches(3), 0.0762),
        (Inches(39.3701), 1.0000005400000003),
        (Inches(200), 5.08),
        (Metres(0.9), 0.9),
        (Metres(1.0), 1),
        (Metres(1.1), 1.1),
        (Miles(0.000001), 0.001609344),
        (Miles(0.000621371), 0.999999690624),
        (Miles(1), 1609.344),
        (Yards(1), 0.9144),
        (Yards(1.09361), 0.9999969839999998),
        (Yards(17), 15.5448),
    ],
)
def test_to_metres(length: Length, expect: float) -> None:
    a = length.to(Metres)
    assert a == expect
