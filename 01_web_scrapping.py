import pandas as pd
import os

# Local imports
import src.web_scrapping as ws

# config file loading
config_f = ws.config_f

# needed variables
base = config_f["url"]
limit = config_f["results_limit"]

# first part of web scrapping
#ws.fetch_ranking(url=base, results_limit=13900)

# second part of web scrapping
ws.fetch_data_per_anime(2000)

ws._clean_raw_data()