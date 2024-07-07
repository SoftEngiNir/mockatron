from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from ddgen.engines.default import DataType
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
        self.data: np.ndarray = np.array(None)
        self.table: Table | None = None

    @abstractmethod
    def generate_data(self, n_rows: int) -> np.ndarray:
        pass

    def add(self, table: Table) -> BaseColumn:
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
