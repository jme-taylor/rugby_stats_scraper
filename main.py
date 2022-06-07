import os
from datetime import datetime, timedelta
from pathlib import Path

import click
import pandas as pd

from rugby_stats_scraper.constants import DATA_FOLDER, EARLIEST_DATE
from rugby_stats_scraper.espn import create_match_data

# where the main data is stored
default_filename = Path('match_data.csv')
default_filepath = DATA_FOLDER.joinpath(default_filename)
file_exists = default_filepath.is_file()

# for iteratively storing data
default_temp_filename = Path('temp_match_data.csv')
default_temp_filepath = DATA_FOLDER.joinpath(default_temp_filename)


@click.command()
@click.option("--earliest-date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--latest-date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--filename")
def main(earliest_date=None, latest_date=None, filename=None):

    if filename:
        filename = filename + ".csv"
        filepath = DATA_FOLDER.joinpath(filename)
        temp_filename = 'temp_' + filename
        temp_filepath = DATA_FOLDER.joinpath(temp_filename)
    else:
        filepath = default_filepath
        temp_filepath = default_temp_filepath

    if not earliest_date:
        # check latest date in existing data - if it exists
        if file_exists:
            existing_match_df = pd.read_csv(filepath)
            existing_match_df['match_date'] = pd.to_datetime(
                existing_match_df['match_date']
            )
            latest_date_in_data = existing_match_df['match_date'].max()
            earliest_date = latest_date_in_data + timedelta(days=1)
        # otherwise, use the earliest date setting previously used
        else:
            earliest_date = EARLIEST_DATE

    if not latest_date:
        latest_date = datetime.today() - timedelta(days=1)

    # loop between the two dates
    match_df = create_match_data(earliest_date, latest_date, temp_filepath)

    # if existing file already exists, concat the two
    if file_exists and not earliest_date:
        match_df = pd.concat([existing_match_df, match_df])

    # save the eventual data, only if it exists though
    if not match_df.empty:
        match_df.to_csv(filepath, index=False)

    # remove temp file at the end, but only if this exists
    if temp_filepath.is_file():
        os.remove(temp_filepath)


if __name__ == '__main__':
    main()
