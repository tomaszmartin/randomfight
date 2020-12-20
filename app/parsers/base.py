"""Contains method that may be usefull for all parsers.
"""
import datetime as dt
import re


def remove_whitespace(element) -> str:
    raw_html = str(element)
    cleantext = re.sub(r"\s+", " ", raw_html)
    cleantext = cleantext.strip()
    return cleantext


def extract_date(date_str: str) -> dt.date:
    date_str = date_str.strip()
    for pattern in ["%b %d, %Y", "%Y-%m-%d"]:
        try:
            return dt.datetime.strptime(date_str, pattern).date()
        except:
            pass
    raise ValueError(f"Unable to parse date {date_str}")
