# split_n_preprocess.py
# author: Tiffany Timbers
# date: 2023-11-27

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn import set_config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector
np.random.seed(522)
set_config(transform_output="pandas")

@click.command()
@click.option('--raw_data', type=str, help="Path to raw data")
@click.option('--write_to', type=str, help="Path to directory where processed data will be written to")

def main(raw_data, write_to):
    '''This script splits the raw data into train and test sets, 
    and then preprocesses the data to be used in exploratory data analysis.
    It also saves the preprocessor to be used in the model training script.'''
    colnames = [
        "id",
        "class",
        "mean_radius",
        "mean_texture",
        "mean_perimeter", 
        "mean_area",
        "mean_smoothness",
        "mean_compactness",
        "mean_concavity",
        "mean_concave_points",
        "mean_symmetry",
        "mean_fractal_dimension",
        "se_radius",
        "se_texture",
        "se_perimeter", 
        "se_area",
        "se_smoothness",
        "se_compactness",
        "se_concavity",
        "se_concave_points",
        "se_symmetry",
        "se_fractal_dimension",
        "max_radius",
        "max_texture",
        "max_perimeter", 
        "max_area",
        "max_smoothness",
        "max_compactness",
        "max_concavity",
        "max_concave_points",
        "max_symmetry",
        "max_fractal_dimension"
    ]

    cancer = pd.read_csv(raw_data, names=colnames, header=None).drop(columns=['id'])
    # re-label Class 'M' as 'Malignant', and Class 'B' as 'Benign'
    cancer['class'] = cancer['class'].replace({
        'M' : 'Malignant',
        'B' : 'Benign'
    })

    # create the split
    cancer_train, cancer_test = train_test_split(
        cancer, train_size=0.70, stratify=cancer["class"]
    )

    cancer_train.to_csv(os.path.join(write_to, "cancer_train.csv"))
    cancer_test.to_csv(os.path.join(write_to, "cancer_test.csv"))

    cancer_preprocessor = make_column_transformer(
        (StandardScaler(), make_column_selector(dtype_include='number')),
        remainder='passthrough',
        verbose_feature_names_out=False
    )
    pickle.dump(cancer_preprocessor, open(os.path.join(write_to, "cancer_preprocessor.pickle"), "wb"))

    cancer_preprocessor.fit(cancer_train)
    scaled_cancer_train = cancer_preprocessor.transform(cancer_train)
    scaled_cancer_test = cancer_preprocessor.transform(cancer_test)

    scaled_cancer_train.to_csv(os.path.join(write_to, "scaled_cancer_train.csv"))
    scaled_cancer_test.to_csv(os.path.join(write_to, "scaled_cancer_test.csv"))

if __name__ == '__main__':
    main()
