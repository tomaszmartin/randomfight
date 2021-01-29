"""Contains method that may be usefull for all parsers."""
import datetime as dt
import re


def remove_whitespace(raw: str) -> str:
    """Removes whitespace from string, so that:
    "x y z" becomes "xyz".

    Args:
        initial: raw string.

    Returns:
        str: string with whitespace removed.
    """
    cleantext = re.sub(r"\s+", " ", raw)
    cleantext = cleantext.strip()
    return cleantext


def extract_date(date_str: str) -> dt.date:
    """Turns string representing date into dt.date object.
    Basically it tries a few common date representations.

    Args:
        date_str: date's string representation.

    Raises:
        ValueError: if string cannot be turned into date.

    Returns:
        date.
    """
    date_str = date_str.strip()
    for pattern in ["%b %d, %Y", "%Y-%m-%d"]:
        try:
            return dt.datetime.strptime(date_str, pattern).date()
        except Exception:  # pylint: disable=broad-except
            pass
    raise ValueError(f"Unable to parse date {date_str}")
