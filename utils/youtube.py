"""
Looks up one relevant YouTube video for a topic using the free YouTube
Data API v3. If no API key is configured (or the call fails), falls
back to a plain YouTube search link so the email/page still has
something useful to click.
"""
import requests

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# Channels that are consistently good for MBBS-level lecture content.
# We nudge the search toward these first for better hit quality.
PREFERRED_CHANNELS = [
    "Ninja Nerd",
    "Osmosis",
    "Armando Hasudungan",
    "Dr. Najeeb Lectures",
]


def get_video(query, api_key, prefer_channel_hint=True):
    fallback = {
        "title": f"Search: {query} lecture",
        "url": f"https://www.youtube.com/results?search_query={requests.utils.quote(query + ' lecture pathophysiology')}",
    }

    if not api_key:
        return fallback

    try:
        search_q = f"{query} lecture pathophysiology"
        params = {
            "part": "snippet",
            "type": "video",
            "maxResults": 5,
            "q": search_q,
            "key": api_key,
            "relevanceLanguage": "en",
            "safeSearch": "strict",
        }
        resp = requests.get(YOUTUBE_SEARCH_URL, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if not items:
            return fallback

        # Prefer a result whose channel matches our known-good list.
        chosen = items[0]
        if prefer_channel_hint:
            for item in items:
                channel_title = item["snippet"].get("channelTitle", "")
                if any(pref.lower() in channel_title.lower() for pref in PREFERRED_CHANNELS):
                    chosen = item
                    break

        video_id = chosen["id"]["videoId"]
        title = chosen["snippet"]["title"]
        return {
            "title": title,
            "url": f"https://www.youtube.com/watch?v={video_id}",
        }
    except Exception:
        return fallback
