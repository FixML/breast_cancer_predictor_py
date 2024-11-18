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
    cancer_train, cancer_test = train_test_split(
        cleaned_data, train_size=train_data_size, stratify=stratify_by #cleaned_data["diagnosis"]
    )

    # test train test split dataframes
    # prepare the train test datasets to Deepchecks Dataset format
    cancer_train = Dataset(cancer_train,features=cleaned_data.columns[1:],label=cleaned_data.columns[0])
    cancer_test = Dataset(cancer_test,features=cleaned_data.columns[1:],label=cleaned_data.columns[0])

    # Datasets Size Comparison Check
    check_instance = (
    DatasetsSizeComparison()
    .add_condition_train_dataset_greater_or_equal_test()
    .add_condition_test_train_size_ratio_greater_than(0.2)
    )  
    data_size_comp = check_instance.run(cancer_train, cancer_test)
    if data_size_comp.passed_conditions():
        raise ValueError("The train test data size ratio should be greater than 0.2")

    # Train Test Samples Mix Check
    check = TrainTestSamplesMix()
    sample_mix_check = check.run(test_dataset=cancer_test, train_dataset=cancer_train)
    if sample_mix_check.passed_conditions():
        raise ValueError("Data from Test dataset also present in Train dataset")


    # Label Drift Check
    check = LabelDrift().add_condition_drift_score_less_than(0.4)
    label_drift_check = check.run(train_dataset=cancer_train, test_dataset=cancer_test)
    drift_score = label_drift_check.reduce_output()
    if label_drift_check.passed_conditions():
        raise ValueError(f"Drift score above threshold: {drift_score['Label Drift Score']} vs "
        f"{0.4}"
        )

    # Feature Drift Check
    check = FeatureDrift().add_condition_drift_score_less_than(0.4)
    feature_drift_check = check.run(train_dataset=cancer_train, test_dataset=cancer_test)
    drift_score = feature_drift_check.reduce_output()
    if feature_drift_check.passed_conditions():
        raise ValueError(f"Drift score above threshold: {drift_score['Feature Drift Score']} vs "
        f"{0.4}"
        )

    # Multivariate Drift Check
    check = MultivariateDrift().add_condition_drift_score_less_than(0.4)
    multivariate_drift_check = check.run(train_dataset=cancer_train, test_dataset=cancer_test)
    drift_score = multivariate_drift_check.reduce_output()
    if multivariate_drift_check.passed_conditions():
        raise ValueError(f"Drift score above threshold: {drift_score['Multivariate Drift Score']} vs "
        f"{0.4}"
        )
    
    return cancer_train, cancer_test