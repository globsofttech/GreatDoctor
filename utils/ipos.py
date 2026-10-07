"""Fetch upcoming and currently open Nepal IPOs."""

from datetime import date
from html import unescape
import json
import re

import requests


IPOS_URL = "https://hamroshare.com.np/investment/upcoming-ipos"
_IPO_SECTION = re.compile(r'\\"label\\":\\"IPO\\".*?(?=\\"label\\":\\"|$)', re.DOTALL)
_ISSUE = re.compile(
    r'\\"opening_date\\":\\"(?P<opening>[^"]*)\\".*?'
    r'\\"closing_date\\":\\"(?P<closing>[^"]*)\\".*?'
    r'\\"companyname\\":\\"(?P<company>[^"]*)\\"',
    re.DOTALL,
)
_TAG = re.compile(r"<[^>]+>")


def _decode(value):
    try:
        return unescape(json.loads(f'"{value}"'))
    except json.JSONDecodeError:
        return unescape(value)


def _days_remaining(opening_date, closing_date, today):
    if opening_date > today:
        return opening_date, f"{(opening_date - today).days} days remaining"
    return closing_date, f"{(closing_date - today).days} days remaining"


def _parse_date(value):
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_ipos(html, today=None):
    today = today or date.today()
    section_match = _IPO_SECTION.search(html)
    if not section_match:
        return []

    results = []
    seen = set()
    for match in _ISSUE.finditer(section_match.group(0)):
        opening_date = _parse_date(match.group("opening"))
        closing_date = _parse_date(match.group("closing"))
        if not opening_date or not closing_date or closing_date < today:
            continue

        company = _TAG.sub("", _decode(match.group("company"))).strip()
        if not company or company in seen:
            continue

        countdown_date, countdown = _days_remaining(
            opening_date, closing_date, today
        )
        results.append({
            "company": company,
            "opening_date": opening_date.isoformat(),
            "closing_date": closing_date.isoformat(),
            "countdown_date": countdown_date.isoformat(),
            "countdown": countdown,
            "source_url": IPOS_URL,
        })
        seen.add(company)

    return sorted(results, key=lambda ipo: (ipo["countdown_date"], ipo["company"]))


def get_upcoming_ipos():
    """Return open and future IPOs, or an empty list if the source is unavailable."""
    try:
        response = requests.get(IPOS_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[WARNING] Could not fetch upcoming IPOs: {exc}")
        return []

    ipos = _parse_ipos(response.text)
    if not ipos:
        print("[WARNING] No open or upcoming IPOs found on the source page")
    return ipos
