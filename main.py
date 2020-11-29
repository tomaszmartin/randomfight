import logging

import pandas as pd

from tools import scraper
from sherdog import parser

def generate_event_listing_uris(start=1, n=500):
    baseuri = "http://www.sherdog.com/events/recent/{}-page"
    return [baseuri.format(i) for i in range(start, n + 1)]


if __name__ == "__main__":
    data = pd.DataFrame()
    lists = generate_event_listing_uris(1)
    for i, listing_url in enumerate(lists):
        listing_content = scraper.get_content(listing_url)
        events = parser.extract_events_links(listing_content, listing_url)
        fights = scraper.run(events, parser.extract_fights, 25)
        curr_frame = pd.DataFrame(fights)
        data = data.append(curr_frame)
        data.to_csv(f"data/fights.csv", index=False)
        logging.info(f"Extracted {i} of {len(lists)}: having {len(data)} fights.")
