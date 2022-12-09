from smoots.meters import Meters, Inches
from smoots.very_precise_number import VeryPreciseNumber


def test_meters_to_meters_and_centimeters() -> None:
    metres_vpn = VeryPreciseNumber(1_023, 100)
    metres = Meters(metres_vpn)
    assert metres.metres == 10
    assert metres.centimetres == 23

def test_meters_to_inches() -> None:
    metres_vpn = VeryPreciseNumber(1_023, 100)  # 10 m + 23 cm
    metres = Meters(metres_vpn)
    inches = metres.to(Inches)
    assert inches.inches == 402  # 4.0275591
    # assert metres.metres == 10
    # assert metres.centimetres == 23
