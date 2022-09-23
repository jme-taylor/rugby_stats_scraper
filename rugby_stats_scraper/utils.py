import os

import requests
from dotenv import load_dotenv


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


def get_json_element(json: dict, json_path: list) -> str:
    """A function to get a JSON element, given an expected path. Will return a
    None value if the path doesn't exist, rather than a KeyError.

    Parameters
    ----------
    json : dict
        The JSON in which the value is expected to be in.
    json_path : list
        The JSON path, in a list format, with the outer layer first, and
        innnermost last.

    Returns
    -------
    value : str
        The string with the value in it, None if this didn't exist.
    """
    total_values = len(json_path)
    for num, path_element in enumerate(json_path):
        if total_values == 1:
            value = json.get(path_element, None)
        elif num + 1 < total_values:
            value = json.get(path_element, {})
        else:
            value = value.get(path_element, None)
    return value
