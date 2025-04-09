# clean_validate.py
# author: Weilin Han
# date: 2024-10-03

import pandas as pd
import pandera as pa

# Function to build schema from the config file
def build_schema_from_DataFrame(data_config, expected_columns):
    """
    Build a Pandera schema for data validation based on a configuration dataframe.

    This function generates a Pandera schema from a configuration dataframe that defines
    the expected types, ranges, and categories for each column in the data. It also includes 
    global checks to ensure no duplicate rows and no entirely empty rows in the dataset.

    Parameters
    ----------
    data_config : pandas.DataFrame
        A dataframe containing the configuration for each column in the dataset. It must have the 
        following columns: 'column', 'type', 'min', 'max', 'category', and 'max_nullable'. Each row 
        represents a column in the dataset and contains the type, min/max values, valid categories, 
        and the allowed fraction of nullable values.

    expected_columns : list
        A list of column names that the configuration should match. The columns in the 
        'data_config' dataframe must match these names.

    Returns
    -------
    pandera.DataFrameSchema
        A Pandera DataFrame schema that can be used for data validation. This schema includes 
        individual column checks (type, range, category, and nullability) as well as global checks 
        for duplicates and empty rows.

    Raises
    ------
    TypeError
        If 'data_config' is not a pandas DataFrame.
    ValueError
        If 'data_config' is empty, does not contain the required columns, or the column names 
        in 'data_config' do not match the expected columns.
    
    Notes
    -----
    The 'type' column in the configuration must specify one of 'int', 'float', or 'str'. 
    The 'category' column can be a comma-separated list of valid categories, or None if 
    no specific category validation is required. The 'min' and 'max' columns should define 
    the allowable range for numeric columns, and the 'max_nullable' column should specify 
    the maximum fraction of null values allowed in the column (values between 0 and 1).
    """

    # Ensure the data_config is a pandas dataframe
    if not isinstance(data_config, pd.DataFrame):
        raise TypeError("data_config must be a pandas dataframe.")
    
    # Ensure the data_config has following columns: column,type,max,min,category,max_nullable
    required_columns = ['column', 'type', 'min', 'max','category', 'max_nullable']
    if data_config.empty:
        raise ValueError("The data_config must contain at least one row.")
    
    if set(data_config.columns) != expected_columns or data_config.shape[1] != 6:
        raise ValueError("The data_config must have following columns: 'column', 'type', 'min', 'max', 'category', 'max_nullable'.")

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
        schema_dict[column_name] = pa.Column(column_type,nullable=True, checks=value_range_checks)

        global_checks=[
        pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
        pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found.")
        ]
    
    return pa.DataFrameSchema(schema_dict, checks=global_checks)
   

# Function to validate schema
def validate_data(schema, dataframe):
    """
    Validates the input cancer data in the form of a pandas DataFrame against a predefined schema,
    and returns the validated DataFrame.

    This function checks that the columns in the input DataFrame conform to the expected types and value ranges.
    It also ensures there are no duplicate rows and no entirely empty rows.

    Parameters
    ----------
    schema: predefined schema in Pandas DataFrame format
    dataframe : pandas.DataFrame
        The DataFrame containing cancer-related data, which includes columns such as 'class', 'mean_radius', 
        'mean_texture', and other related measurements. The data is validated based on specific criteria for 
        each column.

    Returns
    -------
    pandas.DataFrame
        The validated DataFrame that conforms to the specified schema.

    Raises
    ------
    pandera.errors.SchemaError
        If the DataFrame does not conform to the specified schema (e.g., incorrect data types, out-of-range values,
        duplicate rows, or empty rows).
    
    Notes
    -----
    The following columns are validated:
        - 'class': Values must be either 'Benign' or 'Malignant'.
        - Measurement columns (e.g., 'mean_radius', 'mean_texture', etc.) must fall within specific ranges.
        - Additional checks ensure there are no duplicate or completely empty rows in the DataFrame.
    """

    # Ensure the schema is a pandera schema, if not raise an error
    if not isinstance(schema, pa.DataFrameSchema):
        raise TypeError("schema must be a pandera dataframe schema.")
    
    # Ensure the data_frame is a dataframe, if not raise an error
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas data frame.")
    
    schema.validate(dataframe, lazy=True)

