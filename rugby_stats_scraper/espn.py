import logging
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

from rugby_stats_scraper.constants import (
    ESPN_ATTRIBUTES,
    ESPN_BASE_URL,
    ESPN_MATCH_DATA_BASE,
)
from rugby_stats_scraper.utils import get_url_content

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class EspnMatch:
    """Class and methods for a single match on ESPN website.

    Parameters
    ----------
    url: str
        The URL of the website for the match

    Attributes
    ----------
    url: str
        The URL of the website for the match
    soup: BeautifulSoup
        The beautiful soup object of the match
    match_data_dict: dict
        A dictionary containing all the scraped data for the match
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.soup = get_url_content(self.url)
        self.match_data_dict = ESPN_MATCH_DATA_BASE.copy()
        self.match_data_dict['url'] = self.url

    def attribute_text(
        self, attribute: str, soup: BeautifulSoup = None
    ) -> str:
        """Gets the relevant text for an attribute requested.

        Looks up an attribute in a soup object, and returns the text
        associated with that attribute. If that attribute is not present, a
        None Type is returned.

        Parameters
        ----------
        attribute : str
            The attribute that is to be looked up.
        soup : BeautifulSoup, optional
            A beautiful soup object to lookup against, by default None. If
            this isn't specified, the classes' soup attribute is used instead.

        Returns
        -------
        text: str
            The attribute text.
        """
        lookup = ESPN_ATTRIBUTES[attribute]
        if soup:
            source = soup
        else:
            source = self.soup

        try:
            text = source.find(attrs={'class': lookup}).text
        except AttributeError:
            text = None

        return text

    def competition_information(self) -> None:
        """Method to get the competition and year from a match."""
        raw_competition = self.attribute_text('competition')
        self.match_data_dict['competition'] = raw_competition[:-4].strip()
        self.match_data_dict['year'] = raw_competition[-4:]

    def score_information(self) -> None:
        """Method to get home and away score from a match."""
        self.match_data_dict['home_score'] = self.attribute_text('score_home')
        self.match_data_dict['away_score'] = self.attribute_text('score_away')

    def venue_information(self):
        """Method to get stadium information from a match"""
        raw_venue = self.attribute_text('venue')
        self.match_data_dict['venue'] = raw_venue.split(':')[1].lstrip()

    def get_team_information(self, home_away: str) -> None:
        """Method to get team information from a match, for both teams.

        Parameters
        ----------
        home_away: str
            A string to describe if the home or away team's data is required.
        """
        if home_away == 'home':
            lookup = {'class': 'team team-a'}
        elif home_away == 'away':
            lookup = {'class': 'team team-b'}
        else:
            raise ValueError('"home_away" must be one of "home" or "away"')

        team_soup = self.soup.find(attrs=lookup)
        self.match_data_dict[home_away + '_long_name'] = self.attribute_text(
            'long_name', soup=team_soup
        )
        self.match_data_dict[home_away + '_short_name'] = self.attribute_text(
            'short_name', soup=team_soup
        )
        self.match_data_dict[
            home_away + '_abbreviation'
        ] = self.attribute_text('abbreviation', soup=team_soup)

    def match_data(self) -> dict:
        """Method to assemble all match data and return the dictionary containing this.

        Returns
        -------
        self.match_data_dict: dict
            Dictionary containing competition, score, venue and both team's
            information.
        """

        # if not already done - get headline info for match
        self.competition_information()
        self.score_information()
        self.venue_information()
        self.get_team_information('home')
        self.get_team_information('away')

        return self.match_data_dict


class EspnDate:
    def __init__(self, url: str) -> None:
        self.url = url
        self.soup = get_url_content(self.url)
        self.date = datetime.strptime(self.url[-8:], '%Y%m%d')
        self.match_links = list()
        logger.info(f'Getting data for {self.url}')

    def get_matches(self) -> None:
        """Method to get all matches for a date."""
        events = self.soup.find(id='events')
        matches = events.find_all(attrs={'class': 'mobileScoreboardLink'})

        for match in matches:
            try:
                raw_match_link = match['href']
                self.match_links.append(ESPN_BASE_URL + raw_match_link)
            except KeyError:
                continue

        match_count = len(self.match_links)
        logger.info(f'{match_count} matches found')

    def create_date_dataframe(self):
        self.get_matches()
        match_data_dicts = []
        for match_link in self.match_links:
            temp_match = EspnMatch(match_link)
            temp_match_data = temp_match.match_data()
            match_data_dicts.append(temp_match_data)

        date_dataframe = pd.DataFrame(match_data_dicts)
        date_dataframe['match_date'] = self.date
        return date_dataframe
