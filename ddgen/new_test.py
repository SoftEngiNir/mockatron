from ddgen.engines._int import IntRandEngine, IntPrimaryKeyEngine
from ddgen.engines._numerical import NumericalNormalDistEngine
from ddgen.engines._str import StrNameEngine, StrUuidEngine, StrFromListEngine
from ddgen.schema.column import Column
from ddgen.schema.table import TableSchema
from ddgen.schema.db_schema import DBSchema
from ddgen.generator import DummyGenerator
from ddgen.schema.relationship import Relationship
from ddgen.enums import RelationshipType, DataType, ColumnConfiguration
from ddgen.writers import csv_dump
from typing import Dict, List
from ddgen.graph import construct_graph, vizualize_graph


# User Columns
user_id = Column("id", DataType._int, engine=IntPrimaryKeyEngine())
user_name = Column("name", DataType._str, engine=StrNameEngine())
user_age = Column(
    "age",
    DataType._int,
    engine=IntRandEngine(min_val=0, max_val=100),
    is_nullable=True,
    percentage=5,
)
user_creation_date = Column("creation_date", DataType._date)
USER_COLUMNS = [user_id, user_name, user_age, user_creation_date]
# User table
USER_TABLE = TableSchema("user", columns=USER_COLUMNS)


product_id = Column("id", DataType._int, engine=IntPrimaryKeyEngine())
product_name = Column("name", DataType._str)
product_price = Column(
    "price", DataType._str, engine=NumericalNormalDistEngine(100, 10)
)
PRODUCT_COLUMNS = [product_id, product_name, product_price]
# Product table
PRODUCT_TABLE = TableSchema("product", columns=PRODUCT_COLUMNS)


category_id = Column("id", DataType._int, engine=IntPrimaryKeyEngine())
category_name = Column(
    "name",
    DataType._str,
    engine=StrFromListEngine(
        ["Laptops", "Mobile Phones", "Televisions", "Gaming Consoles"]
    ),
)
CATEGORY_COLUMNS = [category_id, category_name]
# Product table
CATEGORY_TABLE = TableSchema("category", columns=CATEGORY_COLUMNS)


product_category_id = Column("id", DataType._int, engine=IntPrimaryKeyEngine())
fk_category_id = Column("category_id", DataType._int)
fk_product_id = Column("product_id", DataType._int)

PRODUCT_CATEGORY_COLUMNS = [product_category_id, fk_category_id, fk_product_id]
# ProductCategory table
PRODUCT_CATEGORY_TABLE = TableSchema("product_category", columns=PRODUCT_CATEGORY_COLUMNS)



order_id = Column("id", DataType._int, engine=IntPrimaryKeyEngine())
fk_user_id = Column("user_id", DataType._int)
fk_order_product_id = Column("product_id", DataType._int)
order_datetime = Column("order_datetime", DataType._datetime)

ORDER_COLUMNS = [order_id, fk_user_id, fk_order_product_id, order_datetime]
# Order table
ORDER_TABLE = TableSchema("order", columns=ORDER_COLUMNS)


# Relationships
relat_id_category_id = Relationship(category_id, fk_category_id, RelationshipType.one_to_many)
relat_id_product_id = Relationship(product_id, fk_product_id, RelationshipType.one_to_many)
relat_id_user_id = Relationship(user_id, fk_user_id, RelationshipType.one_to_many)
relat_id_order_product_id = Relationship(product_id, fk_order_product_id, RelationshipType.one_to_many)
RELATIONSHIPS = [relat_id_category_id, relat_id_product_id, relat_id_user_id, relat_id_order_product_id]


# Schema definition
db_schema = DBSchema(
    "public",
    tables=[USER_TABLE, PRODUCT_TABLE, CATEGORY_TABLE, PRODUCT_CATEGORY_TABLE, ORDER_TABLE],
    relationships=RELATIONSHIPS,
)


table_n_rows = {
    USER_TABLE: 100,
    PRODUCT_TABLE: 15,
    CATEGORY_TABLE: 3,
    PRODUCT_CATEGORY_TABLE: 40,
    ORDER_TABLE: 300,
}


ddgen = DummyGenerator(db_schema)
ddgen.generate(table_n_rows)
path = 'dummy_data'
csv_dump(path, ddgen)






