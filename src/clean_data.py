# clean_data.py
# author: Weilin Han
# date: 2024-10-15

import pandas as pd
import re
import os


def extract_column_name(raw_name_file):
    """Extract and clean column names from .names file."""
    
    # Ensure the raw name file exists, if not raise error
    if not os.path.exists(raw_name_file):
        raise FileNotFoundError(f"The raw_name file does not exist.")
    
    # Extracting column names from downloaded raw file
    text_lines = []
    with open(raw_name_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line.startswith('#') and line:  # Skip comma
                text_lines.append(line)
        start = text_lines.index('7. Attribute information')
        end = text_lines.index('8. Missing attribute values: none')
        text_lines = text_lines[start:end]
        
        pattern = re.compile(r'^[1-9a-z]\)\s*')
        text_lines = [item for item in text_lines if pattern.match(item)]
        text_lines = [pattern.sub('', item) for item in text_lines]
        pattern = re.compile(r'\(.*?\)')
        text_lines = [re.sub(r"\s+", "_", pattern.sub('', item).strip()) for item in text_lines]

        statistics = ['mean','se','max'] 
        #se is standard error, and max is the worst or largest (mean of three largest values)

        # please refer to original file for explanation of feactures
        colnames = text_lines[0:2]
        for stat in statistics:
            for feature in text_lines[2:]:
                colnames.append(stat+'_'+feature)
        colnames = [col.lower() for col in colnames]
        
    return colnames
    
def read_data(raw_data, col_name):
    """Read data from .data or .csv file."""

    # Ensure the raw data file exists, if not raise error
    if not os.path.exists(raw_data):
        raise FileNotFoundError(f"The raw_data file does not exist.")
    
    # Ensure the col_name is a list, if not raise error
    if not isinstance(col_name, list):
        raise TypeError("col_name must be a list.")
    
    # Ensure the list has 32 items, if not raise error
    if len(col_name) != 32:
        raise ValueError("col_name must contain exactly 32 items.")
    
    # Ensure the list only contains strings, if not raise error
    if not all(isinstance(item, str) for item in col_name):
        raise ValueError("col_name must only contain strings.")
    
    imported_data = pd.read_csv(raw_data, names=col_name, header=None)
    return imported_data

def clean_data(imported_data, drop_columns=['id'], relabel={'M' : 'Malignant','B' : 'Benign'}):
    """Clean imported data"""
    # Ensure the imported_data is a dataframe
    if not isinstance(imported_data, pd.DataFrame):
        raise TypeError("imported_data must be a data frame.")
    
    # Ensure the drop_columns is a list
    if not isinstance(drop_columns, list):
        raise TypeError("drop_columns must be a list.")
    
    # Ensure the relabel is a dictionary
    if not isinstance(relabel, dict):
        raise TypeError("relabel must be a dictionary")
    
    cleaned_data = imported_data.drop(columns=drop_columns)
    cleaned_data['diagnosis'] = cleaned_data['diagnosis'].replace(relabel)
    return cleaned_data

def write_data(dataframe, data_to, name_of_file):
    """Write data to directory"""
    # Ensure the data_frame is a dataframe, if not raise an error
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas data frame.")
    
    # Ensure directory path exists, if not raise an error
    if not os.path.exists(data_to):
        raise FileNotFoundError('The directory provided does not exist.')

    # Ensure the dirctory path provided is a directory, if not raise an error
    if not os.path.isdir(data_to):
        raise NotADirectoryError('The directory path provided is not a directory, it is an existing file path. Please provide a path to a new, or existing directory.')
    
    # Ensure the name of file is string, if not raise an error
    if not isinstance(name_of_file, str):
        raise TypeError("name_of_file must be string.")
    
    dataframe.to_csv(os.path.join(data_to, name_of_file), index=False)