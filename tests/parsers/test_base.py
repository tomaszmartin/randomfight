import datetime as dt

import pytest

from app.parsers import base


def test_whitespace_trimming():
    assert base.remove_whitespace("\n\nTE\n   \nST   ") == "TE ST"


def test_date_extraction():
    for date_str in ["2020-12-01", "Dec 1, 2020"]:
        assert base.extract_date(date_str) == dt.date(2020, 12, 1)


def test_date_extraction_new_format():
    with pytest.raises(ValueError):
        base.extract_date("01-12-2020")