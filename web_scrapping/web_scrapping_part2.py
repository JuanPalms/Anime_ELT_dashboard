"""
Web scrapper module: 
This python module implements a web scrapper for the scondary pages of My anime list.
With this web scrapper you get information for each anime that has been rated on the my anime list secondary pages.
It takes as an input the raw_anime_principal_page.csv data in the data/raw folder.
The results are stored in a csv in the raw data folder.
This module only obtains data web scrapping the page, further processing is needed in other python modules.
"""
import pandas as pd
import numpy as np
import os
import outils as ou

import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import numpy as np
import os
import time

CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT)




# Load config file calling load_config function
config_f = ou.load_config("config.yaml")



def _get_studio_themes_genres_demographics(url: str) -> str:
    try:
        soup = ou.fetch_html(url)
        div_elements = soup.find_all('div', class_="spaceit_pad")

        studio = None
        themes_str = None
        genres_str = None
        demos_str = None

        for element in div_elements:
            try:
                if element.span.text == "Studios:":
                    studio = element.a.text
                elif element.span.text == "Theme:" or element.span.text == "Themes:":
                    themes = [a.text for a in element.find_all('a')]
                    themes_str = ', '.join(themes)
                elif element.span.text == "Genre:" or element.span.text == "Genres:":
                    genres = [a.text for a in element.find_all('a')]
                    genres_str = ', '.join(genres)
                elif element.span.text == "Demographic:" or element.span.text == "Demographics:":
                    demos = [a.text for a in element.find_all('a')]
                    demos_str = ', '.join(demos)
            except:
                pass

        return studio, themes_str, genres_str, demos_str
    except AttributeError:
        print(f"Error processing URL: {url}")
        return None, None, None, None

def _process_url(url: str) -> str:
    delay = 0  # Add your desired delay in seconds here
    time.sleep(delay)
    return pd.Series(_get_studio_themes_genres_demographics(url))

def _get_last_anime(file_path):
    last_anime = (
    pd.read_csv(file_path)
    .filter(items=['ranking'])
    .max()
    .values[0])
    return last_anime

def _df_construction(top_anime: pd.DataFrame, k) -> pd.DataFrame:
    urls = top_anime['url'].tolist()
    total_urls = len(urls)
    results = []
    temporal = pd.DataFrame(columns=['k','studio', 'themes', 'genres', 'demographics'])
    for index in range(k,k+5):
        print(f"Processing URL {index+1} of {total_urls}: {(urls[index])}")
        array = _process_url((urls[index])).to_numpy()
        print(temporal)
        # results.append(_process_url((urls[index])))
        # temporal.loc[index,'studio']= results[0]
        # temporal.loc[index,'themes']= results[1]
        # temporal.loc[index,'genres']= results[2]
        # temporal.loc[index,'demographics']= results[3]
    #print(temporal)
    #return temporal
    


def fetch_data_per_anime ():
    k=_get_last_anime(os.path.join(ROOT, config_f['data']['raw']['secondary']))
    top_anime = pd.read_csv(os.path.join(ROOT, config_f['data']['raw']['principal']))
    top_anime = _df_construction(top_anime=top_anime, k=k)
#     top_anime.to_csv(os.path.join(ROOT, config_f['data']['raw']['secondary']),index=False, mode='a',header=False)
    
    
fetch_data_per_anime()   
# def _df_construction(top_anime: pd.DataFrame) -> pd.DataFrame:
#     """
#     Creates a Dataframe with already existing columns of anime_principal_page.csv.
    
#     Args:
#     top_anime: The functions expects a pd.DataFrame of anime_principal_page.csv
    
#     Returns:
#     top_anime: A brand new pd.DataFrame consisting of columns already in anime_principal_page.csv 
#     but it adds:'studio', 'themes', 'genres', 'demographics' to it.
    
#     """
#     urls = top_anime['url'].tolist()
#     results = []
#     total_urls = len(urls)
#     for index, url in enumerate(urls):
#         if index%80==0:
#             print(f"Processing URL {index+1} of {total_urls}: {url}")
#             results.append(_process_url(url))
#             print(results[-1])
#             time.sleep(160)
#         else:
#             print(f"Processing URL {index+1} of {total_urls}: {url}")
#             results.append(_process_url(url))
#             print(results[-1])
#     top_anime[['studio', 'themes', 'genres', 'demographics']] = pd.DataFrame(results)
#     return top_anime
    
    # def fetch_data_per_anime() -> None:
    #     """
    #     Pipeline for creating anime_principal_and_secondary_pages.csv
        
    #     Args:

        
    #     Returns:
        
    #     """
    #     top_anime = pd.read_csv(ou.PARENT_PATH+"/data/raw/anime_principal_page.csv")
    #     top_anime = _df_construction(top_anime=top_anime)
    #     top_anime.to_csv(ou.PARENT_PATH+"/data/raw/anime_principal_and_secondary_pages.csv",index=False, mode='append')
        
    # fetch_data_per_anime()

# df.to_csv(mode='append')
