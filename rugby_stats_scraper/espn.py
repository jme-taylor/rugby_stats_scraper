import datetime
import json
import logging

from rugby_stats_scraper.constants import ESPN_HEADERS
from rugby_stats_scraper.utils import get_request_response

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class EspnMatch:
    def __init__(self, json: dict) -> None:
        self.json = json

    def venue_information(self) -> None:
        self.neutral_site = self.json['competitions'][0]['neutralSite'].astype(
            bool
        )
        self.venue = self.json['competitions'][0]['venue']['fullName']

    def team_information(self, team_json):
        competitors = self.json['competitions'][0]['competitors']
        for competitor in competitors:
            print(competitor['team']['name'])


# get a team dict for each team
# create a function to assemble high level match info
# option for advanced stats? - maybe loop through all the dicts?


class EspnDate:
    def __init__(self, date: str) -> None:
        self.date = date
        try:
            datetime.datetime.strptime(self.date, '%Y%m%d')
        except ValueError:
            raise ValueError(
                'Incorrect Date Format, date must be in "YYYYMMDD" format'
            )
        self.url = f'https://site.web.api.espn.com/apis/site/v2/sports/rugby/scorepanel?contentorigin=espn&dates={self.date}&lang=en&region=gb&tz=Europe/London'  # noqa
        self.response = get_request_response(self.url, ESPN_HEADERS)
        self.json = json.loads(self.response.text)
        logger.info(f'Initialising class for {self.date}')

    def league_and_match_count(self):
        leagues = self.json['scores']
        league_count = len(leagues)
        self.match_list = list()
        for league in leagues:
            match_count = len(league['events'])


# get the amonunt of leagues
# for each league - find a match and parse the information from this
# get an example match


test_date = EspnDate('20220917')
test_date.league_and_match_count()

test_match = test_date.json['scores'][0]['events'][0]
test_match_class = EspnMatch(test_match)
test_match_class.competition_information()
