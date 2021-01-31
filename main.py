import datetime as dt
import logging
from typing import List
import os

import pandas as pd

from app.tools import scraper, repository
from app.parsers import sherdog
from app.service import services


if __name__ == "__main__":
    repo = repository.CSVRepository("data/fights.csv", id_column="id")
    services.extract_fights(repo)
