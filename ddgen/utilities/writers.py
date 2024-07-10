from __future__ import annotations

import pandas as pd
from sqlalchemy.engine import Engine

from ddgen.schema.database import Database
from ddgen.schema.table import Table


def to_df(table: Table) -> pd.DataFrame:
    table_data = {col: col.data for col in table.columns}
    return pd.DataFrame(table_data)


def write_to_csv(path: str, database: Database) -> None:
    for table in database:
        table_df = to_df(table)
        table_df.to_csv(f'{path}/{table.name}.csv', index=False)


def write_to_db(engine: Engine, database: Database) -> None:
    for table in database.tables:
        df = to_df(table)
        df.to_sql(
            name=table.name,
            con=engine,
            schema=table.schema,
            if_exists='append',
            index=False,
        )
