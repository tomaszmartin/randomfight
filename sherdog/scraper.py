import asyncio
from aiohttp import ClientSession
from pprint import pprint
from datetime import datetime as dt
import time
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
from uuid import uuid4

def cleanhtml(element):
    raw_html = str(element)
    raw_html = raw_html.replace('<br/>', ', ')
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_uris():
    baseuri = 'http://www.sherdog.com/events/recent/{}-page'
    return [baseuri.format(i) for i in range(500)]

def get_content(uri):
    with urlopen(uri) as response:
        if response.status == 200:
            content = response.read()
            return content

def scrape_event_links(uri):
    content = get_content(uri)
    soup = bs(content, 'lxml')
    events = [link['href'] for link in soup.find_all('a', href=re.compile('events'))]
    return events

def scrape_event_data(content):
    data = {}
    soup = bs(content, 'lxml')
    data['title'] = cleanhtml(soup.find('h1'))
    data['organization'] = soup.find('h2').text
    info = soup.find('div', {'class': 'authors_info'})
    if info:
        data['date'] = dt.strptime(info.find('span', {'class': 'date'}).text, '%b %d, %Y').date()
        data['location'] = info.find('span', {'itemprop': 'location'}).text.replace(',', ' /')
        return data

def parse_time(time_node, rounds, method):
    try:
        timestr = time_node.text.replace('Time', '').replace('#', '3').replace('!', '1').replace('?', '.').replace('L', '').replace(')', '0').replace('`', '')
        timestr = timestr.replace('$', '4').replace('q', '').replace('"', '.').replace(':;', '.').replace(':', '.').replace(';', '.').strip()
        if timestr.lower() == 'n/a' or timestr.lower() == 'm/a':
            return rounds * 5
        if len(timestr.split('.')) > 1:
            minutes, seconds = timestr.split('.')
        else:
            minutes = timestr
            seconds = '0'
        if not minutes:
            minutes = 0.0
        else:
            minutes = float(minutes)
        if not seconds:
            seconds = 0.0
        else:
            seconds = float(seconds)
        time = (rounds - 1) * 5 + float(minutes + seconds/60)
        if method == 'decision' and minutes == 0:
            return rounds * 5
        return time
    except Exception as exc:
        print(time_node.text)
        raise exc

def scrape_event_fights(content, link):
    data = []
    soup = bs(content, 'lxml')

    main = {}
    mainfight = soup.find('section', {'itemprop': 'subEvent'})
    if mainfight:
        fighter = mainfight.find('div', {'class': 'left_side'})
        opponent = mainfight.find('div', {'class': 'right_side'})
        main['link'] = link
        main['fighter'] = fighter.find('a')['href']
        main['opponent'] = opponent.find('a')['href']
        if 'javascript' not in main['fighter'] and 'javascript' not in main['opponent']:
            mainres = fighter.find('span', {'class': 'final_result'})
            if mainres:
                main['result'] = mainres.text
                details = mainfight.find('table')
                num, method, referee, rounds, time = details.find_all('td', {'class': ''})
                main['method'] = method.text.split('\n')[0].split(' (')[0].lower().replace('method ', '')
                try:
                    main['details'] = method.text.split('\n')[0].split(' (')[1].split(')')[0].lower()
                except:
                    main['details'] = 'none'
                main['rounds'] = int(rounds.text.replace('Round', ''))
                main['time'] = parse_time(time, main['rounds'], main['method'])
                main['position'] = 1
                data.append(main)

    fights = [fight for fight in soup.find_all('tr', {'itemprop': 'subEvent'})]
    for i, fight in enumerate(fights, 2):
        current = {}
        fighter = fight.find('td', {'class': 'text_right'})
        opponent = fight.find('td', {'class': 'text_left'})
        if fighter and opponent:
            current['link'] = link
            current['fighter'] = fighter.find('a')['href']
            current['opponent'] = opponent.find('a')['href']
            if 'javascript' not in current['fighter'] and 'javascript' not in current['opponent']:
                currres = fighter.find('span', {'class': 'final_result'})
                if currres:
                    current['result'] = currres.text
                    num, method, rounds, time = fight.find_all('td', {'class': ''})
                    current['method'] = method.text.split('\n')[0].split(' (')[0].lower()
                    try:
                        current['details'] = method.text.split('\n')[0].split(' (')[1].split(')')[0].lower()
                    except:
                        current['details'] = 'none'
                    current['rounds'] = int(rounds.text)
                    current['time'] = parse_time(time, current['rounds'], current['method'])
                    current['position'] = i
                    data.append(current)

    return data

def scrape_event(uri):
    content = get_content(uri)
    fights = scrape_event_fights(content)
    event = scrape_event_data(content)
    for fight in fights:
        fight['title'] = event['title']
        fight['organization'] = event['organization']
        fight['date'] = event['date']
        fight['location'] = event['location']
    return fights

def download():
    links = pd.read_csv('data/events.csv')
    links['scraped'] == False
    data = []
    start = time.time()
    for i, row in links.iterrows():
        try:
            print(f'Downloading {i+1} out of {len(links)}: http://www.sherdog.com{row["link"]}')
            current = scrape_event('http://www.sherdog.com' + row['link'])
            data.extend(current)
            links.loc[i, 'scraped'] = True
        except Exception as e:
            print('http://www.sherdog.com' + row['link'])
            print(f'App thrown an exception {e}')
        finally:
            links.to_csv('events.csv', index=False)
            frame = pd.DataFrame(data)
            # frame = frame.append(scraped)
            frame.to_csv('data.csv', index=False)

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)], ndx

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read(), url

async def scrape(links, ndx):
    tasks = []
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for link in links:
            task = asyncio.ensure_future(fetch('http://www.sherdog.com' + link, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        data = []
        for content, link in responses:
            try:
                fights = scrape_event_fights(content, link)
                event = scrape_event_data(content)
                if event and fights:
                    for fight in fights:
                        fight['title'] = event['title']
                        fight['organization'] = event['organization']
                        fight['date'] = event['date']
                        fight['location'] = event['location']
            except Exception as e:
                print(link)
                raise e
            data.extend(fights)
        pd.DataFrame(data).to_csv('data/multi/{}.csv'.format(ndx), index=False)


if __name__ == '__main__':
    links = pd.read_csv('data/events.csv')
    links = links['link'].tolist()
    for current, ndx in batch(links, 100):
        if ndx >= 39700:
            start = time.time()
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(scrape(current, ndx))
            loop.run_until_complete(future)
            elapsed = time.time() - start
            print('Saved batch {} in {:.2f} seconds'.format(ndx, elapsed))
