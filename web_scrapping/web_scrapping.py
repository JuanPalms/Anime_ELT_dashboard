"""
Web scrapper module: 
This python module implements a web scrapper for the main page of My anime list.
With this web scrapper you get information for each anime that has been rated on the my anime list top anime page.
The results are stored in a csv in the raw data folder.
"""
import pandas as pd
import numpy as np
import os
from outils import load_config, fetch_html

def web_scrapper_principal(url,parser='lxml'):
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
        soup = fetch_html(url,parser)
        # Empty lists to store each element in the anime list main page
        rankings = []
        scores = []
        titles = []
        number_episodes_list = []
        emission_dates = []
        members_list = []
        urls = []
        # Retrieves each element in a single anime that appears in the main page of top anime
        for anime_element in soup.find_all('tr', class_='ranking-list'):
            span_elements = anime_element.find_all('span')
            ranking = span_elements[0].text
            score = span_elements[1].text
            title = anime_element.find('div',class_="di-ib clearfix").a.text
            number_episodes = anime_element.find('div',class_="information di-ib mt4").text.split('\n')[1].strip()
            emission_date = anime_element.find('div',class_="information di-ib mt4").text.split('\n')[2].strip()
            members = anime_element.find('div', class_="information di-ib mt4").text.split('\n')[3].strip()
            url= anime_element.find('div', class_="di-ib clearfix").a['href']
            # Add the elements to the list
            rankings.append(ranking)
            scores.append(score)
            titles.append(title)
            number_episodes_list.append(number_episodes)
            emission_dates.append(emission_date)
            members_list.append(members)
            urls.append(url)

        data = {
            'ranking': rankings,
            'score': scores,
            'title': titles,
            'number_of_episodes': number_episodes_list,
            'emission_date': emission_dates,
            'number_members': members_list,
            'url': urls
        }

        return pd.DataFrame(data)
    except AttributeError:
        print(f"Error processing URL: {url}")
        return pd.DataFrame()


lista_urls = ['https://myanimelist.net/topanime.php']

#for i in range(50, 13850, 50):
 #   base = "https://myanimelist.net/topanime.php?limit="
  #  lista_urls.append(base + str(i))

# Loop through the list of URLs and process each URL, then concatenate the resulting DataFrames
dataframes = [web_scrapper_principal(url) for url in lista_urls]
combined_df = pd.concat(dataframes, ignore_index=True)
combined_df.to_csv('prueba_pipeline.csv',index=False)