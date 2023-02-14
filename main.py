from datetime import datetime, timedelta

import pandas as pd

from rugby_stats_scraper.constants import DATA_FOLDER, ESPN_EARLIEST_DATE
from rugby_stats_scraper.espn import EspnDate
from rugby_stats_scraper.utils import check_file_has_data

current_date = datetime.today()


def main() -> None:
    """Pulls CSV match data for all matches from ESPN. If you've already got a
    saved match data file - the script will look for the most recent data
    there and use that date as the date to start appending from, so it's not
    rewriting the whole dataset each time (this can take a while)."""

    filename = 'match_data.csv'
    filepath = DATA_FOLDER.joinpath(filename)

    temp_filename = 'tmp_' + filename
    temp_filepath = DATA_FOLDER.joinpath(temp_filename)

    # if the file given has data - use that and drop the last day from it
    if check_file_has_data(filepath):
        date_range_data = pd.read_csv(filepath)
        max_date = date_range_data['match_date'].max()
        date_range_data = date_range_data.drop(
            date_range_data[date_range_data['match_date'] == max_date].index
        )
        date = datetime.strptime(
            date_range_data['match_date'].max(), '%Y-%m-%dT%H:%MZ'
        )
    else:
        date_range_data = pd.DataFrame()
        date = ESPN_EARLIEST_DATE
    latest_date = datetime.today() - timedelta(days=1)

    while date <= latest_date:
        date_string = date.strftime('%Y%m%d')
        temp_date = EspnDate(date_string)
        temp_date_dataframe = temp_date.date_data()
        date_range_data = pd.concat([date_range_data, temp_date_dataframe])
        date += timedelta(days=1)
        date_range_data.to_csv((temp_filepath), index=False)

    date_range_data.to_csv(filepath, index=False)


if __name__ == '__main__':
    main()
