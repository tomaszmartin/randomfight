"""Config for pytest."""
import pytest
import os


def get_path(file_path):
    main_path = os.path.dirname(__file__)
    absolute_path = os.path.join(main_path, file_path)
    return absolute_path


@pytest.fixture(scope="module")
def sherdog_event():
    """Reads a sample event html and passes it to a test function."""
    path = get_path("data/sherdog/event.html")
    with open(path) as input_file:
        content = input_file.read()
        yield content, "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825"


@pytest.fixture(scope="module")
def sherdog_fighter(request):
    """Reads a sample fighter html and passes it to a test function."""
    path = get_path("data/sherdog/fighter.html")
    with open(path) as input_file:
        content = input_file.read()
        yield content, "http://www.sherdog.com/fighter/Jon-Jones-27944"


@pytest.fixture(scope="module")
def sherdog_opponent(request):
    """Reads a sample opponent html and passes it to a test function."""
    path = get_path("data/sherdog/opponent.html")
    with open(path) as input_file:
        content = input_file.read()
        yield content, "http://www.sherdog.com/fighter/Daniel-Cormier-52311"


@pytest.fixture(scope="module")
def sherdog_events_list(request):
    """Reads a sample event list html and passes it to a test function."""
    path = get_path("data/sherdog/events_list.html")
    with open(path) as input_file:
        content = input_file.read()
        yield content, "http://www.sherdog.com/events/0"
