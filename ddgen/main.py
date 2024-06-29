from ddgen.engines._int import IntRandEngine, IntPrimaryKeyEngine
from ddgen.engines._str import StrNameEngine, StrUuidEngine
from ddgen.schema.column import Column
from ddgen.schema.table import TableSchema
from ddgen.schema.db_schema import DBSchema
from ddgen.generator import DummyGenerator
from ddgen.schema.relationship import Relationship
from ddgen.enums import RelationshipType, DataType, ColumnConfiguration
from ddgen.writers import csv_dump


def create_column(col_config: ColumnConfiguration):
    return Column(
        col_config.name,
        col_config.dtype,
        engine=col_config.engine,
        is_primary=col_config.is_primary,
        is_nullable=col_config.is_nullable,
    )


user_id = ColumnConfiguration(
    name="id", dtype=DataType._int, engine=IntPrimaryKeyEngine()
)

print(create_column(user_id))

# Column definition
user_id = Column("id", DataType._int, engine=IntPrimaryKeyEngine())
user_uuid = Column("uuid", DataType._str, engine=StrUuidEngine())
user_name = Column("name", DataType._str, engine=StrNameEngine())
user_age = Column(
    "age",
    DataType._int,
    engine=IntRandEngine(min_val=0, max_val=100),
    is_nullable=True,
    percentage=50,
)
user_creation_date = Column("creation_date", DataType._date)

purchase_id = Column("id", DataType._int, engine=IntPrimaryKeyEngine())
fk_user_id = Column("user_id", DataType._int, engine=IntPrimaryKeyEngine())
purchase_datetime = Column("purchase_datetime", DataType._datetime)
# Table definition
USER_TABLE = TableSchema(
    "User", columns=[user_id, user_uuid, user_name, user_age, user_creation_date]
)
PURCHASE_TABLE = TableSchema(
    "UserPurchase", columns=[purchase_id, fk_user_id, purchase_datetime]
)

relationship_user_id = Relationship(user_id, fk_user_id, RelationshipType.one_to_many)
# relationship_user_id2 = Relationship(fk_user_id, user_id, RelationshipType.one_to_many)

# Schema definition
db_schema = DBSchema(
    "public", tables=[USER_TABLE, PURCHASE_TABLE], relationships=[relationship_user_id]
)

table_n_rows = {
    USER_TABLE: 10,
    PURCHASE_TABLE: 300
}


ddgen = DummyGenerator(db_schema)
ddgen.generate(table_n_rows)
path = 'dummy_data'
csv_dump(path, ddgen)
