import os
import pandas as pd
from sklearn.model_selection import train_test_split

def split_train_test_data(cleaned_data, train_data_size, data_to):
    """Split train test data using cleaned data"""

    # Check if the raw name file exists, if not raise error
    if not os.path.exists(cleaned_data):
        raise FileNotFoundError(f"The cleaned_data file does not exist.")
    
    # Check if train_data_size is a float and is greater than 0 and smaller than 1, if not raise error
    if not isinstance(train_data_size, float) or not (0 < train_data_size < 1):
        raise ValueError("train_data_size must be a float between 0 and 1.")

    # check if the data_to directory path exists, if not raise an error
    if not os.path.exists(data_to):
        raise FileNotFoundError('The data_to directory provided does not exist.')
    
    # check if the data_to dirctory path provided is a directory, if not raise an error
    if not os.path.isdir(data_to):
        raise NotADirectoryError('The data_to directory path provided is not a directory, it is an existing file path. Please provide a path to a new, or existing directory.')

    cancer=pd.read_csv(cleaned_data)

    # create the split
    cancer_train, cancer_test = train_test_split(
        cancer, train_size=train_data_size, stratify=cancer["diagnosis"]
    )

    cancer_train.to_csv(os.path.join(data_to, "cancer_train.csv"), index=False)
    cancer_test.to_csv(os.path.join(data_to, "cancer_test.csv"), index=False)

    return cancer_train, cancer_test