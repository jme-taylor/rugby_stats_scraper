import logging

from rugby_stats_scraper.constants import ESPN_ATTRIBUTES
from rugby_stats_scraper.utils import get_url_content

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class EspnMatch:
    def __init__(self, url):
        self.url = url
        self.soup = get_url_content(self.url)
        self.match_data_dict = dict()
        logger.debug(f'Initialising class for {self.url}')

    def attribute_text(self, attribute, soup=None):
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

    def competition_information(self):
        raw_competition = self.attribute_text('competition')
        self.competition = raw_competition[:-4].strip()
        self.year = raw_competition[-4:]
        self.match_data_dict['competition'] = self.competition
        self.match_data_dict['year'] = self.year

    def score_information(self):
        self.home_score = self.attribute_text('score_home')
        self.away_score = self.attribute_text('score_away')
        self.match_data_dict['home_score'] = self.home_score
        self.match_data_dict['away_score'] = self.away_score

    def venue_information(self):
        self.venue = self.attribute_text('venue')
        self.venue = self.venue.split(':')[1].lstrip()
        self.match_data_dict['venue'] = self.venue

    def get_team_information(self, home_away):
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

    def match_data(self):

        # if not already done - get headline info for match
        self.competition_information()
        self.score_information()
        self.venue_information()

        home_team_dict = self.get_team_information('home')
        self.match_data_dict.update(home_team_dict)

        away_team_dict = self.get_team_information('away')
        self.match_data_dict.update(away_team_dict)

        return self.match_data_dict
