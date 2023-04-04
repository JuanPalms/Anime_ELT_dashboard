"""
This python module defines some useful functions to perform web scrapping
"""
import os
import yaml
import logging
import requests
from bs4 import BeautifulSoup

# folder to load config file
CONFIG_PATH = "../"

# Function to load yaml configuration file
def load_config(config_name):
    """
    Sets the configuration file path
    Args:
    config_name: Name of the configuration file in the directory
    Returns:
    Configuration file
    """
    with open(os.path.join(CONFIG_PATH, config_name), encoding="utf-8") as conf:
        config = yaml.safe_load(conf)
    return config

def fetch_html(url,parser='lxml'):
    """
    This function obtains the information of an url and parses it with some parser
    Args: 
    url: page url to be scrapped
    parser: select 'html.parser' or 'lxml'
    Returns:
    BeautifulSoup object
    """
    response = requests.get(url)  # Send an HTTP GET request to the URL
    if response.status_code == 200:  # Check if the request was successful (status code 200)
        # Parse the response content with BeautifulSoup and return the parsed HTML
        return BeautifulSoup(response.content, parser)
    else:
        return None
