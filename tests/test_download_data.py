import pytest
import os
from click.testing import CliRunner
from unittest.mock import patch
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.download_data import main

# Test files setup
url_txt_csv_zip = 'https://github.com/ttimbers/breast_cancer_predictor_py/raw/main/tests/files_txt_csv.zip'

# URL for empty zip file case
url_empty_zip = 'https://github.com/ttimbers/breast_cancer_predictor_py/raw/main/tests/empty.zip'

# Tests

# test download_data function throws an error if the url does not exist 
# at the input URL is empty
@patch('requests.get')
def test_download_data_error_on_invalid_url(mock_get):
    mock_get.return_value.status_code = 404  # Simulate a 404 response
    runner = CliRunner()

    with pytest.raises(ValueError, match='The URL provided does not exist.'):
        result = runner.invoke(main, ['--url', 'https://example.com/non_existing.zip', '--write-to', 'tests/test_zip_data'], 
                               catch_exceptions=False) # `catch_exceptions=False` to allow pytest to catch the exception


# test download_data function throws an error if the URL is not a zip file
def test_download_data_error_on_nonzip_url():
    runner = CliRunner()

    with pytest.raises(ValueError, match="The URL provided does not point to a zip file."):
        result = runner.invoke(main, ['--url', 'https://github.com/', '--write-to', 'tests/test_zip_data'], 
                               catch_exceptions=False)
