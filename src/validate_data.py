# clean_validate.py
# author: Weilin Han
# date: 2024-10-03

import pandas as pd
import pandera as pa
import os

# Function to build schema from the config file
def build_schema_from_csv(data_config, expected_columns):
    """Building schema for validation"""

    # Ensure the data_config is a pandas dataframe
    if not isinstance(data_config, pd.DataFrame):
        raise TypeError("data_config must be a pandas dataframe.")
    
    # Ensure the data_config has following columns: column,type,max,min,category
    required_columns = ['column', 'type', 'min', 'max','category']
    missing_columns = [col for col in required_columns if col not in data_config.columns]
    if missing_columns:
        raise ValueError(f"The data_config must have following columns: 'column', 'type', 'min', 'max', 'category'.")

    # Ensure the values of 'column' match the column names extracted from name file
    if expected_columns is not None:
        actual_columns = data_config['column'].str.strip("'").tolist()  # Clean up any extra quotation marks in 'column'
        if set(actual_columns) != set(expected_columns):
            raise ValueError("Column names in the config file do not match the expected columns.")
    

    schema_dict = {}
    
    # Loop through each row in the config DataFrame
    for _, row in data_config.iterrows():
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
    
    return pa.DataFrameSchema(schema_dict)
    

# Function to validate schema
def validate_data(schema, dataframe):
    """Building schema to validate data using pandera"""

    # Ensure the schema is a pandera schema, if not raise an error
    if not isinstance(schema, pa.DataFrameSchema):
        raise TypeError("schema must be a pandera dataframe schema.")
    
    # Ensure the data_frame is a dataframe, if not raise an error
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas data frame.")
    
    schema.validate(dataframe, lazy=True)



