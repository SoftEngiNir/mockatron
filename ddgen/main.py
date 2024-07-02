from __future__ import annotations

from datetime import date

from ddgen.dummy_generator.generator import DummyGenerator
from ddgen.engines._date import DateRandEngine
from ddgen.engines._int import IntPrimaryKeyEngine
from ddgen.engines._int import IntRandEngine
from ddgen.engines._str import StrNameEngine
from ddgen.engines._str import StrUuidEngine
from ddgen.enums import DataType
from ddgen.schema.column import Column
from ddgen.schema.column import ForeignKey
from ddgen.schema.database import Database
from ddgen.schema.table import Table
from ddgen.utilities.writers import csv_dump

# Column definition
user_id = Column(
    'id',
    DataType._int,
    engine=IntPrimaryKeyEngine(),
    is_primary=True,
)
user_uuid = Column('uuid', DataType._str, engine=StrUuidEngine())
user_name = Column('name', DataType._str, engine=StrNameEngine())
user_age = Column(
    'age',
    DataType._int,
    engine=IntRandEngine(min_val=0, max_val=100),
    is_nullable=True,
    percentage=50,
)

user_creation_date = Column('creation_date', DataType._date)

# Table definition
USER_TABLE = Table(
    'User',
    columns=[user_id, user_uuid, user_name, user_age, user_creation_date],
)

purchase_id = Column(
    'id',
    DataType._int,
    engine=IntPrimaryKeyEngine(),
    is_primary=True,
)

fk_user_id = ForeignKey('user_id', user_id)


purchase_datetime = Column(
    'purchase_datetime',
    DataType._date,
    engine=DateRandEngine(start_date=date(2000, 1, 1)),
)


PURCHASE_TABLE = Table(
    'UserPurchase',
    columns=[purchase_id, fk_user_id, purchase_datetime],
)


# Schema definition
db_schema = Database(
    'public',
    tables=[USER_TABLE, PURCHASE_TABLE],
)

table_n_rows = {USER_TABLE: 300, PURCHASE_TABLE: 30}


ddgen = DummyGenerator(db_schema)
ddgen.generate(table_n_rows)
path = 'dummy_data'
csv_dump(path, ddgen)
