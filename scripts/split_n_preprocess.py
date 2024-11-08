# split_n_preprocess.py
# author: Tiffany Timbers
# date: 2023-11-27

import click
import os
import numpy as np
from sklearn import set_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.split_train_test import split_train_test_data
from src.preprocessor import create_save_preprocessor

@click.command()
@click.option('--cleaned-data', type=str, help="Path to cleaned data")
@click.option('--train-data-size', type=str, help="Proportion of the dataset to include in the train split")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--preprocessor-to', type=str, help="Path to directory where the preprocessor object will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(cleaned_data, train_data_size, data_to, preprocessor_to, seed):
    '''This script splits the raw data into train and test sets, 
    and then preprocesses the data to be used in exploratory data analysis.
    It also saves the preprocessor to be used in the model training script.'''
    np.random.seed(seed)
    set_config(transform_output="pandas")

    try:
        cancer_train, cancer_test = split_train_test_data(cleaned_data, train_data_size, data_to)
    except:
        os.makedirs(data_to)
        cancer_train, cancer_test = split_train_test_data(cleaned_data, train_data_size, data_to)

    try:
        create_save_preprocessor(cancer_train, cancer_test, data_to, preprocessor_to)
    except:
        os.makedirs(preprocessor_to)
        create_save_preprocessor(cancer_train, cancer_test, data_to, preprocessor_to)

if __name__ == '__main__':
    main()
