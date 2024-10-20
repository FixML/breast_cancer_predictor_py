# clean_data.py
# author: Weilin Han
# date: 2024-10-15

import pandas as pd
import re
import os


def extract_column_name(raw_name_file):
    """Extract and clean column names from .names file."""
    
    # Test 1: Ensure the raw name file exists, if not raise error
    if not os.path.exists(raw_name_file):
        raise FileNotFoundError(f"The raw_name file does not exist.")
    
    # Test 2: Ensure the raw name file is a .names file, if not raise error
    if not raw_name_file.endswith('.names'):
        raise ValueError("The raw_name file must be a .names file.")
    
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
        text_lines = [item.split()[0].lower() for item in text_lines]

        statistics = ['mean','se','max'] 
        #se is standard error, and max is the worst or largest (mean of three largest values)

        # please refer to original file for explanation of feactures
        colnames = text_lines[0:2]
        for stat in statistics:
            for feature in text_lines[2:]:
                colnames.append(stat+'_'+feature)
        
    return colnames
    
def read_raw_data(raw_data, col_name):
    """Read data from .data file."""

    # Test 1: Ensure the raw data file exists, if not raise error
    if not os.path.exists(raw_data):
        raise FileNotFoundError(f"The raw_data file does not exist.")
    
    # Test 2: Ensure the raw_data file's extension is .data', if not raise error
    if not raw_data.endswith('.data'):
        raise ValueError("The raw_data file must be a .data file.")
    
    # Test 3: Ensure the col_name is a list, if not raise error
    if not isinstance(col_name, list):
        raise TypeError("col_name must be a list.")
    
    # Test 4: Ensure the list has 32 items, if not raise error
    if len(col_name) != 32:
        raise ValueError("col_name must contain exactly 32 items.")
    
    # Test 5: Ensure the list only contains strings, if not raise error
    if not all(isinstance(item, str) for item in col_name):
        raise ValueError("col_name must only contain strings.")
    
    imported_data = pd.read_csv(raw_data, names=col_name, header=None)
    return imported_data

def clean_data(imported_data, drop_columns=['id'], relabel={'M' : 'Malignant','B' : 'Benign'}):
    """Clean imported data"""
    # Test 1: Ensure the imported_data is a dataframe
    if not isinstance(imported_data, pd.DataFrame):
        raise TypeError("imported_data must be a data frame.")
    
    # Test 2: Ensure the drop_columns is a list
    if not isinstance(drop_columns, list):
        raise TypeError("drop_columns must be a list.")
    
    # Test 3: Ensure the relabel is a dictionary
    if not isinstance(relabel, dict):
        raise TypeError("relabel must be a dictionary")
    
    cleaned_data = imported_data.drop(columns=drop_columns)
    cleaned_data['diagnosis'] = cleaned_data['diagnosis'].replace(relabel)
    return cleaned_data