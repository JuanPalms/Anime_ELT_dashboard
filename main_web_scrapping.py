import pandas as pd
import os

# Local imports
import source_web_scrapping as ws
import utils as ut

# config file loading
config_f = ut.load_config("config.yaml")

# needed variables
base = config_f["url"]
limit = config_f["results_limit"]

# first part of web scrapping
#ws.fetch_ranking(url=base, results_limit=13900)

# second part of web scrapping
#ws.fetch_data_per_anime(2000)

# 
ws._clean_raw_data()