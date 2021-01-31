"""Provides domain specific functionality."""
import logging
from typing import Set

import pandas as pd

from app.tools import scraper, repository
from app.parsers import sherdog
from app.transformers.sherdog import Sequencer, Cumulator

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(funcName)s] %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
    level=logging.INFO,
)


def generate_event_listing_uris(start: int = 1, end: int = 500):
    """Generates uris for listing pages where all events
    links are listed.

    Args:
        start (int, optional): which page to start. Defaults to 1.
        end (int, optional): which page to end. Defaults to 500.

    Returns:
        List[str]: list of uris
    """
    baseuri = "http://www.sherdog.com/events/recent/{}-page"
    return [baseuri.format(i) for i in range(start, end)]


def extract_fights(repo: repository.AbstractRepository) -> None:
    """Extracts fights and saves them in a specified filename.

    Args:
        repo: repository that provides data persistance functionalities.
    """
    lists = generate_event_listing_uris(1, 500)
    scraped: Set[str] = set()  # TODO: should contain scraped data
    for listing_url in lists:
        logging.info("Scraping %s", listing_url)
        listing_content = scraper.get_content(listing_url)
        events = sherdog.extract_events_links(listing_content, listing_url)
        events = list(set(events).difference(set(scraped)))
        if events:
            results = scraper.run(events, sherdog.extract_fights, 25)
            for result in results:
                repo.add(result)
        repo.commit()


def extract_fighters(fighters: list, repo: repository.AbstractRepository) -> None:
    """Extracts fighters and saves them in a specified filename.

    Args:
        fighters (List[str]): list of fighters urls.
        filename (str): file name where data should be saved.
    """
    for batch, i in scraper.batch(fighters, 100):
        scraped: Set[str] = set()  # TODO: should contain scraped data
        batch = list(set(batch).difference(set(scraped)))
        logging.info("[%s:%s]: Scraping fighters.", i, len(fighters))
        results = scraper.run(batch, sherdog.extract_fighter_info, 25)
        for result in results:
            repo.add(result)
        repo.commit()


def transform_fights(data: pd.DataFrame, repo: repository.AbstractRepository) -> None:
    """From a sequence of n fight stats it creates
    fighters 2n (n for each fighter) results in time.

    Args:
        data: fights stats.
        repo: repository where data should be stored.
    """
    sequencer = Sequencer()
    cumulator = Cumulator()
    # Calculate pre-fight stats
    data = data[data["result"].isin(["win", "loss"])]
    sequences = sequencer.fit_transform(data)
    # Exchange stats
    exchanged = sequencer.exchange(sequences)
    # Calculate cumulative stats
    accumulated = cumulator.fit_transform(exchanged)
    # Exchange stats
    results = cumulator.exchange(accumulated)
    for result in results:
        repo.add(result)
    repo.commit()