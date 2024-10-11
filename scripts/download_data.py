# download_data.py
# author: Tiffany Timbers
# date: 2023-11-27

import click
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_zip import read_zip

@click.command()
@click.option('--url', type=str, help="URL of dataset to be downloaded")
@click.option('--write-to', type=str, help="Path to directory where raw data will be written to")

def main(url, write_to):
    """Downloads data zip data from the web to a local filepath and extracts it."""
    
    request = requests.get(url)
    filename_from_url = os.path.basename(url)

    try:
        read_zip(url, write_to)
    except FileNotFoundError as e:
        if e.args == 'The directory provided does not exist.':
            os.makedirs(write_to)
            read_zip(url, write_to)
        else:
            raise e

if __name__ == '__main__':
    main()
