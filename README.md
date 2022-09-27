# rugby_stats_scraper

A command line tool, and python script that can access rugby match data from the web and store it as a CSV on your local machine. Currently this only uses ESPN data ([here's](https://www.espn.co.uk/rugby/scoreboard?date=20220917) an example), but I may add more sources as I go on.

## Demo

## Installation instructions

Firstly clone the repo.

Dependency management in this project is done via [poetry](https://python-poetry.org/), if you haven't already installed this, the instructions are located [here](https://python-poetry.org/docs/#installation).

Once poetry is installed, you can navigate to where the repo is stored, then run the following commands in order.

```bash
poetry init
poetry install
poetry shell
```

You'll also need some credentials for the ESPN scraper to use with the API. You can then store these in a `.env` file that will be read by the program. To get the headers, you can do this using your network tab in google chrome [(here](https://kiwidamien.github.io/using-api-calls-via-the-network-panel.html) are some more detailed instructions to a more generalised format). An example expected `.env` file can be seen in `example.env`.

## Running the scraper

If these commands have worked, you should then be in the project's virual environment. You can then run the following command:

```bash
python main.py
```

This is the default option without any selections. The selections you have available to you are:

* `earliest-date` - this the earliest date you'd like to pull data from. It must be in `YYYY-MM-DD` format. If you leave this blank, the script will use 2nd February 2005 (this is the earliest date in ESPN data AFAIK).
* `latest-date` - this the latest date you'd like to pull data from. It must be in `YYYY-MM-DD` formati. If you leave this blank, the script will use yesterday's date.
* `filename` - this is the filename you'd like to save it as. The script will add on the `.csv` for you, and the file will appear in the `data` folder. Whilst the script is still running it will iteratively save a `tmp_yourfilename.csv` file so that you still retain some data if the script breaks.

To see details about this in the command line you can run the following:

```bash
python main.py --help
```
