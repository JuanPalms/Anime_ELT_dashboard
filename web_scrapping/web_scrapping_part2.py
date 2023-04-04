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
from outils import load_config, fetch_html
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import numpy as np
import os
import time
from outils import load_config, fetch_html

# Load config file calling load_config function
config_f = load_config("config.yaml")

def get_studio_themes_genres_demographics(url):
    try:
        soup = fetch_html(url)
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

def process_url(url):
    delay = 4  # Add your desired delay in seconds here
    time.sleep(delay)
    return pd.Series(get_studio_themes_genres_demographics(url))

top_anime = pd.read_csv(os.path.join(config_f["data_directory"]+config_f["raw_data"],"raw_anime_principal_page.csv"))
top_anime = top_anime[101:3000]

urls = top_anime['url'].tolist()

results = []

total_urls = len(urls)

for index, url in enumerate(urls):
    print(f"Processing URL {index+1} of {total_urls}: {url}")
    results.append(process_url(url))
    print(results[-1])

top_anime[['studio', 'themes', 'genres', 'demographics']] = pd.DataFrame(results)

top_anime.to_csv(os.path.join(config_f["data_directory"]+config_f["raw_data"],"raw_anime_principal_and_secondary_pages.csv"),index=False)