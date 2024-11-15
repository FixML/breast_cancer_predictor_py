import os
import pandas as pd
from sklearn.model_selection import train_test_split
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import DatasetsSizeComparison, TrainTestSamplesMix, MultivariateDrift, LabelDrift, FeatureDrift
# from src.clean_data import write_data

def split_train_test_data(cleaned_data, train_data_size, stratify_by=None):
    """Split train test data using cleaned data"""

    # Check if the cleaned_data is a dataframe, if not raise error
    if not isinstance(cleaned_data, pd.DataFrame): 
        raise FileNotFoundError(f"The cleaned_data is not a pandas dataframe.")
    
    # # Check if train_data_size is a float and is greater than 0 and smaller than 1, if not raise error
    # if not isinstance(train_data_size, float) or not (0 < train_data_size < 1):
    #     raise ValueError("train_data_size must be a float between 0 and 1.")

    cancer=pd.read_csv(cleaned_data) # put in the script

    # create the split
    cancer_train, cancer_test = train_test_split(
        cancer, train_size=train_data_size, stratify=stratify_by #cancer["diagnosis"]
    )

    # test train test split dataframes
    
    # Datasets Size Comparison Check
    check_instance = (
    DatasetsSizeComparison()
    .add_condition_train_dataset_greater_or_equal_test()
    .add_condition_test_size_greater_or_equal(100)
    .add_condition_test_train_size_ratio_greater_than(0.2)
    )  
    check_instance.run(cancer_train, cancer_test)

    # Train Test Samples Mix Check
    check = TrainTestSamplesMix()
    check.run(test_dataset=cancer_test, train_dataset=cancer_train)

    # Label Drift Check
    check = LabelDrift()
    check.run(train_dataset=cancer_train, test_dataset=cancer_test)

    # Feature Drift Check
    # check = FeatureDrift()
    # check.run(train_dataset=cancer_train, test_dataset=cancer_test, model=model)

    # Multivariate Drift Check
    check = MultivariateDrift()
    check.run(train_dataset=cancer_train, test_dataset=cancer_test)

    
    return cancer_train, cancer_test