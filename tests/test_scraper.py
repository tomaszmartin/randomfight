from datetime import date
from fightmetric.scraper import (
    scrape_links,
    scrape_event_data,
    scrape_fight_data,
    scrape_fighter_data,
    combine_data,
)
from pprint import pprint

# Testing links scraping
def test_empty_links_scraping():
    """Checks if links scraping works correctly for empty html."""
    fights, fighters = scrape_links("")
    assert len(fights) == 0 and len(fighters) == 0


def test_unique_fighters_links():
    """Checks if links scraping extracts unique links."""
    content = """<a href="http://fightmetric.com/fighter-details/d967f0128c323de6"></a>
                 <a href="http://fightmetric.com/fighter-details/d967f0128c323de6"></a>"""
    _, fighters = scrape_links(content)
    assert len(fighters) == 1


def test_fighter_links_scraping(generate_links):
    """Checks if links scraping extracts correct number of links."""
    for i in range(5):
        content = generate_links(fights=1, fighters=i)
        _, fighters = scrape_links(content)
        assert len(fighters) == i


def test_links_scraping(sample_event):
    """Checks if link scraping behaves correctly on sample html."""
    fights, fighters = scrape_links(sample_event)
    assert len(fighters) == 24
    assert len(fights) == 12


# Testing event scraping
def test_event_scraping(sample_event):
    """Checks if event scraping behaves correctly on sample html."""
    event = scrape_event_data(sample_event)
    pprint(event)
    assert event == {
        "event": "UFC 214: Cormier vs. Jones 2",
        "date": date(2017, 7, 29),
        "location": "Anaheim, California, USA",
        "attendance": 16610.0,
    }


# Testng fights scraping
def test_fight_scraping(sample_fight):
    """Checks if fight scraping behaves correctly on sample html."""
    fight = scrape_fight_data(sample_fight, "sample_link", 1)
    from pprint import pprint

    pprint(fight)
    assert fight == [
        {
            "bonus": {
                "fight": False,
                "ko": False,
                "performance": False,
                "submission": False,
            },
            "link": "sample_link",
            "method": "Decision - Unanimous",
            "name": "Tyron Woodley",
            "position": 1,
            "referee": "Herb Dean",
            "result": "Win",
            "round": 5.0,
            "stats": {
                "body": {
                    "avoided": 1.0,
                    "landed": 13.0,
                    "received": 2.0,
                    "thrown": 18.0,
                },
                "clinch": {
                    "avoided": 0.0,
                    "landed": 1.0,
                    "received": 2.0,
                    "thrown": 1.0,
                },
                "distance": {
                    "avoided": 61.0,
                    "landed": 56.0,
                    "received": 26.0,
                    "thrown": 152.0,
                },
                "ground": {
                    "avoided": 0.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 0.0,
                },
                "head": {
                    "avoided": 60.0,
                    "landed": 40.0,
                    "received": 23.0,
                    "thrown": 131.0,
                },
                "knockouts": {
                    "avoided": 0.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 1.0,
                },
                "leg": {"avoided": 0.0, "landed": 4.0, "received": 3.0, "thrown": 4.0},
                "sig. str": {
                    "avoided": 61.0,
                    "landed": 57.0,
                    "received": 28.0,
                    "thrown": 153.0,
                },
                "submissions": {
                    "avoided": 0.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 0.0,
                },
                "td": {"avoided": 21.0, "landed": 0.0, "received": 0.0, "thrown": 0.0},
                "total str.": {
                    "avoided": 61.0,
                    "landed": 57.0,
                    "received": 29.0,
                    "thrown": 153.0,
                },
            },
            "time": 5.0,
            "time format": (10, 5, 5, 5, 5),
            "titlefight": True,
        },
        {
            "bonus": {
                "fight": False,
                "ko": False,
                "performance": False,
                "submission": False,
            },
            "link": "sample_link",
            "method": "Decision - Unanimous",
            "name": "Demian Maia",
            "position": 1,
            "referee": "Herb Dean",
            "result": "Loss",
            "round": 5.0,
            "stats": {
                "body": {
                    "avoided": 5.0,
                    "landed": 2.0,
                    "received": 13.0,
                    "thrown": 3.0,
                },
                "clinch": {
                    "avoided": 0.0,
                    "landed": 2.0,
                    "received": 1.0,
                    "thrown": 2.0,
                },
                "distance": {
                    "avoided": 96.0,
                    "landed": 26.0,
                    "received": 56.0,
                    "thrown": 87.0,
                },
                "ground": {
                    "avoided": 0.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 0.0,
                },
                "head": {
                    "avoided": 91.0,
                    "landed": 23.0,
                    "received": 40.0,
                    "thrown": 83.0,
                },
                "knockouts": {
                    "avoided": 1.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 0.0,
                },
                "leg": {"avoided": 0.0, "landed": 3.0, "received": 4.0, "thrown": 3.0},
                "sig. str": {
                    "avoided": 96.0,
                    "landed": 28.0,
                    "received": 57.0,
                    "thrown": 89.0,
                },
                "submissions": {
                    "avoided": 0.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 0.0,
                },
                "td": {"avoided": 0.0, "landed": 0.0, "received": 0.0, "thrown": 21.0},
                "total str.": {
                    "avoided": 96.0,
                    "landed": 29.0,
                    "received": 57.0,
                    "thrown": 90.0,
                },
            },
            "time": 5.0,
            "time format": (10, 5, 5, 5, 5),
            "titlefight": True,
        },
    ]


# Testing fighters scraping
def test_fighter_scraping(sample_fighter):
    """Checks if fighter scraping behaves correctly on sample html."""
    fighter = scrape_fighter_data(sample_fighter, "sample_link")
    from pprint import pprint

    pprint(fighter)
    assert fighter == [
        {
            "name": "Demian Maia",
            "height": 6.1,
            "reach": 72.0,
            "weight": 170.0,
            "stance": "Southpaw",
            "birth": date(1977, 11, 6),
        }
    ]


# Testing combining data
def test_combine_data(sample_event, sample_fighter, sample_opponent, sample_fight):
    fighter = scrape_fighter_data(sample_fighter, "sample_link")[0]
    opponent = scrape_fighter_data(sample_opponent, "sample_link")[0]
    fighters = {fighter["name"]: fighter, opponent["name"]: opponent}
    fights = {
        data["name"]: data for data in scrape_fight_data(sample_fight, "sample_link", 1)
    }
    event = scrape_event_data(sample_event)
    data = combine_data(event, fights, fighters)
    from pprint import pprint

    pprint(data)
    assert data == [
        {
            "attendance": 16610.0,
            "birth": date(1982, 4, 7),
            "bonus": {
                "fight": False,
                "ko": False,
                "performance": False,
                "submission": False,
            },
            "date": date(2017, 7, 29),
            "event": "UFC 214: Cormier vs. Jones 2",
            "height": 5.9,
            "link": "sample_link",
            "location": "Anaheim, California, USA",
            "method": "Decision - Unanimous",
            "name": "Tyron Woodley",
            "position": 1,
            "reach": 74.0,
            "referee": "Herb Dean",
            "result": "Win",
            "round": 5.0,
            "stance": "Orthodox",
            "stats": {
                "body": {
                    "avoided": 1.0,
                    "landed": 13.0,
                    "received": 2.0,
                    "thrown": 18.0,
                },
                "clinch": {
                    "avoided": 0.0,
                    "landed": 1.0,
                    "received": 2.0,
                    "thrown": 1.0,
                },
                "distance": {
                    "avoided": 61.0,
                    "landed": 56.0,
                    "received": 26.0,
                    "thrown": 152.0,
                },
                "ground": {
                    "avoided": 0.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 0.0,
                },
                "head": {
                    "avoided": 60.0,
                    "landed": 40.0,
                    "received": 23.0,
                    "thrown": 131.0,
                },
                "knockouts": {
                    "avoided": 0.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 1.0,
                },
                "leg": {"avoided": 0.0, "landed": 4.0, "received": 3.0, "thrown": 4.0},
                "sig. str": {
                    "avoided": 61.0,
                    "landed": 57.0,
                    "received": 28.0,
                    "thrown": 153.0,
                },
                "submissions": {
                    "avoided": 0.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 0.0,
                },
                "td": {"avoided": 21.0, "landed": 0.0, "received": 0.0, "thrown": 0.0},
                "total str.": {
                    "avoided": 61.0,
                    "landed": 57.0,
                    "received": 29.0,
                    "thrown": 153.0,
                },
            },
            "time": 5.0,
            "time format": (10, 5, 5, 5, 5),
            "titlefight": True,
            "weight": 170.0,
        },
        {
            "attendance": 16610.0,
            "birth": date(1977, 11, 6),
            "bonus": {
                "fight": False,
                "ko": False,
                "performance": False,
                "submission": False,
            },
            "date": date(2017, 7, 29),
            "event": "UFC 214: Cormier vs. Jones 2",
            "height": 6.1,
            "link": "sample_link",
            "location": "Anaheim, California, USA",
            "method": "Decision - Unanimous",
            "name": "Demian Maia",
            "position": 1,
            "reach": 72.0,
            "referee": "Herb Dean",
            "result": "Loss",
            "round": 5.0,
            "stance": "Southpaw",
            "stats": {
                "body": {
                    "avoided": 5.0,
                    "landed": 2.0,
                    "received": 13.0,
                    "thrown": 3.0,
                },
                "clinch": {
                    "avoided": 0.0,
                    "landed": 2.0,
                    "received": 1.0,
                    "thrown": 2.0,
                },
                "distance": {
                    "avoided": 96.0,
                    "landed": 26.0,
                    "received": 56.0,
                    "thrown": 87.0,
                },
                "ground": {
                    "avoided": 0.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 0.0,
                },
                "head": {
                    "avoided": 91.0,
                    "landed": 23.0,
                    "received": 40.0,
                    "thrown": 83.0,
                },
                "knockouts": {
                    "avoided": 1.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 0.0,
                },
                "leg": {"avoided": 0.0, "landed": 3.0, "received": 4.0, "thrown": 3.0},
                "sig. str": {
                    "avoided": 96.0,
                    "landed": 28.0,
                    "received": 57.0,
                    "thrown": 89.0,
                },
                "submissions": {
                    "avoided": 0.0,
                    "landed": 0.0,
                    "received": 0.0,
                    "thrown": 0.0,
                },
                "td": {"avoided": 0.0, "landed": 0.0, "received": 0.0, "thrown": 21.0},
                "total str.": {
                    "avoided": 96.0,
                    "landed": 29.0,
                    "received": 57.0,
                    "thrown": 90.0,
                },
            },
            "time": 5.0,
            "time format": (10, 5, 5, 5, 5),
            "titlefight": True,
            "weight": 170.0,
        },
    ]
