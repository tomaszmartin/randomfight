"""Config for pytest."""
import pytest
import os


def get_path(file_path):
    main_path = os.path.dirname(__file__)
    absolute_path = os.path.join(main_path, file_path)
    return absolute_path


@pytest.fixture(scope="module")
def generate_links():
    """Creates a function which generates html code
    with given number of fights and fighters links.
    :return generator: function for generating html code."""
    fightlink = """<a href="http://fightmetric.com/fight-details/{}"></a>"""
    fighterlink = """<a href="http://fightmetric.com/fighter-details/{}">"""

    def link_generator(fights=0, fighters=0):
        result = []
        for i in range(fights):
            result.append(fightlink.format(i))
        for i in range(fighters):
            result.append(fighterlink.format(i))
        return "</br>".join(result)

    return link_generator


@pytest.fixture(scope="module")
def sample_event():
    """Reads a sample event html and passes it to a test function.
    :return content(str): event html code."""
    path = get_path("data/event.html")
    with open(path) as input_file:
        content = input_file.read()
        yield content, "https://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825"


@pytest.fixture(scope="module")
def sample_fight():
    """Reads a sample fight html and passes it to a test function.
    :return content(str): fight html code."""
    path = get_path("data/fight.html")
    with open(path) as input_file:
        content = input_file.read()
        yield content


@pytest.fixture(scope="module")
def sample_fighter(request):
    """Reads a sample fighter html and passes it to a test function.
    :return content(str): fighter html code."""
    path = get_path("data/opponent.html")
    with open(path) as input_file:
        content = input_file.read()
        yield content


@pytest.fixture(scope="module")
def sample_opponent(request):
    """Reads a sample fighter html and passes it to a test function.
    :return content(str): fighter html code."""
    path = get_path("data/fighter.html")
    with open(path) as input_file:
        content = input_file.read()
        yield content


@pytest.fixture
def sample_scraped_fight():
    return {
        "attendance": 14037.0,
        "birth": "1976-05-11",
        "bonus": "{'ko': False, 'submission': False, 'performance': False, 'fight': False}",
        "date": "2008-06-15",
        "event": "DREAM 4: Middleweight Grand Prix 2008 2nd Round",
        "height": 5.9,
        "link": "http://www.fightmetric.com/fight-details/4cf4ed1edc8a0b24",
        "location": "Yokohama, Kanagawa, Japan",
        "method": "KO/TKO",
        "name": "Melvin Manhoef",
        "position": 1,
        "reach": None,
        "referee": "Yuji Shimada",
        "result": "Win",
        "round": 1.0,
        "stance": "Orthodox",
        "stats": "{'knockouts': {'thrown': 1.0, 'landed': 1.0, 'received': 0.0, 'avoided': 0.0}, \
                       'total str.': {'thrown': 34.0, 'landed': 23.0, 'received': 0.0, 'avoided': 1.0}, \
                       'td': {'thrown': 0.0, 'landed': 0.0, 'received': 0.0, 'avoided': 1.0}, \
                       'submissions': {'thrown': 0.0, 'landed': 0.0, 'received': 0.0, 'avoided': 0.0}, \
                       'sig. str': {'thrown': 31.0, 'landed': 21.0, 'received': 0.0, 'avoided': 1.0}, \
                       'head': {'thrown': 31.0, 'landed': 21.0, 'received': 0.0, 'avoided': 1.0}, \
                       'body': {'thrown': 0.0, 'landed': 0.0, 'received': 0.0, 'avoided': 0.0}, \
                       'leg': {'thrown': 0.0, 'landed': 0.0, 'received': 0.0, 'avoided': 0.0}, \
                       'distance': {'thrown': 4.0, 'landed': 2.0, 'received': 0.0, 'avoided': 1.0}, \
                       'clinch': {'thrown': 0.0, 'landed': 0.0, 'received': 0.0, 'avoided': 0.0}, \
                       'ground': {'thrown': 27.0, 'landed': 19.0, 'received': 0.0, 'avoided': 0.0}}",
        "time": 1.5,
        "time format": "(10, 5)",
        "titlefight": False,
        "weight": 185.0,
    }
