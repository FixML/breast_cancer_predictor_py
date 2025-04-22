import pytest
import os
import pandas as pd
import pandera as pa
import numpy as np
from pandera import Column, DataFrameSchema
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_data import build_schema_from_DataFrame, validate_data
from src.clean_data import extract_column_name

# Test setup for build_schema_from_DataFrame

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
    'category':["Malignant,Benign",None],
    'max_nullable':[0,0.1]
})
valid_data_config = pd.DataFrame({
    'column':['diagnosis','mean_radius'],
    'type':['str','float'],
    'min':[None,6],
    'max':[None,40],
    'category':["Malignant,Benign",None],
    'max_nullable':[0,0.1]
})

valid_colnames = ['diagnosis','mean_radius']
invalid_data_type = [1, 2, 3, 4, 5]

# Tests for build_schema_from_DataFrame

# test build_schema_from_DataFrame function throws an error
# if the data_config is not a dataframe
def test_build_schema_from_DataFrame_error_on_wrong_data_config_type():
    with pytest.raises(TypeError, match="data_config must be a pandas dataframe."):
        build_schema_from_DataFrame(data_config=invalid_data_type, expected_columns=valid_colnames)

# if pandas dataframe doesn't have following columns: column,type,max,min,category,max_nullable
def test_build_schema_from_DataFrame_error_on_empty_df():
    empty_df = pd.DataFrame(columns=valid_colnames)

    with pytest.raises(ValueError, match="must contain at least one row"):
        build_schema_from_DataFrame(data_config=empty_df, expected_columns=valid_colnames)

def test_build_schema_from_DataFrame_error_on_incorrect_columns():
    with pytest.raises(ValueError, match=f"The data_config must have following columns: 'column', 'type', 'min', 'max', 'category', 'max_nullable'."):
        build_schema_from_DataFrame(data_config=invalid_data_config1, expected_columns=valid_colnames)

# if the values of 'column' match the column names extracted from name file
def test_build_schedma_from_DataFrame_error_on_mismatch_column_names():
    with pytest.raises(ValueError, match=f"Column names in the config file do not match the expected columns."):
        build_schema_from_DataFrame(data_config=invalid_data_config2, expected_columns=valid_colnames)

# Tests setup for validate_data function

data_config_df = pd.read_csv('tests/test_data_config.csv')
with open('tests/test_wdbc.names', 'r') as f:
        raw_lines = [line.strip() for line in f if not line.startswith('#') and line.strip()]
colnames = extract_column_name(raw_lines)[1:] #removing column name: 'id'

valid_schema = build_schema_from_DataFrame(data_config=data_config_df,expected_columns=colnames)
invalid_schema = [1]

valid_data = pd.read_csv('tests/test_cleaned_data.csv', nrows=3)
empty_data_frame = valid_data.copy().iloc[0:0]

# Setup list of invalid data cases 
invalid_data_cases = []

# Case: missing "diagnosis" column
case_missing_class_col = valid_data.copy()
case_missing_class_col = case_missing_class_col.drop("diagnosis", axis=1)  # drop class column
invalid_data_cases.append((case_missing_class_col, "`diagnosis` from DataFrameSchema"))

# Case: label in "diagnosis" column encoded as 0 and 1, instead of Benign and Malignant
case_wrong_label_type = valid_data.copy()
case_wrong_label_type["diagnosis"] = case_wrong_label_type["diagnosis"].map({'Benign': 0, 'Malignant': 1})
invalid_data_cases.append((case_wrong_label_type, "Check incorrect type for'diagnosis' values is missing or incorrect"))

# Case: wrong string value/category in "diagnosis" column
case_wrong_category_label = valid_data.copy()
case_wrong_category_label.loc[0, "diagnosis"] = "benign"
invalid_data_cases.append((case_wrong_category_label, "Check absent or incorrect for wrong string value/category in 'diagnosis' column"))

# Case: missing value in "diagnosis" column
case_missing_class = valid_data.copy()
case_missing_class.loc[0, "diagnosis"] = None
invalid_data_cases.append((case_missing_class, "Check absent or incorrect for missing/null 'diagnosis' value"))

# Case: missing numeric columns (one for each numeric column) where column is missing
numeric_columns = valid_data.select_dtypes(include=np.number).columns
for col in numeric_columns:
    case_missing_col = valid_data.copy()
    case_missing_col = case_missing_col.drop(col, axis=1)  # drop column
    invalid_data_cases.append((case_missing_col, f"'{col}' is missing from DataFrameSchema"))
    
# Generate 30 cases (one for each numeric column) where data is out of range (too large)
numeric_columns = valid_data.select_dtypes(include=np.number).columns
for col in numeric_columns:
    case_too_big = valid_data.copy()
    case_too_big[col] = case_too_big[col] + 5000  # Adding an arbitrary value to make it out of range
    invalid_data_cases.append((case_too_big, f"Check absent or incorrect for numeric values in '{col}' being too large"))

# Generate 30 cases (one for each numeric column) where data is out of range (too small)
numeric_columns = valid_data.select_dtypes(include=np.number).columns
for col in numeric_columns:
    case_too_small = valid_data.copy()
    case_too_small[col] = case_too_small[col] - 1000  # Adding an arbitrary value to make it out of range
    invalid_data_cases.append((case_too_small, f"Check absent or incorrect for numeric values in '{col}' being too small"))

# Generate 30 cases (one for each numeric column) where data is the wrong type
numeric_columns = valid_data.select_dtypes(include=np.number).columns
for col in numeric_columns:
    case_wrong_type = valid_data.copy()
    case_wrong_type[col] = case_wrong_type[col].fillna(0.0).astype(int) # convert from float to int
    invalid_data_cases.append((case_wrong_type, f"Check incorrect type for float values in '{col}' is missing or incorrect"))

# Case: duplicate observations
case_duplicate = valid_data.copy()
case_duplicate = pd.concat([case_duplicate, case_duplicate.iloc[[0], :]], ignore_index=True)
invalid_data_cases.append((case_duplicate, f"Check absent or incorrect for duplicate rows"))

# Case: entire missing observation
case_missing_obs = valid_data.copy()
nan_row = pd.DataFrame([[np.nan] * (case_missing_obs.shape[1] - 1) + [np.nan]], columns=case_missing_obs.columns)
case_missing_obs = pd.concat([case_missing_obs, nan_row], ignore_index=True)
invalid_data_cases.append((case_missing_obs, f"Check absent or incorrect for missing observations (e.g., a row of all missing values)"))


# Tests for validate_data function

# test build_schema_from_DataFrame function throws an error
# if the schema is invalid pandera dataframe schema
def test_validate_data_error_on_invalid_schema_type():
    with pytest.raises(TypeError, match='schema must be a pandera dataframe schema.'):
        validate_data(schema=invalid_schema, dataframe=valid_data)

# if the dataframe is not a pandas data frame
def test_validate_data_error_on_invalid_dataframe_type():
    with pytest.raises(TypeError, match='dataframe must be a pandas data frame.'):
        validate_data(schema=valid_schema, dataframe=invalid_data_type)


# if the dataframe has invalid data
@pytest.mark.parametrize("invalid_data, description", invalid_data_cases)
def test_valid_w_invalid_data(invalid_data, description):
    with pytest.raises(pa.errors.SchemaErrors):
        validate_data(schema=valid_schema, dataframe=invalid_data)
