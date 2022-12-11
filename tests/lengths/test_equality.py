from typing import Any

from pytest import mark, raises

from smoots import Feet, Inches


@mark.parametrize(
    "a, b",
    [
        (Feet(7), Feet(7)),
        (Feet(7), 7),
        (7, Feet(7)),
        (Feet(5) + Inches(6), 5.5),
    ],
)
def test_equal(a: Any, b: Any) -> None:
    assert a == b


@mark.parametrize(
    "a, b",
    [
        (Feet(7), Feet(6)),
        (Feet(7), 6),
        (7, Feet(6)),
        (Feet(5) + Inches(6), 5.49),
    ],
)
def test_not_equal(a: Any, b: Any) -> None:
    assert a != b


def test_unsupported() -> None:
    with raises(TypeError) as ex:
        _ = Feet(1) == "foo"

    assert str(ex.value) == "Cannot compare Feet with str ('foo')"
