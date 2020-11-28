import logging

import pandas as pd

from tools import scraper
from sherdog import parser

def generate_event_listing_uris(start=1, n=500):
    baseuri = "http://www.sherdog.com/events/recent/{}-page"
    return [baseuri.format(i) for i in range(start, n + 1)]


if __name__ == "__main__":
    start = 70
    lists = generate_event_listing_uris(start, 7)
    for i, listing_url in enumerate(lists):
        logging.info(f"Downloading {i} of {len(lists)}")
        listing_content = scraper.get_content(listing_url)
        events = parser.extract_events_links(listing_content, listing_url)
        fights = scraper.run(events, parser.extract_fights, 25)
        pd.DataFrame(fights).to_csv(f"data/fights/{start+i}.csv", index=False)
