import pytest
import os
import pandas as pd
import numpy as np
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import DatasetsSizeComparison, TrainTestSamplesMix, MultivariateDrift, LabelDrift, FeatureDrift
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.split_train_test import split_train_test_data, validate_split_data

# Test setup
invalid_data_type = [1,2,3]

valid_data = pd.read_csv('tests/test_cleaned_data.csv')

# sample datasets for Datasets Size Comparison Check
data_train1 = valid_data.iloc[:90]
data_test1 = valid_data.iloc[90:]

# sample datasets for Samples Mix Check
data_train2 = valid_data.iloc[:70]
data_test2 = valid_data.iloc[60:]

# sample datasets for Label Drift Check
data_train3 = valid_data.iloc[:70]
data_test3 = valid_data.iloc[70:]
data_test3.loc[70:,'diagnosis']='Malignant'

# sample datasets for Feature Drift Check
data_train4 = valid_data.iloc[:50]
data_test4 = valid_data.iloc[50:]
data_test4['mean_radius'] = data_test4['mean_radius'].astype('float') + np.random.normal(100, 300, 50)

# sample datasets for Multivariate Drift Check
data_train5 = valid_data.iloc[:70]
data_test5 = valid_data.iloc[70:]



# Tests

# test split_train_test function throws an error
# if the cleaned_data is not a dataframe
def test_split_train_test_data_error_on_wrong_data_type():
    with pytest.raises(TypeError, match="The cleaned_data must be a pandas DataFrame."):
        split_train_test_data(cleaned_data=invalid_data_type, train_data_size=0.3)

# if the train_data_size is not a valid portion
def test_split_train_test_data_error_on_invalid_train_size():
    with pytest.raises(ValueError, match="train_data_size must be a float between 0 and 1."):
        split_train_test_data(cleaned_data=valid_data, train_data_size=1.5)

# if the stratify_by column is not in the cleaned_data
def test_split_train_test_data_error_on_invalid_stratify_column():
    with pytest.raises(KeyError, match="The column 'invalid_column' does not exist in the cleaned_data."):
        split_train_test_data(cleaned_data=valid_data, train_data_size=0.8, stratify_by="invalid_column")


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
    with pytest.raises(ValueError, match="Label drift score above threshold: 0.4"):
        validate_split_data(data_train=data_train3,data_test=data_test3)

# if Feature Drift Check failed
def test_validate_split_data_error_on_feature_drift():
    with pytest.raises(ValueError, match="Feature drift score above threshold: 0.4"):
        validate_split_data(data_train=data_train4,data_test=data_test4)

# if Multivariate Drift Check failed
def test_validate_split_data_error_on_multivariate_drift():
    with pytest.raises(ValueError, match="Multivariate drift score above threshold: 0.4"):
        validate_split_data(data_train=data_train5,data_test=data_test5)