"""
Pulls a short summary + thumbnail image for a topic from Wikipedia's
public REST API. No API key needed, no rate-limit issues for this
kind of low-volume personal use.
"""
import requests

SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"


def get_summary(title):
    try:
        resp = requests.get(SUMMARY_URL.format(requests.utils.quote(title)), timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        return {
            "summary": data.get("extract"),
            "image_url": (data.get("thumbnail") or {}).get("source"),
            "page_url": (data.get("content_urls") or {}).get("desktop", {}).get("page"),
        }
    except Exception:
        return None
