from __future__ import annotations

from sqlalchemy import text

from ddgen.enums import DataType
from ddgen.new_test import db_schema
from ddgen.schema.table import Table
from ddgen.sql.connection import session_context
from ddgen.sql.connection import TEST_ENGINE

COL_TYPE_MAP = {
    DataType._int: 'int',
    DataType._str: 'varchar',
    DataType._date: 'date',
}


def create_schema_sql(schema: str):
    return f"""
    CREATE SCHEMA IF NOT EXISTS {schema};
    SET search_path TO {schema};
    """


def drop_table_sql(table: Table) -> str:
    return f"""
        DROP TABLE IF EXISTS {table.name} CASCADE;
        """


def create_table_sql(table: Table) -> str:
    # col_str = "\n".join(
    #     [f"{col.name} {COL_TYPE_MAP.get(col.col_type)}," for col in table.columns]
    # )
    col_str = '\n'
    statements = []
    schema = f'{table.schema}.' if table.schema else ''
    for col in table.columns:
        not_null = ''
        if not col.is_nullable:
            not_null = 'NOT NULL'
        statements.append(
            f'{col.name} {COL_TYPE_MAP.get(col.col_type)} {not_null},',
        )
    col_str = col_str.join(statements).strip()

    create_table_str = f"""
        CREATE TABLE IF NOT EXISTS {schema}{table.name} (
                {col_str[:-1]}
        );
        """
    return create_table_str


schema_sql = create_schema_sql('public')
table_sql = create_table_sql(db_schema.tables[0])

with session_context(TEST_ENGINE) as session:
    session.execute(text(table_sql))
