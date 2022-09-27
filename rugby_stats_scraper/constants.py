from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

DATA_FOLDER = PROJECT_ROOT.joinpath('data')

ESPN_EARLIEST_DATE = datetime(2005, 2, 5)
