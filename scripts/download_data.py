# download_data.py
# author: Tiffany Timbers
# date: 2023-11-27

import click
import os
import sys
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_zip import read_zip

@click.command()
@click.option('--url', type=str, help="URL of dataset to be downloaded")
@click.option('--write-to', type=str, help="Path to directory where raw data will be written to")

def main(url, write_to):
    """Downloads data zip data from the web to a local filepath and extracts it."""
    
    request = requests.get(url)
    filename_from_url = os.path.basename(url)

    # check if URL exists, if not raise an error
    if request.status_code != 200:
        raise ValueError('The URL provided does not exist.')
    
    # check if the URL points to a zip file, if not raise an error  
    #if request.headers['content-type'] != 'application/zip':
    if filename_from_url[-4:] != '.zip':
        raise ValueError('The URL provided does not point to a zip file.')

    try:
        read_zip(url, write_to)
    except:
        os.makedirs(write_to)
        read_zip(url, write_to)

if __name__ == '__main__':
    main()
