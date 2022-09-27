from datetime import datetime, timedelta

import click
import pandas as pd

from rugby_stats_scraper.constants import DATA_FOLDER, ESPN_EARLIEST_DATE
from rugby_stats_scraper.espn import EspnDate

# default file storage
default_filename = 'match_data.csv'
default_filepath = DATA_FOLDER.joinpath(default_filename)


current_date = datetime.today()


@click.command()
@click.option('--earliest-date', type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--latest-date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--filename")
def main(
    earliest_date: datetime = None,
    latest_date: datetime = None,
    filename: str = None,
) -> None:
    """Pulls CSV match data for all matches between the specified dates. If the
    dates are left as null, the defaults will be used. For the earliest date,
    this will be the earliest date available on the site - 2nd February 2005.
    For the latest date, this default will be yesterday's date. There is also
    a filename parameter, which is also optional. '.csv' will be appended to
    this for you. If left default, it will be saved as 'match_data.csv' in
    your data folder.

    Parameters
    ----------
    earliest_date : datetime, optional
        A string of the earliest date you'd like in format 'YYYY-MM-DD', by
        default None
    latest_date : datetime, optional
        A string of the latest date you'd like in format 'YYYY-MM-DD', by
        default None
    filename : str, optional
        A string of the filename you'd like, by default None
    """
    if filename:
        filename = filename + '.csv'
        filepath = DATA_FOLDER.joinpath(filename)
    else:
        filename = default_filename
        filepath = default_filepath

    temp_filename = 'tmp_' + filename
    temp_filepath = DATA_FOLDER.joinpath(temp_filename)

    if not earliest_date:
        earliest_date = ESPN_EARLIEST_DATE

    if not latest_date:
        latest_date = datetime.today() - timedelta(days=1)

    date_range_data = pd.DataFrame()
    date = earliest_date
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
