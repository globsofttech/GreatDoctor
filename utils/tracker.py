"""
Keeps a persistent queue of topics on disk so the same disease never
gets picked twice in a row through the whole list, and history is kept
so you can look back at everything you've already covered.
"""
import json
import os
import random
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
TODAY_FILE = os.path.join(DATA_DIR, "today.json")


def _load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)


def _save_json(path, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def get_next_topic(all_topics):
    """
    Returns one topic from the current cycle. Every topic is used exactly
    once before a new shuffled cycle begins.
    """
    stored_queue = _load_json(QUEUE_FILE, None)
    history = _load_json(HISTORY_FILE, [])
    topic_by_name = {topic["name"]: topic for topic in all_topics}
    topic_names = set(topic_by_name)

    # The old queue format was only a list and may represent a smaller topic
    # bank. Start a clean cycle when it is encountered or when topics change.
    is_managed_queue = isinstance(stored_queue, dict)
    if is_managed_queue:
        queue = stored_queue.get("queue", [])
        stored_names = set(stored_queue.get("topic_names", []))
    else:
        queue = []
        stored_names = set()

    if not is_managed_queue:
        queue = []
    else:
        queue = [name for name in queue if name in topic_names]
        added_names = topic_names - stored_names
        if added_names:
            queue.extend(added_names)
            random.shuffle(queue)

    if not queue:
        names = list(topic_names)
        random.shuffle(names)
        last_used = history[-1]["name"] if history else None
        if names and names[0] == last_used and len(names) > 1:
            names[0], names[1] = names[1], names[0]
        queue = names

    next_name = queue.pop(0)
    _save_json(QUEUE_FILE, {
        "topic_names": sorted(topic_names),
        "queue": queue
    })

    return topic_by_name[next_name]


def record_today(topic, video_info, wiki_info):
    """Save today's pick to history.json and today.json (used by the web page)."""
    history = _load_json(HISTORY_FILE, [])
    entry = {
        "date": date.today().isoformat(),
        "name": topic["name"],
        "category": topic["category"],
        "video_title": video_info.get("title") if video_info else None,
        "video_url": video_info.get("url") if video_info else None,
        "summary": wiki_info.get("summary") if wiki_info else None,
        "image_url": wiki_info.get("image_url") if wiki_info else None,
        "wiki_url": wiki_info.get("page_url") if wiki_info else None,
    }
    history.append(entry)
    _save_json(HISTORY_FILE, history)
    _save_json(TODAY_FILE, entry)
    return entry


def get_history():
    return _load_json(HISTORY_FILE, [])


def get_today():
    return _load_json(TODAY_FILE, None)
