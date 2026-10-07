import os
from flask import Flask, render_template
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from topics import TOPICS
from utils import tracker, youtube, wiki, emailer, nav, ipos

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL", SMTP_USER)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # optional
SEND_HOUR = int(os.getenv("SEND_HOUR", "7"))
SEND_MINUTE = int(os.getenv("SEND_MINUTE", "0"))

app = Flask(__name__)


def run_daily_job():
    topic = tracker.get_next_topic(TOPICS)
    video_info = youtube.get_video(topic["query"], YOUTUBE_API_KEY)
    wiki_info = wiki.get_summary(topic["query"])
    nav_info = nav.get_latest_nav()
    ipo_info = ipos.get_upcoming_ipos()

    entry = tracker.record_today(topic, video_info, wiki_info)

    if SMTP_USER and SMTP_PASS and TO_EMAIL:
        try:
            emailer.send_email(
                SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, TO_EMAIL,
                topic, video_info, wiki_info, nav_info, ipo_info,
            )
            print(f"[OK] Sent email for: {topic['name']}")
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
    else:
        print("[INFO] SMTP not configured -- skipping email, topic still saved for the web page.")

    return entry


@app.route("/")
def home():
    today = tracker.get_today()
    if not today:
        # Nothing sent yet -- generate one on the fly so the page isn't empty.
        today = run_daily_job()
    return render_template("today.html", entry=today)


@app.route("/history")
def history():
    entries = list(reversed(tracker.get_history()))
    return render_template("history.html", entries=entries)


@app.route("/send-now")
def send_now():
    entry = run_daily_job()
    return {"status": "sent", "topic": entry["name"]}


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_daily_job, "cron", hour=SEND_HOUR, minute=SEND_MINUTE)
    scheduler.start()
    print(f"[INFO] Scheduler started -- daily topic will run at {SEND_HOUR:02d}:{SEND_MINUTE:02d}.")


if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True, use_reloader=False, port=5000)
