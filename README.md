# Mockatron

## Overview

Mockatron is a Python-based tool designed to create realistic and customizable mock databases for testing and development purposes. This tool can currently generate data for SQL databases only (NoSQL will be supported in the future).

## Features

- **Customizable Data Generation**: Create realistic mock data for different database schemas.
- **Relational data**: Create different types of relationships, for example - user.creation_date comes before order.purchase_date
- **DDL**: Autogenerates the ddl to create the database tables and relationships.
- **Writers**: Write to csv or directly into your databse.
- **Flexible Configuration**: Easily configure the data generation process using a JSON file.
- **Extensible**: Add custom data generation functions.

## The Database object

This object is responsible for managing the database tables and the relationships between them. As data in different columns is dependent on data from other columns through relationships of different kinds, the order of data generation becomes important.

Each database table is reponsible for grouping it's columns into a single place, and storing information regarding that table (schema, primary key column)

Each column object takes a bunch of attributes the defines it's properties (nullability, is_fk, dtype, etc.)
Currently there are 3 types of columns that each generates data in a different way:

1. Column - An independent column, data will be generated using an engine.

2. ForeignKey - Can be either one_to_one or one_to_many (default).

3. RelatedColumn - custom type of relationship (see `ddgen/enums.py` for the different `RelationshipType`), for example can be used to define a chronological order between dates.

## Engines

The engines here are the basic data generators for the Column types. Here I leverage 3 libraries to use as a base engine for all engines - random, faker and numpy. The premise of the engines is that they implement the `sample` method that returns a single value of a certain type. They are meant to be small, light so that it's easy to create your own engines and use them. (See `ddgen/engines`)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/SoftEngiNir/mockatron.git
    cd mockatron
    ```
2. Create a virtual environment
    ```bash
    python3 -m venv venv
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Basic Usage

1. Define your database is a `config.json` file according to the model rules defined in `ddgen/models.py`

2. Adjust the main file to include your the path to your json file.

3. Adjust the csv_output_path and/or db_connection_details to write to csv or your running db.

4. Run main script:
    ```bash
    python ddgen.main.py
    ```

### Configuration File Example (config.json)


```json
{
  "tables": [
    {
      "name": "users",
      "nrows": 30,
      "columns": [
        {
          "name": "id",
          "dtype": "integer",
          "is_primary": true,
          "engine": {
            "name": "IntPrimaryKeyEngine"
          }
        },
        {
          "name": "name",
          "dtype": "string",
          "engine": {
            "name": "StrNameEngine"
          }
        },
        {
          "name": "email",
          "dtype": "string",
          "engine": {
            "name": "StrEmailEngine"
          }
        },
        {
          "name": "created_at",
          "dtype": "timestamp",
          "engine": {
            "name": "DateTimeRandEngine",
            "config": {
              "start_datetime": "2000-01-01T01:00:00+0000",
              "end_datetime": "2024-07-07T18:22:39+0000"
            }
          }
        }
      ]
    }
  ]
}
```
