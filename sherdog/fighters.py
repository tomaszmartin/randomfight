"""Responsible for sequencing fights data in time."""
from pprint import pprint
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from datetime import datetime as dt
from threading import Thread
from multiprocessing.pool import ThreadPool
import os
import re
import time
import asyncio
from aiohttp import ClientSession


def filepath(file):
    basepath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join(basepath, "data")
    return os.path.join(datapath, file)


def get_fighters(raw):
    """Returns a list of fighter's names."""
    return raw["fighter"].unique().tolist()


def get_content(uri):
    uri = "http://www.sherdog.com/" + uri
    with urlopen(uri) as response:
        if response.status == 200:
            content = response.read()
            return content


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)], ndx


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read(), url


async def scrape(links, ndx):
    tasks = []
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for link in links:
            task = asyncio.ensure_future(
                fetch("http://www.sherdog.com/" + link, session)
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        data = []
        for content, url in responses:
            current = parse(content, url)
            data.append(current)

        pd.DataFrame(data).to_csv("data/fighters/{}.csv".format(ndx), index=False)


def parse(content, uri):
    try:
        soup = bs(content, "lxml")
        data = {"fighter": uri}
        data["birth"] = soup.find("span", {"itemprop": "birthDate"}).text
        height = soup.find("span", {"class": "height"})
        if height:
            height = height.find("strong").text
            height = height.replace('"', "")
            data["height"] = float(height.replace("'", "."))
        else:
            data["height"] = None
        association = soup.find("a", {"class": "association"})
        if association:
            data["association"] = association.text
        else:
            data["association"] = None
        data["nationality"] = soup.find("strong", {"itemprop": "nationality"}).text
        return data
    except Exception as e:
        print(uri)
        print(e)
        return {}


def download(fighters, start):
    final = []
    for i, fighter in enumerate(fighters):
        try:
            data = scrape(fighter)
            final.append(data)
            print(f"Scraped fighter {i}")
        except Exception as e:
            print(f"Error at fighter {i}")
            pass

    pd.DataFrame(final).to_csv(f"data/fighters_{start}.csv")


def combine():
    fightspath = filepath("data.csv")
    fighterspath = filepath("fighters.csv")
    fights = pd.read_csv(fightspath)
    fighters = pd.read_csv(fighterspath, sep=";", encoding="latin-1")
    merged = fights.merge(fighters, on=["fighter"], how="left")
    fighters.rename(columns={"fighter": "opponent"}, inplace=True)
    merged.rename(
        columns={
            "association": "fighter association",
            "birth": "fighter birth",
            "height": "fighter height",
            "nationality": "fighter nationality",
        },
        inplace=True,
    )
    merged = merged.merge(fighters, on=["opponent"], how="left")
    merged.rename(
        columns={
            "association": "opponent association",
            "birth": "opponent birth",
            "height": "opponent height",
            "nationality": "opponent nationality",
        },
        inplace=True,
    )
    merged.to_csv(filepath("merged.csv"), index=False)


if __name__ == "__main__":
    links = pd.read_csv("data/fighters.csv", sep=";", encoding="latin-1")
    links = links["fighter"].tolist()
    for current, ndx in batch(links, 100):
        if ndx > 16600:
            start = time.time()
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(scrape(current, ndx))
            loop.run_until_complete(future)
            elapsed = time.time() - start
            print("Saved batch {} in {:.2f} seconds".format(ndx, elapsed))
