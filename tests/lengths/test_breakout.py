from smoots import Centimetres, Feet, Metres


def test() -> None:
    length = Feet(8).breakout(Metres, Centimetres)
    assert length[Metres] == 2
    assert length[Centimetres] == 43.84


def test_reversed() -> None:
    length = Feet(8).breakout(Centimetres, Metres)
    assert length[Metres] == 2
    assert length[Centimetres] == 43.84
