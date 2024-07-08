class TableNotFoundError(Exception):
    def __init__(self, table_name):
        super().__init__(f"Table '{table_name}' not found.")


class ColumnNotFoundError(Exception):
    def __init__(self, table_name, col_name):
        super().__init__(f"Column '{col_name}' not found in table '{table_name}'.")
