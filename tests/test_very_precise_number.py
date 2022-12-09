from csv import reader

from pytest import mark

from smoots.very_precise_number import VeryPreciseNumber


@mark.parametrize(
    "a, b, expect",
    [
        (VeryPreciseNumber(0), VeryPreciseNumber(0), VeryPreciseNumber(0)),
        (VeryPreciseNumber(0), VeryPreciseNumber(1), VeryPreciseNumber(1)),
        (VeryPreciseNumber(1), VeryPreciseNumber(0), VeryPreciseNumber(1)),
        (VeryPreciseNumber(1), VeryPreciseNumber(2), VeryPreciseNumber(3)),
        (
            VeryPreciseNumber(1, 3),
            VeryPreciseNumber(1, 6),
            VeryPreciseNumber(1, 2),
        ),
        (
            VeryPreciseNumber(7, 4),
            VeryPreciseNumber(-1, 4),
            VeryPreciseNumber(3, 2),
        ),
    ],
)
def test_add(
    a: VeryPreciseNumber,
    b: VeryPreciseNumber,
    expect: VeryPreciseNumber,
) -> None:
    actual = a + b
    assert actual == expect


@mark.parametrize(
    "a, b, expect",
    [
        (0, 0, 0),
        (6, 4, 2),
    ],
)
def test_greatest_common_factor(a: int, b: int, expect: int) -> None:
    actual = VeryPreciseNumber.greatest_common_factor(a, b)
    assert actual == expect


@mark.parametrize(
    "a, b, expect",
    [
        (VeryPreciseNumber(0), VeryPreciseNumber(0), False),
        (VeryPreciseNumber(1), VeryPreciseNumber(0), True),
        (VeryPreciseNumber(2, 6), VeryPreciseNumber(1, 3), False),
        (VeryPreciseNumber(3, 6), VeryPreciseNumber(1, 3), True),
    ],
)
def test_gt(a: VeryPreciseNumber, b: VeryPreciseNumber, expect: bool) -> None:
    assert (a > b) is expect


@mark.parametrize(
    "a, b, expect",
    [
        (VeryPreciseNumber(0), VeryPreciseNumber(0), VeryPreciseNumber(0)),
        (VeryPreciseNumber(1), VeryPreciseNumber(0), VeryPreciseNumber(0)),
        (VeryPreciseNumber(1), VeryPreciseNumber(1), VeryPreciseNumber(1)),
        (VeryPreciseNumber(3), VeryPreciseNumber(5), VeryPreciseNumber(15)),
    ],
)
def test_mul(
    a: VeryPreciseNumber,
    b: VeryPreciseNumber,
    expect: VeryPreciseNumber,
) -> None:
    actual = a * b
    assert actual == expect


@mark.parametrize(
    "a, b, expect",
    [
        (
            VeryPreciseNumber(1, 3),
            VeryPreciseNumber(1, 6),
            (VeryPreciseNumber(6, 18), VeryPreciseNumber(3, 18)),
        ),
    ],
)
def test_same_denominator(
    a: VeryPreciseNumber,
    b: VeryPreciseNumber,
    expect: tuple[VeryPreciseNumber, VeryPreciseNumber],
) -> None:
    actual = VeryPreciseNumber.same_denominator(a, b)
    assert actual == expect


@mark.parametrize(
    "a, b, expect",
    [
        (VeryPreciseNumber(0), VeryPreciseNumber(0), VeryPreciseNumber(0)),
        (VeryPreciseNumber(0), VeryPreciseNumber(1), VeryPreciseNumber(-1)),
        (
            VeryPreciseNumber(7, 4),
            VeryPreciseNumber(1, 4),
            VeryPreciseNumber(3, 2),
        ),
    ],
)
def test_sub(
    a: VeryPreciseNumber,
    b: VeryPreciseNumber,
    expect: VeryPreciseNumber,
) -> None:
    actual = a - b
    assert actual == expect


@mark.parametrize(
    "s, expect",
    [
        ("0", VeryPreciseNumber(0)),
        ("0.0", VeryPreciseNumber(0)),
        ("1", VeryPreciseNumber(1)),
        ("1.0", VeryPreciseNumber(1)),
        ("1.1", VeryPreciseNumber(11, 10)),
        ("1.2", VeryPreciseNumber(6, 5)),
        ("12.34", VeryPreciseNumber(617, 50)),
    ],
)
def test_from_string(s: str, expect: VeryPreciseNumber) -> None:
    actual = VeryPreciseNumber.from_string(s)
    assert actual == expect


@mark.parametrize(
    "vpn, expect",
    [
        (VeryPreciseNumber(0), "0.0"),
        (VeryPreciseNumber(1), "1.0"),
        (VeryPreciseNumber(3, 2), "1.5"),
        (VeryPreciseNumber(1, 3), "0.̅3"),
        (VeryPreciseNumber(9, 11), "0.̅8̅1"),
    ],
)
def test_decimal(vpn: VeryPreciseNumber, expect: str) -> None:
    assert vpn.decimal() == expect


def test_decimal__long_recurring() -> None:
    d = VeryPreciseNumber(9, 11).decimal(decimals=8, recursion=False)
    assert d == "0.81818181"


@mark.parametrize(
    "vpn, expect",
    [
        (VeryPreciseNumber(0), VeryPreciseNumber(0)),
        (VeryPreciseNumber(1), VeryPreciseNumber(1)),
        (VeryPreciseNumber(3, 15), VeryPreciseNumber(1, 5)),
        (VeryPreciseNumber(15, 3), VeryPreciseNumber(5)),
    ],
)
def test_reduced(vpn: VeryPreciseNumber, expect: VeryPreciseNumber) -> None:
    actual = vpn.reduced
    assert actual == expect


@mark.parametrize(
    "vpn, expect",
    [
        (VeryPreciseNumber(0), "0/1"),
    ],
)
def test_repr(vpn: VeryPreciseNumber, expect: str) -> None:
    assert repr(vpn) == expect


@mark.parametrize(
    "a, b, expect",
    [
        (VeryPreciseNumber(0), VeryPreciseNumber(0), VeryPreciseNumber(0)),
        (VeryPreciseNumber(15), VeryPreciseNumber(3), VeryPreciseNumber(5)),
    ],
)
def test_truediv(
    a: VeryPreciseNumber,
    b: VeryPreciseNumber,
    expect: VeryPreciseNumber,
) -> None:
    actual = a / b
    assert actual == expect


def test_pi() -> None:
    with open("./tests/data/leibniz-fractions.csv", mode="r") as f:
        rows = reader(f)
        next(rows)
        for row in rows:
            iterations = int(row[0])
            expect = VeryPreciseNumber.from_string(row[1])
            actual = VeryPreciseNumber.pi(iterations)
            assert (
                actual == expect
            ), f"Expected {expect} but got {actual} at {iterations} iterations"


def test_pi__default() -> None:
    expect = (
        "3.1410926536210432286970258295579986968615976706526522734076010821989"
        "956717378555703318046748194710489"
    )
    assert VeryPreciseNumber.pi().decimal(recursion=False) == expect
