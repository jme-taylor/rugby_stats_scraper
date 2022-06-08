# rugby_stats_scraper

A command line tool, and python script that can access rugby match data from the web and store it as a CSV on your local machine.

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

## Running the scraper

If these commands have worked, you should then be in the project's virual environment. You can then run the following command:

```bash
python main.py
```

This is the default option without any selections. To see the options that you have, run this:

```bash
python main.py --help
```
