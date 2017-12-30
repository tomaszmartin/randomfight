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

def filepath(file):
    basepath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join(basepath, 'data')
    return os.path.join(datapath, file)

def get_fighters(raw):
    """Returns a list of fighter's names."""
    return raw['fighter'].unique().tolist()

def get_content(uri):
    uri = 'http://www.sherdog.com/' + uri
    with urlopen(uri) as response:
        if response.status == 200:
            content = response.read()
            return content

def scrape(uri):
    content = get_content(uri)
    soup = bs(content, 'lxml')
    data = {'fighter': uri}
    data['birth'] = soup.find('span', {'itemprop': 'birthDate'}).text
    height = soup.find('span', {'class': 'height'})
    if height:
        height = height.find('strong').text
        height = height.replace('"', '')
        data['height'] = float(height.replace('\'', '.'))
    else:
        data['height'] = None
    association = soup.find('a', {'class': 'association'})
    if association:
        data['association'] = association.text
    else:
        data['association'] = None
    data['nationality'] = soup.find('strong', {'itemprop': 'nationality'}).text

    return data

def download(fighters, start):
    final = []
    for i, fighter in enumerate(fighters):
        try:
            data = scrape(fighter)
            final.append(data)
            print(f'Scraped fighter {i}')
        except Exception as e:
            print(f'Error at fighter {i}')
            pass

    pd.DataFrame(final).to_csv(f'data/fighters_{start}.csv')

def combine():
    fightspath = filepath('data.csv')
    fighterspath = filepath('fighters.csv')
    fights = pd.read_csv(fightspath, sep=';', encoding='latin-1')
    fighters = pd.read_csv(fighterspath, sep=';', encoding='latin-1')
    merged = fights.merge(fighters, on=['fighter'], how='left')
    fighters.rename(columns={'fighter': 'opponent'}, inplace=True)
    merged.rename(columns={'association': 'fighter association',
                            'birth': 'fighter birth',
                            'height': 'fighter height',
                            'nationality': 'fighter nationality'}, inplace=True)
    merged = merged.merge(fighters, on=['opponent'], how='left')
    merged.rename(columns={'association': 'opponent association',
                            'birth': 'opponent birth',
                            'height': 'opponent height',
                            'nationality': 'opponent nationality'}, inplace=True)
    merged.to_csv(filepath('merged.csv'), index=False)


if __name__ == '__main__':
    combine()
