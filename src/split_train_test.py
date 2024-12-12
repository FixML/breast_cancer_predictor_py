import os
import pandas as pd
from sklearn.model_selection import train_test_split
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import DatasetsSizeComparison, TrainTestSamplesMix, MultivariateDrift, LabelDrift, FeatureDrift

def split_train_test_data(cleaned_data, train_data_size, stratify_by=None):
    """Split train test data using cleaned data"""

    # Ensure cleaned_data is a dataframe, if not raise error
    if not isinstance(cleaned_data, pd.DataFrame): 
        raise FileNotFoundError(f"The cleaned_data is not a pandas dataframe.")
    
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
    if data_size_comp.passed_conditions():
        raise ValueError("The train test data size ratio should be greater than 0.2")

    # Train Test Samples Mix Check
    check = TrainTestSamplesMix.add_condition_duplicates_ratio_less_or_equal(0)
    sample_mix_check = check.run(test_dataset=data_test, train_dataset=data_train)
    if sample_mix_check.passed_conditions():
        raise ValueError("Data from Test dataset also present in Train dataset")


    # Label Drift Check
    check = LabelDrift().add_condition_drift_score_less_than(0.2)
    label_drift_check = check.run(train_dataset=data_train, test_dataset=data_test)
    # drift_score = label_drift_check.reduce_output()
    if label_drift_check.passed_conditions():
        raise ValueError(f"Drift score above threshold: 0.2")

    # Feature Drift Check
    check = FeatureDrift().add_condition_drift_score_less_than(0.4)
    feature_drift_check = check.run(train_dataset=data_train, test_dataset=data_test)
    # drift_score = feature_drift_check.reduce_output()
    if feature_drift_check.passed_conditions():
        raise ValueError(f"Drift score above threshold: 0.4")

    # Multivariate Drift Check
    check = MultivariateDrift().add_condition_overall_drift_value_less_than(0.4)
    multivariate_drift_check = check.run(train_dataset=data_train, test_dataset=data_test)
    # drift_score = multivariate_drift_check.reduce_output()
    if multivariate_drift_check.passed_conditions():
        raise ValueError(f"Drift score above threshold: 0.4")