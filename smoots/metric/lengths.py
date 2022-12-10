from smoots.metric.metric import Metric
from smoots.metric.units import CentimetreUnit, MetreUnit


class Centimetres(CentimetreUnit, Metric):
    """
    A length in centimetres.
    """


class Metres(MetreUnit, Metric):
    """
    A length in metres.
    """
