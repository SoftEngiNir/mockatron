from ddgen.dummy_generator.generator import DummyGenerator
from ddgen.utilities.connection import (ConnectionDetails,
                                        create_engine_postgres,
                                        session_context)
from ddgen.utilities.database_builder import DatabaseBuilder
from ddgen.utilities.readers import read_json_to_db_model
from ddgen.utilities.schema_utils import get_table_by_name
from ddgen.utilities.sql import execute_raw_sql, get_ddl
from ddgen.utilities.writers import write_to_csv, write_to_db

db_model = read_json_to_db_model(path='examples/example.json')
builder = DatabaseBuilder()
database = builder.build(db_model)


USERS = get_table_by_name(database, 'users')
PRODUCTS = get_table_by_name(database, 'products')
ORDERS = get_table_by_name(database, 'orders')


generator = DummyGenerator(database)

# Define the number of rows from each table
table_nrows = {
    USERS: 30,
    PRODUCTS: 20,
    ORDERS: 70,
}

# Provide a path to write the csv files to
path = ''
generator.generate(table_nrows)
write_to_csv('path', database)


# Provide connectin details of your db to write the data directly into you db
DB_CNXT = ConnectionDetails(
    username='',
    host='localhost',
    port=5432,
    dbname='postgres',
    password='',
)

TEST_ENGINE = create_engine_postgres(DB_CNXT)

# The session context creaetes the database schema
with session_context(engine=TEST_ENGINE) as session:
    ddl = get_ddl(database)
    # print(ddl)
    execute_raw_sql(session, ddl)

# Writes the fake data into your database
write_to_db(TEST_ENGINE, database)

# Will create a vizualiztion of the database tables and relationships (dependencies)
# from ddgen.utilities.graph import construct_graph, vizualize_graph
# graph = construct_graph(database.graph_dict)
# vizualize_graph(graph)
