import os
import zipfile
import requests

def read_zip(url, directory):
    """
    Read a zip file from the given URL and extract its contents to the specified directory.

    Parameters:
    ----------
    url : str
        The URL of the zip file to be read.
    directory : str
        The directory where the contents of the zip file will be extracted.

    Returns:
    -------
    None
    """
    request = requests.get(url)
    filename_from_url = os.path.basename(url)

    # check if URL exists, if not raise an error
    if request.status_code != 200:
        raise ValueError('The URL provided does not exist.')
    
    # check if the URL points to a zip file, if not raise an error  
    if request.headers['content-type'] != 'application/zip':
        raise ValueError('The URL provided does not point to a zip file.')
    
    # check if the directory exists, if not raise an error
    if not os.path.isdir(directory):
        raise ValueError('The directory provided does not exist.')

    # write the zip file to the directory
    path_to_zip_file = os.path.join(directory, filename_from_url)
    with open(path_to_zip_file, 'wb') as f:
        f.write(request.content)

    # get list of files/directories in the directory
    original_files = os.listdir(directory)

    # extract the zip file to the directory
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory)

    # check if any files were extracted, if not raise an error
    # get list of files/directories in the directory
    current_files = os.listdir(directory)
    if len(current_files) == len(original_files):
        raise ValueError('The ZIP file is empty.')
