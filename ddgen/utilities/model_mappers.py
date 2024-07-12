from ddgen.models import DatabaseModel, TableModel
from ddgen.schema.database import Database
from ddgen.schema.table import Table
from ddgen.utilities.column_factory import ColumnFactory


def table_from_model(table_model: TableModel, database: Database):
    columns = []
    for col_model in table_model.columns:
        column = ColumnFactory.create_column(col_model, database)
        columns.append(column)
    return Table(table_model.name, columns)


def database_from_model(db_model: DatabaseModel, schema: str = 'public') -> Database:
    table_nrows: dict = {}
    database = Database(schema=schema)
    for table_model in db_model.tables:
        table = table_from_model(table_model, database)
        database.add_table(table)
        table_nrows[table] = table_model.nrows
    database.table_nrows = table_nrows
    return database
