import pytest
import numpy as np
import pandas as pd
from click.testing import CliRunner
from click import BadParameter
import os
import great_expectations as gx
from unittest.mock import Mock
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_data import *

# Tests file set up
cleaned_data1 = pd.DataFrame({
        'id': [1, 2, 3],
        'class': ['M', 'B', 'M']
    })
cleaned_data2 = [1, 2, 3, 4, 5]

invalid_batch = "This is not a batch"
valid_batch = create_data_batch(cleaned_data1)
test_columns_list1 = ['diagnosis', 'mean_radius']
test_columns_list2 = {1:'diagnosis', 2:'mean_radius'}
test_columns_list3 = ['diagnosis', 'mean_radius',2]

col_set1 = {'class': ['Malignant', 'Benign']}
col_set2 = ['class']
col_set3 = {123: ['Malignant', 'Benign']}

col_type1 = {'diagnosis': 'string'}
col_type2 = ['diagnosis']
col_type3 = {1: 'string'}
col_type4 = {'diagnosis': 1}

col_percent1 = {'mean_radium': 0.3}
col_percent2 = ['mean_radium']
col_percent3 = {1: 0.3}
col_percent4 = {'mean_radium': '0.3'}
col_percent5 = {'mean_radium': -0.3}
col_percent6 = {'mean_radium': 1.3}

col_range1 = {'mean_radium': [5, 25, False, False]}
col_range2 = ['mean_radium']
col_range3 = {1: [5, 25, False, False]}
col_range4 = {'mean_radium': '0.3'}
col_range5 = {'mean_radius': [5, 25, False]}
col_range6 = {'mean_radius': ['invalid_min', 25, False, False]}
col_range7 = {'mean_radius': [5, 'invalid_max', False, False]}
col_range8 = {'mean_radius': [5, 25, 'invalid_boolean', False]}
col_range9 = {'mean_radius': [5, 25, False, 'invalid_boolean']}
# Tests

# Tests for create_data_batch

# test create_data_batch function throws an error
# if the imported_data is not a dataframe
def test_create_data_batch_error_on_wrong_cleaned_data_format():
    with pytest.raises(TypeError, match="cleaned_data must be a dataframe."):
        create_data_batch(cleaned_data2)

#Tests for check_validation_result

# test check_validation_result function throws an error
# if the validation result success is false
def test_check_validation_result_failure():
    # Create a mock validation result with success = False
    validation_results = Mock()
    validation_results.success = False
    validation_results.expectation_config.type = "expect_column_to_exist"
    validation_results.expectation_config.kwargs = {"column": "class"}
    
    # Test that ValidationError is raised and the error message is correct
    with pytest.raises(ValidationError, match="Validation for column 'class' failed. The data did not meet the expectations: expect_column_to_exist."):
        check_validation_result(validation_results)

# Tests for exp_column_exsist

# test exp_column_exsist function throws an error
# if the batch is not a gx batch object
def test_exp_column_exsist_with_invalid_batch():
    
    with pytest.raises(TypeError, match="batch must be a great expectation batch object."):
        exp_column_exsist(invalid_batch, test_columns_list1)

# if the columns is not a list
def test_exp_column_exsist_error_on_non_list():
    with pytest.raises(TypeError, match="columns must be a list."):
        exp_column_exsist(valid_batch, test_columns_list2)

# if the columns contains items other than string
def test_exp_column_exsist_error_on_wrong_item_type():
    with pytest.raises(ValueError, match="columns must only contain strings."):
        exp_column_exsist(valid_batch, test_columns_list3)

# Tests for exp_value_set_in_col

# test exp_value_set_in_col function throws an error
# if the batch is not a gx batch object
def test_exp_value_set_in_col_with_invalid_batch():
    
    with pytest.raises(TypeError, match="batch must be a great expectation batch object."):
        exp_value_set_in_col(invalid_batch, col_set1)

# if the columns is not a list
def test_exp_value_set_in_col_error_on_non_list():
    with pytest.raises(TypeError, match="col_set must be a dict."):
        exp_value_set_in_col(valid_batch, col_set2)

# if col_set keys are not strings
def test_exp_value_set_in_col_invalid_col_set_keys():
    with pytest.raises(TypeError, match="col_set keys must be strings."):
        exp_value_set_in_col(valid_batch, col_set3)


# Tests for exp_type_of_col_values

# test exp_type_of_col_values function throws an error
# if the batch is not a gx batch object
def test_exp_type_of_col_values_with_invalid_batch():
    with pytest.raises(TypeError, match="batch must be a great expectation batch object."):
        exp_type_of_col_values(invalid_batch, col_type1)

# if the columns is not a list
def test_exp_type_of_col_values_error_on_non_list():
    with pytest.raises(TypeError, match="col_type must be a dict."):
        exp_type_of_col_values(valid_batch, col_type2)

# if the type of col_type's key is not string
def test_exp_type_of_col_values_invalid_keys():
    with pytest.raises(TypeError, match="col_type keys must be strings."):
        exp_type_of_col_values(valid_batch, col_type3)

# if the type of col_type's value is not string
def test_exp_type_of_col_values_invalid_values():
    with pytest.raises(TypeError, match="col_type values must be strings."):
        exp_type_of_col_values(valid_batch, col_type4)

# Tests for exp_col_not_null

# test exp_col_not_null function throws an error
# if the batch is not a gx batch object
def test_exp_col_not_null_with_invalid_batch():
    with pytest.raises(TypeError, match="batch must be a great expectation batch object."):
        exp_col_not_null(invalid_batch, col_percent1)

# if the columns is not a list
def test_exp_col_not_null_error_on_non_list():
    with pytest.raises(TypeError, match="col_percent must be a dict."):
        exp_col_not_null(valid_batch, col_percent2)

# if the type of col_type's key is not string
def test_exp_col_not_null_invalid_keys():
    with pytest.raises(TypeError, match="col_percent keys must be strings."):
        exp_col_not_null(valid_batch, col_percent3)

# if the type of col_percent's value is not numeric
def test_exp_col_not_null_invalid_values():
    with pytest.raises(TypeError, match="col_percent values must be numeric value."):
        exp_col_not_null(valid_batch, col_percent4)

# if the col_percent values are negative
def test_exp_col_not_null_negative_values():
    with pytest.raises(ValueError, match="col_percent values must be positive."):
        exp_col_not_null(valid_batch, col_percent5)

# if the col_percent values are greater than 1
def test_exp_col_not_null_values_greater_than_one():
    with pytest.raises(ValueError, match="col_percent values must not be greater than 1."):
        exp_col_not_null(valid_batch, col_percent6)


# Tests for exp_value_range

# test exp_value_range function throws an error
# if the batch is not a gx batch object
def test_exp_value_range_with_invalid_batch():
    with pytest.raises(TypeError, match="batch must be a great expectation batch object."):
        exp_value_range(invalid_batch, col_range1)

# if the columns is not a list
def test_exp_value_range_error_on_non_list():
    with pytest.raises(TypeError, match="col_range must be a dict."):
        exp_value_range(valid_batch, col_range2)

# if the type of col_type's key is not string
def test_exp_value_range_invalid_keys():
    with pytest.raises(TypeError, match="col_range keys must be strings."):
        exp_value_range(valid_batch, col_range3)

# if the type of col_range's value is not list
def test_exp_value_range_invalid_values():
    with pytest.raises(TypeError, match="col_range must be a list."):
        exp_value_range(valid_batch, col_range4)

# if col_range's values do not have four items
def test_exp_value_range_list_length():
    with pytest.raises(ValueError, match="Each col_range value list must contain exactly four items."):
        exp_value_range(valid_batch, col_range5)

# if the first item (min_value) is not numeric or None
def test_exp_value_range_invalid_min_value():
    with pytest.raises(TypeError, match="The first item in col_range value must be a numeric value or None"):
        exp_value_range(valid_batch, col_range6)

# if the second item (min_value) is not numeric or None
def test_exp_value_range_invalid_max_value():
    with pytest.raises(TypeError, match="The second item in col_range value must be a numeric value or None"):
        exp_value_range(valid_batch, col_range7)

# if third item (strict_min) is not a boolean
def test_exp_value_range_invalid_strict_min():
    with pytest.raises(TypeError, match="The third item in col_range value must be a boolean value"):
        exp_value_range(valid_batch, col_range8)

# if the fourth item (strict_max) is not a boolean
def test_exp_value_range_invalid_strict_max():
    with pytest.raises(TypeError, match="The fourth item in col_range value must be a boolean value"):
        exp_value_range(valid_batch, col_range9)