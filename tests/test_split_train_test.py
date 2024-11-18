import pytest
import os
import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.split_train_test import split_train_test_data

# Test setup
invalid_data_type = [1,2,3]
# Tests

# test split_train_test function throws an error
# if the cleaned_data is not a dataframe
def test_split_train_test_data_error_on_wrong_data_type():
    with pytest.raises(TypeError, match="data_config must be a pandas dataframe."):
        split_train_test_data(cleaned_data=invalid_data_type, train_data_size=0.3)

# if the Datasets Size Comparison Check failed

# if the Train Test Samples Mix Check failed

# if Label Drift Check failed

# if Feature Drift Check failed

# if Multivariate Drift Check failed