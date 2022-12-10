"""
&copy; 2022 Cariad Eccleston and released under the MIT License.

For usage and support, see https://github.com/cariad/smoots.
"""

from importlib.resources import files

from smoots.imperial import Feet, Imperial, Inches, Miles, Yards
from smoots.length import Length
from smoots.metric import Centimetres, Metres, Metric


def version() -> str:
    """
    Gets the package's version.
    """

    with files(__package__).joinpath("VERSION").open("r") as t:
        return t.readline().strip()


__all__ = [
    "Centimetres",
    "Feet",
    "Imperial",
    "Inches",
    "Length",
    "Metres",
    "Metric",
    "Miles",
    "Yards",
    "version",
]
