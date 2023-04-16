# base python imports
import requests
import time
import os

# external imports
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# local imports
from .utils import load_config, ROOT

# Load config file calling load_config function
config_f = load_config("config.yaml")

PRINCIPAL = os.path.join(ROOT, config_f["data"]["raw"]["principal"])
SECONDARY = os.path.join(ROOT, config_f["data"]["raw"]["secondary"])
PRE_CLEAN = os.path.join(ROOT, config_f["data"]["clean"]["pre_clean"])
CLEAN = os.path.join(ROOT, config_f["data"]["clean"]["clean"])


# ==================================================
# ========= Scrapper First Part ====================
# ==================================================


def _fetch_html(url, parser="lxml"):
    """
    This function obtains the information of an url and parses it with some parser
    Args:
    url: page url to be scrapped
    parser: select 'html.parser' or 'lxml'
    Returns:
    BeautifulSoup object
    """
    response = requests.get(url)  # Send an HTTP GET request to the URL
    if (
        response.status_code == 200
    ):  # Check if the request was successful (status code 200)
        # Parse the response content with BeautifulSoup and return the parsed HTML
        return BeautifulSoup(response.content, parser)
    else:
        return None


def _web_scrapper_principal(url, parser="lxml"):
    """
    Scrapps on a url of the main page of My animelist top animes.
    Find the element "div, class=Ranking-list" which is where each anime is stored on the page.
    It stores each item found for each anime within the url in a list for each item.
    It creates a pandas dataframe with the stored lists.

    Args:
    url: receive a url from myanimelist homepage
    parser: select 'html.parser' or 'lxml'. Default = 'lxml'
    """
    try:
        # Creates sopu object
        soup = _fetch_html(url, parser)
        # Empty lists to store each element in the anime list main page
        rankings = []
        scores = []
        titles = []
        number_episodes_list = []
        emission_dates = []
        members_list = []
        urls = []
        # Retrieves each element in a single anime that appears in the main page of top anime
        for anime_element in soup.find_all("tr", class_="ranking-list"):
            span_elements = anime_element.find_all("span")
            ranking = span_elements[0].text
            score = span_elements[1].text
            title = anime_element.find("div", class_="di-ib clearfix").a.text
            number_episodes = (
                anime_element.find("div", class_="information di-ib mt4")
                .text.split("\n")[1]
                .strip()
            )
            emission_date = (
                anime_element.find("div", class_="information di-ib mt4")
                .text.split("\n")[2]
                .strip()
            )
            members = (
                anime_element.find("div", class_="information di-ib mt4")
                .text.split("\n")[3]
                .strip()
            )
            url = anime_element.find("div", class_="di-ib clearfix").a["href"]
            # Add the elements to the list
            rankings.append(ranking)
            scores.append(score)
            titles.append(title)
            number_episodes_list.append(number_episodes)
            emission_dates.append(emission_date)
            members_list.append(members)
            urls.append(url)

        data = {
            "ranking": rankings,
            "score": scores,
            "title": titles,
            "number_of_episodes": number_episodes_list,
            "emission_date": emission_dates,
            "number_members": members_list,
            "url": urls,
        }

        return pd.DataFrame(data)
    except AttributeError:
        print(f"Error processing URL: {url}")
        return pd.DataFrame()


def fetch_ranking(url, results_limit):
    base = url
    lista_urls = [base]
    ## iterates over 13850 elements in 300 pages
    for i in range(50, results_limit, 50):
        lista_urls.append(base + "?limit=" + str(i))

    # Initialize an empty list to store the DataFrames
    dataframes = []

    # Loop through the list of URLs and process each URL, then append the resulting DataFrame to the list
    checkpoints = [50, 100, 150, 200, 240]
    for pages, url in enumerate(lista_urls):
        if pages in checkpoints:
            dataframes.append(_web_scrapper_principal(url))
            # Sleeps for 2 minutes
            print(dataframes[-1])
            time.sleep(200)
        else:
            dataframes.append(_web_scrapper_principal(url))
            print(dataframes[-1])
            time.sleep(5)

    # Concatenate the list of DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    # DF exported to csv
    combined_df.to_csv(ROOT + "/data/raw/anime_principal_page.csv", index=False)


# ==================================================
# ========= Scrapper Second Part ===================
# ==================================================


def _get_studio_themes_genres_demographics(url: str) -> str:
    try:
        soup = _fetch_html(url)
        div_elements = soup.find_all("div", class_="spaceit_pad")
        studio = None
        themes_str = None
        genres_str = None
        demos_str = None

        for element in div_elements:
            try:
                if element.span.text == "Studios:":
                    studio = element.a.text
                elif element.span.text == "Theme:" or element.span.text == "Themes:":
                    themes = [a.text for a in element.find_all("a")]
                    themes_str = ", ".join(themes)
                elif element.span.text == "Genre:" or element.span.text == "Genres:":
                    genres = [a.text for a in element.find_all("a")]
                    genres_str = ", ".join(genres)
                elif (
                    element.span.text == "Demographic:"
                    or element.span.text == "Demographics:"
                ):
                    demos = [a.text for a in element.find_all("a")]
                    demos_str = ", ".join(demos)
            except:
                pass

        return studio, themes_str, genres_str, demos_str
    except AttributeError:
        print(f"Error processing URL: {url}")
        return None, None, None, None


def _process_url(url: str) -> str:
    delay = 1  # Add your desired delay in seconds here
    time.sleep(delay)
    return pd.Series(_get_studio_themes_genres_demographics(url))


def _get_last_anime(file_path):
    last_anime = pd.read_csv(file_path).filter(items=["ranking"]).max().values[0]
    return last_anime


def _df_construction(top_anime: pd.DataFrame, start, window) -> pd.DataFrame:
    urls = top_anime["url"].tolist()

    # Global object to store scrapper output
    temp_ = np.empty(shape=(0, 5))

    for index in range(start, start + window):
        print(f"Processing URL {index+1} of {len(urls)}: {(urls[index])}")

        # Convert url output to ndarray
        array = _process_url((urls[index])).to_numpy()

        # Store url output in global object
        array = np.insert(arr=array, obj=0, values=index).reshape((1, 5))

        # Dismiss None anime
        if array is not None:
            temp_ = np.append(arr=temp_, values=array, axis=0)

    # Format global objet to dataframe
    temp_ = pd.DataFrame(
        temp_, columns=["id", "studio", "themes", "genres", "demographics"]
    ).set_index("id")

    return temp_


def fetch_data_per_anime(iterations):
    for i in range(iterations):
        if i % 15 == 0:
            # Get web scrapper start point
            start = _get_last_anime(SECONDARY)

            # Define web scrapper query window
            window = 5

            # Get dataframe with all existing anime
            top_anime = pd.read_csv(PRINCIPAL)

            # Mask anime df with scrapper window
            top_mask_ = top_anime.loc[range(start, start + window)]

            # Build scrapper output
            df_ = _df_construction(top_anime=top_anime, start=start, window=window)

            # Add scrapper output to existing data
            top_mask_ = top_mask_.join(df_)

            # Save output to existing file
            top_mask_.to_csv(SECONDARY, index=False, mode="a", header=False)
            time.sleep(210)
            print("Job 1 done")
        else:
            # Get web scrapper start point
            start = _get_last_anime(SECONDARY)

            # Define web scrapper query window
            window = 5

            # Get dataframe with all existing anime
            top_anime = pd.read_csv(PRINCIPAL)

            # Mask anime df with scrapper window
            top_mask_ = top_anime.loc[range(start, start + window)]

            # Build scrapper output
            df_ = _df_construction(top_anime=top_anime, start=start, window=window)

            # Add scrapper output to existing data
            top_mask_ = top_mask_.join(df_)

            # Save output to existing file
            top_mask_.to_csv(SECONDARY, index=False, mode="a", header=False)

            print("Job 2 done")


# ==================================================
# ========== transform - Juan P ====================
# ==================================================

# Load config file calling load_config function

def _clean_raw_data():
    top_anime = pd.read_csv(SECONDARY)
    top_anime = (
        top_anime
            .assign(
                type_of_emission = lambda df_: df_['number_of_episodes'].str.extract(r'(\D+)'),
                emission_type = lambda df_: df_['type_of_emission'].str.replace('(', '', regex=True),
                number_episode = lambda df_: df_['number_of_episodes'].str.extract(r'(\d+)'),
                miembros = lambda df_: df_['number_members'].str.replace('members', '', regex=True),
                members = lambda df_: df_['miembros'].str.replace(',', '', regex=True)
            #end assign
            )
            .drop(columns= ['number_of_episodes','type_of_emission','miembros','number_members'])
        #end preprocessing
        )

    # Split the 'emission_date' column into two new columns using the ' - ' delimiter
    split_columns = top_anime['emission_date'].str.split(' - ', expand=True)

    top_anime = (
        top_anime
            .assign(
                # Assign the new columns to the original DataFrame with the desired names
                first_emission = split_columns[0],
                last_emission  = split_columns[1],
                #ist_emission = lambda df_:df_['first_emission_y'].to_datetime(format='%b %Y')
                #df['last_emission'] = pd.to_datetime(df['last_emission'], format='%b %Y')
            ))

    top_anime['first_emission'] = pd.to_datetime(top_anime['first_emission'], format='%b %Y', errors='coerce')
    top_anime['last_emission'] = pd.to_datetime(top_anime['last_emission'], format='%b %Y', errors='coerce')

    # Split the strings in 'themes' and 'genres' columns into lists
    top_anime['themes'] = top_anime['themes'].fillna('Not_available').apply(lambda x: x.split(', ') if x else [])
    top_anime['genres'] = top_anime['genres'].fillna('Not_available').apply(lambda x: x.split(', ') if x else [])

    # Perform one-hot encoding for 'themes' and 'genres'
    themes_dummies = pd.get_dummies(top_anime['themes'].apply(pd.Series).stack()).sum(level=0)
    genres_dummies = pd.get_dummies(top_anime['genres'].apply(pd.Series).stack()).sum(level=0)

    # Concatenate the one-hot encoded columns with the original DataFrame
    result_df = pd.concat([top_anime, themes_dummies, genres_dummies], axis=1)
    print(result_df.head())

    result_df.to_csv(PRE_CLEAN, index=False)


# ==================================================
# ============ transform - Miguel C ================
# ==================================================


def build_catalog(df_, columns, count=True):
    '''
    Generate catalog of unique classes in column
    for given dataframe

    Params:
        df_: Dataframe
        columns: Columns to extract classes
        count: Whether to return value counts or not

    Returns:
        catalogs: List of dictionaries, length = len(columns)
        containing unique classes per column in dataframe
    '''
    # Generate list of catalogs to compute
    catalogs = [{col_:None} for col_ in columns]
    
    # Populate all catalogs
    for id_, col_ in enumerate(columns):
        
        # Empty list of tokens in catalog
        tokens = []
        
        # Append all existing tokens in column
        for val_ in df_[col_]:
            tokens += val_
        
        # Assign unique tokens in list to catalog
        if count:
            catalogs[id_][col_] = (
                # Convert tokens list to pandas series
                pd.Series(tokens)
                # Extract series value counts
                .value_counts()
                # Reset index to store tokens as dataframe
                .reset_index()
                # Rename columns with convenient names
                .rename(columns={'index':col_, 0:'count'})
                # Sort tokens alphabetically
                .sort_values(by=col_)
                # Reset dataframe index
                .reset_index(drop=True))
        else:
            catalogs[id_][col_] = (
                # Convert array to dataframe for manipulation
                pd.DataFrame(
                    # Convert tokens list to pandas series
                    pd.Series(tokens)
                    # Extract series unique values
                    .unique())
                # Rename columns with convenient names
                .rename(columns={0:col_})
                # Sort tokens alphabetically
                .sort_values(by=col_)
                # Reset dataframe index
                .reset_index(drop=True))
    
    return catalogs

if __name__ == '__main__':
    print('Web scrapping module')
