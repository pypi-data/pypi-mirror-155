"""
Utility functionality around supporting database interfaces and data ingestion
"""

from collections import defaultdict
import logging
from typing import Dict, Iterable, List
import click
from tqdm import tqdm
import pandas as pd
import sqlalchemy as sql

SCHEMA_EXCLUSION = {
    "postgresql": ["information_schema"],
    "mysql": ["mysql", "performance_schema", "sys", "information_schema"],
    "mssql": ["INFORMATION_SCHEMA", "guest", "sys"],
}


def get_engine(
    connection_string: str, test_connection: bool = True, verbose: bool = False
) -> sql.engine.Engine:
    """
    Get a sqlalchemy engine using a given connection string

    Args:
        connection_string: sqlalchemy connection string (https://docs.sqlalchemy.org/en/latest/core/engines.html)
        test_connection: attempt to pull from the database to test connection
        verbose: flag to enable status messages

    Returns:
        sqlalchemy database engine
    """
    logging.debug("Getting engine for database connection.")
    engine = sql.create_engine(connection_string)
    if test_connection:
        try:
            if verbose:
                click.secho("Testing database connection...", fg="white")
            engine.connect()
        except sql.exc.OperationalError as err:
            logging.exception(f"Could not connect to database! {err}")
            raise err
        if verbose:
            click.secho("Connection established!", fg="white")
    return engine


def get_database_type(
    engine: sql.engine.Engine,
    check_valid: bool = True,
    valid_database_types: Iterable = tuple(SCHEMA_EXCLUSION.keys()),
) -> str:
    """
    Get the name of the type of database given sqlalchemy engine
    Args:
        engine: The name of the type of database being connected to
        check_valid: Check to see if this database type is supported by fidescls
        valid_database_types: iterable

    Returns:
        name of the type of database the engine is pointing to
    """
    database_type = engine.dialect.name
    logging.debug(f"Database type: {database_type}")
    if check_valid:
        if database_type not in valid_database_types:
            raise ValueError(f"{database_type} is not currently supported!")
    return database_type


def include_schema(
    schema: str,
    database_type: str,
    exclusion_map: Dict[str, list[str]] = SCHEMA_EXCLUSION,
) -> bool:
    """
    Check to see if a schema should be included based on database type and schema name
    Args:
        schema: The name of the schema being checked
        database_type: the name of the database type
        exclusion_map: a dictionary mapping between database name and an exclusion list

    Returns:
        True if the schema should be included, False otherwise
    """
    if database_type == "mssql":
        return schema not in exclusion_map[database_type] and not schema.startswith(
            "db_"
        )
    return schema not in exclusion_map[database_type]


def get_table_key(schema: str, table: str, database_type: str) -> str:
    """
    Construct the table name key based on database type
    Args:
        schema: name of the schema
        table: name of the table
        database_type: name of the database type

    Returns:
        the appropriately formatted tabel name
    """
    return f"{schema}.{table}" if database_type == "postgresql" else table


def get_db_table_column_names(
    engine: sql.engine.Engine, hide_progress: bool = False
) -> Dict[str, Dict[str, List[str]]]:
    """
    Extract the table and column names from a database given a sqlalchemy engine
    Args:
        engine: sqlalchemy engine
        hide_progress: flag to disable progress bars and status messages

    Returns:
        Nested dictionary containing a database's tables and column names
    """
    logging.debug("Getting database name metadata...")
    inspector = sql.inspect(engine)
    database_type = get_database_type(engine)

    if not hide_progress:
        click.secho("Scanning database...", fg="white")

    db_tables: Dict[str, Dict[str, List]] = {}
    for schema in tqdm(
        inspector.get_schema_names(), disable=hide_progress, position=0, desc="Schema"
    ):
        if include_schema(schema, database_type):
            logging.debug(f"Extracting Schema: {schema}")
            db_tables[schema] = {}
            for table in tqdm(
                inspector.get_table_names(schema=schema),
                disable=hide_progress,
                position=1,
                desc="Tables",
                leave=False,
            ):
                # postgres table key name is handled differently for unknown reason at this time
                # table_key = f'{schema}.{table}' if database_type == 'postgresql' else table
                db_tables[schema][table] = [
                    column["name"]
                    for column in inspector.get_columns(table, schema=schema)
                ]
        else:
            logging.debug(f"Skipping schema: {schema}")
    return db_tables


def scan_database_metadata(
    connection_string: str, hide_progress: bool = False
) -> Dict[str, Dict[str, List[str]]]:
    """
    Scan a database for schema, table, and column names

    Args:
        connection_string: The sqlalchemy compatible connection string to the database
        hide_progress: flag to hide the progress bars

    Returns:
        The database's schema, tabel, and column names.
        Format: {schema_name: {table_name: [column names, ]}}
    """
    engine = get_engine(connection_string)
    metadata = get_db_table_column_names(engine, hide_progress=hide_progress)
    return metadata


def metadata_to_dataframe(
    database_metadata: Dict[str, Dict[str, List[str]]]
) -> pd.DataFrame:
    """
    Convert a metadata nested dictionary to a dense pandas dataframe to ease processing
    Args:
        database_metadata: nested dictionary containing database metadata (output of scan_database_metadata)

    Returns:
        dense dataframe containing a database's metadata
    """
    temp_list = []
    for schema, tables in database_metadata.items():
        for table, columns in tables.items():
            temp_list.append({"schema": schema, "table": table, "columns": columns})
    return pd.DataFrame.from_dict(temp_list)


def get_table_samples(
    engine: sql.engine.Engine, schema_name: str, table_name: str, num_samples: int = 10
) -> Dict[str, List[str]]:
    """
    Get a number of content samples from a table
    Args:
        engine: sqlalchemy engine with connection to the database
        schema_name: the name of the schema for the table
        table_name: the name of the table from which to query
        num_samples: the number of rows to pull from the table

    Returns:

    """
    with engine.begin() as connection:
        # TODO: figure out how to make this a random sample - abstracted for database type
        raw_query = sql.select("*", sql.table(table_name, schema=schema_name)).limit(  # type: ignore[arg-type, call-arg]
            num_samples
        )
        query_result = connection.execute(raw_query)
        query_columns = list(query_result.keys())
        query_samples = query_result.all()

    # reformat into an easier way to load into a pandas dataframe later
    # {column_name: [sample1, sample2, ..., sampleN]}
    table_samples: Dict[str, List[str]] = defaultdict(list)
    for i, column in enumerate(query_columns):
        for result in query_samples:
            table_samples[column].append(str(result[i]))
    return dict(table_samples)
