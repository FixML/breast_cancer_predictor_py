import pytest
import os
import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_data import validate_data

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

valid_data = pd.DataFrame({
        'id': [1, 2, 3],
        'class': ['M', 'B', 'M']
    })
invalid_data = [1, 2, 3, 4, 5]

# Tests

# Tests for extract_column_name

# test extract_column_name function throws an error
# if the data_config file does not exist
def test_validate_data_error_on_missing_file():
    with pytest.raises(FileNotFoundError, match='The data_config file does not exist.'):
        validate_data('tests/test_missing_file.csv',valid_colnames,valid_data)

# if pandas dataframe doesn't have exactly four columns: column,type,max,min
def test_validate_data_error_on_incorrect_columns(tmp_path):
    with pytest.raises(ValueError, match=f"The configuration file must have following columns: 'column', 'type', 'min', 'max', 'category'."):
        invalid_csv_file = write_temp_csv(invalid_csv_content, tmp_path)
        validate_data(invalid_csv_file,valid_colnames,valid_data)

# if the values of 'column' match the column names extracted from name file
def test_build_schedma_from_csv_error_on_mismatch_column_names(tmp_path):
    with pytest.raises(ValueError, match="Column names in the config file do not match the expected columns."):
        valid_csv_file = write_temp_csv(valid_csv_content, tmp_path)
        validate_data(valid_csv_file,invalid_colnames,valid_data)

# if the dataframe is not a dataframe
def test_validate_data_error_on_wrong_cleaned_data_format(tmp_path):
    with pytest.raises(TypeError, match="cleaned_data must be a data frame."):
        valid_csv_file = write_temp_csv(valid_csv_content, tmp_path)
        validate_data(valid_csv_file,invalid_colnames,invalid_data)

# Tests for Pandera validation function
