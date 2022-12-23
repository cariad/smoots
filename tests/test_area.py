from smoots import Centimetres, Inches
from smoots.area import Area2

def test() -> None:
    area = Area2(Centimetres(5), Inches(6))

    area.width.decimal()

    assert area.width == Centimetres(5)
