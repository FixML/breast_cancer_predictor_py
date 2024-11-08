# clean_validate.py
# author: Weilin Han
# date: 2024-10-20

import click
import os
import sys
import pandas as pd
import pandera as pa
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean_data import extract_column_name, read_raw_data, clean_data, write_data
from src.validate_data import build_schema_from_csv

@click.command()
@click.option('--raw-data-file', type=str, help="Path to raw data file")
@click.option('--name-file', type=str, help="Path to names file")
@click.option('--data-config-file', type=str, help="Path to data configuration file")
@click.option('--write-to', type=str, help="Path to directory where cleaned data will be written to")

def main(raw_data_file, name_file, data_config_file, write_to):
    """Clean raw data and validate it."""
    # Extract column names from .names file
    colnames = extract_column_name(name_file)

    # Read raw data
    imported_data = read_raw_data(raw_data_file, colnames)

    # Removing id column and relabel diagnosis column
    cleaned_data = clean_data(imported_data)

    # Validate cleaned data
    # define schema
    schema = build_schema_from_csv(data_config=data_config_file, expected_columns=colnames)
    schema.validate(cleaned_data)

    # Write data to specified directory
    write_data(cleaned_data, write_to)

if __name__ == '__main__':
    main()