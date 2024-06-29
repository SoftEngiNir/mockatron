import enum
from typing import NamedTuple, Optional
from ddgen.engines.base import Engine

class DataType(enum.Enum):

    _int = 1
    _str = 2
    _date = 3
    _datetime = 4

class RelationshipType(enum.Enum):

    one_to_one = 1
    one_to_many = 2
    many_to_many = 3
    greater_than = 4


class ColumnConfiguration(NamedTuple):

    name: str
    dtype: DataType
    engine: Optional[Engine] = None
    is_primary: Optional[bool]=False,
    is_nullable: Optional[bool]=False,
    percentage: Optional[int]=5