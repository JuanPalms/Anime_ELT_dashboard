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

try:
    current = pd.read_csv(ws.SECONDARY)
    current_rows = len(current)
    missing_rows =13900-current_rows
    iterations = missing_rows//5
    ws.fetch_data_per_anime(iterations)
except:
    iterations = 3000
    top_anime = pd.read_csv(ws.PRINCIPAL)
    top_mask_ = top_anime.loc[range(0, 5)]
    secondary = ws._df_construction(top_anime=top_anime,start=0,window=5)
    secondary = top_mask_.join(secondary)
    secondary.to_csv(ws.SECONDARY, index=False)

ws.fetch_data_per_anime(3000) 

#ws._clean_raw_data()