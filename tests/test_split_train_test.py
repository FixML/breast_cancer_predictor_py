import pytest
import os
import pandas as pd
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import DatasetsSizeComparison, TrainTestSamplesMix, MultivariateDrift, LabelDrift, FeatureDrift
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.split_train_test import split_train_test_data

# Test setup
invalid_data_type = [1,2,3]

cleaned_data1 = pd.read_csv('tests/test_cleaned_data.csv').iloc[10:]

sample_data = cleaned_data1.iloc[:10]
cleaned_data2 = sample_data.loc[sample_data.index.repeat(20)].reset_index(drop=True)
 

# Tests

# test split_train_test function throws an error
# if the cleaned_data is not a dataframe
def test_split_train_test_data_error_on_wrong_data_type():
    with pytest.raises(TypeError, match="cleaned_data must be a pandas dataframe."):
        split_train_test_data(cleaned_data=invalid_data_type, train_data_size=0.3)

# if the Datasets Size Comparison Check failed
def test_split_train_test_data_error_on_datsets_size():
    with pytest.raises(ValueError, match="The train test data size ratio should be greater than 0.2"):     
        split_train_test_data(cleaned_data1, train_data_size=0.01, stratify_by=cleaned_data1["diagnosis"])


# if the Train Test Samples Mix Check failed
def test_split_train_test_data_error_on_sample_mix():
    with pytest.raises(ValueError, match="Data from Test dataset also present in Train dataset"):     
        split_train_test_data(cleaned_data2, train_data_size=0.01, stratify_by=cleaned_data2["diagnosis"])
