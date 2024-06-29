from ddgen.schema.db_schema import DBSchema
from ddgen.schema.table import TableSchema
from ddgen.schema.column import Column
from ddgen.enums import RelationshipType
from ddgen.helper_functions import sample_from_array
from typing import Dict, Tuple
import numpy as np
import random

from ddgen.engines.base import ArrayEngine
from ddgen.engines.default import DEFAULT_ENGINES


def add_nones(array: np.ndarray, percentage: int):
    per_size = int(array.size * percentage / 100)
    indecies = random.sample(range(array.size), per_size)
    np.put(array, indecies, None)
    return array


def generate_col_data(column: Column, n_rows):
    if not column.engine:
        column.engine = DEFAULT_ENGINES.get(column.col_type)()
    a_eng = ArrayEngine(column.engine, n_rows)
    array_out = np.array(a_eng.sample())
    if column.is_nullable:
        array_out = array_out.astype("object")
        add_nones(array_out, column.percentage)
    return array_out


RELATIONSHIP_HANDLERS = {
    RelationshipType.one_to_one: lambda from_data, n_rows :sample_from_array(
            from_data, n_rows, False
        ),
    RelationshipType.one_to_many: lambda from_data, n_rows :sample_from_array(
            from_data, n_rows, True
        ),
    RelationshipType.greater_than: lambda from_data, n_rows :sample_from_array(
            from_data, n_rows, True
        )
}


class DummyGenerator:
    def __init__(self, db_schema: DBSchema) -> None:
        self.db_schema = db_schema
        self.data_dict = {}
        pass

            
    def _handle_relation(self, n_rows, cols: Tuple[Column, Column], r_type: RelationshipType):
        to_col, from_col = cols
        from_data = self.data_dict[from_col]
        self.data_dict[to_col] = RELATIONSHIP_HANDLERS[r_type](from_data, n_rows)


    def generate(self, table_nrows: Dict[TableSchema, int] = {}):
        table_dependencies = self.db_schema.get_table_dependencies()
        for _, tables in table_dependencies.items():
            for table in tables:
                n_rows = table_nrows[table]
                self._generate_table_data(n_rows, table)


    def _generate_table_data(self, n_rows, table: TableSchema):
        for column in table:
            if column not in self.db_schema.to_from_cols.keys():
                self.data_dict[column] = generate_col_data(column, n_rows)

            else:
                cols = (column,self.db_schema.to_from_cols[column])
                r_type = self.db_schema.relation_map[cols]
                self._handle_relation(n_rows, cols, r_type)
                
