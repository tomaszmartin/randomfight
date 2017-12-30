"""Responsible for sequencing fights data in time."""
from ast import literal_eval
import copy
from datetime import datetime as dt
import json
from pprint import pprint
import pandas as pd


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
        result = sorted(fights_list, key=lambda x: x['date'])
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
        try:
            return dt.strptime(x, '%d.%m.%Y').date()
        except:
            return None

    @staticmethod
    def to_float(number):
        map = {
            'sty': 1, 'lut': 2, 'mar': 3, 'kwi': 4, 'maj': 5, 'cze': 6,
            'lip': 7, 'sie': 8, 'wrz': 9, 'pa\x90': 10, 'lis': 11, 'gru': 12
        }
        try:
            return float(number)
        except ValueError:
            big = str(number).split('.')[0]
            small = str(number).split('.')[1]
            if big.isdigit():
                big = float(big)
            else:
                big = float(map[big])
            if small.isdigit():
                small = float(small) / 10
            else:
                small = float(map[small]) / 10
            if small > 1:
                small = small / 10
            return big + small

    def build_stats(self, fights):
        """Creates a list of fighters fights, with stats on the day before the fight."""
        stats = []
        for i, current_fight in enumerate(fights):
            current = {
                'id': current_fight['id'],
                'date': self.parse_date(current_fight['date']),
                'location': current_fight['location'],
                'fighter': {
                    'started': self.parse_date(current_fight['date']),
                    'birth': self.parse_date(current_fight['fighter birth']),
                    'association': self.parse_date(current_fight['fighter association']),
                    'nationality': self.parse_date(current_fight['fighter nationality']),
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
                        'fights': 0.0,
                        'time': 0.0,
                        'positions': 0.0,
                    }
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
                for key in ['location', 'result', 'method', 'details']:
                    current[key] = current_fight[key]

                # Add result from plast fight
                result = previous_fight['result']
                current['fighter']['history'][result]['total'] += 1
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
                current['fighter']['history'][result][method] += 1

                # Add stats
                current['fighter']['history']['fights'] += 1
                current['fighter']['history']['time'] += self.to_float(previous_fight['time'])
                current['fighter']['history']['positions'] += self.to_float(previous_fight['position'])
            stats.append(current)

        return stats

    def exchange(self, data):
        ids = list(set([row['id'] for row in data]))
        result = []
        for current in ids:
            try:
                pair = []
                for row in data:
                    if row['id'] == current:
                        print(current)
                        pair.append(row)
                fighter, opponent = pair
                fighter['opponent'] = opponent['fighter']
                opponent['opponent'] = fighter['fighter']
                result.extend(pair)
            except:
                pass
        return result

        frame = pd.DataFrame(e(t))

    def transform(self):
        """Transforms fight stats into sequences."""
        self.transformed = []
        fighters = self.get_fighters()
        for i, fighter in enumerate(fighters):
            print('Working on {} fighter out of {}'.format(i, len(fighters)))
            fights = self.get_fights_for_fighter(fighter)
            current = self.build_stats(fights)
            self.transformed.extend(current)
        return self.exchange(self.transformed)

    def fit_transform(self, data):
        """Transforms fight stats into sequences."""
        self.fit(data)
        return self.transform()


class Cumulator(Sequencer):

    def build_stats(self, fights):
        """Build cumulative stats for fighter."""
        stats = []
        for i, fight in enumerate(fights):
            pass
        return stats

    def transform(self):
        """Transforms fight stats into sequences."""
        self.transformed = []
        fighters = self.get_fighters()
        for i, fighter in enumerate(fighters):
            print('Working on {} fighter out of {}'.format(i, len(fighters)))
            fights = self.get_fights_for_fighter(fighter)
            current = self.build_stats(fights)
            self.transformed.extend(current)

        return self.transformed


if __name__ == '__main__':
    transformer = Cumulator()
    data = pd.read_json('data/transformed.json')
    transformed = transformer.fit_transform(data)
    transformed = pd.DataFrame.from_records(transformed)
    transformed.to_json('data/cumulative.json')
