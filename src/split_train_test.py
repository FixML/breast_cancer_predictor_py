import os
import pandas as pd
from sklearn.model_selection import train_test_split
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import DatasetsSizeComparison, TrainTestSamplesMix, MultivariateDrift, LabelDrift, FeatureDrift

def split_train_test_data(cleaned_data, train_data_size, stratify_by=None):
    """Split train test data using cleaned data"""

    # Ensure cleaned_data is a dataframe
    if not isinstance(cleaned_data, pd.DataFrame):
        raise TypeError("The cleaned_data must be a pandas DataFrame.")

    # Ensure train_data_size is a valid proportion
    if not (0 < train_data_size < 1):
        raise ValueError("train_data_size must be a float between 0 and 1.")

    # Handle stratify_by
    if stratify_by:
        if stratify_by not in cleaned_data.columns:
            raise KeyError(f"The column '{stratify_by}' does not exist in the cleaned_data.")
    
    # create the split
    data_train, data_test = train_test_split(
        cleaned_data, train_size=train_data_size, stratify=stratify_by #cleaned_data["diagnosis"]
    )
    
    return data_train, data_test

def validate_split_data(data_train, data_test):
    """Test split datasets using Deepchecks"""

    # test train test split dataframes
    # prepare the train test datasets to Deepchecks Dataset format
    data_train = Dataset(data_train,features=data_train.columns[1:],label=data_train.columns[0])
    data_test = Dataset(data_test,features=data_test.columns[1:],label=data_test.columns[0])

    # Datasets Size Comparison Check
    check_instance = (
    DatasetsSizeComparison()
    .add_condition_train_dataset_greater_or_equal_test()
    .add_condition_test_train_size_ratio_greater_than(0.2)
    )  
    data_size_comp = check_instance.run(data_train, data_test)
    if not data_size_comp.passed_conditions():
        raise ValueError("The train test data size ratio should be greater than 0.2")

    # Train Test Samples Mix Check
    check = TrainTestSamplesMix().add_condition_duplicates_ratio_less_or_equal(0)
    sample_mix_check = check.run(test_dataset=data_test, train_dataset=data_train)
    if not sample_mix_check.passed_conditions():
        raise ValueError("Data from Test dataset also present in Train dataset")

    # Label Drift Check
    check = LabelDrift().add_condition_drift_score_less_than(0.4)
    label_drift_check = check.run(train_dataset=data_train, test_dataset=data_test)
    # drift_score = label_drift_check.reduce_output()
    if not label_drift_check.passed_conditions():
        raise ValueError(f"Label drift score above threshold: 0.4")

    # Feature Drift Check
    check = FeatureDrift().add_condition_drift_score_less_than(0.4)
    feature_drift_check = check.run(train_dataset=data_train, test_dataset=data_test)
    # drift_score = feature_drift_check.reduce_output()
    if not feature_drift_check.passed_conditions():
        raise ValueError(f"Feature drift score above threshold: 0.4")

    # Multivariate Drift Check
    check = MultivariateDrift().add_condition_overall_drift_value_less_than(0.4)
    multivariate_drift_check = check.run(train_dataset=data_train, test_dataset=data_test)
    # drift_score = multivariate_drift_check.reduce_output()
    if not multivariate_drift_check.passed_conditions():
        raise ValueError(f"Multivariate drift score above threshold: 0.4")