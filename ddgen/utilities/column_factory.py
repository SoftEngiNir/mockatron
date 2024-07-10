from ddgen.engines import ENGINE_REGISTRY, Engine
from ddgen.engines.default import DEFAULT_ENGINES
from ddgen.enums import DataType, RelationshipType
from ddgen.models import ColumnModel
from ddgen.schema.base_column import BaseColumn
from ddgen.schema.column import Column, ForeignKey, RelatedColumn
from ddgen.schema.database import Database
from ddgen.utilities.schema_utils import get_column

COL_TYPE: dict[str, DataType] = {
    'string': DataType._str,
    'integer': DataType._int,
    'date': DataType._date,
    'timestamp': DataType._datetime,
}

RTYPE: dict[str, RelationshipType] = {
    'one_to_one': RelationshipType.one_to_one,
    'one_to_many': RelationshipType.one_to_many,
    'after': RelationshipType.after,
    'before': RelationshipType.before,
}


class ColumnFactory:
    @staticmethod
    def create_column(col_model: ColumnModel, database: Database) -> BaseColumn:
        if col_model.foreign_key:
            return ColumnFactory._create_foreign_key_column(col_model, database)

        if col_model.related_column:
            return ColumnFactory._create_related_column(col_model, database)

        return ColumnFactory._create_standard_column(col_model)

    @staticmethod
    def _create_foreign_key_column(
        col_model: ColumnModel, database: Database
    ) -> ForeignKey:
        if col_model.foreign_key is None:
            raise ValueError('Foreign key model is None')
        source_col = get_column(
            database, col_model.foreign_key.table, col_model.foreign_key.source_col
        )
        return ForeignKey(col_model.name, source_col)

    @staticmethod
    def _create_related_column(
        col_model: ColumnModel, database: Database
    ) -> RelatedColumn:
        if col_model.related_column is None:
            raise ValueError('Related column model is None')

        source_col = get_column(
            database,
            col_model.related_column.table,
            col_model.related_column.source_col,
        )
        rtype = RTYPE[col_model.related_column.rtype]
        return RelatedColumn(col_model.name, source_col, rtype)

    @staticmethod
    def _create_standard_column(col_model: ColumnModel) -> Column:
        if col_model.dtype is None:
            raise ValueError('Column dtype is None')
        dtype = COL_TYPE[col_model.dtype]
        engine = ColumnFactory._get_engine(col_model, dtype)
        return Column(
            col_model.name,
            dtype,
            engine,
            col_model.is_primary,
            col_model.is_nullable,
            col_model.percentage,
        )

    @staticmethod
    def _get_engine(col_model: ColumnModel, dtype: DataType) -> Engine:
        if not col_model.engine:
            return DEFAULT_ENGINES[dtype]()
        engine_class = ENGINE_REGISTRY[col_model.engine.name]
        return (
            engine_class(**col_model.engine.config)
            if col_model.engine.config
            else engine_class()
        )
