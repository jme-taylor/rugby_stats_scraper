# Rugby Stats Scraper

I found it hard to find my own source of rugby match results. So I decided to make my own scraper to solve that issue and practice a few python/data engineering-y skills at the same time. This is no means what I deem a 'finished product' and there's a lot of scope for improvements in at [scoped improvements](#scoped-improvements)

The main code is python script that can access rugby match data from the web and store it as a CSV on your local machine. Currently this only uses ESPN data ([here's](https://www.espn.co.uk/rugby/scoreboard?date=20220917) an example), but I may add more sources as I go on.

## Installation instructions

Firstly clone the repo, then navigate to the folder on your machine where the repository is stored. You then have two options for running this project:

1. Docker (preferred)
2. Locally within poetry virtual environment

### Docker

If you wish to run the project within Docker, firstly make sure that Docker is installed on your local machine (instructions [here](https://docs.docker.com/get-docker/) if you haven't).

Once this is done you'll then need to build the docker image, I've used `rugby-stats-scraper` but you can name it however you'd like (do make sure you replace any reference to your own name if you do that):

```bash
docker build -t rugby-stats-scraper .
```

Then you should be able to run the docker container:

```bash
docker run rugby-stats-scraper
```

### Poetry Virtual Environment

Dependency management in this project is done via [poetry](https://python-poetry.org/), if you haven't already installed this, the instructions are located [here](https://python-poetry.org/docs/#installation).

Once poetry is installed, you can navigate to where the repo is stored, then run the following commands in order.

```bash
poetry install
poetry shell
```

If these commands have worked, you should then be in the project's virual environment. You can then run the following command:

```bash
python main.py
```

### Data

Data will populate in a `match_data.csv` in the `data` folder with all the matches that the scraper can find. If it's your first time runnning the data, it will take quite a while to entirely populate this file (scope for improvements here). But, on every subsequent run, the scraper will run from the last populated date in the `match_data.csv`.

### Scoped Improvements

- Use a database rather than `.csv` files. Currently I'm using a `.csv` output. This will, and already hits performance + scalability issues. Something like `postgresql` or even using a storage bucket like `S3` could work.
- Change the classes within `espn.py` could be better implemented as `dataclasses` as there isn't much method logic here, just using them to store data.
- Pulling team level stats like posession could be useful too
- Champions cup data is spotty, might need a different source for this.
