from pytest import raises
from vinculum import Rational

from smoots import Feet, Inches


def test_int() -> None:
    length = Feet(5) + 2
    assert length == Feet(7)


def test_float() -> None:
    length = Feet(5) + 2.5
    assert length == Feet(7) + Inches(6)


def test_fraction() -> None:
    length = Feet(5) + Rational(9, 4)
    assert length == Feet(7) + Inches(3)


def test_length() -> None:
    length = Feet(5) + Inches(7)
    assert length == 5.583333333333333


def test_unsupported() -> None:
    with raises(TypeError) as ex:
        _ = Feet(1) + "foo"

    assert str(ex.value) == "Cannot add str ('foo') to Feet"
