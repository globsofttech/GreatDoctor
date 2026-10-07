"""Fetch the latest NIBL Sahabhagita Fund NAV."""

from html.parser import HTMLParser
import re

import requests


NAV_URL = "https://nimbacecapital.com/nav-nibl-sahabhagita-fund/"


class _TableTextParser(HTMLParser):
    """Collect normalized text for each HTML table."""

    def __init__(self):
        super().__init__()
        self._table_depth = 0
        self._current_table = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._table_depth += 1
            if self._table_depth == 1:
                self._current_table = []

    def handle_endtag(self, tag):
        if tag == "table" and self._table_depth:
            if self._table_depth == 1:
                self.tables.append(" ".join(self._current_table))
                self._current_table = []
            self._table_depth -= 1

    def handle_data(self, data):
        if self._table_depth:
            text = " ".join(data.split())
            if text:
                self._current_table.append(text)


def _parse_nav(html):
    parser = _TableTextParser()
    parser.feed(html)

    for table in parser.tables:
        if "Net Assets Value" not in table:
            continue
        match = re.search(
            r"Date:\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}).*?"
            r"\bNAV\s+([0-9]+(?:\.[0-9]+)?)\b",
            table,
        )
        if match:
            return {
                "date": match.group(1),
                "value": match.group(2),
                "source_url": NAV_URL,
            }
    return None


def get_latest_nav():
    """Return the latest NAV, or ``None`` when the source is unavailable."""
    try:
        response = requests.get(NAV_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[WARNING] Could not fetch NIBL Sahabhagita Fund NAV: {exc}")
        return None

    nav = _parse_nav(response.text)
    if nav is None:
        print("[WARNING] NIBL Sahabhagita Fund NAV was not found in the source page")
    return nav
