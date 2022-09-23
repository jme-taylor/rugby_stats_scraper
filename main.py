from datetime import datetime, timedelta

import pandas as pd

from rugby_stats_scraper.constants import DATA_FOLDER, ESPN_EARLIEST_DATE
from rugby_stats_scraper.espn import EspnDate

# where the main data is stored
filename = 'match_data.csv'
filepath = DATA_FOLDER.joinpath(filename)
file_exists = filepath.is_file()

# for iteratively storing data
temp_filename = 'tmp_' + filename
temp_filepath = DATA_FOLDER.joinpath(temp_filename)

current_date = datetime.today()


def main():
    date_range_data = pd.DataFrame()
    date = ESPN_EARLIEST_DATE
    while date <= current_date:
        date_string = date.strftime('%Y%m%d')
        temp_date = EspnDate(date_string)
        temp_date_dataframe = temp_date.date_data()
        date_range_data = pd.concat([date_range_data, temp_date_dataframe])
        date += timedelta(days=1)
        date_range_data.to_csv((temp_filepath), index=False)

    date_range_data.to_csv(filepath, index=False)


if __name__ == '__main__':
    main()
