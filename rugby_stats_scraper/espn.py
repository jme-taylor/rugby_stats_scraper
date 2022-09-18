import logging

from bs4 import BeautifulSoup

from rugby_stats_scraper.constants import ESPN_ATTRIBUTES
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
        self.match_data_dict = dict()

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

    def get_team_information(self, home_away: str) -> dict:
        """Method to get team information from a match, for both teams.

        Parameters
        ----------
        home_away: str
            A string to describe if the home or away team's data is required.

        Returns
        -------
        team_dict: dict
            A dictionary containing the team's long name, short name and their
            abrreviation.
        """
        if home_away == 'home':
            lookup = {'class': 'team team-a'}
        elif home_away == 'away':
            lookup = {'class': 'team team-b'}
        else:
            raise ValueError('"home_away" must be one of "home" or "away"')

        team_soup = self.soup.find(attrs=lookup)
        team_dict = {
            'long_name_'
            + home_away: self.attribute_text('long_name', soup=team_soup),
            'short_name_'
            + home_away: self.attribute_text('short_name', soup=team_soup),
            'abbreviation_'
            + home_away: self.attribute_text('abbreviation', soup=team_soup),
        }
        team_dict = {home_away + '_' + k: v for k, v in team_dict.items()}

        return team_dict

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

        home_team_dict = self.get_team_information('home')
        self.match_data_dict.update(home_team_dict)

        away_team_dict = self.get_team_information('away')
        self.match_data_dict.update(away_team_dict)

        return self.match_data_dict
