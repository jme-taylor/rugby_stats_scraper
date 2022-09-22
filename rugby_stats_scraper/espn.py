import datetime
import json
import logging

import pandas as pd

from rugby_stats_scraper.utils import get_request_response, load_espn_headers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


ESPN_HEADERS = load_espn_headers()


class EspnMatch:
    """
    Class for a single match from ESPN data.

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
        self.venue = self.json['competitions'][0]['venue']['fullName']
        self.city = self.json['competitions'][0]['venue']['address']['city']
        self.state = self.json['competitions'][0]['venue']['address']['state']
        self.neutral_site = self.json['competitions'][0]['neutralSite']
        self.indoor = self.json['competitions'][0]['venue']['indoor']
        self.match_date = self.json['date']

    def team_information(
        self, team_json: dict, num: str, include_team_statistics: bool = False
    ) -> dict:
        """Method to get information at a team level.

        Parameters
        ----------
        team_json : dict
            A JSON containing the team level information.
        num : str
            The number of the team - will be '1' or '2'
        include_team_statistics : bool, optional
            Whether to include detailed team statistics.

        Returns
        -------
        team_dict: dict
            A dictionary with team level information.
        """
        team_dict = dict()
        team_dict[num + '_id'] = team_json['id']
        team_dict[num + '_name'] = team_json['team']['name']
        team_dict[num + '_abbreviation'] = team_json['team']['abbreviation']
        team_dict[num + '_home_away'] = team_json['homeAway']
        team_dict[num + '_score'] = team_json['score']
        team_dict[num + '_winner'] = team_json['winner']
        if include_team_statistics:
            team_dict[num + '_statistics'] = team_json['statistics']
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

    def __init__(self, date: str) -> None:
        self.date = date
        try:
            formatted_date = datetime.datetime.strptime(self.date, '%Y%m%d')
        except ValueError:
            raise ValueError(
                'Incorrect Date Format, date must be in "YYYYMMDD" format'
            )
        self.url = f'https://site.web.api.espn.com/apis/site/v2/sports/rugby/scorepanel?contentorigin=espn&dates={self.date}&lang=en&region=gb&tz=Europe/London'  # noqa
        self.response = get_request_response(self.url, ESPN_HEADERS)
        self.json = json.loads(self.response.text)
        logger.info(f'Getting matches for: {formatted_date}')

    def date_data(self, include_team_statistics: bool = False):
        """Method to create a date dataframe.

        Parameters
        ----------
        include_team_statistics : bool, optional
            Whether to include detailed team statistics or not, by default
            False

        Returns
        -------
        date_dataframe: pd.DataFrame
            The dataframe containing all matches on that date.
        """
        competitions = self.json['scores']
        competition_count = len(competitions)
        match_count = 0
        match_data_dicts = []
        for competition in competitions:
            competition_name = competition['leagues'][0]['name']
            competition_season = competition['season']['year']
            matches = competition['events']
            for match in matches:
                match_count += 1
                temp_match = EspnMatch(match)
                temp_match_data = temp_match.match_data()
                temp_match_data['competition'] = competition_name
                temp_match_data['season'] = competition_season
                match_data_dicts.append(temp_match_data)

        logger.info(
            f'{match_count} matches parsed from {competition_count} competitions'  # noqa
        )
        date_dataframe = pd.DataFrame(match_data_dicts)
        return date_dataframe
