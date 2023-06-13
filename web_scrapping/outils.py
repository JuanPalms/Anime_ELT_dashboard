# anime_scraper.py

import requests
from bs4 import BeautifulSoup
import configparser
import pylint

# Load configuration from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the base URL and target page from the configuration
base_url = config.get('website', 'base_url')
target_page = config.get('website', 'target_page')

def scrape_anime_list():
    # Construct the full URL
    url = base_url + target_page

    # Send an HTTP GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the anime list elements
        anime_list = soup.find_all('div', class_='anime')

        # Extract information from each anime element
        for anime in anime_list:
            title = anime.find('h2').text.strip()
            rating = anime.find('span', class_='rating').text.strip()
            episodes = anime.find('span', class_='episodes').text.strip()

            # Print the extracted information
            print(f"Title: {title}")
            print(f"Rating: {rating}")
            print(f"Episodes: {episodes}")
            print()

    else:
        print(f"Error: Failed to retrieve the web page. Status code: {response.status_code}")

def main():
    scrape_anime_list()

if __name__ == '__main__':
    main()
##To use this module, you would need to create a config.ini file in the same directory as the anime_scraper.py file, with the following content:

[website]
base_url = <website_base_url>
target_page = <target_page_url>

Replace <website_base_url> with the base URL of the anime website you want to scrape, and <target_page_url> with the specific page containing the anime list.

To run the module, execute python anime_scraper.py in the command line.

Make sure you have the required libraries (requests, beautifulsoup4, configparser, and pylint) installed before running the code.
