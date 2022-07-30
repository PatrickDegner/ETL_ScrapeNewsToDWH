import requests

from bs4 import BeautifulSoup


# Begin Extraction (Scrape News)
def extract():
    # init
    url = 'https://www.zdf.de/nachrichten'
    response = requests.get(url)
    simple_soup = BeautifulSoup(response.content, 'html.parser')

    # action
    finder_header = simple_soup.find_all(
        'div', class_='news-liveblog-item cell medium-6 large-4 m-clickarea js-impression-track'
    )
    return finder_header
