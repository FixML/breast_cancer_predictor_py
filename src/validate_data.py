# clean_validate.py
# author: Weilin Han
# date: 2024-10-03

import pandas as pd
import pandera as pa
import os

# Function to build schema from the config file
def build_schema_from_csv(data_config, expected_columns):
    """Building schema to validate data using pandera"""

    # Input Validation Checks 1: Ensure the data_config file exists, if not raise error
    if not os.path.exists(data_config):
        raise FileNotFoundError(f"The data_config file does not exist.")
    
    config_df = pd.read_csv(data_config)

    # Ensure the pandas dataframe has following columns: column,type,max,min,category
    required_columns = ['column', 'type', 'min', 'max','category']
    if required_columns not in list(config_df.columns):
        raise ValueError(f"The configuration file must have following columns: 'column', 'type', 'min', 'max', 'category'.")

    # Ensure the values of 'column' match the column names extracted from name file
    if expected_columns is not None:
        actual_columns = config_df['column'].str.strip("'").tolist()  # Clean up any extra quotation marks in 'column'
        if set(actual_columns) != set(expected_columns):
            raise ValueError("Column names in the config file do not match the expected columns.")

    schema_dict = {}
    
    # Loop through each row in the config DataFrame
    for _, row in config_df.iterrows():
        column_name = row['column'].strip()  # Removing potential extra spaces
        column_type = row['type'].strip()    # Strip any spaces
        min_value = row['min'] if pd.notna(row['min']) else None
        max_value = row['max'] if pd.notna(row['max']) else None
        category_in = row['category'] if pd.notna(row['category']) else None
        
        # Define the correct Pandera data type
        if column_type == 'int':
            dtype = pa.Int
        elif column_type == 'float':
            dtype = pa.Float
        elif column_type == 'str':
            dtype = pa.String
        else:
            raise ValueError(f"Unsupported column type: {column_type}")
        
        # Create validation checks
        checks = []
        if min_value is not None:
            checks.append(pa.Check.greater_than_or_equal_to(float(min_value)))
        if max_value is not None:
            checks.append(pa.Check.less_than_or_equal_to(float(max_value)))
        if category_in is not None:
            category_list = category_in.split(',')
            checks.append(pa.Check.isin(category_list))
        
        # Add the column schema to the schema dictionary
        schema_dict[column_name] = pa.Column(dtype, checks=checks, nullable=False)
    
    # Return the DataFrameSchema object
    return pa.DataFrameSchema(schema_dict)



