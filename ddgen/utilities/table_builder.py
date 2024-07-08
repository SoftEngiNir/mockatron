from ddgen.models import TableModel
from ddgen.schema.database import Database
from ddgen.schema.table import Table
from ddgen.utilities.column_factory import ColumnFactory


class TableBuilder:
    def __init__(self, table_model: TableModel, database: Database):
        self.table_model = table_model
        self.database = database

    def build(self) -> Table:
        columns = []
        for col_model in self.table_model.columns:
            column = ColumnFactory.create_column(col_model, self.database)
            columns.append(column)
        return Table(self.table_model.name, columns)
