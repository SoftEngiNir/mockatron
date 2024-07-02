from __future__ import annotations

from ddgen.dummy_generator.generator import DummyGenerator
from ddgen.engines._int import IntPrimaryKeyEngine, IntRandEngine
from ddgen.engines._numerical import NumericalNormalDistEngine
from ddgen.engines._str import StrFromListEngine, StrNameEngine
from ddgen.enums import DataType
from ddgen.schema.column import Column, ForeignKey
from ddgen.schema.database import Database
from ddgen.schema.table import Table
from ddgen.utilities.connection import TEST_ENGINE, session_context
from ddgen.utilities.sql import execute_raw_sql, get_ddl
from ddgen.utilities.writers import csv_dump, db_dump

# from ddgen.utilities.graph import construct_graph
# from ddgen.utilities.graph import vizualize_graph

# User Columns
user_id = Column('id', DataType._int, engine=IntPrimaryKeyEngine(), is_primary=True)
user_name = Column('name', DataType._str, engine=StrNameEngine())
user_age = Column(
    'age',
    DataType._int,
    engine=IntRandEngine(min_val=0, max_val=100),
    is_nullable=True,
    percentage=5,
)
user_creation_date = Column('creation_date', DataType._date)
USER_COLUMNS = [user_id, user_name, user_age, user_creation_date]
# User table
USER_TABLE = Table('users', columns=USER_COLUMNS)


product_id = Column('id', DataType._int, engine=IntPrimaryKeyEngine(), is_primary=True)
product_name = Column('name', DataType._str)
product_price = Column(
    'price',
    DataType._str,
    engine=NumericalNormalDistEngine(100, 10),
)
PRODUCT_COLUMNS = [product_id, product_name, product_price]
# Product table
PRODUCT_TABLE = Table('product', columns=PRODUCT_COLUMNS)


category_id = Column('id', DataType._int, engine=IntPrimaryKeyEngine(), is_primary=True)
category_name = Column(
    'name',
    DataType._str,
    engine=StrFromListEngine(
        ['Laptops', 'Mobile Phones', 'Televisions', 'Gaming Consoles'],
    ),
)
CATEGORY_COLUMNS = [category_id, category_name]
# Product table
CATEGORY_TABLE = Table('category', columns=CATEGORY_COLUMNS)


product_category_id = Column(
    'id',
    DataType._int,
    engine=IntPrimaryKeyEngine(),
    is_primary=True,
)
fk_category_id = ForeignKey('category_id', category_id)
fk_product_id = ForeignKey('product_id', product_id)


PRODUCT_CATEGORY_COLUMNS = [product_category_id, fk_category_id, fk_product_id]
# ProductCategory table
PRODUCT_CATEGORY_TABLE = Table(
    'product_category',
    columns=PRODUCT_CATEGORY_COLUMNS,
)


order_id = Column('id', DataType._int, engine=IntPrimaryKeyEngine(), is_primary=True)
fk_user_id = ForeignKey('user_id', user_id)
fk_order_product_id = ForeignKey('product_id', product_id)
order_datetime = Column('order_datetime', DataType._datetime)

ORDER_COLUMNS = [order_id, fk_user_id, fk_order_product_id, order_datetime]
# Order table
ORDER_TABLE = Table('orders', columns=ORDER_COLUMNS)


# Schema definition
database = Database(
    'public',
    tables=[
        USER_TABLE,
        PRODUCT_TABLE,
        CATEGORY_TABLE,
        PRODUCT_CATEGORY_TABLE,
        ORDER_TABLE,
    ],
)

table_n_rows = {
    USER_TABLE: 100,
    PRODUCT_TABLE: 15,
    CATEGORY_TABLE: 4,
    PRODUCT_CATEGORY_TABLE: 40,
    ORDER_TABLE: 300,
}

ddgen = DummyGenerator(database)
ddgen.generate(table_n_rows)
path = 'dummy_data'
csv_dump(path, database)

with session_context(engine=TEST_ENGINE) as session:
    ddl = get_ddl(database)
    execute_raw_sql(session, ddl)

db_dump(TEST_ENGINE, database)


# graph = construct_graph(db_schema.graph_dict)
# vizualize_graph(graph)
