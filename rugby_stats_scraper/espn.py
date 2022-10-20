import datetime
import json
import logging
import time

import pandas as pd
import requests

from rugby_stats_scraper.utils import get_json_element

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s',
)


class EspnMatch:
    """
    Class for a single match from ESPN data.

    Parameters
    ----------
    json: dict
        A JSON with the match data inside of it.

    Attributes
    ----------
    json: dict
        A JSON of the match data
    venue: str
        The stadium that the match was played in.
    city: str
        The city that the match was played in.
    state: str
        The state that the match was played in.
    neutral_site: bool
        Whether the venue was neutral (i.e. neither of the two teams would
        call it their home stadium).
    indoor: bool
        Whether the match was played indoors or not.
    match_date: str
        The date and time the match was played at.
    """

    def __init__(self, json: dict) -> None:
        self.json = json

    def date_and_venue_information(self) -> None:
        """Method to get the date and venue information for the match."""
        self.venue = get_json_element(
            self.json, ('competitions', 0, 'venue', 'fullName')
        )
        self.city = get_json_element(
            self.json, ('competitions', 0, 'venue', 'address', 'city')
        )
        self.state = get_json_element(
            self.json, ('competitions', 0, 'venue', 'address', 'state')
        )
        self.neutral_site = get_json_element(
            self.json, ('competitions', 0, 'neutralSite')
        )
        self.indoor = get_json_element(
            self.json, ('competitions', 0, 'venue', 'indoor')
        )

        self.match_date = get_json_element(self.json, ('date',))

    def team_information(self, team_json: dict, num: str) -> dict:
        """Method to get information at a team level.

        Parameters
        ----------
        team_json : dict
            A JSON containing the team level information.
        num : str
            The number of the team - will be '1' or '2'

        Returns
        -------
        team_dict: dict
            A dictionary with team level information.
        """
        team_dict = dict()
        team_dict[num + '_id'] = get_json_element(team_json, ('id',))
        team_dict[num + '_name'] = get_json_element(
            team_json, ('team', 'name')
        )
        team_dict[num + '_abbreviation'] = get_json_element(
            team_json, ('team', 'abbreviation')
        )
        team_dict[num + '_home_away'] = get_json_element(
            team_json, ('homeAway',)
        )
        team_dict[num + '_score'] = get_json_element(team_json, ('score',))
        team_dict[num + '_winner'] = get_json_element(team_json, ('winner',))
        return team_dict

    def match_data(self) -> dict:
        """Generates the full match dataset.

        Returns
        -------
        match_dict: dict
            A dictionary containing all the match information.
        """
        match_dict = dict()
        self.date_and_venue_information()

        match_dict['match_date'] = self.match_date
        match_dict['venue'] = self.venue
        match_dict['city'] = self.city
        match_dict['state'] = self.state
        match_dict['neutral_site'] = self.neutral_site
        match_dict['indoor'] = self.indoor

        teams = self.json['competitions'][0]['competitors']
        for team, team_num in zip(teams, ['team_1', 'team_2']):
            team_data = self.team_information(team, team_num)
            match_dict.update(team_data)

        return match_dict


class EspnDate:
    """
    Class for a single date from ESPN data.

    Parameters
    ----------
    try_count: int, optional
        An integer to determine how many retries will be made in the event of
        a connection or connection reset error to the API. By default, this is
        set at 3.

    Attributes
    ----------
    date: str
        A string of the date to get data from in 'YYYY-MM-DD' format.
    url: str
        The URL for the API to hit
    response: requests.Respons
        The API response
    json: dict
        A JSON of the API response.
    """

    def __init__(self, date: str, try_count: int = 3) -> None:
        self.date = date
        try:
            formatted_date = datetime.datetime.strptime(self.date, '%Y%m%d')
        except ValueError:
            raise ValueError(
                'Incorrect Date Format, date must be in "YYYYMMDD" format'
            )

        self.url = f'https://site.web.api.espn.com/apis/site/v2/sports/rugby/scorepanel?contentorigin=espn&dates={self.date}&lang=en&region=gb&tz=Europe/London'  # noqa
        self.try_count = try_count
        while self.try_count > 0:
            try:
                self.response = requests.get(self.url)
                self.try_count = 0
            except (ConnectionError, ConnectionResetError):
                if self.try_count <= 0:
                    raise ConnectionError(
                        f'API connection for {self.date} aborted'
                    )
                else:
                    self.try_count -= 1
                time.sleep(0.5)
        self.json = json.loads(self.response.text)
        logger.info(f'Getting matches for: {formatted_date}')

    def date_data(self):
        """Method to create a date dataframe.


        Returns
        -------
        date_dataframe: pd.DataFrame
            The dataframe containing all matches on that date.
        """
        competitions = get_json_element(self.json, ('scores',))
        match_count = 0
        match_data_dicts = []
        if competitions:
            competition_count = len(competitions)
            for competition in competitions:
                competition_name = get_json_element(
                    competition, ('leagues', 0, 'name')
                )
                competition_season = get_json_element(
                    competition, ('season', 'year')
                )

                matches = get_json_element(competition, ('events',))
                for match in matches:
                    match_count += 1
                    temp_match = EspnMatch(match)
                    temp_match_data = temp_match.match_data()
                    temp_match_data['competition'] = competition_name
                    temp_match_data['season'] = competition_season

                    match_data_dicts.append(temp_match_data)
        else:
            competition_count = 0
        logger.info(
            f'{match_count} matches parsed from {competition_count} competitions'  # noqa
        )
        date_dataframe = pd.DataFrame(match_data_dicts)
        return date_dataframe
