import asyncio
from aiohttp import ClientSession, TCPConnector
from pprint import pprint
from datetime import datetime as dt
import time
import logging
from typing import Any, List, Iterable, Optional, Callable

import re
import requests
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
import pandas as pd
from uuid import uuid4

logging.getLogger().setLevel(logging.INFO)


def get_content(uri: str) -> Optional[str]:
    """Extracts content from web page.

    Args:
        uri (str): web page adress.

    Returns:
        str: web page content.
    """
    with requests.get(uri) as response:
        if response.status_code == 200:
            content = response.content
            return content.decode(encoding="utf8")
    return None


def run(links: List[str], func: Callable, batch_size: int=50):
    result = []
    for current, ndx in batch(links, batch_size):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(scrape(current, func))
        partial = loop.run_until_complete(future)
        result.extend(partial)
    return result



async def scrape(links: List[str], func: Callable):
    tasks = []
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        for link in links:
            task = asyncio.ensure_future(fetch(link, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # All content is now extracted
        data = []
        for content, link in responses:
            try:
                result = func(content, link)
            except Exception as e:
                logging.exception(f"Exception while parsing {link}")
                raise e
            data.extend(result)
        return data


def batch(iterable: List[Any], n: int=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)], ndx


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read(), url


if __name__ == "__main__":
    # event_lists_uris = get_events_uris(start=0, n=500)
    # events_uris = []
    # for events_page in event_lists_uris:
    #     print(events_page)
    #     curr_events_uris = scrape_event_links(events_page)
    #     events_uris.extend(curr_events_uris)

    # pd.DataFrame(set(events_uris), columns=["url"]).to_csv(
    #     "../data/events2.csv", index=False
    # )

    links_frame = pd.read_csv("../data/events.csv")
    fights = pd.read_csv("../data/fights.csv")
    for ix in range(50, 55):
        start, batch_size = (ix * 1000, 50)
        links = sorted(links_frame["link"].tolist())[: start + (batch_size * 20)]
        for current, ndx in batch(links, batch_size):
            if ndx >= start:
                start_time = time.time()
                loop = asyncio.get_event_loop()
                future = asyncio.ensure_future(scrape(current, ndx))
                frame = loop.run_until_complete(future)
                fights = fights.append(frame, sort=False)
                elapsed = time.time() - start_time
                print("Saved batch {} in {:.2f} seconds".format(ndx, elapsed))

        fights["id"] = fights["link"] + fights["fighter"] + fights["opponent"]
        fights = fights.drop_duplicates(subset=["id"])
        fights.to_csv("../data/fights.csv", index=False)
