# clean_validate.py
# author: Weilin Han
# date: 2024-10-03

import numpy as np
import pandas as pd
import great_expectations as gx

def create_data_batch(cleaned_data):
    """Create batch for data validation using great expectation package"""
    
    # Test 1: Ensure the cleaned_data is a dataframe
    if not isinstance(cleaned_data, pd.DataFrame):
        raise TypeError("cleaned_data must be a dataframe.")

    context = gx.get_context(mode="ephemeral")

    # Retrieve the dataframe Batch Definition
    data_source_name = "cleaned_data"
    data_source = context.data_sources.add_pandas(name=data_source_name)

    data_asset_name = "cleaned_data_data_asset"
    data_asset = data_source.add_dataframe_asset(name=data_asset_name)

    data_asset = context.data_sources.get(data_source_name).get_asset(data_asset_name)

    batch_definition_name = "cleaned_data_batch_definition"
    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        batch_definition_name
    )

    batch = batch_definition.get_batch(batch_parameters={"dataframe": cleaned_data})
    return batch

# Customize Exception class for validation error
class ValidationError(Exception):
    """Custom Exception for Validation Failure."""
    pass

def check_validation_result(validation_results):
    """Check validation result and raise an error if it's unsuccessful."""
    overall_success = validation_results.success
    exp = validation_results.expectation_config.type
    col = validation_results.expectation_config.kwargs['column']

    if not overall_success:
        raise ValidationError(f"Validation for column '{col}' failed. The data did not meet the expectations: {exp}.")

# Data Schema Validations
def exp_column_exsist(batch, columns):
    """
    Validates that the table contains specific columns.
    
    Parameters
    ----------
    batch : great_expectations.dataset.Dataset
        The Great Expectations batch object that contains the dataset to be validated.
        This object must support the `validate()` method that takes an expectation and returns a validation result.
    
    columns : list
        A list contains column names to be validated.
    
    Returns
    -------
    None
        The function does not return anything. It raises an error if validation fails.
    
    Raises
    ------
    ValidationError
        Raised if the validation result for any column fails, as determined by the `check_validation_result()` function.
    
    Examples
    --------
    >>> batch = some_great_expectations_batch_object
    >>> columns = ['diagnosis',	'mean_radius']
    >>> exp_value_set_in_col(batch, col_set)
    """

    # Test 1: Ensure the batch is a gx batch object, if not raise the error
    if not isinstance(batch, gx.datasource.fluent.interfaces.Batch):
        raise TypeError("batch must be a great expectation batch object.")
    
    # Test 2: Ensure the columns is a list, if not raise the error
    if not isinstance(columns, list):
        raise TypeError("columns must be a list.")
    
    # Test 3: Ensure the columns is a list only contains strings, if not raise the error
    if not all(isinstance(item, str) for item in columns):
        raise ValueError("columns must only contain strings.")
    
    for i in columns:
        expectation = gx.expectations.ExpectColumnToExist(
            column=i
        )
        validation_result = batch.validate(expectation)
        # Test if this expectation passed, if not throw an error
        check_validation_result(validation_result)

# Data Integrity Validations
def exp_value_set_in_col(batch, col_set):
    """
    Validates that the distinct values in specified columns of a dataset contain the expected values.
    
    Parameters
    ----------
    batch : great_expectations.dataset.Dataset
        The Great Expectations batch object that contains the dataset to be validated.
        This object must support the `validate()` method that takes an expectation and returns a validation result.
    
    col_set : dict
        A dictionary where:
        - The keys are column names (str) in the dataset.
        - The values are lists of expected distinct values for the corresponding columns.
    
    Returns
    -------
    None
        The function does not return anything. It raises an error if validation fails.
    
    Raises
    ------
    ValidationError
        Raised if the validation result for any column fails, as determined by the `check_validation_result()` function.
    
    Examples
    --------
    >>> batch = some_great_expectations_batch_object
    >>> col_set = {
    >>>     'diagnosis': ['Malignant', 'Benign'],
    >>>     'gender': ['Male', 'Female']
    >>> }
    >>> exp_value_set_in_col(batch, col_set)
    """
    # Test 1: Ensure the batch is a gx batch object, if not raise the error
    if not isinstance(batch, gx.datasource.fluent.interfaces.Batch):
        raise TypeError("batch must be a great expectation batch object.")
    
    # Test 2: Ensure the col_set is a dict, if not raise the error
    if not isinstance(col_set, dict):
        raise TypeError("col_set must be a dict.")
    
    # Test 3: Ensure the col_set's keys are strings, if not raise the error
    for col in col_set.keys():
        if not isinstance(col, str):
            raise TypeError("col_set keys must be strings.")
    
    for i in col_set:
        expectation = gx.expectations.ExpectColumnDistinctValuesToContainSet(
            column=i,value_set=col_set[i]
        )
        validation_result = batch.validate(expectation)
        # Test if this expectation passed, if not throw an error
        check_validation_result(validation_result)


def exp_type_of_col_values(batch, col_type):
    """
    Validates that the type of values of specified column is correct.
    
    Parameters
    ----------
    batch : great_expectations.dataset.Dataset
        The Great Expectations batch object that contains the dataset to be validated.
        This object must support the `validate()` method that takes an expectation and returns a validation result.
    
    col_type : dict
        A dictionary where:
        - The keys are column names (str) in the dataset.
        - The values are expected type for the corresponding columns.
    
    Returns
    -------
    None
        The function does not return anything. It raises an error if validation fails.
    
    Raises
    ------
    ValidationError
        Raised if the validation result for any column fails, as determined by the `check_validation_result()` function.
    
    Examples
    --------
    >>> batch = some_great_expectations_batch_object
    >>> col_type = {
    >>>     'diagnosis': 'string',
    >>>     'mean_radium': 'number'
    >>> }
    >>> exp_type_of_col_values(batch, col_type)
    """
    # Test 1: Ensure the batch is a gx batch object, if not raise the error
    if not isinstance(batch, gx.datasource.fluent.interfaces.Batch):
        raise TypeError("batch must be a great expectation batch object.")
    
    # Test 2: Ensure the col_type is a dict, if not raise the error
    if not isinstance(col_type, dict):
        raise TypeError("col_type must be a dict.")
    
    # Test 3: Eunsure the type of col_type's keys is string, if not raise the error
    for key in col_type:
            if not isinstance(key, str):
                raise TypeError("col_type keys must be strings.")
            
    # Test 4: Ensure the type of col_type's values is string, if not raise the error
    for value in col_type.values():
        if not isinstance(value, str):
            raise TypeError("col_type values must be strings.")

    for i in col_type:
        expectation = gx.expectations.ExpectColumnValuesToBeOfType(
            column=i, type=col_type[i]
        )
        validation_result = batch.validate(expectation)
        # Test if this expectation passed, if not throw an error
        check_validation_result(validation_result)


# Data Quality Validations
def exp_col_not_null(batch, col_percent):
    """
    Validates that the numbers of nulls of specific columns are within the tolerable limit.
    
    Parameters
    ----------
    batch : great_expectations.dataset.Dataset
        The Great Expectations batch object that contains the dataset to be validated.
        This object must support the `validate()` method that takes an expectation and returns a validation result.
    
    col_percent : dict
        A dictionary where:
        - The keys are column names (str) in the dataset.
        - The values are the tolerable percentage limit of nulls.
    
    Returns
    -------
    None
        The function does not return anything. It raises an error if validation fails.
    
    Raises
    ------
    ValidationError
        Raised if the validation result for any column fails, as determined by the `check_validation_result()` function.
    
    Examples
    --------
    >>> batch = some_great_expectations_batch_object
    >>> col_percent = {
    >>>     'diagnosis': 1,
    >>>     'mean_radium': 0.3 # No more than 30% of values are nulls
    >>> }
    >>> exp_col_not_null(batch, col_percent)
    """
    # Test 1: Ensure the batch is a gx batch object, if not raise the error
    if not isinstance(batch, gx.datasource.fluent.interfaces.Batch):
        raise TypeError("batch must be a great expectation batch object.")
    
    # Test 2: Ensure the col_percent is a dict, if not raise the error
    if not isinstance(col_percent, dict):
        raise TypeError("col_percent must be a dict.")
    
    # Test 3: Eunsure the type of col_percent's keys is string, if not raise the error
    for key in col_percent:
            if not isinstance(key, str):
                raise TypeError("col_percent keys must be strings.")
            
    # Test 4: Ensure the type of col_percent's values is numeric value, if not raise the error
    for value in col_percent.values():
        if not isinstance(value, float):
            raise TypeError("col_percent values must be numeric value.")
    
    # Test 5: Ensure the value of col_percent is possitive, if not raise the error
    for value in col_percent.values():
        if value < 0:
            raise ValueError("col_percent values must be positive.")

    # Test 6: Ensure the col_percent values are not greater than 1, if not raise the error
    for value in col_percent.values():
        if value > 1:
            raise ValueError("col_percent values must not be greater than 1.")
    
    for i in col_percent:
        expectation = gx.expectations.ExpectColumnValuesToNotBeNull(
            column=i, mostly=1-col_percent[i]
        )
        validation_result = batch.validate(expectation)
        # Test if this expectation passed, if not throw an error
        check_validation_result(validation_result)


def exp_value_range(batch, col_range):
    """
    Validates that the numeric values of specified columns are within specified range.
    
    Parameters
    ----------
    batch : great_expectations.dataset.Dataset
        The Great Expectations batch object that contains the dataset to be validated.
        This object must support the `validate()` method that takes an expectation and returns a validation result.
    
    col_range : dict
        A dictionary where:
        - The keys are column names (str) in the dataset.
        - The values are the list that contains following value:
            min_value (comparable type or None): The minimum value for a column entry.
            max_value (comparable type or None): The maximum value for a column entry.
            strict_min (boolean): If True, values must be strictly larger than min_value. Default=False.
            strict_max (boolean): If True, values must be strictly smaller than max_value. Default=False.

    
    Returns
    -------
    None
        The function does not return anything. It raises an error if validation fails.
    
    Raises
    ------
    ValidationError
        Raised if the validation result for any column fails, as determined by the `check_validation_result()` function.
    
    Examples
    --------
    >>> batch = some_great_expectations_batch_object
    >>> col_range = {
    >>>     'mean_radium': [5,25,False,False],
    >>>     'mean_perimeter': [30,150,False,False]
    >>> }
    >>> exp_value_range(batch, col_range)
    """
    # Test 1: Ensure the batch is a gx batch object, if not raise the error
    if not isinstance(batch, gx.datasource.fluent.interfaces.Batch):
        raise TypeError("batch must be a great expectation batch object.")
    
    # Test 2: Ensure the col_range is a dict, if not raise the error
    if not isinstance(col_range, dict):
        raise TypeError("col_range must be a dict.")
    
    # Test 3: Eunsure the type of col_range's keys is string, if not raise the error
    for key in col_range:
            if not isinstance(key, str):
                raise TypeError("col_range keys must be strings.")
            
    # Test 4: Ensure the type of col_range is a list, if not raise the error
    for value in col_range.values():
        if not isinstance(value, list):
            raise TypeError("col_range must be a list.")
    
    # Test 5: Ensure the col_range's value(list) has four values, if not raise the error
    for value in col_range.values():
        if len(value) != 4:
            raise ValueError("Each col_range value list must contain exactly four items.")

    # Test 6: Ensure the first item of col_range's value is numeric, if not raise the error
    for value in col_range.values():
        if value[0] is not None and not isinstance(value[0], (int, float)):
            raise TypeError("The first item in col_range value must be a numeric value or None (min_value).")

    # Test 7: Ensure the second item of col_range's value is numeric, if not raise the error
    for value in col_range.values():
        if value[1] is not None and not isinstance(value[1], (int, float)):
            raise TypeError("The second item in col_range value must be a numeric value or None (max_value).")

    # Test 8: Ensure the third item of col_range's value is boolean, if not raise the error
    for value in col_range.values():
        if not isinstance(value[2], bool):
            raise TypeError("The third item in col_range value must be a boolean value (strict_min).")

    # Test 9: Ensure the fourth item of col_range's value is boolean, if not raise the error
    for value in col_range.values():
        if not isinstance(value[3], bool):
            raise TypeError("The fourth item in col_range value must be a boolean value (strict_max).")
        
    for i in col_range:
        expectation = gx.expectations.ExpectColumnValuesToNotBeNull(
            column=i, 
            min_value=col_range[i][0], max_value=col_range[i][1], 
            strict_min=col_range[i][2], strict_max=col_range[i][3]
        )
        validation_result = batch.validate(expectation)
        # Test if this expectation passed, if not throw an error
        check_validation_result(validation_result)


