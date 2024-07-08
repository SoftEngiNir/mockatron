from __future__ import annotations

import numpy as np

from ddgen.dummy_generator.utils import (add_nones, data_from_engine, fk_data,
                                         related_data)
from ddgen.engines.base import Engine
from ddgen.engines.default import DEFAULT_ENGINES, DataType
from ddgen.enums import RelationshipType
from ddgen.schema.base_column import BaseColumn


class Column(BaseColumn):
    def __init__(
        self,
        name,
        dtype: DataType,
        engine: Engine | None = None,
        is_primary=False,
        is_nullable=False,
        percentage=5,
    ):
        super().__init__(
            name,
            dtype=dtype,
            is_nullable=is_nullable,
            percentage=percentage,
        )
        self.engine = engine
        self.is_primary = is_primary

    def generate_data(self, n_rows: int) -> np.ndarray:
        if not self.engine:
            self.engine = DEFAULT_ENGINES[self.dtype]()

        self.data = data_from_engine(self.engine, n_rows)
        if self.is_nullable:
            self.data = add_nones(self.data, self.percentage)
        return self.data


class ForeignKey(BaseColumn):
    def __init__(
        self,
        name,
        source_col: BaseColumn,
        rtype=RelationshipType.one_to_many,
        is_nullable=False,
        percentage=5,
    ):
        super().__init__(
            name,
            dtype=source_col.dtype,
            is_nullable=is_nullable,
            percentage=percentage,
        )
        self.source_col = source_col
        self.rtype = rtype

    def generate_data(self, n_rows: int) -> np.ndarray:
        self.data = fk_data(self.source_col.data, n_rows, self.rtype)
        if self.is_nullable:
            self.data = add_nones(self.data, self.percentage)
        return self.data


class RelatedColumn(BaseColumn):
    def __init__(
        self,
        name,
        source_col: BaseColumn,
        rtype,
        is_nullable=False,
        percentage=5,
    ):
        super().__init__(name, source_col.dtype, is_nullable, percentage)
        self.source_col = source_col
        self.rtype = rtype
        self.source_pk = (
            self.source_col.table.primary_key if self.source_col.table else None
        )
        self.target_fk = None

    def generate_data(self, n_rows: int) -> np.ndarray:
        self.data = related_data(self, n_rows)
        return self.data

    def get_fk_col(self):
        for col in self.table.columns:
            if (
                isinstance(col, ForeignKey)
                and col.source_col.table == self.source_pk.table
            ):
                return col
