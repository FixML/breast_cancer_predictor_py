# clean_validate.py
# author: Weilin Han
# date: 2024-10-20

import click
import os
import sys
import re
import pandas as pd
import great_expectations as gx
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean_data import *
from src.validate_data import *

@click.command()
@click.option('--raw-data', type=str, help="Path to directory where raw data resides")
@click.option('--name-file', type=str, help="Path to dirctory where names file resides")
@click.option('--write-to', type=str, help="Path to directory where cleaned data will be written to")

def main(raw_data, name_file, write_to):
    """Clean raw data and validate it."""
    # Extract column names from .names file
    colnames = extract_column_name(name_file)

    # Read raw data
    imported_data = read_raw_data(raw_data, colnames)

    # Removing id column and relabel diagnosis column
    cleaned_data = clean_data(imported_data)

    # Create Great Expectation batch object for data validation
    batch = create_data_batch(cleaned_data)

    # Validate cleaned data
    # Validates that the dataframe contains specific columns.
    exp_column_exsist(batch, colnames)

    # Validates that the distinct values in specified columns of a dataset contain the expected values.
    col_set = {
        'diagnosis': ['Malignant', 'Benign']
    }
    exp_value_set_in_col(batch, col_set)

    # Validates that the type of values of specified column is correct.
    col_type = {'diagnosis': 'string'}
    for key in colnames[2:]:
        col_type[key] = 'number'
    exp_type_of_col_values(batch, col_type)

    # Validates that the numbers of nulls of specific columns are within the tolerable limit.
    col_percent = {'diagnosis': 0}
    for key in colnames[2:]:
        col_type[key] = 0.1
    # For numerical columns, no more than 10% of values are nulls
    exp_col_not_null(batch, col_percent)

    # Validates that the numeric values of specified columns are within specified range.
    col_range = {
            'mean_radius': [6,30,False,False],
            'mean_texture': [9,40,False,False],
            'mean_perimeter': [40,200,False,False],
            'mean_area': [140,2510,False,False],
            'mean_smoothness': [0,1,False,False],
            'mean_compactness': [0,1,False,False],
            'mean_concavity': [0,1,False,False],
            'mean_concave': [0,1,False,False],
            'mean_symmetry': [0,1,False,False],
            'mean_fractal': [0,1,False,False],
            'se_radius': [0,3,False,False],
            'se_texture': [0,5,False,False],
            'se_perimeter': [0,22,False,False],
            'se_area': [6,550,False,False],
            'se_smoothness': [0,1,False,False],
            'se_compactness': [0,1,False,False],
            'se_concavity': [0,1,False,False],
            'se_concave': [0,1,False,False],
            'se_symmetry': [0,1,False,False],
            'se_fractal': [0,1,False,False],
            'max_radius': [7,40,False,False],
            'max_texture': [12,50,False,False],
            'max_perimeter': [50,260,False,False],
            'max_area': [180,4300,False,False],
            'max_smoothness': [0,1,False,False],
            'max_compactness': [0,2,False,False],
            'max_concavity': [0,2,False,False],
            'max_concave': [0,1,False,False],
            'max_symmetry': [0,1,False,False],
            'max_fractal': [0,1,False,False]
    }
    exp_value_range(batch, col_range)

    write_data(cleaned_data, write_to)

if __name__ == '__main__':
    main()