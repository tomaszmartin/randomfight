"""Extracting information from event web page."""
from urllib.request import urlopen
from datetime import datetime as dt
from copy import deepcopy
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
import pandas as pd


def extract(attr):
    """Extracts key and value from attribute."""
    attr = attr.text.replace('\n', '').strip()
    attr = re.sub(r'([A-Za-z]+)(\.?)(:)', r'\1<break>', attr)
    key, value = attr.split('<break>')
    try:
        key = clean_label(key)
        value = clean_value(value)
        if value.isdigit():
            value = float(value)
        if key == 'time format':
            try:
                time_format = re.search(r'\d+\-(\d+\-?)+', value).group()
                value = tuple(int(x) for x in time_format.split('-'))
            except:
                value = (5, 5, 5)
        if key == 'time':
            value = float(value.split(':')[0]) + float(value.split(':')[1]) / 60
        if key == 'dob':
            value = dt.strptime(value, '%b %d, %Y').date()
        if key == 'date':
            value = dt.strptime(value, '%B %d, %Y').date()
        if key in ['weight', 'height', 'reach', 'attendance']:
            value = metric_to_float(value)
    except ValueError:
        value = None

    return key, value

def clean_label(text):
    """Cleans label."""
    label = text.replace('\n', '').strip().lower()
    label = {'fighter': 'name', 'kd': 'knockdowns'}.get(label, label)
    return label

def clean_value(text):
    """Cleans value."""
    return text.replace('\n', '').strip()

def metric_to_float(value):
    """Changes various metrics into a float."""
    value = str(value)
    value = value.replace("'", '.')
    value = value.replace(",", '')
    value = re.sub(r'[A-Za-z" ]+', '', value)
    try:
        return float(value)
    except ValueError:
        return None

def stat_to_dict(data):
    """Split `1 of 2` like strings into dict."""
    new = deepcopy(data)
    new['stats'] = {}
    for key, value in data.items():
        if ' of ' in str(value):
            landed, thrown = value.split(' of ')
            new['stats'][key] = {'thrown': float(thrown), 'landed': float(landed)}
            del new[key]
        if key in ['pass']:
            new['stats'][key] = {'thrown': float(value), 'landed': float(value)}
            del new[key]
        if key == 'sub. att':
            landed = 0.0
            if data['method'] == 'Submission' and data['result'] == 'Win':
                landed = 1.0
            new['stats']['submissions'] = {'thrown': float(value), 'landed': landed}
            del new[key]
        if key == 'knockdowns':
            landed = 0.0
            if (data['method'] == 'KO' or data['method'] == 'KO/TKO') and data['result'] == 'Win':
                landed = 1.0
            new['stats']['knockouts'] = {'thrown': float(value), 'landed': landed}
            del new[key]

    return new

def exchange_stats(fight):
    """Exchanges stats between fighters in a fight."""
    fighter, opponent = fight
    for key in fighter['stats'].keys():
        fighter['stats'][key]['received'] = opponent['stats'][key]['landed']
        fighter['stats'][key]['avoided'] = opponent['stats'][key]['thrown'] - opponent['stats'][key]['landed']
        opponent['stats'][key]['received'] = fighter['stats'][key]['landed']
        opponent['stats'][key]['avoided'] = fighter['stats'][key]['thrown'] - fighter['stats'][key]['landed']
    return [fighter, opponent]

def extract_title(soup):
    """Extracts title from html"""
    return get_name(soup.find('span', {'class': 'b-content__title-highlight'}).get_text().strip())

def extract_attrs(soup):
    """Extracts title from html"""
    result = soup.find_all('i', {'class': ['b-fight-details__text-item_first',
                                           'b-fight-details__text-item']})
    result.extend(soup.find_all('li', {'class': 'b-list__box-list-item'}))
    return result

def clean_data(data):
    """Cleans the data."""
    cleaned = deepcopy(data)
    results = {'W': 'Win', 'L': 'Loss', 'D': 'Draw', 'NC': 'No contest'}
    for key, value in data.items():
        if key in ['slpm', 'sapm', 'str. acc', 'str. def',
                   'td avg', 'td acc', 'td def', 'sub. avg']:
            del cleaned[key]

        if key in ['rev.', 'td %', 'sig. str. %', 'pass',
                   'details', 'sig. str.']:
            del cleaned[key]
        if key == 'dob':
            del cleaned[key]
            cleaned['birth'] = value
        if key == 'result':
            cleaned['result'] = results[value]
    return cleaned

def attach_attrs(data, soup):
    """Attaches attributes to the data."""
    for attr in extract_attrs(soup):
        if ':' in attr.text.replace('\n', '').strip():
            key, value = extract(attr)
            data[key] = value
    return data

def get_name(name):
    aliases = {
        'Jacare Souza': 'Ronaldo Souza',
        'Minotauro Nogueira': 'Antonio Rodrigo Nogueira',
        'Rodrigo Nogueira': 'Antonio Rodrigo Nogueira',
        'Rampage Jackson': 'Quinton Jackson',
        'Rogerio Nogueira': 'Antonio Rogerio Nogueira',
        'Minotoro Nogueira': 'Antonio Rogerio Nogueira',
        'Mirko Cro Cop': 'Mirko Filipovic',
        'Rafael Feijao': 'Rafael Cavalcante',
        'Cris Cyborg': 'Cristiane Justino',
    }
    return aliases.get(name, name)




def scrape_links(content):
    """Extracts fights and fighters links from web content.
    :param content (string): html content of a webpage.
    :return fights, fighters (tuple): tuple of fights and fighters links"""
    soup = bs(content, 'lxml')
    # Extract fights link
    fights = [link['data-link'] for link in soup.find_all('tr', {'class': 'js-fight-details-click'})]
    fighters = [link['href'] for link in soup.find_all('a', href=re.compile('fighter-detail'))]
    # Get only unique values
    fighters = list(set(fighters))
    return fights, fighters

def scrape_basic_data(content, key):
    """Extracts basic information from a web content."""
    data = {}
    soup = bs(content, 'lxml')
    # Extract event name
    data[key] = extract_title(soup)
    data = attach_attrs(data, soup)
    return clean_data(data)

def scrape_event_data(content):
    """Extracts event data from a web content."""
    return scrape_basic_data(content, 'event')

def scrape_fighter_data(content, link):
    """Extracts fighter information from web content"""
    return [scrape_basic_data(content, 'name')]

def scrape_fight_data(content, link, position):
    """Extracts fight data from w given web page.
    :param content (string): web page content.
    :result data (list): list of attribtes for both fighters."""
    # TODO: Fix issue with lack of stats
    data = [{'link': link, 'position': position}, {'link': link, 'position': position}]
    soup = bs(content, 'lxml')
    # Extract fight stats
    for table in soup.find_all('table', {'class': ''}):
        names = [clean_label(elem.get_text()) for elem in table.find_all('th')]
        value_pairs = [value.get_text().strip() for value in table.find_all('td')]
        for name, value_pair in zip(names, value_pairs):
            value_pair = [clean_value(value) for value in re.split(r'\n\n+', value_pair)]
            value_pair = [int(value) if value.isdigit() else value for value in value_pair]
            data[0][name] = value_pair[0]
            data[1][name] = value_pair[1]
    # Extract fight information
    results = soup.find_all('i', {'class' : 'b-fight-details__person-status'})
    for i, fighter in enumerate(data):
        fighter = attach_attrs(fighter, soup)
        fighter['result'] = results[i].string.strip()
    result = []
    for fighter in data:
        info = soup.find('i', {'class': 'b-fight-details__fight-title'})
        fighter['bonus'] = {'ko': False, 'submission': False, 'performance': False, 'fight': False}
        if ('ko.png' in str(info) and fighter['result'] == 'W'):
            fighter['bonus']['ko'] = True
        if ('sub.png' in str(info) and fighter['result'] == 'W'):
            fighter['bonus']['submission'] = True
        if ('perf.png' in str(info) and fighter['result'] == 'W'):
            fighter['bonus']['performance'] = True
        if ('fight.png' in str(info)):
            fighter['bonus']['fight'] = True
        fighter['titlefight'] = 'title' in info.get_text().lower()
        result.append(stat_to_dict(clean_data(fighter)))
    result = exchange_stats(result)
    return result

def combine_data(event, fights, fighters):
    """Combines data from all sources.
    :param event (dict): event's attributes.
    :param fights (list): event's fights.
    :param fighters (list): fighter's in event.
    :return data (list): list of information about each fight."""
    combined = []
    for link, fight in deepcopy(fights).items():
        key = get_name(fight['name'])
        if key in fighters:
            fighter = fighters[key]
            fight = {**fight, **fighter, **event}
            combined.append(fight)
        else:
            print(f'Problem with fighter {key}')
            print(fighters.keys())
            raise Exception('Problem with finding fighter')

    return combined

def create_key(link, name):
    link = link.rsplit('/', 1)[-1]
    name = name.lower().replace(' ', '_')
    return link+name




class EventScraper():
    """Scrapes data for a specific event.
    Combines all the information from different links."""

    @staticmethod
    def read(url):
        """Reads content from an url
        :param url (string): url address"""
        with urlopen(url) as response:
            if response.status == 200:
                return response.read()

    def get(self, event_url):
        """Extracts data about specific event.
        It extracts every fight and every fighters data.
        :param event_url (string): event's url
        :return data (list): list of fights data"""
        # Read data from an url
        event_content = self.read(event_url)
        fights_links, fighters_links = scrape_links(event_content)
        # Collect and combine data from urls
        event = scrape_event_data(event_content)
        fights = {}
        for i, link in enumerate(fights_links):
            content = self.read(link)
            currents = scrape_fight_data(content, link, i+1)
            for current in currents:
                if 'name' in current:
                    key = current['name']
                    fights[create_key(link, key)] = current
        fighters = {}
        for link in fighters_links:
            content = self.read(link)
            currents = scrape_fighter_data(content, link)
            for current in currents:
                key = current['name']
                fighters[key] = current

        data = combine_data(event, fights, fighters)
        return data

if __name__ == '__main__':
    links = pd.read_csv('../data/events.csv')
    scraped = pd.read_csv('../data/data.csv')
    data = []
    scraper = EventScraper()
    for i, row in links.iterrows():
        try:
            if not row['scraped']:
                print(f'Downloading {i+1} out of {len(links)}: {row["link"]}')
                current = scraper.get(row['link'])
                data.extend(current)
                links.loc[i, 'scraped'] = True
        except Exception as e:
            print(f'App thrown an exception {e}')
        finally:
            links.to_csv('../data/events.csv', index=False)
            frame = pd.DataFrame(data)
            frame = frame.append(scraped)
            frame.to_csv('../data/data.csv', index=False)
