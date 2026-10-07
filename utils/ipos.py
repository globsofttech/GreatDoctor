"""Fetch upcoming and currently open Nepal IPOs."""

from datetime import date, datetime
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
_UPCOMING_SECTION = re.compile(
    r"<section>.*?<span[^>]*>\s*Upcoming\s*</span>.*?</section>",
    re.IGNORECASE | re.DOTALL,
)
_UPCOMING_CARD = re.compile(r"<article\b.*?</article>", re.IGNORECASE | re.DOTALL)
_DATE_LABELS = re.compile(
    r"\bOpen\s+(?P<opening>\d{1,2}\s+[A-Za-z]+\s+\d{4})\s+"
    r"Close\s+(?P<closing>\d{1,2}\s+[A-Za-z]+\s+\d{4})",
    re.IGNORECASE,
)


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


def _parse_display_date(value):
    try:
        return datetime.strptime(value, "%d %b %Y").date()
    except ValueError:
        return None


def _plain_text(value):
    return " ".join(_TAG.sub(" ", value).split())


def _parse_rendered_upcoming(html, today):
    section_match = _UPCOMING_SECTION.search(html)
    if not section_match:
        return []

    results = []
    for card_match in _UPCOMING_CARD.finditer(section_match.group(0)):
        card = card_match.group(0)
        text = _plain_text(card)
        dates = _DATE_LABELS.search(text)
        if not dates:
            continue

        opening_date = _parse_display_date(dates.group("opening"))
        closing_date = _parse_display_date(dates.group("closing"))
        if not opening_date or not closing_date or closing_date < today:
            continue

        header = re.search(
            r"<span[^>]*>\s*([^<]+)\s*</span>.*?"
            r"<span[^>]*>\s*Forthcoming\s*</span>.*?"
            r"<div[^>]*>\s*([^<]+)\s*</div>.*?"
            r"<span[^>]*>\s*([^<]+)\s*</span>",
            card,
            re.IGNORECASE | re.DOTALL,
        )
        if not header:
            continue

        countdown_date, countdown = _days_remaining(
            opening_date, closing_date, today
        )
        results.append({
            "company": f"{header.group(1).strip()} - {header.group(2).strip()}",
            "type": header.group(3).strip(),
            "opening_date": opening_date.isoformat(),
            "closing_date": closing_date.isoformat(),
            "countdown_date": countdown_date.isoformat(),
            "countdown": countdown,
            "source_url": IPOS_URL,
        })
    return results


def _parse_ipos(html, today=None):
    today = today or date.today()
    rendered_results = _parse_rendered_upcoming(html, today)
    if rendered_results:
        return sorted(
            rendered_results,
            key=lambda ipo: (ipo["countdown_date"], ipo["company"]),
        )

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
            "type": "IPO",
            "opening_date": opening_date.isoformat(),
            "closing_date": closing_date.isoformat(),
            "countdown_date": countdown_date.isoformat(),
            "countdown": countdown,
            "source_url": IPOS_URL,
        })
        seen.add(company)

    return sorted(results, key=lambda ipo: (ipo["countdown_date"], ipo["company"]))


def get_upcoming_ipos():
    """Return open and future issues, or an empty list if unavailable."""
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
