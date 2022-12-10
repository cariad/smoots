from pytest import raises

from smoots.metric import Centimetres, Metres


def test() -> None:
    m = Metres(1.75)
    assert m.metres == 1
    assert m.centimetres == 75


def test_add__unsupported() -> None:
    with raises(TypeError) as ex:
        _ = Metres(1) + "zero"

    assert str(ex.value) == "Cannot add str ('zero') to Metres"


def test_eq__float() -> None:
    assert Metres(1.2) == 1.2


def test_eq__int() -> None:
    assert Metres(1) == 1


def test_eq__length() -> None:
    assert Metres(1) == Centimetres(100)


def test_eq__unsupported() -> None:
    with raises(TypeError) as ex:
        _ = Metres(1) == "zero"

    assert str(ex.value) == "Cannot compare Metres with str ('zero')"
