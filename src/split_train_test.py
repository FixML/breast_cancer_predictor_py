import os
import pandas as pd
from sklearn.model_selection import train_test_split
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import DatasetsSizeComparison, TrainTestSamplesMix, MultivariateDrift, LabelDrift, FeatureDrift
# from src.clean_data import write_data

def split_train_test_data(cleaned_data, train_data_size, stratify_by=None):
    """Split train test data using cleaned data"""

    # Ensure cleaned_data is a dataframe, if not raise error
    if not isinstance(cleaned_data, pd.DataFrame): 
        raise FileNotFoundError(f"The cleaned_data is not a pandas dataframe.")
    
    # create the split
    cancer_train, cancer_test = train_test_split(
        cleaned_data, train_size=train_data_size, stratify=stratify_by #cancer["diagnosis"]
    )

    # test train test split dataframes
    
    # Datasets Size Comparison Check
    check_instance = (
    DatasetsSizeComparison()
    .add_condition_train_dataset_greater_or_equal_test()
    .add_condition_test_train_size_ratio_greater_than(0.2)
    )  
    check_instance.run(cancer_train, cancer_test)

    # Train Test Samples Mix Check
    check = TrainTestSamplesMix()
    sample_mix_check = check.run(test_dataset=cancer_test, train_dataset=cancer_train)
    assert (
        sample_mix_check.passed_conditions()
    ), ("Data from Test dataset also present in Train dataset")


    # Label Drift Check
    check = LabelDrift().add_condition_drift_score_less_than(0.4)
    label_drift_check = check.run(train_dataset=cancer_train, test_dataset=cancer_test)
    drift_score = label_drift_check.reduce_output()
    assert label_drift_check.passed_conditions(), (
    f"Drift score above threshold: {drift_score['Label Drift Score']} vs "
    f"{0.4}"
    )

    # Feature Drift Check
    check = FeatureDrift().add_condition_drift_score_less_than(0.4)
    feature_drift_check = check.run(train_dataset=cancer_train, test_dataset=cancer_test)
    drift_score = feature_drift_check.reduce_output()
    assert feature_drift_check.passed_conditions(), (
    f"Drift score above threshold: {drift_score['Feature Drift Score']} vs "
    f"{0.4}"
    )

    # Multivariate Drift Check
    check = MultivariateDrift()
    multivariate_drift_check = check.run(train_dataset=cancer_train, test_dataset=cancer_test)

    
    return cancer_train, cancer_test