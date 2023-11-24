import pytest
import os
import shutil

# Test files setup
# setup empty directory for data files to be downloaded to
if not os.path.exists('test_zip_data1'):
    os.makedirs('test_zip_data1')

# setup directory that contains a file for data files to be downloaded to
if not os.path.exists('test_zip_data2'):
    os.makedirs('test_zip_data2')
with open('test_zip_data2/test3.txt', 'w') as file:
    pass  # The 'pass' statement does nothing, creating an empty file

# test read_zip function can download and extract a zip file containing files 
# and subdirectories containing files
def test_read_zip_function():
    # add tests here


# test read_zip function throws an error if the zip file is empty
def test_read_zip_error_on_empty():
    # add tests here


# test read_zip function throws an error if the input URL is invalid 
# (e.g., points to a non-existent file or a non-zip file)
def test_read_zip_error_on_invalid_url():
    # add tests here


# test read_zip function throws an error 
# if the  directory path provided does not exist
def test_read_zip_error_on_missing_dir():
    # add tests here


# clean up data directory
if os.path.exists("subdir"):
    shutil.rmtree("subdir")

