import requests
from bs4 import BeautifulSoup


def get_url_content(url: str) -> BeautifulSoup:
    """
    Function to create a beautiful soup object from a URL.

    Parameters
    ----------
    url: str
        The url of the website, as a string

    Returns
    -------
    soup: bs4.BeautifulSoup
        A beautiful soup object with the parsed URL
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    return soup
