import pytest
import os
import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_data import build_schema_from_csv, validate_data
from src.clean_data import extract_column_name

# Test setup

invalid_data_config1 = pd.DataFrame({
    'column':['diagnosis','mean_radius'],
    'type':['str','float'],
    'min':[None,4],
    'max':[None,30]
})
invalid_data_config2 = pd.DataFrame({
    'column':['diagnosis','mean_texture'],
    'type':['str','float'],
    'min':[None,4],
    'max':[None,30],
    'category':["Malignant,Benign",None]
})
valid_data_config = pd.DataFrame({
    'column':['diagnosis','mean_radius'],
    'type':['str','float'],
    'min':[None,6],
    'max':[None,40],
    'category':["Malignant,Benign",None]
})

valid_colnames = ['diagnosis','mean_radius']
invalid_data_type = [1, 2, 3, 4, 5]


# Tests

# Tests for build_schema_from_csv

# test build_schema_from_csv function throws an error
# if the data_config file does not exist
# if the data_config is not a dataframe
def test_build_schema_from_csv_error_on_wrong_data_config_type():
    with pytest.raises(TypeError, match="data_config must be a pandas dataframe."):
        build_schema_from_csv(data_config=invalid_data_type, expected_columns=valid_colnames)

# if pandas dataframe doesn't have following columns: column,type,max,min,category
def test_build_schema_from_csv_error_on_incorrect_columns():
    with pytest.raises(ValueError, match=f"The data_config must have following columns: 'column', 'type', 'min', 'max', 'category'."):
        build_schema_from_csv(data_config=invalid_data_config1, expected_columns=valid_colnames)

# if the values of 'column' match the column names extracted from name file
def test_build_schedma_from_csv_error_on_mismatch_column_names():
    with pytest.raises(ValueError, match="Column names in the config file do not match the expected columns."):
        build_schema_from_csv(data_config=invalid_data_config2, expected_columns=valid_colnames)


# Tests for validate_data function
data_config_df = pd.read_csv('tests/test_data_config.csv')
colnames = extract_column_name('tests/test_wdbc.names')[1:] #removing column name: 'id'

valid_schema = build_schema_from_csv(data_config=data_config_df,expected_columns=colnames)
invalid_schema = [1]

valid_data = pd.read_csv('tests/test_cleaned_data.csv').iloc[10:]
invalid_data = pd.read_csv('tests/test_cleaned_data.csv').iloc[:10]

def test_validate_data_error_on_invalid_schema_type():
    with pytest.raises(TypeError, match='schema must be a pandera dataframe schema.'):
        validate_data(schema=invalid_schema, dataframe=valid_data)

def test_validate_data_error_on_invalid_dataframe_type():
    with pytest.raises(TypeError, match='dataframe must be a pandas data frame.'):
        validate_data(schema=valid_schema, dataframe=invalid_data_type)

def test_validate_data_error_on_invalid_data_type():
    with pytest.raises(pa.errors.SchemaErrors):
        validate_data(schema=valid_schema,dataframe=invalid_data)
