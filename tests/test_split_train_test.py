import pytest
import os
import pandas as pd
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import DatasetsSizeComparison, TrainTestSamplesMix, MultivariateDrift, LabelDrift, FeatureDrift
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.split_train_test import split_train_test_data, validate_split_data

# Test setup
invalid_data_type = [1,2,3]

valid_data = pd.read_csv('tests/test_cleaned_data.csv').iloc[10:]

data_train1 = valid_data.iloc[:100]
data_test1 = valid_data.iloc[100:102]
data_train1 = Dataset(data_train1,features=valid_data.columns[1:],label=valid_data.columns[0])
data_test1 = Dataset(data_test1,features=valid_data.columns[1:],label=valid_data.columns[0])

data_train2 = valid_data.iloc[0:200]
data_test2 = valid_data.iloc[150:200]
data_train2 = Dataset(data_train2,features=valid_data.columns[1:],label=valid_data.columns[0])
data_test2 = Dataset(data_test2,features=valid_data.columns[1:],label=valid_data.columns[0])

data_train3 = valid_data.iloc[:50]
data_test3 = valid_data.iloc[50:60]
data_train3 = Dataset(data_train3,features=valid_data.columns[1:],label=valid_data.columns[0])
data_test3 = Dataset(data_test3,features=valid_data.columns[1:],label=valid_data.columns[0])

data_train4 = valid_data.iloc[:50]
data_test4 = valid_data.iloc[60:70]
data_train4 = Dataset(data_train4,features=valid_data.columns[1:],label=valid_data.columns[0])
data_test4 = Dataset(data_test4,features=valid_data.columns[1:],label=valid_data.columns[0])

data_train5 = valid_data.iloc[:50]
data_test5 = valid_data.iloc[80:90]
data_train5 = Dataset(data_train5,features=valid_data.columns[1:],label=valid_data.columns[0])
data_test5 = Dataset(data_test5,features=valid_data.columns[1:],label=valid_data.columns[0])
# Tests

# test split_train_test function throws an error
# if the cleaned_data is not a dataframe
def test_split_train_test_data_error_on_wrong_data_type():
    with pytest.raises(TypeError, match="cleaned_data must be a pandas dataframe."):
        split_train_test_data(cleaned_data=invalid_data_type, train_data_size=0.3)

# test validate_split_data function throws an error
# if the Datasets Size Comparison Check failed
def test_validate_split_data_error_on_datsets_size():
    with pytest.raises(ValueError, match="The train test data size ratio should be greater than 0.2"):     
        validate_split_data(data_train=data_train1,data_test=data_test1)

# if the Train Test Samples Mix Check failed
def test_validate_split_data_error_on_sample_mix():
    with pytest.raises(ValueError, match="Data from Test dataset also present in Train dataset"):     
        validate_split_data(data_train=data_train2,data_test=data_test2)

# if Label Drift Check failed
def test_validate_split_data_error_on_label_drift():
    with pytest.raises(ValueError, match="Drift score above threshold: 0.4"):
        validate_split_data(data_train=data_train3,data_test=data_test3)

# if Feature Drift Check failed
def test_validate_split_data_error_on_feature_drift():
    with pytest.raises(ValueError, match="Drift score above threshold: 0.4"):
        validate_split_data(data_train=data_train4,data_test=data_test4)

# if Multivariate Drift Check failed
def test_validate_split_data_error_on_multivariate_drift():
    with pytest.raises(ValueError, match="Drift score above threshold: 0.4"):
        validate_split_data(data_train=data_train5,data_test=data_test5)