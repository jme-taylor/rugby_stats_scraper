from dataclasses import field, dataclass, InitVar, asdict
import datetime
import json
import logging
import time

import pandas as pd
import requests

from rugby_stats_scraper.utils import get_json_element
from rugby_stats_scraper.constants import DATA_FOLDER

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s",
)


@dataclass
class TeamStats:

    team_json: InitVar[dict]

    id: str = field(init=False)
    name: str = field(init=False)
    abbreviation: str = field(init=False)
    home_away: str = field(init=False)
    score: str = field(init=False)
    winner: str = field(init=False)
    statistics: list = field(init=False)

    def __post_init__(self, team_json: dict) -> None:
        self.id = get_json_element(team_json, ("id",))
        self.name = get_json_element(team_json, ("team", "name"))
        self.abbreviation = get_json_element(team_json, ("team", "abbreviation"))
        self.home_away = get_json_element(team_json, ("homeAway",))
        self.score = get_json_element(team_json, ("score",))
        self.winner = get_json_element(team_json, ("winner",))
        self.statistics = get_json_element(team_json, ("statistics",))


@dataclass
class MatchStats:

    match_json: InitVar[dict]

    match_id: str = field(init=False)
    unique_id: str = field(init=False)
    venue: str = field(init=False)
    city: str = field(init=False)
    state: str = field(init=False)
    neutral_site: str = field(init=False)
    indoor: str = field(init=False)
    match_date: str = field(init=False)

    def __post_init__(self, match_json: dict) -> None:
        self.match_id = get_json_element(match_json, ('competitions', 0, 'id'))
        self.unique_id = get_json_element(match_json, ('competitions', 0, 'uid'))
        self.venue = get_json_element(match_json, ('competitions', 0, 'venue', 'fullName'))
        self.city = get_json_element(match_json, ('competitions', 0, 'venue', 'address', 'city'))
        self.state = get_json_element(match_json, ('competitions', 0, 'venue', 'address', 'state'))
        self.neutral_site = get_json_element(match_json, ('competitions', 0, 'neutralSite'))
        self.indoor = get_json_element(match_json, ('competitions', 0, 'venue', 'indoor'))
        self.match_date = get_json_element(match_json, ('date',))


class Match:
    def __init__(self, match_json: dict) -> None:
        self.match_json = match_json

    def create_match_data_dict(self) -> dict:
        match_data_dict = dict()

        match_data = MatchStats(self.match_json)
        match_data_dict.update(asdict(match_data))

        teams = get_json_element(self.match_json, ('competitions', 0, 'competitors'))

        for team, team_name in zip(teams, ['team_1', 'team_2']):
            team_data = TeamStats(team)
            team_data_dict = {f"{team_name}_{k}": v for k, v in asdict(team_data).items()}
            match_data_dict.update(team_data_dict)

        return match_data_dict


class Date:
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

    def create_date_dataframe(self):
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
                    temp_match = Match(match)
                    temp_match_data = temp_match.create_match_data_dict()
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


date = Date('20220917')
date_df = date.create_date_dataframe()
filepath = DATA_FOLDER.joinpath('espn_date_test.csv')
date_df.to_csv(filepath, index=False)
