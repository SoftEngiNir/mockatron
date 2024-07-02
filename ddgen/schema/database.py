from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator

from ddgen.schema.column import BaseColumn, ForeignKey
from ddgen.schema.table import Table
from ddgen.utilities.graph import construct_graph, sorted_in_degree


class Database:
    def __init__(
        self,
        schema_name: str,
        tables: list[Table] = [],
    ) -> None:
        self.schema_name = schema_name
        self.graph_dict: dict[BaseColumn, list[BaseColumn]] = defaultdict(list)
        self.tables = [self.add_table(table) for table in tables]

    def __iter__(self) -> Iterator[Table]:
        return iter(self.tables)

    def _add_fk_relationships(self, table):
        for column in table:
            if isinstance(column, ForeignKey):
                self.graph_dict[column.source_col].append(column)

    def add_table(self, table: Table):
        table.schema = self.schema_name
        self._add_fk_relationships(table)
        return table

    def get_table_dependencies(self) -> dict[int, list[Table]]:
        graph = construct_graph(self.graph_dict)
        return sorted_in_degree(graph)
