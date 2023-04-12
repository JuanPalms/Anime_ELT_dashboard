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

# Load config file calling load_config function
config_f = ou.load_config("config.yaml")

# Relative paths to root and current dir
CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT)

# Main data files
PRINCIPAL = os.path.join(ROOT, config_f['data']['raw']['principal'])
SECONDARY = os.path.join(ROOT, config_f['data']['raw']['secondary'])

# Module functions
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


def _df_construction(top_anime: pd.DataFrame, start, window) -> pd.DataFrame:
    urls = top_anime['url'].tolist()
    
    # Global object to store scrapper output
    temp_ = np.empty(shape=(0,5))

    for index in range(start, start+window):
        print(f"Processing URL {index+1} of {len(urls)}: {(urls[index])}")
        
        # Convert url output to ndarray
        array = _process_url((urls[index])).to_numpy()

        # Store url output in global object
        array = np.insert(
            arr=array
            ,obj=0
            ,values=index).reshape((1,5))
        
        # Dismiss None anime
        if array is not None:
            temp_ = np.append(
                arr=temp_
                ,values=array
                ,axis=0)
    
    # Format global objet to dataframe
    temp_ = (
        pd.DataFrame(
            temp_
            ,columns=['id','studio', 'themes', 'genres', 'demographics'])
        .set_index('id')
    )

    return temp_


if __name__ == '__main__':

    # Get web scrapper start point
    start = _get_last_anime(SECONDARY)
    
    # Define web scrapper query window
    window = 5

    # Get dataframe with all existing anime
    top_anime = pd.read_csv(PRINCIPAL)
    
    # Mask anime df with scrapper window
    top_mask_ = (
        top_anime
        .loc[range(start, start+window)]
    )
    
    # Build scrapper output
    df_ = _df_construction(
        top_anime=top_anime
        ,start=start
        ,window=window)
    
    # Add scrapper output to existing data
    top_mask_ = top_mask_.join(df_)

    # Save output to existing file
    top_mask_.to_csv(
        SECONDARY
        ,index=False
        ,mode='a'
        ,header=False)
    
    print('Job done')


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