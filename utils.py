import os
import yaml
import logging
import requests

from ast import literal_eval

CURRENT = os.path.dirname(os.path.abspath(__file__))


# Function to load yaml configuration file
def load_config(config_name):
    """
    Sets the configuration file path
    Args:
    config_name: Name of the configuration file in the directory
    Returns:
    Configuration file
    """
    with open(os.path.join(CURRENT, config_name), encoding="utf-8") as conf:
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
    x = re.sub(pattern=r"[°.-]+", repl='_', string=x)
    x = re.sub(pattern="'s", repl='', string=x)
    return x

# lambda function to format single string data in cell
format_single_str = lambda cel_: '_'.join(
    cel_.rstrip().lstrip().split(sep=' ')
).lower()

# lambda function to format list like data in cell
format_list_str = lambda cel_: [
    global_format(
        '_'.join(val_.split(' ')).lower()
    ) for val_ in literal_eval(cel_)
]