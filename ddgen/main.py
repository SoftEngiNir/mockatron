from ddgen.dummy_generator.generator import DummyGenerator
from ddgen.models import DatabaseModel
from ddgen.schema.database import Database
from ddgen.utilities.connection import (ConnectionDetails,
                                        create_engine_postgres,
                                        session_context)
from ddgen.utilities.model_mappers import database_from_model
from ddgen.utilities.readers import model_from_json
from ddgen.utilities.sql import execute_raw_sql
from ddgen.utilities.writers import write_to_csv, write_to_db


def main():
    # File paths
    db_model_path = 'examples/example.json'
    connection_details_path = 'connection.json'
    csv_output_path = 'dummy_data'

    # Read database model from JSON file and create the database object
    db_model = model_from_json(path=db_model_path, model=DatabaseModel)
    database = database_from_model(db_model)

    # Initialize DummyGenerator with the database
    generator = DummyGenerator(database)

    # Generate the dummy data
    generator.generate()

    # Write generated data to CSV files
    write_to_csv(csv_output_path, database)

    # Read database connection details from JSON file
    db_connection_details = model_from_json(path=connection_details_path, model=ConnectionDetails)

    # Create a PostgreSQL engine
    db_engine = create_engine_postgres(db_connection_details)

    # Create the database schema
    with session_context(engine=db_engine) as session:
        execute_raw_sql(session, database.get_ddl())

    # Write the fake data into the database
    write_to_db(db_engine, database)

    # Optional: Visualize the database tables and relationships (dependencies)
    # visualize_database_schema(database)


def visualize_database_schema(database: Database):
    from ddgen.utilities.graph import construct_graph, visualize_graph
    graph = construct_graph(database.graph_dict)
    visualize_graph(graph)


if __name__ == '__main__':
    main()
