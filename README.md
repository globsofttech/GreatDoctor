# Daily Disease Reminder

A small Flask app that picks a new disease/topic every morning (never
repeating until the full list has cycled through), pulls a short
summary + image from Wikipedia and a relevant lecture from YouTube,
and emails it to you. It also serves a simple web page if you'd
rather just check it in your browser.

## 1. Install

```bash
cd disease-reminder
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configure

```bash
cp .env.example .env
```

Then open `.env` and fill in:
- **SMTP_USER / SMTP_PASS / TO_EMAIL** — needed if you want an actual
  email each morning. For Gmail, generate an "App Password" at
  https://myaccount.google.com/apppasswords (your normal password
  won't work with 2FA enabled).
- **YOUTUBE_API_KEY** — optional. Get a free one from the Google Cloud
  Console (enable "YouTube Data API v3"). Without it, you still get a
  working link — it just points to a YouTube search instead of one
  exact video.
- **SEND_HOUR / SEND_MINUTE** — what time it fires daily (24h, server's
  local time).

## 3. Run

```bash
python app.py
```

Leave this running (see "Keeping it running" below). It will:
- Fire automatically every day at the time you set.
- Serve `http://localhost:5000/` — today's topic.
- Serve `http://localhost:5000/history` — everything covered so far.
- Serve `http://localhost:5000/send-now` — manually trigger one right
  now (use this to test your setup immediately instead of waiting
  until tomorrow morning).

## How "don't repeat" works

`topics.py` holds the master list (~55 topics across medicine,
surgery, pediatrics, OB-GYN, psychiatry, etc. — edit this file to add
your own). Each day the app shuffles through the *entire* list once
before any topic repeats, and everything sent is logged to
`data/history.json` so you can see your full coverage over time.

## Keeping it running every morning

Running `python app.py` only works while your laptop is on and the
script is open. Two easy ways around that:

1. **Free hosting** — deploy this to a free-tier host like
   [Render](https://render.com) or [PythonAnywhere](https://www.pythonanywhere.com)
   so it runs in the cloud even when your laptop is off. Both have
   simple "deploy from GitHub" flows for small Flask apps.
2. **Phone/laptop always-on background** — on Linux/Mac you can run
   it with `nohup python app.py &` or set it up as a `systemd`
   service; on Windows, Task Scheduler can launch it at login.

## Customizing

- Add more diseases: edit the `TOPICS` list in `topics.py`.
- Change how topics are picked (e.g. force one "Surgery" and one
  "Medicine" topic to alternate): edit `utils/tracker.py`.
- Change the email design: edit `utils/emailer.py`'s `build_html()`.
