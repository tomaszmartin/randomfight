import datetime as dt
import logging
from typing import List
import os

import pandas as pd

from app.tools import scraper
from app.parsers import sherdog
from app.transformers.sherdog import Sequencer, Cumulator

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(funcName)s] %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
    level=logging.INFO,
)


def extract_fighters(fighters: List[str], filename: str):
    """Extracts fighters and saves them in a specified filename.

    Args:
        fighters (List[str]): list of fighters urls.
        filename (str): file name where data should be saved.
    """
    data = pd.DataFrame()
    if os.path.exists(filename):
        data = pd.read_csv(filename)

    for batch, i in scraper.batch(fighters, 100):
        done = data["fighter"].unique().tolist()
        batch = list(set(batch).difference(set(done)))
        logging.info("[%s:%s]: Scraping fighters.", i, len(fighters))
        scraped = scraper.run(batch, sherdog.extract_fighter_info, 25)
        data = data.append(pd.DataFrame(scraped))
        data.to_csv(filename, index=False)


def transform_fights(data):
    transformer = Sequencer()
    # Calculate pre-fight stats
    data = data[data["result"].isin(["win", "loss"])]
    transformed = transformer.fit_transform(data)
    frame = pd.DataFrame.from_records(transformed)
    frame.to_json("data/step1.json", "records")

    # Exchange stats
    transformed = pd.read_json("data/step1.json").to_dict("records")
    exchanged = transformer.exchange(transformed)
    frame = pd.DataFrame.from_records(exchanged)
    frame.to_json("data/step2.json", "records")

    # Calculate cumulative stats
    transformer = Cumulator()
    step = pd.read_json("data/step2.json")
    transformed = transformer.fit_transform(step)
    transformed_df = pd.DataFrame.from_records(transformed)
    transformed_df.to_json("data/step3.json")

    # Exchange stats
    transformed = pd.read_json("data/step3.json").to_dict("records")
    exchanged = transformer.exchange(transformed)
    frame = pd.DataFrame.from_records(exchanged)
    frame.to_json("data/final.json")


if __name__ == "__main__":
    data = pd.read_csv("data/fights.csv")
    transform_fights(data)
