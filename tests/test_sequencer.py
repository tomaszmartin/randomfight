import datetime
from pprint import pprint
from fightmetric.sequencer import Sequencer

def test_returning_fighters():
    """Checks if sequencer extracts correct fighters."""
    fighters = [{'name': 'Tyron Woodley'},
                {'name': 'Demian Maia'},
                {'name': 'Demian Maia'}]
    sequencer = Sequencer()
    sequencer.fit(fighters)
    assert sequencer.get_fighters() == ['Tyron Woodley',
                                        'Demian Maia']

def test_no_fighters():
    fighters = []
    sequencer = Sequencer()
    sequencer.fit(fighters)
    assert sequencer.get_fighters() == []

def test_empty_stats():
    sequencer = Sequencer()
    data = sequencer.fit_transform([])
    assert data == []

def test_build_pre_fight_stats(sample_scraped_fight):
    sequencer = Sequencer()
    sequenced = sequencer.build_fighter_stats([sample_scraped_fight])
    pprint(sequenced)
    assert sequenced == [{'date': datetime.date(2008, 6, 15),
                          'event': 'DREAM 4: Middleweight Grand Prix 2008 2nd Round',
                          'fighter': {'age': 32,
                                      'bonus': {'fight': 0, 'ko': 0, 'performance': 0, 'submission': 0},
                                      'current': {'attendance': 14037.0, 'position': 1, 'rounds': (10, 5)},
                                      'height': 5.9,
                                      'history': {'attendance': 0.0, 'draws': 0, 'fights': 0, 'losses': 0,
                                                  'position': 0, 'time': 0.0, 'titlefights': 0, 'wins': 0},
                                      'name': 'Melvin Manhoef',
                                      'reach': None,
                                      'stance': 'Orthodox',
                                      'stats': {'body': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'clinch': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'distance': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'ground': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'head': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'knockouts': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'leg': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'sig. str': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'submissions': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'td': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'total str.': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0}},
                                      'streak': {'losses': 0, 'wins': 0},
                                      'weight': 185.0},
                          'link': 'http://www.fightmetric.com/fight-details/4cf4ed1edc8a0b24',
                          'location': 'Yokohama, Kanagawa, Japan',
                          'method': 'KO/TKO',
                          'referee': 'Yuji Shimada',
                          'result': 'Win'}]

def test_build_fight_stats(sample_scraped_fight):
    sequencer = Sequencer()
    sequenced = sequencer.build_fighter_stats([sample_scraped_fight, sample_scraped_fight])
    pprint(sequenced)
    assert sequenced == [{'date': datetime.date(2008, 6, 15),
                          'event': 'DREAM 4: Middleweight Grand Prix 2008 2nd Round',
                          'fighter': {'age': 32,
                                      'bonus': {'fight': 0, 'ko': 0, 'performance': 0, 'submission': 0},
                                      'current': {'attendance': 14037.0, 'position': 1, 'rounds': (10, 5)},
                                      'height': 5.9,
                                      'history': {'attendance': 0.0, 'draws': 0, 'fights': 0, 'losses': 0,
                                                  'position': 0, 'time': 0.0, 'titlefights': 0, 'wins': 0},
                                      'name': 'Melvin Manhoef',
                                      'reach': None,
                                      'stance': 'Orthodox',
                                      'stats': {'body': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'clinch': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'distance': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'ground': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'head': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'knockouts': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'leg': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'sig. str': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'submissions': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'td': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'total str.': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0}},
                                      'streak': {'losses': 0, 'wins': 0},
                                      'weight': 185.0},
                          'link': 'http://www.fightmetric.com/fight-details/4cf4ed1edc8a0b24',
                          'location': 'Yokohama, Kanagawa, Japan',
                          'method': 'KO/TKO',
                          'referee': 'Yuji Shimada',
                          'result': 'Win'},
                         {'date': datetime.date(2008, 6, 15),
                          'event': 'DREAM 4: Middleweight Grand Prix 2008 2nd Round',
                          'fighter': {'age': 32,
                                      'bonus': {'fight': 0, 'ko': 0, 'performance': 0, 'submission': 0},
                                      'current': {'attendance': 14037.0, 'position': 1, 'rounds': (10, 5)},
                                      'height': 5.9,
                                      'history': {'attendance': 14037.0, 'draws': 0, 'fights': 1, 'losses': 0,
                                                  'position': 1, 'time': 1.5, 'titlefights': 0, 'wins': 1},
                                      'name': 'Melvin Manhoef',
                                      'reach': None,
                                      'stance': 'Orthodox',
                                      'stats': {'body': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'clinch': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'distance': {'avoided': 1.0, 'landed': 2.0, 'received': 0.0, 'thrown': 4.0},
                                                'ground': {'avoided': 0.0, 'landed': 19.0, 'received': 0.0, 'thrown': 27.0},
                                                'head': {'avoided': 1.0, 'landed': 21.0, 'received': 0.0, 'thrown': 31.0},
                                                'knockouts': {'avoided': 0.0, 'landed': 1.0, 'received': 0.0, 'thrown': 1.0},
                                                'leg': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'sig. str': {'avoided': 1.0, 'landed': 21.0, 'received': 0.0, 'thrown': 31.0},
                                                'submissions': {'avoided': 0.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'td': {'avoided': 1.0, 'landed': 0.0, 'received': 0.0, 'thrown': 0.0},
                                                'total str.': {'avoided': 1.0, 'landed': 23.0, 'received': 0.0, 'thrown': 34.0}},
                                      'streak': {'losses': 0, 'wins': 1},
                                      'weight': 185.0},
                          'link': 'http://www.fightmetric.com/fight-details/4cf4ed1edc8a0b24',
                          'location': 'Yokohama, Kanagawa, Japan',
                          'method': 'KO/TKO',
                          'referee': 'Yuji Shimada',
                          'result': 'Win'}]
