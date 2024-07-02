from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from ddgen.enums import DataType
from ddgen.schema.column import ForeignKey
from ddgen.schema.database import Database
from ddgen.schema.table import Table

COL_TYPE_MAP = {
    DataType._int: 'INT',
    DataType._str: 'VARCHAR',
    DataType._date: 'DATE',
    DataType._datetime: 'TIMESTAMP',
}


def create_schema_sql(schema: str):
    return f"""
    DROP SCHEMA IF EXISTS {schema} CASCADE;
    CREATE SCHEMA IF NOT EXISTS {schema};
    SET search_path TO {schema};
    """


def drop_table_sql(table: Table) -> str:
    return f"""
        DROP TABLE IF EXISTS {table.name} CASCADE;
        """


def create_table_sql(table: Table) -> str:
    statements = []
    schema = f'{table.schema}.' if table.schema else ''

    for col in table.columns:
        not_null = 'NOT NULL' if not col.is_nullable else ''
        statements.append(
            f'    {col.name} {COL_TYPE_MAP.get(col.col_type)} {not_null},',
        )

    col_str = '\n'.join(statements).strip()

    create_table_str = f"""
    CREATE TABLE IF NOT EXISTS {schema}{table.name} (
    {col_str}
    PRIMARY KEY ({table.primary_key})
    );
    """
    return create_table_str.strip()


def add_foreign_key_sql(column: ForeignKey):
    if column.source_col.table is None or column.table is None:
        raise ValueError('A fk must belond to a table')
    schema = f'{column.table.schema}.' if column.table.schema else ''
    return f"""
    ALTER TABLE {schema}{column.table.name}
    ADD FOREIGN KEY ({column.name}) REFERENCES {schema}{column.source_col.table.name}({column.source_col.name}
    );
    """.strip()


def table_post_setup_sql(table: Table) -> str:
    statements = []
    for col in table:
        if isinstance(col, ForeignKey):
            statements.append(add_foreign_key_sql(col))
    return '\n'.join(statements).strip()


def get_ddl(database: Database) -> str:
    create_schema = [create_schema_sql(database.schema_name)]
    create_tables = []
    post_setup = []
    for table in database.tables:
        create_tables.append(create_table_sql(table))
        post_setup_sql = table_post_setup_sql(table)
        if post_setup_sql:
            post_setup.append(post_setup_sql)
    return '\n'.join(create_schema + create_tables + post_setup).strip()


def execute_raw_sql(session: Session, sql: str) -> None:
    session.execute(text(sql))
