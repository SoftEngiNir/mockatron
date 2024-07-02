from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from ddgen.dummy_generator.utils import add_nones, data_from_engine, fk_data
from ddgen.engines.base import Engine
from ddgen.engines.default import DEFAULT_ENGINES, DataType
from ddgen.enums import RelationshipType
from ddgen.utilities.helper_functions import generate_uuid_as_str

if TYPE_CHECKING:
    from ddgen.schema.table import Table


class BaseColumn(ABC):
    def __init__(
        self,
        name,
        col_type: DataType,
        is_primary=False,
        is_nullable=False,
        percentage=5,
    ):
        self._id = generate_uuid_as_str()
        self.name = name
        self.col_type = col_type
        self.is_primary = is_primary
        self.is_nullable = is_nullable
        self.percentage = percentage
        self.data = None
        self.table: Table | None = None

    @abstractmethod
    def generate_data(self, n_rows: int) -> np.ndarray:
        pass

    def add(self, table) -> BaseColumn:
        self.table = table
        if self.is_primary:
            table.primary_key = self
        return self

    def __repr__(self):
        return f'{self.name}'

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        if isinstance(other, BaseColumn):
            return self._id == other._id
        return False


class Column(BaseColumn):
    def __init__(
        self,
        name,
        col_type: DataType,
        engine: Engine | None = None,
        is_primary=False,
        is_nullable=False,
        percentage=5,
    ):
        super().__init__(
            name,
            col_type=col_type,
            is_nullable=is_nullable,
            percentage=percentage,
        )
        self.engine = engine
        self.is_primary = is_primary

    def generate_data(self, n_rows):
        if not self.engine:
            self.engine = DEFAULT_ENGINES.get(self.col_type)()

        self.data = data_from_engine(self.engine, n_rows)
        if self.is_nullable:
            self.data = add_nones(self.data, self.percentage)
        return self.data


class ForeignKey(BaseColumn):
    def __init__(
        self,
        name,
        source_col: BaseColumn,
        r_type=RelationshipType.one_to_many,
        is_nullable=False,
        percentage=5,
    ):
        super().__init__(
            name,
            col_type=source_col.col_type,
            is_nullable=is_nullable,
            percentage=percentage,
        )
        self.source_col = source_col
        self.r_type = r_type
        self.is_primary = False  # Can't be both FK and PK

    def generate_data(self, n_rows):
        self.data = fk_data(self.source_col.data, n_rows, self.r_type)
        if self.is_nullable:
            self.data = add_nones(self.data, self.percentage)
        return self.data


# class RelatedColumn(BaseColumn):
#     def __init__(
#         self,
#         name,
#         source_col: BaseColumn,
#         r_type=RelationshipType.one_to_many,
#         is_nullable=False,
#         percentage=5,
#     ):
#         super().__init__(name, source_col.col_type, is_nullable, percentage)
#         self.source_col = source_col  # user_creation_date
#         self.r_type = r_type
#         self.source_pk = self.source_col.table.primary_key  # User.id
#         self.target_fk = None

#     def get_fk_col(self):
#         for col in self.table.columns:
#             if isinstance(col, FK) and col.source_col.table == self.source_pk.table:
#                 return col
