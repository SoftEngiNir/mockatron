from ddgen.models import DatabaseModel, TableModel
from ddgen.schema.database import Database
from ddgen.utilities.table_builder import TableBuilder


class DatabaseBuilder:
    def __init__(self, schema: str = 'public'):
        self.database = Database(schema=schema)
        self.table_nrows: dict = {}

    def add_table(self, table_model: TableModel):
        table_builder = TableBuilder(table_model, self.database)
        table = table_builder.build()
        self.database.add_table(table)

    def build(self, db_model: DatabaseModel) -> Database:
        for table_model in db_model.tables:
            table_builder = TableBuilder(table_model, self.database)
            table = table_builder.build()
            self.database.add_table(table)
            self.table_nrows[table] = table_model.nrows
        return self.database

    def get_table_nrows(self):
        return self.table_nrows
