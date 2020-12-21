"""Parses html from sherdog.com.
Extracts events and fights data.
"""
import datetime as dt
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
import hashlib
import re

from bs4 import BeautifulSoup
from bs4.element import Tag
import pandas as pd

from app.parsers import base


def combine_data(fights: pd.DataFrame, fighters: pd.DataFrame) -> pd.DataFrame:
    """Adds figter and opponent statistcs to a given fight.

    Args:
        fights (pd.DataFrame): fights data.
        fighters (pd.DataFrame): fighters data.

    Returns:
        pd.DataFrame: combined data.
    """
    merged = fights.merge(fighters, on=["fighter"], how="left")
    fighters.rename(columns={"fighter": "opponent"}, inplace=True)
    merged.rename(
        columns={
            "association": "fighter association",
            "birth": "fighter birth",
            "height": "fighter height",
            "nationality": "fighter nationality",
        },
        inplace=True,
    )
    merged = merged.merge(fighters, on=["opponent"], how="left")
    merged.rename(
        columns={
            "association": "opponent association",
            "birth": "opponent birth",
            "height": "opponent height",
            "nationality": "opponent nationality",
        },
        inplace=True,
    )
    return merged


def extract_fighter_info(content: Optional[str], url: str) -> Dict[str, Any]:
    """Extracts fighter information from website content.

    Args:
        content (Optional[str]): website content.
        url (str): url of the website.

    Returns:
        Dict[str, Any]: data about the fighter.
    """
    try:
        soup = BeautifulSoup(content, "lxml")
        data: Dict[str, Any] = {"fighter": url}
        data["birth"] = None
        birth_elem = soup.find("span", {"itemprop": "birthDate"})
        if birth_elem:
            data["birth"] = base.extract_date(birth_elem.text)
        height = soup.find("span", {"class": "height"})
        if height:
            height = height.find("strong").text
            height = height.replace('"', "")
            data["height"] = float(height.replace("'", "."))
        else:
            data["height"] = None
        association = soup.find("a", {"class": "association"})
        if association:
            data["association"] = base.remove_whitespace(association.text)
        else:
            data["association"] = None
        data["nationality"] = None
        nat_elem = soup.find("strong", {"itemprop": "nationality"})
        if nat_elem:
            data["nationality"] = base.remove_whitespace(nat_elem.text)
        return data
    except Exception as err:
        logging.exception("Error parsing: %s", url)
        raise err


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
    event = extract_event_data(content, url)
    if not event["date"] or event["date"] >= dt.date.today():
        return []
    fights = _extract_fights_from_event(content)
    # Add event info to the fights
    for fight in fights:
        fight["url"] = url
        fight["title"] = event["title"]
        fight["organization"] = event["organization"]
        fight["date"] = event["date"]
        fight["location"] = event["location"]
        fight["id"] = _create_fight_id(fight)
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
    events = {domain + link["href"] for link in links}
    events = {link for link in events if "events/" in link}
    events = {link for link in events if not link.endswith("events/")}
    events = {link for link in events if not link.endswith("-page")}
    return sorted(list(events))


def _create_fight_id(fight: Dict[str, Any]) -> str:
    raw_id = (
        fight["fighter"]
        + fight["opponent"]
        + fight["date"].isoformat()
        + fight["title"]
    )
    result = hashlib.md5(raw_id.encode())
    return result.hexdigest()


def extract_event_data(content: str, url: str) -> Dict[str, Any]:
    """Extracts data about the event.

    Args:
        content (str): event page html.

    Returns:
        dict: event information.
    """
    soup = BeautifulSoup(content, "lxml")
    data: Dict[str, Any] = {
        "title": base.remove_whitespace(soup.find("h1").text),
        "organization": base.remove_whitespace(soup.find("h2").text),
        "date": None,
        "location": None,
        "url": url,
    }
    info = soup.find("div", {"class": "authors_info"})
    if info:
        date_str = info.find("span", {"class": "date"}).text
        data["date"] = base.extract_date(date_str)
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
    fights = soup.find_all("tr", {"itemprop": "subEvent"})
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
        data["method"] = base.remove_whitespace(method_elem.text)
        data["method"] = data["method"].split("(")[0].lower()
        data["method"] = data["method"].replace("method ", "")
        data["method"] = data["method"].strip()
        data["details"] = re.findall(r"(\(.*\))", method_elem.text)[0]
        data["details"] = data["details"].replace("(", "")
        data["details"] = data["details"].replace(")", "")
        data["details"] = data["details"].lower()
        data["result"] = base.remove_whitespace(result_elem.text).lower()
        data["rounds"] = int(rounds_elem.text.replace("Round", ""))
        data["time"] = _parse_time(time_elem.text, data["rounds"])
        data["fighter"] = "http://www.sherdog.com" + fighter_elem.find("a")["href"]
        data["opponent"] = "http://www.sherdog.com" + opponent_elem.find("a")["href"]
        data["position"] = position
        return data
    except Exception:
        return None


def _parse_time(text: str, rounds: int) -> float:
    try:
        # First try to clean the text
        timestr = text.replace("#", "3")
        timestr = timestr.replace("N/A", "")
        timestr = timestr.replace("!", "1")
        timestr = timestr.replace("$", "4")
        timestr = timestr.replace(")", "0")
        timestr = timestr.replace("?", ".")
        timestr = timestr.replace('"', ".")
        timestr = timestr.replace(":;", ".")
        timestr = timestr.replace(":", ".")
        timestr = timestr.replace(";", ".")
        timestr = timestr.replace("`", "")

        timestr = re.sub(r"[a-z]+", "", timestr, flags=re.I)
        timestr = "".join(timestr.split())
        parts = timestr.split(".")

        if len(parts) == 3:
            if not parts[:-2]:
                minutes = 0.0
            else:
                minutes = float(parts[-2])
            seconds = float(parts[-1])
        elif len(parts) == 2:
            if not parts[0]:
                minutes = 0.0
            else:
                minutes = float(parts[0])
            seconds = float(parts[1])
        else:
            try:
                minutes = float(timestr)
            except ValueError:
                minutes = 5
            seconds = 0.0

        if not minutes:
            minutes = 0

        time = (rounds - 1) * 5.0 + float(minutes + seconds / 60.0)
        return time
    except Exception as exc:
        logging.exception("Error parsing time from: %s", time)
        raise exc
