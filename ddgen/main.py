from ddgen.dummy_generator.generator import DummyGenerator
from ddgen.utilities.connection import (ConnectionDetails,
                                        create_engine_postgres,
                                        session_context)
from ddgen.utilities.database_builder import DatabaseBuilder
from ddgen.utilities.readers import read_json_to_db_model
from ddgen.utilities.sql import execute_raw_sql
from ddgen.utilities.writers import write_to_csv, write_to_db

# Read database model from JSON file
db_model = read_json_to_db_model(path='examples/example.json')

# Initialize DatabaseBuilder and build the database
builder = DatabaseBuilder()
database = builder.build(db_model)

# Get the number of rows for each table
table_nrows = builder.get_table_nrows()

# Initialize DummyGenerator with the database
generator = DummyGenerator(database)

# Generate the dummy data and write it to CSV files
csv_output_path = ''  # Provide the path to write the CSV files to
generator.generate(table_nrows)
write_to_csv(csv_output_path, database)

# Define connection details for the database
db_connection_details = ConnectionDetails(
    username='',
    host='localhost',
    port=5432,
    dbname='postgres',
    password='',
)

# Create a PostgreSQL engine
db_engine = create_engine_postgres(db_connection_details)

# Create the database schema and write the fake data to the database
with session_context(engine=db_engine) as session:

    execute_raw_sql(session, database.get_ddl())

# Write the fake data into the database
write_to_db(db_engine, database)

# Optional: Visualize the database tables and relationships (dependencies)
# from ddgen.utilities.graph import construct_graph, visualize_graph
# graph = construct_graph(database.graph_dict)
# visualize_graph(graph)
