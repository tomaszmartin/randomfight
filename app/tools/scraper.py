"""Used to scrape multiple websites.
Handles the asynchronous http calls.
"""
import asyncio
import logging
from typing import Any, List, Iterable, Optional, Callable, Tuple

from aiohttp import ClientSession, TCPConnector
import requests

logging.getLogger().setLevel(logging.INFO)


def get_content(uri: str) -> Optional[str]:
    """Extracts content from web page.

    Args:
        uri (str): web page adress.

    Returns:
        str: web page content.
    """
    with requests.get(uri) as response:
        if response.status_code == 200:
            content = response.content
            return content.decode(encoding="utf8")
    return None


def run(links: List[str], func: Callable, batch_size: int = 50) -> List[Any]:
    """Runs a scraping processs. Takes a list of url to be scraped,
    the function that parses them and a batch size.
    Returns a list of results. Single result is returned by the
    func calllable which should parse the html content.

    Args:
        links (List[str]): list of urls to be scraped.
        func (Callable): parser function.
        batch_size (int, optional): batch size, how many urls should be loaded
            at once. Defaults to 50.

    Returns:
        List[Any]: list of the resutls.
    """
    result = []
    for current, _ in batch(links, batch_size):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(scrape(current, func))
        partial = loop.run_until_complete(future)
        result.extend(partial)
    return result


async def scrape(links: List[str], func: Callable) -> List[Any]:
    """Extracts content of a given set of urls/links
    and parses them using func.

    Args:
        links (List[str]): list of urls to scrape.
        func (Callable): function that parses utl content.
            Takes two arguments: content and url.

    Returns:
        List[Any]: list of parsing results.
    """
    tasks = []
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        for link in links:
            task = asyncio.ensure_future(fetch(link, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # All content is now extracted
        data = []
        for content, link in responses:
            try:
                result = func(content, link)
            except Exception as err:
                logging.exception("Exception while parsing %s", link)
                raise err
            if not isinstance(result, list):
                data.append(result)
            else:
                data.extend(result)
        return data


def batch(iterable: List[Any], size: int = 1) -> Iterable[Tuple[Any, int]]:
    """Allows to generate a batch of n subsets
    from the given iterable.

    Args:
        iterable (List[Any]): contains data.
        size (int, optional): batch size. Defaults to 1.

    Yields:
        Tuple[Any, int]: tuple of batch and its start position.
    """
    length = len(iterable)
    for ndx in range(0, length, size):
        yield iterable[ndx : min(ndx + size, length)], ndx


async def fetch(url: str, session: ClientSession) -> Tuple[bytes, str]:
    """Fetches content of a single url.

    Args:
        url (str): full url address.
        session (ClientSession): session.

    Returns:
        Tuple[str, str]: contents of the url, and the url itself
    """
    async with session.get(url) as response:
        return await response.read(), url
