from __future__ import annotations

from ddgen.schema.base_column import BaseColumn
from ddgen.schema.database import Database
from ddgen.schema.table import Table
from ddgen.utilities.exceptions import ColumnNotFoundError, TableNotFoundError


def get_table_by_name(database: Database, table_name: str) -> Table:
    for table in database.tables:
        if table.name == table_name:
            return table
    raise TableNotFoundError(table_name)


def get_column_by_name(table: Table, col_name: str) -> BaseColumn:
    for col in table.columns:
        if col.name == col_name:
            return col
    raise ColumnNotFoundError(table.name, col_name)


def get_column(database: Database, table_name: str, col_name: str) -> BaseColumn:
    table = get_table_by_name(database, table_name)
    return get_column_by_name(table, col_name)
