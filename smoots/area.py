from typing import Any, Generic
from bounden import Volume, Volume2
from smoots.lengths import LengthT


class Area(Volume, Generic[LengthT]):
    def __init__(self, *lengths: LengthT, **kwargs: Any) -> None:
        super().__init__(*lengths, **kwargs)



class Area2(Volume2, Generic[LengthT]):
    def __init__(self, width: LengthT, height: LengthT, **kwargs: Any) -> None:
        super().__init__(width, height, **kwargs)
