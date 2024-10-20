# clean_validate.py
# author: Weilin Han
# date: 2024-10-03

import numpy as np
import pandas as pd
import re
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
    >>> exp_col_not_null(batch, col_type)
    """
    for i in col_percent:
        expectation = gx.expectations.ExpectColumnValuesToNotBeNull(
            column=i, mostly=1-col_percent[i]
        )
        validation_result = batch.validate(expectation)
        # Test if this expectation passed, if not throw an error
        check_validation_result(validation_result)


def exp_value_range(batch, col_range):
    """
    Validates that the numeric values of specified columns are within specific range.
    
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
    for i in col_range:
        expectation = gx.expectations.ExpectColumnValuesToNotBeNull(
            column=i, 
            min_value=col_range[i][0], max_value=col_range[i][1], 
            strict_min=col_range[i][2], strict_max=col_range[i][3]
        )
        validation_result = batch.validate(expectation)
        # Test if this expectation passed, if not throw an error
        check_validation_result(validation_result)


