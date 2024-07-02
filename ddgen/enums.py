from __future__ import annotations

import enum


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
    smaller_than = 5
    before = 6
    after = 7
