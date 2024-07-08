from ddgen.engines import ENGINE_REGISTRY
from ddgen.engines.default import DEFAULT_ENGINES
from ddgen.enums import DataType
from ddgen.models import ColumnModel
from ddgen.schema.base_column import BaseColumn
from ddgen.schema.column import Column, ForeignKey
from ddgen.schema.database import Database
from ddgen.utilities.schema_utils import get_column

COL_TYPE: dict[str, DataType] = {
    'string': DataType._str,
    'integer': DataType._int,
    'date': DataType._date,
    'timestamp': DataType._datetime,
}


class ColumnFactory:
    @staticmethod
    def create_column(col_model: ColumnModel, database: Database) -> BaseColumn:
        dtype = COL_TYPE[col_model.dtype]
        if col_model.foreign_key is not None:
            source_col_name = col_model.foreign_key.source_col
            source_table_name = col_model.foreign_key.table
            source_col = get_column(database, source_table_name, source_col_name)
            return ForeignKey(col_model.name, source_col)

        if not col_model.engine:
            engine = DEFAULT_ENGINES[dtype]()
        else:
            engine_class = ENGINE_REGISTRY[col_model.engine.name]
            engine = (
                engine_class(**col_model.engine.config)
                if col_model.engine.config
                else engine_class()
            )
        return Column(
            col_model.name,
            dtype,
            engine,
            col_model.is_primary,
            col_model.is_nullable,
            col_model.percentage,
        )
