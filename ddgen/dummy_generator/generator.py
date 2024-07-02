from __future__ import annotations

import numpy as np

from ddgen.schema.column import BaseColumn
from ddgen.schema.database import Database
from ddgen.schema.table import Table


class DummyGenerator:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.data_dict: dict[BaseColumn, np.ndarray] = {}
        pass

    def generate(self, table_nrows: dict[Table, int] = {}):
        table_dependencies = self.database.get_table_dependencies()
        for _, tables in table_dependencies.items():
            for table in tables:
                n_rows = table_nrows[table]
                self._generate_table_data(n_rows, table)

    def _generate_table_data(self, n_rows, table: Table):
        for column in table:
            self.data_dict[column] = column.generate_data(n_rows)
