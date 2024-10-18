import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean_data import *

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

# Tests

# Tests for extract_column_name

# test extract_column_name function throws an error 
# if the raw name file does not exist
def test_extract_column_name_error_on_missing_file():
    with pytest.raises(FileNotFoundError, match='The raw name file does not exist.'):
        extract_column_name('tests/test_name_data.name')

# test extract_column_name function throws an error 
# if the raw name file is not a .names file
def test_extract_column_name_error_on_wrong_file_type():
    with pytest.raises(ValueError, match='The raw name file must be a .names file.'):
        extract_column_name('tests/empty.zip')

# Tests for read_raw_data

# test read_raw_data function throws an error 
# if the raw data file does not exist
def test_read_raw_data_error_on_missing_file():
    with pytest.raises(FileNotFoundError, match='The raw_data file does not exist.'):
        read_raw_data('tests/test_raw_data.data',col_name1)

# test read_raw_data function throws an error 
# if the raw data file is not a .data file
def test_read_raw_data_error_on_wrong_file_format():
    with pytest.raises(ValueError, match='The raw data file must be a .names file.'):
        read_raw_data('tests/empty.zip', col_name1)

# test read_raw_data function throws an error 
# if the col_name is not a list
def test_read_raw_data_error_on_non_list():
    with pytest.raises(ValueError, match="col_name must be a list."):
        read_raw_data('tests/test_wdbc.data',col_name2)

# test read_raw_data function throws an error 
# if the col_name does not have 32 values
def test_read_raw_data_error_on_insufficient_list_item():
    with pytest.raises(ValueError, match="col_name must contain exactly 32 items."):
        read_raw_data('tests/test_wdbc.data', col_name3)

# test read_raw_data function throws an error 
# if the col_name contains items other than string
def test_read_raw_data_error_on_wrong_item_type():
    with pytest.raises(ValueError, match="col_name must only contain strings."):
        read_raw_data('tests/test_wdbc.data', col_name4)

# Tests for clean_data

# test clean_data function throws an error
# if the imported_data is not a dataframe
def test_clean_data_error_on_wrong_imported_data_format():
    with pytest.raises(ValueError, match="imported_data must be a data frame."):
        clean_data(imported_data2, drop_columns1, relabel1)

# test clean_data function throws an error
# if the drop_columns is not a list
def test_clean_data_error_on_wrong_drop_columns_format():
    with pytest.raises(ValueError, match="drop_columns must be a list."):
        clean_data(imported_data1, drop_columns2, relabel1)


# test clean_data function throws an error
# if the relabel is not a dictionary
def test_clean_data_error_on_wrong_relabel_format():
    with pytest.raises(ValueError, match="relabel must be a dictionary"):
        clean_data(imported_data1, drop_columns1, relabel2)