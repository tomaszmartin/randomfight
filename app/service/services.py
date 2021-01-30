"""Provides domain specific functionality."""
from typing import Set

from app.repository import base
from app.tools import scraper
from app.parsers import sherdog


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


def extract_fights(repo: base.AbstractRepository):
    """Extracts fights and saves them in a specified filename.

    Args:
        filename (str): file name where data should be saved.
    """
    lists = generate_event_listing_uris(1, 500)
    scraped: Set[str] = set()  # TODO: should contain scraped data
    for _, listing_url in enumerate(lists):
        listing_content = scraper.get_content(listing_url)
        events = sherdog.extract_events_links(listing_content, listing_url)
        events = list(set(events).difference(set(scraped)))
        if events:
            fights = scraper.run(events, sherdog.extract_fights, 25)
            for fight in fights:
                repo.add(fight)
        # TODO: commit to repository
