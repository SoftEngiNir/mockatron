from ._int import IntRandEngine
from ._str import StrRandEngine
from ._date import DateRandEngine, DateTimeRandEngine
from ddgen.enums import DataType
from typing import Final, Dict
from ..engines.base import Engine

DEFAULT_ENGINES: Final[Dict[DataType, Engine]] = {
    DataType._int: IntRandEngine,
    DataType._str: StrRandEngine,
    DataType._date: DateRandEngine,
    DataType._datetime: DateTimeRandEngine,
}
