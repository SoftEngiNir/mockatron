import json

from ddgen.dummy_generator.generator import DummyGenerator
from ddgen.models import DatabaseModel
from ddgen.utilities.connection import (ConnectionDetails,
                                        create_engine_postgres,
                                        session_context)
from ddgen.utilities.database_builder import DatabaseBuilder
from ddgen.utilities.graph import construct_graph, vizualize_graph
from ddgen.utilities.schema_utils import get_table_by_name
from ddgen.utilities.sql import execute_raw_sql, get_ddl
from ddgen.utilities.writers import csv_dump, db_dump


def read_json_to_db_model(path: str) -> DatabaseModel:
    with open(path) as f:
        return DatabaseModel.model_validate(json.load(f))


db_model = read_json_to_db_model(path='examples/example.json')
builder = DatabaseBuilder()
database = builder.build(db_model)


USERS = get_table_by_name(database, 'users')
PRODUCTS = get_table_by_name(database, 'products')
ORDERS = get_table_by_name(database, 'orders')


generator = DummyGenerator(database)
table_nrows = {
    USERS: 30,
    PRODUCTS: 20,
    ORDERS: 70,
}

generator.generate(table_nrows)
csv_dump('dummy_data', database)


TEST_DB_CNXT = ConnectionDetails(
    username='',
    host='localhost',
    port=5432,
    dbname='postgres',
    password='',
)

TEST_ENGINE = create_engine_postgres(TEST_DB_CNXT)

with session_context(engine=TEST_ENGINE) as session:
    ddl = get_ddl(database)
    # print(ddl)
    execute_raw_sql(session, ddl)

db_dump(TEST_ENGINE, database)


graph = construct_graph(database.graph_dict)
vizualize_graph(graph)
