import requests


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
