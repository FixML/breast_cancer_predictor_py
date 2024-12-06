# clean_validate.py
# author: Weilin Han
# date: 2024-10-03

import pandas as pd
import pandera as pa

# Function to build schema from the config file
def build_schema_from_csv(data_config, expected_columns):
    """Building schema for validation"""

    # Ensure the data_config is a pandas dataframe
    if not isinstance(data_config, pd.DataFrame):
        raise TypeError("data_config must be a pandas dataframe.")
    
    # Ensure the data_config has following columns: column,type,max,min,category
    required_columns = ['column', 'type', 'min', 'max','category', 'max_nullable']
    missing_columns = [col for col in required_columns if col not in data_config.columns]
    if missing_columns:
        raise ValueError(f"The data_config must have following columns: 'column', 'type', 'min', 'max', 'category', 'max_nullable'.")

    # Ensure the values of 'column' match the column names extracted from name file
    if expected_columns is not None:
        actual_columns = data_config['column'].str.strip("'").tolist()  # Clean up any extra quotation marks in 'column'
        if actual_columns != expected_columns:
            raise ValueError("Column names in the config file do not match the expected columns.")
    

    schema_dict = {}
    
    # Loop through each row in the config DataFrame
    for _, row in data_config.iterrows():
        column_name = row['column'].strip()  # Removing potential extra spaces
        column_type = row['type'].strip()    # Strip any spaces
        min_value = row['min'] if pd.notna(row['min']) else None
        max_value = row['max'] if pd.notna(row['max']) else None
        category_in = row['category'] if pd.notna(row['category']) else None
        max_nullable = row['max_nullable'] if pd.notna(row['max_nullable']) else None
        
        # Define the correct Pandera data type
        if column_type == 'int':
            dtype = pa.Int
        elif column_type == 'float':
            dtype = pa.Float
        elif column_type == 'str':
            dtype = pa.String
        else:
            raise ValueError(f"Unsupported column type: {column_type}")
        
        # Create value range validation checks
        value_range_checks = []
        if min_value is not None:
            value_range_checks.append(pa.Check.greater_than_or_equal_to(float(min_value),
                                                                        error=f'Value is smaller than {min_value}'))
        if max_value is not None:
            value_range_checks.append(pa.Check.less_than_or_equal_to(float(max_value),
                                                                     error=f'Value is larger than {max_value}'))
        if category_in is not None:
            category_list = category_in.split(',')
            value_range_checks.append(pa.Check.isin(category_list,
                                                    error=f'Value not in {category_list}'))
        if max_nullable is not None:
            value_range_checks.append(pa.Check(lambda s: s.isna().mean() <= max_nullable,
                                               error=f'Too many missing values, must have at least {(1-max_nullable)*100}% non-null values.'))
        
        # Add the column schema to the schema dictionary
        schema_dict[column_name] = pa.Column(dtype,nullable=True, checks=value_range_checks)

        global_checks=[
        pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
        pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found.")
        ]
    
    return pa.DataFrameSchema(schema_dict, checks=global_checks)
   

# Function to validate schema
def validate_data(schema, dataframe):
    """Building schema to validate data using pandera"""

    # Ensure the schema is a pandera schema, if not raise an error
    if not isinstance(schema, pa.DataFrameSchema):
        raise TypeError("schema must be a pandera dataframe schema.")
    
    # Ensure the data_frame is a dataframe, if not raise an error
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas data frame.")

    # Ensure the data_frame has observations, if not raise an error
    if dataframe.empty:
        raise ValueError("dataframe must contain observations.")
    
    schema.validate(dataframe, lazy=True)
    # return print(f"Expected Columns:  {expected_columns}, Actual Columns:  {actual_columns}")




