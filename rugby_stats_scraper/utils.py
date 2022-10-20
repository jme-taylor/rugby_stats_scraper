import os

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas.errors import EmptyDataError


def get_request_response(url: str, headers: dict) -> requests.Response:
    """Gets a response from an API, given a url and headers

    Parameters
    ----------
    url : str
        The URL to get the request response from.
    headers : dict
        The authentication headers for the response.

    Returns
    -------
    requests.Response
        The response from the request - in requests.Response format
    """
    response = requests.get(url, headers)
    return response


def load_espn_headers() -> dict:
    """Loads ESPN API headers from .env file

    Returns
    -------
    espn_headers: dict
        A dict containing the headers to access the ESPN API
    """
    load_dotenv()
    espn_headers = {
        'authority': os.getenv('AUTHORITY'),
        'accept': os.getenv('ACCEPT'),
        'accept-language': os.getenv('ACCEPT-LANGUAGE'),
        'origin': os.getenv('ORIGIN'),
        'referer': os.getenv('REFERER'),
        'sec-ch-ua': os.getenv('SEC-CH-UA'),
        'sec-ch-ua-mobile': os.getenv('SEC-CH-UA-MOBILE'),
        'sec-ch-ua-platform': os.getenv('SEC-CH-UA-PLATFORM'),
        'sec-fetch-dest': os.getenv('SEC-FETCH-DEST'),
        'sec-fetch-mode': os.getenv('SEC-FETCH-MODE'),
        'sec-fetch-site': os.getenv('SEC-FETCH-SITE'),
        'user-agent': os.getenv('USER-AGENT'),
    }
    return espn_headers


def get_json_element(json: dict, path: tuple) -> str:
    """Function to safely get a value from a nested JSON. Returns a None value
    if the path doesn't exist.

    Parameters
    ----------
    json : dict
        The json for which you want to extract the value from.
    path : tuple
         A tuple containing each element of the path, with the first element of
        the tuple being the outermost, and the last value being the innermost.

    Returns
    -------
    value : str
        A string with the value from the nested path - None if this doesn't
        exist.
    """
    value = json
    for p in path:
        try:
            value = value[p]
        except (KeyError, TypeError):
            value = None
    return value


def check_file_has_data(filepath: str) -> bool:
    """Checks that a CSV of existing data exists and is populated.

    Paramaters
    ----------
    filepath: str
        The filepath of the CSV file.

    Returns
    -------
    bool
        Boolean flag indicating if the file exists and has data.
    """
    file_exists = os.path.exists(filepath)
    if file_exists:
        try:
            df = pd.read_csv(filepath)
            file_empty = not df.empty
        except EmptyDataError:
            file_empty = False
    else:
        file_empty = False
    return file_exists and file_empty
