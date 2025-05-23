import pytest
import warnings
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean_data import extract_column_name,read_data,clean_data,write_data

# Test files setup
col_name1 = ["col" + str(i) for i in range(32)] # 32 strings
col_name2 = {"1":"apple"}
col_name3 = ['1','2','3']
col_name4 = ["col" + str(i) for i in range(31)] + [123]  # 31 strings + 1 integer

imported_data1 = pd.DataFrame({
        'id': [1, 2, 3],
        'class': ['M', 'B', 'M']
    })
imported_data2 = [1, 2, 3, 4, 5]
drop_columns1=['id']
drop_columns2={'1':'id'}
relabel1={'M' : 'Malignant','B' : 'Benign'}
relabel2=['M','B']

cleaned_data1 = pd.DataFrame({
        'diagnosis': ['Malignant','Benign','Malignant'],
        'mean_raius': [1, 2, 3]
    })
cleaned_data2 = [1, 2, 3, 4, 5]
# setup empty directory for data files to be downloaded to
if not os.path.exists('tests/test_write_data1'):
    os.makedirs('tests/test_write_data1')

# Tests

# Tests for read_data

# test read_data function throws an error 
# if the raw data file does not exist
def test_read_data_error_on_missing_file():
    with pytest.raises(FileNotFoundError, match='The raw_data file does not exist.'):
        read_data('tests/test_data.data',col_name1)

# test read_data function throws an error 
# if the col_name is not a list
def test_read_data_error_on_non_list():
    with pytest.raises(TypeError, match="col_name must be a list."):
        read_data('tests/test_wdbc.data',col_name2)

# test read_data function throws an error 
# if the col_name contains items other than string
def test_read_data_warns_on_wrong_item_type():
    with pytest.warns(UserWarning, match="col_name contains non-string values"):
        read_data('tests/test_wdbc.data', col_name4)
        
# test read_data function throws an error 
# if the items in col_name list does not match the number of columns of raw_data
def test_read_data_error_on_insufficient_list_item():
    with pytest.raises(ValueError, match="The number of items in col_name must match the number of columns in raw_data."):
        read_data('tests/test_wdbc.data', col_name3)


# Tests for clean_data

# test clean_data function throws an error
# if the imported_data is not a dataframe
def test_clean_data_error_on_wrong_imported_data_format():
    with pytest.raises(TypeError, match="imported_data must be a data frame."):
        clean_data(imported_data2, drop_columns1, relabel1)

# test clean_data function throws an error
# if the drop_columns is not a list
def test_clean_data_error_on_wrong_drop_columns_format():
    with pytest.raises(TypeError, match="drop_columns must be a list."):
        clean_data(imported_data1, drop_columns2, relabel1)


# test clean_data function throws an error
# if the relabel is not a dictionary
def test_clean_data_error_on_wrong_relabel_format():
    with pytest.raises(TypeError, match="relabel must be a dictionary"):
        clean_data(imported_data1, drop_columns1, relabel2)

# Tests for write_data

# test write_data function throws an error
# if the dataframe is not a dataframe
def test_write_data_error_on_wrong_cleaned_data_format():
    with pytest.raises(TypeError, match="dataframe must be a pandas data frame."):
        write_data(cleaned_data2, 'tests/', 'test_write_data1')

# test write_data function throws an error 
# if the write_to path provided does not exist
def test_write_data_error_on_nonexistent_dir():
    with pytest.raises(FileNotFoundError, match='The directory provided does not exist.'):
        write_data(cleaned_data1, 'test/', 'test_write_data2')

# if the directory path provided is not directory
def test_write_data_error_on_missing_dir():
    with pytest.raises(NotADirectoryError, match='The directory path provided is not a directory, it is an existing file path. Please provide a path to a new, or existing directory.'):
        write_data(cleaned_data1, 'tests/conftest.py','test_write_data3')     
