"""Parses html from sherdog.com.
Extracts events and fights data.
"""
import datetime as dt
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import re
from bs4 import BeautifulSoup
from bs4.element import Tag


def extract_fights(content: Optional[str], url: str) -> List[Dict[str, Any]]:
    """Takes a content of an event page and
    extracts all fights data from it.

    Args:
        content (str): web page content.
        url (str): web page url.

    Returns:
        List[Dict[str, Any]]: list of fights.
    """
    if not content:
        return []
    event = _extract_event_data(content, url)
    if not event["date"] or event["date"] >= dt.date.today():
        return []
    fights = _extract_fights_from_event(content)
    # Add event info to the fights
    for fight in fights:
        fight["title"] = event["title"]
        fight["organization"] = event["organization"]
        fight["date"] = event["date"]
        fight["location"] = event["location"]
    return fights


def extract_events_links(content: Optional[str], url: str) -> List[str]:
    """Takes a events list page and extracts
    events links from it.

    Args:
        content (str): web page content.
        url (str): web page URL.

    Returns:
        List[str]: list of fight urls.
    """
    if not content:
        return []
    parsed_uri = urlparse(url)
    domain = "{uri.scheme}://{uri.netloc}".format(uri=parsed_uri)
    soup = BeautifulSoup(content, "lxml")
    links = soup.find_all("a", href=re.compile("events"))
    events = [domain + link["href"] for link in links]
    return events


def _extract_event_data(content: str, url: str) -> Dict[str, Any]:
    """Extracts data about the event.

    Args:
        content (str): event page html.

    Returns:
        dict: event information.
    """
    soup = BeautifulSoup(content, "lxml")
    data = {
        "title": _clean_html(soup.find("h1")),
        "organization": soup.find("h2").text,
        "date": None,
        "location": None,
        "url": url,
    }
    info = soup.find("div", {"class": "authors_info"})
    if info:
        date_str = info.find("span", {"class": "date"}).text
        data["date"] = dt.datetime.strptime(date_str, "%b %d, %Y").date()
        location = info.find("span", {"itemprop": "location"}).text
        data["location"] = location.replace(",", " /")

    return data


def _extract_fights_from_event(content: str) -> List[Dict[str, Any]]:
    fights: List[Optional[Dict[str, Any]]] = []
    soup = BeautifulSoup(content, "lxml")
    main_fight = _extract_main_fight_from_event(soup)
    fights.append(main_fight)
    other_fights = _extract_other_fights_from_event(soup)
    fights.extend(other_fights)
    # Since fights are optional we need to check
    # if they are not None before return
    return [fight for fight in fights if fight]


def _extract_main_fight_from_event(soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
    main_fight_elem = soup.find("section", {"itemprop": "subEvent"})
    if not main_fight_elem:
        return None

    fighter_elem = main_fight_elem.find("div", {"class": "left_side"})
    opponent_elem = main_fight_elem.find("div", {"class": "right_side"})
    result_elem = fighter_elem.find("span", {"class": "final_result"})
    details = main_fight_elem.find("table")
    _, method_elem, _, rounds_elem, time_elem = details.find_all("td", {"class": ""})
    return _create_fight(
        fighter_elem, opponent_elem, result_elem, method_elem, rounds_elem, time_elem, 1
    )


def _extract_other_fights_from_event(
    soup: BeautifulSoup,
) -> List[Optional[Dict[str, Any]]]:
    data = []
    fights = [fight for fight in soup.find_all("tr", {"itemprop": "subEvent"})]
    for position, fight in enumerate(fights, 2):
        fighter_elem = fight.find("td", {"class": "text_right"})
        opponent_elem = fight.find("td", {"class": "text_left"})
        result_elem = fighter_elem.find("span", {"class": "final_result"})
        _, method_elem, rounds_elem, time_elem = fight.find_all("td", {"class": ""})
        data.append(
            _create_fight(
                fighter_elem,
                opponent_elem,
                result_elem,
                method_elem,
                rounds_elem,
                time_elem,
                position,
            )
        )
    return data


def _create_fight(
    fighter_elem: Tag,
    opponent_elem: Tag,
    result_elem: Tag,
    method_elem: Tag,
    rounds_elem: Tag,
    time_elem: Tag,
    position: Tag,
) -> Optional[Dict[str, Any]]:
    try:
        data: Dict[str, Any] = {}
        data["method"] = method_elem.text.split("\n")[0]
        data["method"] = data["method"].split("(")[0].lower()
        data["method"] = data["method"].replace("method ", "")
        data["details"] = re.findall(r"(\(.*\))", method_elem.text)[0]
        data["details"] = data["details"].replace("(", "").replace(")", "").lower()
        data["result"] = result_elem.text
        data["rounds"] = int(rounds_elem.text.replace("Round", ""))
        data["time"] = _parse_time(time_elem.text, data["rounds"], data["method"])
        data["fighter"] = fighter_elem.find("a")["href"]
        data["opponent"] = opponent_elem.find("a")["href"]
        data["position"] = position
        return data
    except Exception:
        return None


def _parse_time(text: str, rounds: int, method: str) -> float:
    try:
        # First try to clean the text
        timestr = text.replace("#", "3")
        timestr = timestr.replace("!", "1")
        timestr = timestr.replace(")", "0")
        timestr = timestr.replace("?", ".")
        timestr = timestr.replace('"', ".")
        timestr = timestr.replace(":;", ".")
        timestr = timestr.replace(":", ".")
        timestr = timestr.replace(";", ".")
        timestr = timestr.replace("`", "")

        timestr = re.sub(r"[a-z]+", "", timestr, flags=re.I)
        parts = timestr.split(".")

        if len(parts) == 2:
            minutes = float(parts[0])
            seconds = float(parts[1])
        else:
            if timestr:
                minutes = float(timestr)
                seconds = 0.0

        if not minutes:
            minutes = 0

        time = (rounds - 1) * 5 + float(minutes + seconds / 60)
        return time
    except Exception as exc:
        logging.warning(f"Error parsing time from: {text}")
        raise exc


def _clean_html(element) -> str:
    raw_html = str(element)
    raw_html = raw_html.replace("<br/>", ", ")
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext
