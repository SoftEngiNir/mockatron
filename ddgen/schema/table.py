from ddgen.schema.column import Column
from typing import List, Iterator
from ddgen.helper_functions import generate_uuid_as_str

class TableSchema:
    def __init__(self, name: str, columns: List[Column] = []):
        self.id = generate_uuid_as_str()
        self.name = name
        self.columns = [self.add_column(col) for col in columns]

    def add_column(self, column: Column):
        column.table = self
        return column

    def __repr__(self):
        return f"{self.name}"

    def __iter__(self) -> Iterator[Column]:
        return iter(self.columns)
    
    # def __hash__(self):
    #     return hash((self.id))

    # def __eq__(self, other):
    #     if isinstance(other, TableSchema):
    #         return self.id == other.id 
    #     return False

