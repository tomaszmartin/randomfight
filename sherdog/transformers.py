"""Responsible for sequencing fights data in time."""
from ast import literal_eval
import copy
from datetime import datetime as dt
import json
from pprint import pprint
import pandas as pd
import time


class Sequencer():
    """Transforms fights stats into sequences of pre fight stats."""

    def __init__(self):
        self.data = None

    def fit(self, data):
        """Saves the data for transformation."""
        data = pd.DataFrame(data)
        self.data = self.enrich(data)

    def get_fights_for_fighter(self, name):
        """Extracts all fights for a specific fighter."""
        fights = self.data[self.data['fighter'] == name]
        fights_list = fights.T.to_dict().values()
        # Sort fights from oldest to earliest
        result = sorted(fights_list, key=lambda x: dt.strptime(x['date'], '%Y-%m-%d'))
        return result

    def get_fighters(self):
        """Returns a list of fighter's names."""
        return self.data['fighter'].unique().tolist()

    def enrich(self, data):
        data['id'] = data['fighter'] + data['opponent'] + data['title']
        opponent = data.copy()
        opponent.rename(columns={
            'fighter': 'opponent_',
            'fighter association': 'opponent_ association',
            'fighter birth': 'opponent_ birth',
            'fighter height': 'opponent_ height',
            'fighter nationality': 'opponent_ nationality',
            'opponent': 'fighter',
            'opponent association': 'fighter association',
            'opponent birth': 'fighter birth',
            'opponent height': 'fighter height',
            'opponent nationality': 'fighter nationality',
        }, inplace=True)
        opponent.rename(columns={
            'opponent_': 'opponent',
            'opponent_ association': 'opponent association',
            'opponent_ birth': 'opponent birth',
            'opponent_ height': 'opponent height',
            'opponent_ nationality': 'opponent nationality',
        }, inplace=True)
        opponent['result'] = 'loss'
        data = data.append(opponent)
        data = data.sort_values(by=['fighter'])

        return data

    @staticmethod
    def parse_date(x):
        return dt.strptime(x, '%Y-%m-%d').date()

    def build_stats(self, fights):
        """Creates a list of fighters fights, with stats on the day before the fight."""
        stats = []
        for i, current_fight in enumerate(fights):
            try:
                current = {
                    'id': current_fight['id'],
                    'date': ['date'],
                    'location': current_fight['location'],
                    'organization': current_fight['organization'],
                    'fighter': {
                        'started': current_fight['date'],
                        'birth': current_fight['fighter birth'],
                        'association': current_fight['fighter association'],
                        'nationality': current_fight['fighter nationality'],
                        'id': current_fight['fighter'],
                        'history': {
                            'win': {
                                'total': 0.0,
                                'decision': 0.0,
                                'submission': 0.0,
                                'knockout': 0.0
                            },
                            'loss': {
                                'total': 0.0,
                                'decision': 0.0,
                                'submission': 0.0,
                                'knockout': 0.0,
                            },
                            'since_last_fight': 0,
                            'fights': 0.0,
                            'time': 0.0,
                            'positions': 0.0,
                        },
                        'streak': {
                            'win': 0.0,
                            'loss': 0.0
                        },
                    },
                    'result': current_fight['result'],
                    'method': current_fight['method'],
                    'details': current_fight['details'],
                }
                if i > 0:
                    # Copt information form previous fights
                    current = copy.deepcopy(stats[i-1])
                    previous_fight = fights[i-1]
                    # Update stats with current information
                    current['id'] = current_fight['id']
                    current['date'] = self.parse_date(current_fight['date'])
                    for key in ['location', 'result', 'method', 'details', 'organization']:
                        current[key] = current_fight[key]

                    # Add result from past fight
                    result = previous_fight['result'].lower()
                    current['fighter']['history'][result]['total'] += 1.0
                    if result == 'win':
                        current['fighter']['streak']['win'] += 1.0
                        current['fighter']['streak']['loss'] = 0.0
                    else:
                        current['fighter']['streak']['loss'] += 1.0
                        current['fighter']['streak']['win'] = 0.0
                    method = 'decision'
                    knockout_flags = ['ko', 'punches', 'knockout', 'cut', 'towel']
                    for flag in knockout_flags:
                        if flag in str(previous_fight['method']):
                            method = 'knockout'
                    submission_flags = ['sub', 'mata', 'armbar', 'choke', 'isaac',
                                        'tapout', 'ubmission', 'forfeit']
                    for flag in submission_flags:
                        if flag in str(previous_fight['method']):
                            method = 'submission'
                    current['fighter']['history'][result][method] += 1.0

                    # Add stats
                    current['fighter']'history']['since_last_fight'] = (current['date'] - stats[i-1]['date']).days
                    current['fighter']['history']['fights'] += 1.0
                    current['fighter']['history']['time'] += float(previous_fight['time']) * float(previous_fight['position'])
                    current['fighter']['history']['positions'] += float(previous_fight['position'])

                    assert current['fighter']['history']['since_last_fight'] > 0
                    assert current['fighter']['history']['fights'] < 100
                stats.append(current)
            except Exception as exc:
                print(exc)
                pprint(stats)
                raise exc

        print([s['fighter']['history'] for s in stats])
        if (len(stats) > 10):
            pprint(stats)
            exit()
        return stats

    def exchange(self, data):
        ids = list(set([row['id'] for row in data]))
        result = []
        start = time.time()
        for i, current in enumerate(ids):
            if (i % 1000 == 0):
                print('Exchenging data {} from {} in {:.2f}'.format(i, len(ids), time.time() - start))
                start = time.time()
            try:
                pair = []
                for row in data:
                    if row['id'] == current:
                        pair.append(row)
                fighter, opponent = pair
                fighter['opponent'] = opponent['fighter']
                opponent['opponent'] = fighter['fighter']
                result.extend(pair)
            except:
                pass
        return result

    def transform(self):
        """Transforms fight stats into sequences."""
        self.transformed = []
        fighters = self.get_fighters()
        start = time.time()
        for i, fighter in enumerate(fighters):
            if (i % 1000 == 0):
                print('Working on {} fighter out of {} in {:.2f}'.format(i, len(fighters), time.time() - start))
                start = time.time()
            fights = self.get_fights_for_fighter(fighter)
            current = self.build_stats(fights)
            self.transformed.extend(current)
        return self.transformed

    def fit_transform(self, data):
        """Transforms fight stats into sequences."""
        self.fit(data)
        return self.transform()


class Cumulator(Sequencer):

    def fit(self, data):
        """Saves the data for transformation."""
        self.data = pd.DataFrame(data)

    def get_fighters(self):
        """Returns a list of fighter's names."""
        fighter_ids = self.data['fighter'].apply(lambda x: x['id'])
        return fighter_ids.unique().tolist()

    def get_fights_for_fighter(self, name):
        """Extracts all fights for a specific fighter."""
        self.data['fighterid'] = self.data['fighter'].apply(lambda x: x['id'])
        fights = self.data[self.data['fighterid'] == name]
        fights_list = fights.T.to_dict().values()
        # Sort fights from oldest to earliest
        result = sorted(fights_list, key=lambda x: x['date'])
        return result

    def build_stats(self, fights):
        """Build cumulative stats for fighter."""
        stats = []
        raw = {
            'win': {
                'win': { 'total': 0.0, 'decision': 0.0, 'submission': 0.0, 'knockout': 0.0},
                'loss': {'total': 0.0, 'decision': 0.0, 'submission': 0.0, 'knockout': 0.0},
            }, 'loss': {
                'win': { 'total': 0.0, 'decision': 0.0, 'submission': 0.0, 'knockout': 0.0},
                'loss': {'total': 0.0, 'decision': 0.0, 'submission': 0.0, 'knockout': 0.0},
            }
        }
        for i, fight in enumerate(fights):
            fight = copy.deepcopy(fight)
            if i == 0:
                fight['fighter']['cumulative'] = raw
                stats.append(fight)
            else:
                fight['fighter']['cumulative'] = copy.deepcopy(stats[i-1]['fighter']['cumulative'])
                previous = stats[i-1]
                result = previous['result'].lower()
                for key in fight['fighter']['cumulative'][result].keys():
                    for subkey, value in fight['fighter']['cumulative'][result][key].items():
                        fight['fighter']['cumulative'][result][key][subkey] += previous['fighter']['history'][key][subkey]
                stats.append(fight)

        return stats

    def transform(self):
        """Transforms fight stats into sequences."""
        self.transformed = []
        fighters = self.get_fighters()
        start = time.time()
        for i, fighter in enumerate(fighters):
            if (i % 1000 == 0):
                print('Working on {} fighter out of {} in {:.2f}'.format(i, len(fighters), time.time() - start))
                start = time.time()
            fights = self.get_fights_for_fighter(fighter)
            current = self.build_stats(fights)
            self.transformed.extend(current) # not append!
        return self.transformed


if __name__ == '__main__':
    transformer = Sequencer()
    data = pd.read_csv('data/merged.csv')
    data = data[data['result'].isin['win', loss]]
    transformed = transformer.fit_transform(data)
    frame = pd.DataFrame.from_records(transformed)
    frame.to_json('data/transformed2.json')
    exchanged = transformer.exchange(transformed)
    final = pd.DataFrame.from_records(exchanged)
    final.to_json('data/transformed_exchanged2.json')

    # transformer = Cumulator()
    # data = pd.read_json('data/final.json')
    # transformed = transformer.fit_transform(data)
    # transformed_df = pd.DataFrame.from_records(transformed)
    # transformed_df.to_json('data/partial-cumulative.json')
    # exchanged = transformer.exchange(transformed)
    # final = pd.DataFrame.from_records(exchanged)
    # final.to_json('data/cumulative.json')
