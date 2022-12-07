from pytest import mark

from smoots.very_precise_number import VeryPreciseNumber
from csv import reader
from smoots.log import log

@mark.parametrize(
    "a, b, expect",
    [
        (VeryPreciseNumber(0), VeryPreciseNumber(0), VeryPreciseNumber(0)),
        (VeryPreciseNumber(0), VeryPreciseNumber(1), VeryPreciseNumber(1)),
        (VeryPreciseNumber(1), VeryPreciseNumber(2), VeryPreciseNumber(3)),
        (VeryPreciseNumber(10), VeryPreciseNumber(20), VeryPreciseNumber(30)),
        (VeryPreciseNumber(10), VeryPreciseNumber(2, e=1), VeryPreciseNumber(30)),
        (
            VeryPreciseNumber(1),
            VeryPreciseNumber(57, e=-1),
            VeryPreciseNumber(67, e=-1),
        ),
        (VeryPreciseNumber(5), VeryPreciseNumber(5), VeryPreciseNumber(10)),
        (VeryPreciseNumber(9), VeryPreciseNumber(9), VeryPreciseNumber(18)),
    ],
)
def test_add(
    a: VeryPreciseNumber,
    b: VeryPreciseNumber,
    expect: VeryPreciseNumber,
) -> None:
    actual = a + b
    assert actual == expect


# @mark.parametrize(
#     "vpn, expect",
#     [
#         (VeryPreciseNumber(0), 0),
#         (VeryPreciseNumber(1), 1),
#         (VeryPreciseNumber(10), 2),
#         (VeryPreciseNumber(1, exponent=2), 3),
#         (VeryPreciseNumber(10_000, exponent=-3), 2),
#     ],
# )
# def test_integral_length(vpn: VeryPreciseNumber, expect: int) -> None:
#     assert vpn.integral_length == expect


@mark.parametrize(
    "vpn, e, expect",
    [
        (VeryPreciseNumber(0), 0, 0),
        (VeryPreciseNumber(0), 1, 0),
        (VeryPreciseNumber(0), -1, 0),
        # 123:
        (VeryPreciseNumber(123), -1, 0),
        (VeryPreciseNumber(123), 0, 3),
        (VeryPreciseNumber(123), 1, 2),
        (VeryPreciseNumber(123), 2, 1),
        (VeryPreciseNumber(123), 3, 0),
        # 1,230:
        (VeryPreciseNumber(123, e=1), 0, 0),
        (VeryPreciseNumber(123, e=1), 1, 3),
        (VeryPreciseNumber(123, e=1), 2, 2),
        (VeryPreciseNumber(123, e=1), 3, 1),
        (VeryPreciseNumber(123, e=1), 4, 0),
        # 12.3:
        (VeryPreciseNumber(123, e=-1), -2, 0),
        (VeryPreciseNumber(123, e=-1), -1, 3),
        (VeryPreciseNumber(123, e=-1), 0, 2),
        (VeryPreciseNumber(123, e=-1), 1, 1),
        (VeryPreciseNumber(123, e=-1), 2, 0),
    ],
)
def test_at_exponent(vpn: VeryPreciseNumber, e: int, expect: int) -> None:
    assert vpn.at_exponent(e) == expect


@mark.parametrize(
    "a, b, expect",
    [
        (VeryPreciseNumber(0), VeryPreciseNumber(0), True),
        (VeryPreciseNumber(11, e=-1), VeryPreciseNumber(12, e=-1), False),
        (
            VeryPreciseNumber(101, e=0),
            VeryPreciseNumber(1010, e=-1),
            True,
        ),
    ],
)
def test_eq(a: VeryPreciseNumber, b: VeryPreciseNumber, expect: bool) -> None:
    assert (a == b) is expect


@mark.parametrize(
    "s, expect",
    [
        ("0", VeryPreciseNumber(0)),
        ("1", VeryPreciseNumber(1)),
        ("2", VeryPreciseNumber(2)),
        ("3", VeryPreciseNumber(3)),
        ("0.0", VeryPreciseNumber(0)),
        ("1.0", VeryPreciseNumber(1)),
        ("1.2", VeryPreciseNumber(12, e=-1)),
        ("1.23", VeryPreciseNumber(123, e=-2)),
        ("12.34", VeryPreciseNumber(1234, e=-2)),
    ],
)
def test_from_string(s: str, expect: VeryPreciseNumber) -> None:
    actual = VeryPreciseNumber.from_string(s)
    assert actual == expect


@mark.parametrize(
    "vpn, expect",
    [
        (VeryPreciseNumber(0), 0),
        (VeryPreciseNumber(1), 0),
        (VeryPreciseNumber(10), 0),
        (VeryPreciseNumber(1, e=-1), -1),
    ],
)
def test_least_significant_exponent(vpn: VeryPreciseNumber, expect: int) -> None:
    assert vpn.least_significant_exponent == expect


@mark.parametrize(
    "vpn, expect",
    [
        (VeryPreciseNumber(0), 0),
        (VeryPreciseNumber(1), 0),
        (VeryPreciseNumber(10), 1),
        (VeryPreciseNumber(100), 2),
        (VeryPreciseNumber(1, e=1), 1),
        (VeryPreciseNumber(1, e=2), 2),
        (VeryPreciseNumber(1, e=-1), -1),
    ],
)
def test_most_significant_exponent(vpn: VeryPreciseNumber, expect: int) -> None:
    assert vpn.most_significant_exponent == expect


@mark.parametrize(
    "vpn, expect",
    [
        (VeryPreciseNumber(0), (0, 0)),
        (VeryPreciseNumber(1), (0, 0)),
        (VeryPreciseNumber(10), (0, 0)),
        (VeryPreciseNumber(1, e=-1), (1, -1)),
        (VeryPreciseNumber(1, e=-2), (1, -2)),
        (VeryPreciseNumber(300, e=-5), (3, -3)),  # 0.00300
        (VeryPreciseNumber(1, e=-1), (1, -1)),
        (VeryPreciseNumber(1, e=-2), (1, -2)),
        (VeryPreciseNumber(1, e=-3), (1, -3)),
        (VeryPreciseNumber(97, e=-2), (97, -2)),
    ],
)
def test_normal_fractional(vpn: VeryPreciseNumber, expect: tuple[int, int]) -> None:
    assert vpn.normal_fractional == expect


@mark.parametrize(
    "number, expect",
    [
        (0, 0),
        (1, 1),
        (11, 2),
        (111, 3),
        (1111, 4),
        (11111, 5),
        (1234567890, 10),
    ],
)
def test_length(number: int, expect: int) -> None:
    assert VeryPreciseNumber.length(number) == expect


@mark.parametrize(
    "number, index, expect",
    [
        # Positive indexes:
        (123456789, 0, 9),
        (123456789, 1, 8),
        (123456789, 2, 7),
        (123456789, 3, 6),
        (123456789, 4, 5),
        (123456789, 5, 4),
        (123456789, 6, 3),
        (123456789, 7, 2),
        (123456789, 8, 1),
        (123456789, 9, 0),
        # Negative indexes:
        # (123456789, -1, 1),
        # (123456789, -2, 7),
        # (123456789, -3, 6),
        # (123456789, -4, 5),
        # (123456789, -5, 4),
        # (123456789, -6, 3),
        # (123456789, -7, 2),
        # (123456789, -8, 1),
        # (123456789, -9, 0),
    ],
)
def test_nth(number: int, index: int, expect: int) -> None:
    assert VeryPreciseNumber.nth(number, index) == expect


@mark.parametrize(
    "vpn, expect",
    [
        (VeryPreciseNumber(0), 0),
        (VeryPreciseNumber(1), 1),
        (VeryPreciseNumber(2), 2),
        (VeryPreciseNumber(3, e=1), 30),
        (VeryPreciseNumber(30, e=-1), 3),
        (VeryPreciseNumber(31, e=-1), 3),
        (VeryPreciseNumber(31, e=-2), 0),
    ],
)
def test_integral(vpn: VeryPreciseNumber, expect: int) -> None:
    assert vpn.integral == expect


# @mark.parametrize(
#     "vpn, expect",
#     [
#         (VeryPreciseNumber(0), 1),
#         (VeryPreciseNumber(0, exponent=1), 10),
#         (VeryPreciseNumber(0, exponent=2), 100),
#         (VeryPreciseNumber(0, exponent=-1), 0.1),
#         (VeryPreciseNumber(0, exponent=-2), 0.01),
#     ],
# )
# def test_scale(vpn: VeryPreciseNumber, expect: int) -> None:
#     assert vpn.scale == expect


@mark.parametrize(
    "vpn, expect",
    [
        # (VeryPreciseNumber(0), VeryPreciseNumber(1)),
        # (VeryPreciseNumber(0, exponent=1), 10),
        # (VeryPreciseNumber(0, exponent=2), 100),
        # (VeryPreciseNumber(0, exponent=-1), 0.1),
        # (VeryPreciseNumber(0, exponent=-2), 0.01),
    ],
)
def test_scale(vpn: VeryPreciseNumber, expect: VeryPreciseNumber) -> None:
    assert vpn.scale == expect


@mark.parametrize(
    "a, b, expect",
    [
        (VeryPreciseNumber(0), VeryPreciseNumber(0), VeryPreciseNumber(0)),
        (VeryPreciseNumber(1), VeryPreciseNumber(0), VeryPreciseNumber(1)),
        (VeryPreciseNumber(1), VeryPreciseNumber(1), VeryPreciseNumber(0)),
        # (VeryPreciseNumber(2), VeryPreciseNumber(1), VeryPreciseNumber(1)),
        # (VeryPreciseNumber(30), VeryPreciseNumber(20), VeryPreciseNumber(10)),
        # (VeryPreciseNumber(34), VeryPreciseNumber(23), VeryPreciseNumber(11)),
        # (VeryPreciseNumber(300), VeryPreciseNumber(1), VeryPreciseNumber(299)),
        # (VeryPreciseNumber(3, e=2), VeryPreciseNumber(1), VeryPreciseNumber(299)),
        # (VeryPreciseNumber(3), VeryPreciseNumber(11, e=-1), VeryPreciseNumber(19, e=-1)),
        # (VeryPreciseNumber(125, e=-2), VeryPreciseNumber(11, e=-1), VeryPreciseNumber(15, e=-2)),
        # (VeryPreciseNumber(5), VeryPreciseNumber(9, e=-1), VeryPreciseNumber(41, e=-1)),
        # (VeryPreciseNumber(5, e=1), VeryPreciseNumber(9, e=-1), VeryPreciseNumber(491, e=-1)),
        (
            VeryPreciseNumber(7, e=4),
            VeryPreciseNumber(96, e=-2),
            VeryPreciseNumber(6999904, e=-2),
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
    "vpn, expect",
    [
        (VeryPreciseNumber(0), "0.0"),
        (VeryPreciseNumber(1), "1.0"),
        (VeryPreciseNumber(1, e=-1), "0.1"),
        (VeryPreciseNumber(1, e=-2), "0.01"),
        (VeryPreciseNumber(1, e=-3), "0.001"),
        (VeryPreciseNumber(97, e=-2), "0.97"),
    ],
)
def test_repr(vpn: VeryPreciseNumber, expect: str) -> None:
    assert repr(vpn) == expect


# @mark.parametrize(
#     "number, expect",
#     [
#         (0, 0),
#         (1, 1),
#         (12, 21),
#         (123, 321),
#         (40, 321),
#     ],
# )
# def test_reverse(number: int, expect: int) -> None:
#     assert VeryPreciseNumber.reverse(number) == expect


@mark.parametrize(
    "vpn, d, expect",
    [
        # Even integers divided by even integers:
        (VeryPreciseNumber(2), 2, VeryPreciseNumber(1)),
        (VeryPreciseNumber(4), 2, VeryPreciseNumber(2)),
        (VeryPreciseNumber(4), 4, VeryPreciseNumber(1)),
        # Odd integers divided by even integers:
        (VeryPreciseNumber(1), 2, VeryPreciseNumber(5, e=-1)),
        (VeryPreciseNumber(1), 4, VeryPreciseNumber(25, e=-2)),
        (VeryPreciseNumber(1), 8, VeryPreciseNumber(125, e=-3)),
        # Even decimals divided by even integers:
        (VeryPreciseNumber(22, e=-1), 2, VeryPreciseNumber(11, e=-1)),
        (VeryPreciseNumber(48, e=-1), 2, VeryPreciseNumber(24, e=-1)),
        (
            VeryPreciseNumber(10044, e=-2),
            2,
            VeryPreciseNumber(5022, e=-2),
        ),
        # Odd decimals divided by even integers:
        (VeryPreciseNumber(23, e=-1), 2, VeryPreciseNumber(115, e=-2)),
        (VeryPreciseNumber(49, e=-1), 2, VeryPreciseNumber(245, e=-2)),
        (
            VeryPreciseNumber(10045, e=-2),
            2,
            VeryPreciseNumber(50225, e=-3),
        ),
        # Repeating:
        (VeryPreciseNumber(1), 3, VeryPreciseNumber(3, e=-1, repeating=3)),
        (VeryPreciseNumber(9), 11, VeryPreciseNumber(81, e=-2, repeating=81)),
    ],
)
def test_truediv(
    vpn: VeryPreciseNumber,
    d: int,
    expect: VeryPreciseNumber,
) -> None:
    actual = vpn / d
    assert actual == expect


# @mark.parametrize(
#     "iterations, expect",
#     [
#         (1, VeryPreciseNumber(4)),
#         (2, VeryPreciseNumber(27, e=-1)),
#         (3, VeryPreciseNumber(35, e=-1)),
#         (4, VeryPreciseNumber(2928572, e=-6)),
#         (5, VeryPreciseNumber(3328572, e=-6)),
#     ],
# )
# def test_pi(iterations: int, expect: VeryPreciseNumber) -> None:
#     assert VeryPreciseNumber.pi(iterations) == expect


def test_pi() -> None:
    log.setLevel("INFO")

    with open("./tests/data/leibniz.csv", mode="r") as f:
        rows = reader(f)
        next(rows)
        for row in rows:
            iterations = int(row[0])
            expect = VeryPreciseNumber.from_string(row[1])
            actual = VeryPreciseNumber.pi(iterations)
            assert actual == expect, f"Expected {expect} but got {actual} at {iterations} iterations"
