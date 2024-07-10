from __future__ import annotations

from collections.abc import Iterator, Sequence

from ddgen.schema.base_column import BaseColumn
from ddgen.utilities.helper_functions import generate_uuid_as_str


class Table:
    def __init__(
        self,
        name: str,
        columns: Sequence[BaseColumn] = [],
        schema: str = 'public',
    ) -> None:
        self.id = generate_uuid_as_str()
        self.name = name
        self.primary_key: BaseColumn | None = None
        self.columns = [self.add_column(col) for col in columns]
        self.schema = schema

    def add_column(self, column: BaseColumn) -> BaseColumn:
        return column.add(self)

    def __repr__(self):
        return f'{self.name}'

    def __iter__(self) -> Iterator[BaseColumn]:
        return iter(self.columns)
