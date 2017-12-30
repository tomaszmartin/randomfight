from pprint import pprint
from datetime import datetime as dt
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd

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
    data['date'] = dt.strptime(info.find('span', {'class': 'date'}).text, '%b %d, %Y').date()
    data['location'] = info.find('span', {'itemprop': 'location'}).text.replace(',', ' /')
    return data

def scrape_event_fights(content):
    data = []
    soup = bs(content, 'lxml')

    main = {}
    mainfight = soup.find('section', {'itemprop': 'subEvent'})
    fighter = mainfight.find('div', {'class': 'left_side'})
    opponent = mainfight.find('div', {'class': 'right_side'})
    main['fighter'] = fighter.find('a')['href']
    main['opponent'] = opponent.find('a')['href']
    main['result'] = fighter.find('span', {'class': 'final_result'}).text
    details = mainfight.find('table')
    num, method, referee, rounds, time = details.find_all('td', {'class': ''})
    main['method'] = method.text.split('\n')[0].split(' (')[0].lower().replace('method ', '')
    try:
        main['details'] = method.text.split('\n')[0].split(' (')[1].split(')')[0].lower()
    except:
        main['details'] = 'none'
    main['rounds'] = int(rounds.text.replace('Round', ''))
    main['time'] = float(time.text.replace('Time', '').split(':')[0]) + float(time.text.replace('Time', '').split(':')[1])/60
    main['position'] = 1
    data.append(main)

    fights = [fight for fight in soup.find_all('tr', {'itemprop': 'subEvent'})]
    for i, fight in enumerate(fights):
        current = {}
        fighter = fight.find('td', {'class': 'text_right'})
        opponent = fight.find('td', {'class': 'text_left'})
        current['fighter'] = fighter.find('a')['href']
        current['opponent'] = opponent.find('a')['href']
        current['result'] = fighter.find('span', {'class': 'final_result'}).text
        num, method, rounds, time = fight.find_all('td', {'class': ''})
        current['method'] = method.text.split('\n')[0].split(' (')[0].lower()
        try:
            current['details'] = method.text.split('\n')[0].split(' (')[1].split(')')[0].lower()
        except:
            current['details'] = 'none'
        current['rounds'] = int(rounds.text)
        current['time'] = float(time.text.split(':')[0]) + float(time.text.split(':')[1])/60
        current['position'] = i+2
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

if __name__ == '__main__':
    links = pd.read_csv('events.csv')
    # scraped = pd.read_csv('data.csv')
    data = []
    current = scrape_event('http://www.sherdog.com/events/MMAX-14-MMA-Xtreme-14-5859')
    for i, row in links.iterrows():
        if i < 10000:
            try:
                print(f'Downloading {i+1} out of {len(links)}')
                current = scrape_event('http://www.sherdog.com' + row['link'])
                data.extend(current)
                links.loc[i, 'scraped'] = True
            except Exception as e:
                print(f'App thrown an exception {e}')
            finally:
                links.to_csv('events.csv', index=False)
                frame = pd.DataFrame(data)
                # frame = frame.append(scraped)
                frame.to_csv('data.csv', index=False)
