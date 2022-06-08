import logging
from datetime import datetime, timedelta

import pandas as pd

from rugby_stats_scraper.constants import BASE_URL, SCORES_URL
from rugby_stats_scraper.utils import get_url_content

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_all_matches(soup):
    """
    Function that returns all match links from days page

    Parameters
    ----------
    soup: bs4.BeautifulSoup
        A beautiful soup of a day's rugby matches

    Returns
    -------
    game_links: list
        A list of all of the URLs of parsable match links from that date
    """
    events = soup.find(id='events')
    matches = events.find_all(attrs={'class': 'mobileScoreboardLink'})

    match_links = []

    for match in matches:
        try:
            raw_match_link = match['href']
            match_links.append(BASE_URL + raw_match_link)
        except KeyError:
            continue

    return match_links


def get_attribute_text(soup, attribute):
    """
    Function to get attribute text for a given attribute, whilst doing error
    handling

    Parameters
    ----------
    soup: bs4.BeautifulSoup
        A beautiful soup object
    attribute: str
        An attribute that you're trying to get the text for

    Returns
    -------
    text: str
        The text returned for the specific attribute
    """
    attribute_dict = {
        'competition': 'game-details header',
        'long_name': 'long-name',
        'short_name': 'short-name',
        'abbreviation': 'abbrev',
        'score_home': 'score icon-font-after',
        'score_away': 'score icon-font-before',
    }
    lookup = attribute_dict[attribute]
    try:
        text = soup.find(attrs={'class': lookup}).text
    except AttributeError:
        text = None

    return text


def get_match_information(soup):
    """
    Function to get match information from a match soup object and return them

    Parameters
    ----------
    soup: bs4.BeautifulSoup
        A beautiful soup object of the match URL

    Returns
    -------
    match_information: dict
        A dictionary containing the following information, the competition the
        match was played in, the home teams name and score and the away team's
        name and score
    """
    competition = get_attribute_text(soup, 'competition')
    home_team = soup.find(attrs={'class': 'team team-a'})

    home_team_long_name = get_attribute_text(home_team, 'long_name')
    home_team_short_name = get_attribute_text(home_team, 'short_name')
    home_team_abbrev = get_attribute_text(home_team, 'abbreviation')
    home_team_score = get_attribute_text(home_team, 'score_home')

    away_team = soup.find(attrs={'class': 'team team-b'})

    away_team_long_name = get_attribute_text(away_team, 'long_name')
    away_team_short_name = get_attribute_text(away_team, 'short_name')
    away_team_abbrev = get_attribute_text(away_team, 'abbreviation')
    away_team_score = get_attribute_text(away_team, 'score_away')

    match_information = {
        'competition': competition,
        'home_team_long_name': home_team_long_name,
        'home_team_short_name': home_team_short_name,
        'home_team_abbrev': home_team_abbrev,
        'home_team_score': home_team_score,
        'away_team_long_name': away_team_long_name,
        'away_team_short_name': away_team_short_name,
        'away_team_abbrev': away_team_abbrev,
        'away_team_score': away_team_score,
    }
    return match_information


def get_date_match_information(url):
    """
    Function that takes a date's URL and returns a pandas dataframe containing
    all the days match's information

    Parameters
    ----------
    url: str
        A string of the url of the date

    Returns
    -------
    date_match_information: pd.DataFrame
        A dataframe containing information on all matches that occured that
        date
    """
    url_soup = get_url_content(url)
    matches = get_all_matches(url_soup)

    date_string = url[-8:]
    date = datetime.strptime(date_string, '%Y%m%d')

    matches_information = []
    for match in matches:
        match_soup = get_url_content(match)
        match_information = get_match_information(match_soup)
        matches_information.append(match_information)

    date_match_information = pd.DataFrame(matches_information)
    if not date_match_information.empty:
        date_match_information = date_match_information.assign(
            match_date=date, date_url=url
        )
    return date_match_information


def create_match_data(start_date, end_date, filepath):
    """
    Get all available match data between two given dates

    Parameters
    ----------
    start_date: datetime.datetime
        The earliest date to start looking for matches in between
    end_date: datetime.datetime
        The latest date to look matches up to
    filepath: str
        The filepath of where the data is going to be saved

    Returns
    -------
    match_data: pd.DataFrame
        A dataframe containing all available match data between the two dates
    """

    delta = timedelta(days=1)
    match_data = pd.DataFrame()

    current_date = start_date

    while current_date <= end_date:
        logger.info(f'Trying to get matches for {current_date}')
        current_date_string = datetime.strftime(current_date, '%Y%m%d')
        current_url = SCORES_URL + current_date_string
        current_dataframe = get_date_match_information(current_url)
        if not current_dataframe.empty:
            match_data = pd.concat([match_data, current_dataframe])
            logger.info('Match data parsed')
        else:
            logger.info('No match data available')
        match_data.to_csv(filepath, index=False)
        current_date += delta

    return match_data
