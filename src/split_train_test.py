import os
import pandas as pd
from sklearn.model_selection import train_test_split

def split_train_test_data(cleaned_data, train_data_size, data_to):
    """Split train test data using cleaned data"""
    
    cancer=pd.read_csv(cleaned_data)

    # create the split
    cancer_train, cancer_test = train_test_split(
        cancer, train_size=train_data_size, stratify=cancer["diagnosis"]
    )

    cancer_train.to_csv(os.path.join(data_to, "cancer_train.csv"), index=False)
    cancer_test.to_csv(os.path.join(data_to, "cancer_test.csv"), index=False)

    return cancer_train, cancer_test