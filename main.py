import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from rugby_stats_scraper.constants import DATA_FOLDER, EARLIEST_DATE
from rugby_stats_scraper.espn import create_match_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# where the main data is stored
filename = Path('raw_match_data.csv')
filepath = DATA_FOLDER.joinpath(filename)
file_exists = filepath.is_file()

# for iteratively storing data
temp_filename = Path('temp_raw_match_data.csv')
temp_filepath = DATA_FOLDER.joinpath(temp_filename)


def main():
    # check latest date in existing data - if it exists
    if file_exists:
        existing_match_df = pd.read_csv(filepath)
        existing_match_df['match_date'] = pd.to_datetime(
            existing_match_df['match_date']
        )
        latest_date_in_data = existing_match_df['match_date'].max().date()
        earliest_date = latest_date_in_data + timedelta(days=1)
    # otherwise, use the earliest date setting previously used
    else:
        earliest_date = EARLIEST_DATE

    latest_date = datetime.today().date() - timedelta(days=1)

    # loop between the two dates
    match_df = create_match_data(earliest_date, latest_date, temp_filepath)

    # if existing file already exists, concat the two
    if file_exists:
        match_df = pd.concat([existing_match_df, match_df])

    # save the eventual data
    match_df.to_csv(filepath, index=False)

    # remove temp file at the end
    os.remove(temp_filepath)


if __name__ == '__main__':
    main()
