import os
import yaml
import logging
import requests

from re import sub
from ast import literal_eval

CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT)

# Function to load yaml configuration file
def load_config(config_name):
    """
    Sets the configuration file path
    Args:
    config_name: Name of the configuration file in the directory
    Returns:
    Configuration file
    """
    with open(os.path.join(ROOT, config_name), encoding="utf-8") as conf:
        config = yaml.safe_load(conf)
    return config


def global_format(x):
    '''
    Remove atypical character from given string

    Params:
        x: String to format
    
    Returns:
        x: String without atypical characters
    '''
    x = sub(pattern=r"[°.-]+", repl='_', string=x)
    x = sub(pattern="'s", repl='', string=x)
    return x

# lambda to format single string in dataframe cell
format_single_str = lambda cel_: '_'.join(
    cel_.rstrip().lstrip().split(sep=' ')
).lower()

# lambda to format list like strings in dataframe cell
format_list_str = lambda cel_: [
    '_'.join(
        global_format(val_.rstrip().lstrip())
        .lower()
        .split(' ')
    ) for val_ in cel_.split(',')
]


if __name__ == '__main__':
    print(f'''Utils module paths:
    - CURRENT: {CURRENT}
    - ROOT: {ROOT}''')