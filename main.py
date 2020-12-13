import logging
from typing import List

import pandas as pd

from app.tools import scraper
from app.parsers import sherdog


def geenerate_event_listing_uris(start: int = 1, end: int = 500):
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

def extract_fights(filename: str):
    """Extracts fights and saves them in a specified filename.

    Args:
        filename (str): file name where data should be saved.
    """
    data = pd.read_csv(filename)
    scraped = data["url"].unique().tolist()
    lists = generate_event_listing_uris()
    for i, listing_url in enumerate(lists):
        listing_content = scraper.get_content(listing_url)
        events = sherdog.extract_events_links(listing_content, listing_url)
        events = list(set(events).difference(set(scraped)))
        logging.info("[%s:%s]: Scraping events.", i, len(lists))
        if events:
            fights = scraper.run(events, sherdog.extract_fights, 25)
            curr_frame = pd.DataFrame(fights)
            data = data.append(curr_frame)
            data.to_csv(filename, index=False)


def extract_fighters(fighters: List[str], filename: str):
    """Extracts fighters and saves them in a specified filename.

    Args:
        fighters (List[str]): list of fighters urls.
        filename (str): file name where data should be saved.
    """
    data = pd.read_csv(filename)
    for batch, i in scraper.batch(fighters, 100):
        done = data["fighter"].unique().tolist()
        batch = list(set(batch).difference(set(done)))
        logging.info("[%s:%s]: Scraping fighters.", i, len(fighters))
        scraped = scraper.run(batch, sherdog.extract_fighter_info, 25)
        data = data.append(pd.DataFrame(scraped))
        data.to_csv(filename, index=False)


if __name__ == "__main__":
    data = pd.read_csv("data/fights.csv")
    fighters = [
        f"http://www.sherdog.com/{fighter}"
        for fighter in data["fighter"].unique().tolist()
    ]
    extract_fighters(fighters, "data/fighters.csv")
