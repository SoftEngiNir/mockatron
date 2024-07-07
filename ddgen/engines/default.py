from __future__ import annotations

from typing import Final

from ddgen.engines._date import DateRandEngine, DateTimeRandEngine
from ddgen.engines._int import IntRandEngine
from ddgen.engines._str import StrRandEngine
from ddgen.engines.base import RandEngine
from ddgen.enums import DataType

DEFAULT_ENGINES: Final[dict[DataType, type[RandEngine]]] = {
    DataType._int: IntRandEngine,  # type: ignore
    DataType._str: StrRandEngine,  # type: ignore
    DataType._date: DateRandEngine,  # type: ignore
    DataType._datetime: DateTimeRandEngine,  # type: ignore
}
