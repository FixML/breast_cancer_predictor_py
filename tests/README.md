## How to run the test suite

### Preparation of test zip files
The test zip files used in `test_read_zip.py` were genereated 
by running the `generate_test_zip_files.py` script in the `tests` directory.
These files need to exist in the remote GitHub repository for the tests to pass.
If for some reason they go missing from the remote repository,
we can re-run the `generate_test_zip_files.py` script to re-generate them
and then push them to the remote repository.