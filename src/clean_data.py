# clean_data.py
# author: Weilin Han
# date: 2024-10-15

import pandas as pd
import warnings
import re
import os


def extract_column_name(text_lines):
    """
    Extract and clean column names from a .names file.

    This function processes the content of a .names file by extracting column names 
    between the sections "7. Attribute information" and "8. Missing attribute values: none".
    It cleans the column names by removing line numbers, special characters, and replacing 
    spaces with underscores. Additionally, the function adds statistics-based column names 
    (such as 'mean', 'se', 'max') for each attribute.

    Parameters
    ----------
    text_lines : list of str
        A list of lines from the .names file containing the attribute information.

    Returns
    -------
    list of str
        A list of cleaned and formatted column names, including statistics-based columns 
        like 'mean', 'se', and 'max' for each feature.

    Notes
    -----
    The function assumes the .names file has specific sections, where the attribute information
    starts at "7. Attribute information" and ends before "8. Missing attribute values: none".
    The statistics added to each feature include:
    - 'mean': The average value of the feature.
    - 'se': The standard error of the feature.
    - 'max': The maximum value, represented by the mean of the three largest values.

    """
    
    # Get lines between attribute info and missing values section
    start = text_lines.index('7. Attribute information')
    end = text_lines.index('8. Missing attribute values: none')
    text_lines = text_lines[start:end]

    # Remove line numbers and special characters
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
    """
    Read data from a CSV file and assign custom column names.

    This function loads data from a CSV file and assigns the provided column names to the 
    dataframe. It performs a series of checks to ensure the file exists, the column names list 
    is correctly formatted, and the number of column names matches the number of columns in 
    the data.

    Parameters
    ----------
    raw_data : str
        The path to the raw CSV data file to be read.

    col_name : list of str
        A list containing the column names to be assigned to the dataframe. This list must contain 
        exactly 32 strings, corresponding to the number of columns in the data.

    Returns
    -------
    pandas.DataFrame
        A dataframe containing the data from the CSV file, with the specified column names.

    Raises
    ------
    FileNotFoundError
        If the specified raw data file does not exist at the provided path.
    
    TypeError
        If 'col_name' is not a list.
    
    ValueError
        If 'col_name' does not contain exactly 32 items.

    Warns
    -----
    UserWarning
        If any item in 'col_name' is not a string.

    Notes
    -----
    - The function checks that the raw data file exists before attempting to read it.
    - It also ensures that the 'col_name' parameter is a list of strings containing exactly 32 items, 
      matching the number of columns in the CSV file.
    - If any item in the 'col_name' list is not a string, a warning is issued.

    """

    # Ensure the raw data file exists, if not raise error
    if not os.path.exists(raw_data):
        raise FileNotFoundError(f"The raw_data file does not exist.")
    
    # Ensure the col_name is a list, if not raise error
    if not isinstance(col_name, list):
        raise TypeError("col_name must be a list.")
    
    # Ensure the list only contains strings, if not raise warning
    if not all(isinstance(item, str) for item in col_name):
        warnings.warn("col_name contains non-string values")
    
    imported_data = pd.read_csv(raw_data, header=None)

    # Ensure the items in col_name list is same as the number of columns, if not raise error
    if len(col_name) != imported_data.shape[1]:
        raise ValueError("The number of items in col_name must match the number of columns in raw_data.")
    
    imported_data.columns = col_name

    return imported_data

def clean_data(imported_data, drop_columns=['id'], relabel={'M' : 'Malignant','B' : 'Benign'}):
    """
    Clean the imported data by dropping specified columns and relabeling values.

    This function cleans the imported data by performing two operations:
    1. Dropping the columns specified in the `drop_columns` parameter.
    2. Replacing values in the 'diagnosis' column according to the mappings provided in the `relabel` dictionary.

    Parameters
    ----------
    imported_data : pandas.DataFrame
        The dataframe containing the raw data to be cleaned.

    drop_columns : list of str, optional, default=['id']
        A list of column names to be dropped from the dataframe. By default, the 'id' column is dropped.

    relabel : dict, optional, default={'M' : 'Malignant', 'B' : 'Benign'}
        A dictionary for relabeling values in the 'diagnosis' column. Keys are original values, and values are the new labels.

    Returns
    -------
    pandas.DataFrame
        A cleaned dataframe with the specified columns dropped and the 'diagnosis' column relabeled.

    Raises
    ------
    TypeError
        If 'imported_data' is not a pandas dataframe, if 'drop_columns' is not a list, or if 'relabel' is not a dictionary.

    Notes
    -----
    - The function assumes the 'diagnosis' column exists in the dataframe and contains values that need to be relabeled.
    - The columns specified in `drop_columns` will be removed from the dataframe, and the 'diagnosis' column will be updated according to the `relabel` dictionary.

    """
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
    """
    Write a dataframe to a specified directory as a CSV file.

    This function saves the given dataframe to a CSV file in the specified directory. It performs
    checks to ensure that the dataframe is valid, the directory exists, and the provided path is
    indeed a directory (not a file).

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The dataframe containing the data to be written to a CSV file.

    data_to : str
        The directory path where the CSV file should be saved.

    name_of_file : str
        The name of the file (including the '.csv' extension) where the dataframe will be saved.

    Raises
    ------
    TypeError
        If 'dataframe' is not a pandas DataFrame.

    FileNotFoundError
        If the provided directory path ('data_to') does not exist.

    NotADirectoryError
        If the provided 'data_to' path exists but is not a directory.

    Notes
    -----
    - The dataframe will be saved without including the index (index=False).
    - The function checks if the directory exists and raises an error if it doesn't. If the provided
      path is not a directory, it raises a NotADirectoryError.

    """
    # Ensure the data_frame is a dataframe, if not raise an error
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas data frame.")
    
    # Ensure directory path exists, if not raise an error
    if not os.path.exists(data_to):
        raise FileNotFoundError('The directory provided does not exist.')

    # Ensure the dirctory path provided is a directory, if not raise an error
    if not os.path.isdir(data_to):
        raise NotADirectoryError('The directory path provided is not a directory, it is an existing file path. Please provide a path to a new, or existing directory.')
    
    
    dataframe.to_csv(os.path.join(data_to, name_of_file), index=False)