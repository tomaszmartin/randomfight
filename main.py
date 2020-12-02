import logging

import pandas as pd

from tools import scraper
from sherdog import parser

def generate_event_listing_uris(start: int=1, end: int=500):
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


if __name__ == "__main__":
    filename = "data/fights.csv"
    data = pd.read_csv(filename)
    scraped = data["url"].unique().tolist()
    lists = generate_event_listing_uris(100, 150)
    for i, listing_url in enumerate(lists):
        listing_content = scraper.get_content(listing_url)
        events = parser.extract_events_links(listing_content, listing_url)
        events = list(set(events).difference(set(scraped)))
        logging.info(f"[{listing_url} {i}:{len(lists)}]: Found {len(events)} events to scrape.")
        if events:
            fights = scraper.run(events, parser.extract_fights, 25)
            curr_frame = pd.DataFrame(fights)
            data = data.append(curr_frame)
            data.to_csv(filename, index=False)
        
