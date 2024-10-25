import pytest
import pandas as pd
import os
from io import StringIO
import pandera as pa
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_data import build_schema_from_csv

# Test setup
# Helper function to write CSV content to a temporary file
def write_temp_csv(content, tmp_path, filename="data_config.csv"):
    temp_file = tmp_path / filename
    temp_file.write_text(content)
    return temp_file

invalid_csv_content = """
column,type,min
'mean_radius',int,6
"""
valid_csv_content = """
column,type,min,max
'diagnosis',str,,
'mean_radius',float,6,12
"""

invalid_colnames = ['diagnosis','mean_texture']
valid_colnames = ['diagnosis','mean_radius']

# Tests

# Tests for extract_column_name

# test extract_column_name function throws an error 
# if the data_config file does not exist
def test_build_schema_from_csv_error_on_missing_file():
    with pytest.raises(FileNotFoundError, match='The data_config file does not exist.'):
        build_schema_from_csv('tests/test_missing_file.csv',valid_colnames)

# if pandas dataframe doesn't have exactly four columns: column,type,max,min
def test_build_schema_from_csv_error_on_incorrect_columns(tmp_path):
    with pytest.raises(ValueError, match=f"The configuration file must have exactly four columns: 'column', 'type', 'min', 'max'."):
        invalid_csv_file = write_temp_csv(invalid_csv_content, tmp_path)
        build_schema_from_csv(invalid_csv_file,valid_colnames)

# if the values of 'column' match the column names extracted from name file
def test_build_schedma_from_csv_error_on_mismatch_column_names(tmp_path):
    with pytest.raises(ValueError, match="Column names in the config file do not match the expected columns."):
        valid_csv_file = write_temp_csv(valid_csv_content, tmp_path)
        build_schema_from_csv(valid_csv_file,invalid_colnames)