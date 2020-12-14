import datetime as dt

from bs4 import BeautifulSoup
import pandas as pd

from app.parsers import sherdog


def test_event_parsing(sherdog_event):
    page_content, page_url = sherdog_event
    event_data = sherdog.extract_event_data(page_content, page_url)
    assert event_data == {
        "title": "UFC 214 Cormier vs. Jones 2",
        "organization": "Ultimate Fighting Championship (UFC)",
        "date": dt.date(2017, 7, 29),
        "location": "Honda Center / Anaheim / California / United States",
        "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
    }


def test_main_fight_parsing(sherdog_event):
    page_content, _ = sherdog_event
    soup = BeautifulSoup(page_content, "lxml")
    fights = sherdog._extract_main_fight_from_event(soup)
    assert fights == {
        "method": "no contest",
        "details": "overturned by csac",
        "result": "nc",
        "rounds": 3,
        "time": 13.016666666666666,
        "fighter": "http://www.sherdog.com/fighter/Jon-Jones-27944",
        "opponent": "http://www.sherdog.com/fighter/Daniel-Cormier-52311",
        "position": 1,
    }


def test_other_fights_parsing(sherdog_event):
    page_content, _ = sherdog_event
    soup = BeautifulSoup(page_content, "lxml")
    fights = sherdog._extract_other_fights_from_event(soup)
    assert fights == [
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 5,
            "time": 25.0,
            "fighter": "http://www.sherdog.com/fighter/Tyron-Woodley-42605",
            "opponent": "http://www.sherdog.com/fighter/Demian-Maia-14637",
            "position": 2,
        },
        {
            "method": "tko",
            "details": "knees",
            "result": "win",
            "rounds": 3,
            "time": 11.933333333333334,
            "fighter": "http://www.sherdog.com/fighter/Cristiane-Justino-14477",
            "opponent": "http://www.sherdog.com/fighter/Tonya-Evinger-18248",
            "position": 3,
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Robbie-Lawler-2245",
            "opponent": "http://www.sherdog.com/fighter/Donald-Cerrone-15105",
            "position": 4,
        },
        {
            "method": "ko",
            "details": "punches",
            "result": "win",
            "rounds": 1,
            "time": 0.7,
            "fighter": "http://www.sherdog.com/fighter/Volkan-Oezdemir-58503",
            "opponent": "http://www.sherdog.com/fighter/Jimi-Manuwa-37528",
            "position": 5,
        },
        {
            "method": "tko",
            "details": "punches",
            "result": "win",
            "rounds": 1,
            "time": 4.566666666666666,
            "fighter": "http://www.sherdog.com/fighter/Ricardo-Lamas-32051",
            "opponent": "http://www.sherdog.com/fighter/Jason-Knight-44957",
            "position": 6,
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Aljamain-Sterling-66313",
            "opponent": "http://www.sherdog.com/fighter/Renan-Barao-23156",
            "position": 7,
        },
        {
            "method": "submission",
            "details": "guillotine choke",
            "result": "win",
            "rounds": 3,
            "time": 12.983333333333334,
            "fighter": "http://www.sherdog.com/fighter/Brian-Ortega-65310",
            "opponent": "http://www.sherdog.com/fighter/Renato-Carneiro-61700",
            "position": 8,
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Calvin-Kattar-23782",
            "opponent": "http://www.sherdog.com/fighter/Andre-Fili-58385",
            "position": 9,
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Aleksandra-Albu-144949",
            "opponent": "http://www.sherdog.com/fighter/Kailin-Curran-62703",
            "position": 10,
        },
        {
            "method": "decision",
            "details": "split",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Jarred-Brooks-174665",
            "opponent": "http://www.sherdog.com/fighter/Eric-Shelton-86414",
            "position": 11,
        },
        {
            "method": "ko",
            "details": "punch",
            "result": "win",
            "rounds": 1,
            "time": 3.066666666666667,
            "fighter": "http://www.sherdog.com/fighter/Drew-Dober-23982",
            "opponent": "http://www.sherdog.com/fighter/Joshua-Burkman-10003",
            "position": 12,
        },
    ]


def test_fights_parsing(sherdog_event):
    page_content, page_url = sherdog_event
    fights = sherdog.extract_fights(page_content, page_url)
    assert fights == [
        {
            "method": "no contest",
            "details": "overturned by csac",
            "result": "nc",
            "rounds": 3,
            "time": 13.016666666666666,
            "fighter": "http://www.sherdog.com/fighter/Jon-Jones-27944",
            "opponent": "http://www.sherdog.com/fighter/Daniel-Cormier-52311",
            "position": 1,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "3cda3aefbd92cf77156efcd4bbbd0723",
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 5,
            "time": 25.0,
            "fighter": "http://www.sherdog.com/fighter/Tyron-Woodley-42605",
            "opponent": "http://www.sherdog.com/fighter/Demian-Maia-14637",
            "position": 2,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "125e438263086c8f3d0f469a815720ff",
        },
        {
            "method": "tko",
            "details": "knees",
            "result": "win",
            "rounds": 3,
            "time": 11.933333333333334,
            "fighter": "http://www.sherdog.com/fighter/Cristiane-Justino-14477",
            "opponent": "http://www.sherdog.com/fighter/Tonya-Evinger-18248",
            "position": 3,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "4da8792140df9e0c36ea83f18611b25b",
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Robbie-Lawler-2245",
            "opponent": "http://www.sherdog.com/fighter/Donald-Cerrone-15105",
            "position": 4,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "a6456a74295f38e27b6cbacbd521bceb",
        },
        {
            "method": "ko",
            "details": "punches",
            "result": "win",
            "rounds": 1,
            "time": 0.7,
            "fighter": "http://www.sherdog.com/fighter/Volkan-Oezdemir-58503",
            "opponent": "http://www.sherdog.com/fighter/Jimi-Manuwa-37528",
            "position": 5,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "64e4b168f12b54fa952d1f955312f3b6",
        },
        {
            "method": "tko",
            "details": "punches",
            "result": "win",
            "rounds": 1,
            "time": 4.566666666666666,
            "fighter": "http://www.sherdog.com/fighter/Ricardo-Lamas-32051",
            "opponent": "http://www.sherdog.com/fighter/Jason-Knight-44957",
            "position": 6,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "97f54afbfa1c0ba3bbb5a92e0592f808",
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Aljamain-Sterling-66313",
            "opponent": "http://www.sherdog.com/fighter/Renan-Barao-23156",
            "position": 7,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "02ddcea5da241841b429dfa7b43597c6",
        },
        {
            "method": "submission",
            "details": "guillotine choke",
            "result": "win",
            "rounds": 3,
            "time": 12.983333333333334,
            "fighter": "http://www.sherdog.com/fighter/Brian-Ortega-65310",
            "opponent": "http://www.sherdog.com/fighter/Renato-Carneiro-61700",
            "position": 8,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "baf70455b161fe5f6e2c1878c0b5c4e2",
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Calvin-Kattar-23782",
            "opponent": "http://www.sherdog.com/fighter/Andre-Fili-58385",
            "position": 9,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "fa391e5f03b8f341b58e79206d753047",
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Aleksandra-Albu-144949",
            "opponent": "http://www.sherdog.com/fighter/Kailin-Curran-62703",
            "position": 10,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "dabc81a4aa934403839f391fbdaefd34",
        },
        {
            "method": "decision",
            "details": "split",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Jarred-Brooks-174665",
            "opponent": "http://www.sherdog.com/fighter/Eric-Shelton-86414",
            "position": 11,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "8328f6dc4410e35e850facf4dfc1f29b",
        },
        {
            "method": "ko",
            "details": "punch",
            "result": "win",
            "rounds": 1,
            "time": 3.066666666666667,
            "fighter": "http://www.sherdog.com/fighter/Drew-Dober-23982",
            "opponent": "http://www.sherdog.com/fighter/Joshua-Burkman-10003",
            "position": 12,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "f5ba70e3ad5338b4fddc69380632dbad",
        },
    ]


def test_empty_webiste_fights_parsing():
    fights = sherdog.extract_fights(None, "")
    assert len(fights) == 0


def test_fighter_parsing(sherdog_fighter):
    page_content, page_url = sherdog_fighter
    fighter = sherdog.extract_fighter_info(page_content, page_url)
    assert fighter == {
        "fighter": "http://www.sherdog.com/fighter/Jon-Jones-27944",
        "birth": dt.date(1987, 7, 19),
        "height": 6.4,
        "association": "Jackson-Wink MMA",
        "nationality": "United States",
    }


def test_opponent_parsing(sherdog_opponent):
    page_content, page_url = sherdog_opponent
    fighter = sherdog.extract_fighter_info(page_content, page_url)
    assert fighter == {
        "fighter": "http://www.sherdog.com/fighter/Daniel-Cormier-52311",
        "birth": dt.date(1979, 3, 20),
        "height": 5.11,
        "association": "American Kickboxing Academy",
        "nationality": "United States",
    }


def test_combining_fight_and_fighters(sherdog_event, sherdog_fighter, sherdog_opponent):
    fighter = sherdog.extract_fighter_info(*sherdog_fighter)
    opponent = sherdog.extract_fighter_info(*sherdog_opponent)
    fights = sherdog.extract_fights(*sherdog_event)
    fighters = pd.DataFrame([fighter, opponent])
    result = sherdog.combine_data(pd.DataFrame(fights[:1]), fighters)
    actuall = result.to_dict("records")[0]
    assert actuall == {
        "method": "no contest",
        "details": "overturned by csac",
        "result": "nc",
        "rounds": 3,
        "time": 13.016666666666666,
        "fighter": "http://www.sherdog.com/fighter/Jon-Jones-27944",
        "opponent": "http://www.sherdog.com/fighter/Daniel-Cormier-52311",
        "position": 1,
        "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
        "title": "UFC 214 Cormier vs. Jones 2",
        "organization": "Ultimate Fighting Championship (UFC)",
        "date": dt.date(2017, 7, 29),
        "location": "Honda Center / Anaheim / California / United States",
        "id": "3cda3aefbd92cf77156efcd4bbbd0723",
        "fighter birth": dt.date(1987, 7, 19),
        "fighter height": 6.4,
        "fighter association": "Jackson-Wink MMA",
        "fighter nationality": "United States",
        "opponent birth": dt.date(1979, 3, 20),
        "opponent height": 5.11,
        "opponent association": "American Kickboxing Academy",
        "opponent nationality": "United States",
    }
