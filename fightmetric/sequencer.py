"""Responsible for sequencing fights data in time."""
from ast import literal_eval
import copy
import datetime
import json
from pprint import pprint
import pandas as pd


class Sequencer():
    """Transforms fights stats into sequences of pre fight stats."""


    def __init__(self):
        self.data = None


    def fit(self, data):
        """Saves the data for transformation."""
        self.data = pd.DataFrame(data)
        self.impute_attendance()
        self.fill_attendance()


    def get_fights_for_fighter(self, name):
        """Extracts all fights for a specific fighter."""
        fights = self.data[self.data['name'] == name]
        fights_list = fights.T.to_dict().values()
        # Sort fights from oldest to earliest
        return sorted(fights_list, key=lambda x: x['date'])


    def impute_attendance(self):
        filled = self.data.dropna(subset=['attendance'])
        filled['year'] = filled['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').year)
        grouped = filled.groupby(['year']).mean()
        self.attendance = grouped.drop(['height', 'position', 'reach',
                                        'round', 'time', 'titlefight',
                                        'weight'], axis=1)


    def fill_attendance(self):
        """Attendence is imputed as the average for the current year."""
        self.data['year'] = self.data['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').year)
        avg_attendance = self.data['year'].apply(lambda x: self.attendance.ix[int(x)]['attendance'])
        self.data['attendance'].fillna(avg_attendance, inplace=True)
        self.data = self.data.drop(['year'], axis=1)


    def get_fighters(self):
        """Returns a list of fighter's names."""
        return self.data['name'].unique().tolist()


    @staticmethod
    def fight_to_dict(fight):
        data = copy.deepcopy(fight)
        data['stats'] = json.loads(data['stats'].replace("'", "\""))
        data['bonus'] = json.loads(data['bonus'].replace('False', 'false').replace('True', 'true').replace("'", "\""))
        data['date'] = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
        try:
            data['birth'] = datetime.datetime.strptime(data['birth'], '%Y-%m-%d').date()
        except:
            data['birth'] = None
        data['time format'] = literal_eval(data['time format'])
        return data


    @staticmethod
    def age(born_at, fight_at):
        if born_at is None or fight_at is None:
            return None
        return fight_at.year - born_at.year - ((fight_at.month, fight_at.day) < (born_at.month, born_at.day))


    def build_fighter_stats(self, list_of_fights):
        """Creates a list of fighters fights, with stats on the day before the fight."""
        stats = []
        for i, current_fight in enumerate(list_of_fights):
            current_fight = self.fight_to_dict(current_fight)
            if i == 0:
                stats.append({'fighter': {'stats': {}, 'bonus': {}}})
                for key in current_fight['stats']:
                    stats[i]['fighter']['stats'][key] = {}
                    for attr in current_fight['stats'][key]:
                        stats[i]['fighter']['stats'][key][attr] = 0.0
                for key in current_fight['bonus']:
                    stats[i]['fighter']['bonus'][key] = 0
                stats[i]['fighter']['current'] = {'attendance': current_fight['attendance'],
                                       'position': current_fight['position'],
                                       'rounds': current_fight['time format']}
                stats[i]['fighter']['history'] = {'attendance': 0.0,
                                       'position': 0,
                                       'time': 0.0,
                                       'wins': 0,
                                       'losses': 0,
                                       'draws': 0,
                                       'titlefights': 0,
                                       'fights': 0}
                stats[i]['fighter']['streak'] = {'wins': 0,
                                      'losses': 0}
            if i > 0:
                previous_fight = self.fight_to_dict(list_of_fights[i-1])
                stats.append(copy.deepcopy(stats[i-1]))
                for key in current_fight['stats']:
                    for attr in current_fight['stats'][key]:
                        stats[i]['fighter']['stats'][key][attr] += previous_fight['stats'][key][attr]
                for key in current_fight['bonus']:
                    if previous_fight['bonus'][key]:
                        stats[i]['fighter']['bonus'][key] += 1

                stats[i]['fighter']['current'] = {'attendance': current_fight['attendance'],
                                       'position': current_fight['position'],
                                       'rounds': current_fight['time format']}
                stats[i]['fighter']['history']['fights'] += 1
                stats[i]['fighter']['history']['attendance'] += previous_fight['attendance']
                stats[i]['fighter']['history']['position'] += previous_fight['position']
                stats[i]['fighter']['history']['time'] += previous_fight['time']
                for round in range(int(previous_fight['round']-1)):
                    stats[i]['fighter']['history']['time'] += round
                if previous_fight['result'] == 'Win':
                    stats[i]['fighter']['history']['wins'] += 1
                    stats[i]['fighter']['streak']['wins'] += 1
                    stats[i]['fighter']['streak']['losses'] = 0
                elif previous_fight['result'] == 'Loss':
                    stats[i]['fighter']['history']['losses'] += 1
                    stats[i]['fighter']['streak']['wins'] = 0
                    stats[i]['fighter']['streak']['losses'] += 1
                else:
                    stats[i]['fighter']['history']['draws'] += 1
                    stats[i]['fighter']['streak']['wins'] = 0
                    stats[i]['fighter']['streak']['losses'] = 0
                if previous_fight['titlefight']:
                    stats[i]['fighter']['history']['titlefights'] += 1

            # All stats
            stats[i]['fighter']['age'] = self.age(current_fight['birth'], current_fight['date'])
            stats[i]['event'] = current_fight['event']
            stats[i]['link'] = current_fight['link']
            stats[i]['fighter']['height'] = current_fight['height']
            stats[i]['location'] = current_fight['location']
            stats[i]['fighter']['weight'] = current_fight['weight']
            stats[i]['result'] = current_fight['result']
            stats[i]['method'] = current_fight['method']
            stats[i]['fighter']['name'] = current_fight['name']
            stats[i]['fighter']['reach'] = current_fight['reach']
            stats[i]['referee'] = current_fight['referee']
            stats[i]['fighter']['stance'] = current_fight['stance']
            stats[i]['date'] = current_fight['date']
        return stats


    @staticmethod
    def exchange_stats(data):
        links = list(set([row['link'] for row in data]))
        for link in links:
            pair = []
            for row in data:
                if row['link'] == link:
                    pair.append(row)
            fighter, opponent = pair
            fighter['opponent'] = opponent['fighter']
            opponent['opponent'] = fighter['fighter']
        return data


    def transform(self):
        """Transforms fight stats into sequences."""
        stats = []
        for fighter in self.get_fighters():
            fights = self.get_fights_for_fighter(fighter)
            current = self.build_fighter_stats(fights)
            stats.extend(current)
        return self.exchange_stats(stats)


    def fit_transform(self, data):
        """Transforms fight stats into sequences."""
        self.fit(data)
        return self.transform()


if __name__ == '__main__':
    seq = Sequencer()
    raw = pd.read_csv('data/data.csv')
    transformed = seq.fit_transform(raw)
    pd.DataFrame.from_records(transformed).to_json('data/imputed.json')
