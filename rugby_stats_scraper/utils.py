import os
from typing import Union

import pandas as pd
from pandas.errors import EmptyDataError


def get_json_element(json: dict, path: tuple) -> Union[str, dict, None]:
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
    value : Union[str, dict, None]
        Depending on the path provided, one of three things will be returned;
        if the path leads to a single value, the string of this value will be
        returned; if the path leads to another dictionary, this dictionary
        will be returned; if the path isn't valid, a none type will be
        returned.
    """
    value = json
    for p in path:
        try:
            value = value[p]
        except (KeyError, TypeError):
            return None
    return value


def check_file_has_data(filepath: str) -> bool:
    """Checks that a CSV of existing data exists and is populated.

    Parameters
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
