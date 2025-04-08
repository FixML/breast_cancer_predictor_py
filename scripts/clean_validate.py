# clean_validate.py
# author: Weilin Han
# date: 2024-10-20

import click
import os
import sys
import pandas as pd
import pandera as pa
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean_data import extract_column_name, read_data, clean_data, write_data
from src.validate_data import build_schema_from_DataFrame, validate_data

@click.command()
@click.option('--raw-data-file', type=str, help="Path to raw data file")
@click.option('--name-file', type=str, help="Path to names file")
@click.option('--data-config-file', type=str, help="Path to data configuration file")
@click.option('--write-to', type=str, help="Path to directory where cleaned data will be written to")
@click.option('--file-name', type=str, help="The name of the file will be written")

def main(raw_data_file, name_file, data_config_file, write_to, written_file_name):
    """Clean raw data and validate it."""
    # Extract column names from .names file
    with open(name_file, 'r') as f:
        raw_lines = [line.strip() for line in f if not line.startswith('#') and line.strip()]

    colnames = extract_column_name(raw_lines)

    # Read raw data
    imported_data = read_data(raw_data_file, colnames)

    # Removing id column and relabel diagnosis column
    cleaned_data = clean_data(imported_data)

    
    # Create schema
    config_df = pd.read_csv(data_config_file)
    
    clean_colnames = colnames.remove("id")
    schema = build_schema_from_DataFrame(data_config=config_df, expected_columns=clean_colnames)
    # Validate cleaned data
    validate_data(schema=schema, dataframe=cleaned_data)

    # Write data to specified directory
    write_data(cleaned_data, write_to, written_file_name)

if __name__ == '__main__':
    main()