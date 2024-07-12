from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator

from ddgen.schema.column import ForeignKey
from ddgen.schema.table import Table
from ddgen.utilities.graph import construct_graph, sorted_in_degree
from ddgen.utilities.sql import _get_ddl


class Database:
    def __init__(
        self,
        schema: str,
        tables: list[Table] = [],
    ) -> None:
        self.schema = schema
        self.graph_dict: dict[Table, list[Table]] = defaultdict(list)
        self.tables = []
        self.tables = [self.add_table(table) for table in tables]
        self.table_nrows: dict[Table, int] = {}

    def __iter__(self) -> Iterator[Table]:
        return iter(self.tables)

    def _add_fk_relationships(self, table):
        for column in table:
            if isinstance(column, ForeignKey):
                self.graph_dict[column.source_col.table].append(column.table)

    def add_table(self, table: Table):
        table.schema = self.schema
        self.tables.append(table)
        if table not in self.graph_dict.keys():
            self.graph_dict[table] = []
        self._add_fk_relationships(table)
        return table

    def get_table_dependencies(self) -> dict[int, list[Table]]:
        graph = construct_graph(self.graph_dict)
        return sorted_in_degree(graph)

    def get_ddl(self) -> str:
        return _get_ddl(self)
