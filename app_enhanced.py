"""
Enhanced Medical Knowledge Portal - Daily Disease Lessons + Portal
Features: Auto-daily emails, User login, Read tracking, Recycle bin, 150-day repeat
"""
import os
import json
from flask import Flask, render_template, request, session, redirect, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from bson.objectid import ObjectId
from functools import wraps

from topics import TOPICS
from utils import tracker, youtube, wiki, emailer
from models import User, Lesson, UserLessonStatus, EmailLog, Topic

load_dotenv()

# ============ CONFIG ============
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-prod")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL", SMTP_USER)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
SEND_HOUR = int(os.getenv("SEND_HOUR", "7"))
SEND_MINUTE = int(os.getenv("SEND_MINUTE", "0"))

# ============ MIDDLEWARE ============
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


def no_cache(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    decorated_function.__name__ = f.__name__
    return decorated_function


# ============ AUTHENTICATION ============
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        
        if not email or not password or not name:
            return render_template("register.html", error="All fields required")
        
        if User.find_by_email(email):
            return render_template("register.html", error="Email already registered")
        
        password_hash = generate_password_hash(password)
        user_id = User.create(email, password_hash, name)
        
        session["user_id"] = str(user_id)
        session["email"] = email
        return redirect("/dashboard")
    
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.find_by_email(email)
        if user and check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])
            session["email"] = email
            return redirect("/dashboard")
        
        return render_template("login.html", error="Invalid email or password")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ============ MAIN PORTAL ============
@app.route("/dashboard")
@login_required
@no_cache
def dashboard():
    """Show all lessons with read status"""
    user_id = session.get("user_id")
    statuses = UserLessonStatus.get_user_lessons(user_id)
    
    lessons_with_content = []
    for status in statuses:
        lesson = Lesson.find_by_id(status["lesson_id"])
        lessons_with_content.append({
            "status": status,
            "lesson": lesson
        })
    
    return render_template("dashboard.html", lessons=lessons_with_content)


@app.route("/lesson/<lesson_id>")
@login_required
def view_lesson(lesson_id):
    """View single lesson in detail"""
    user_id = session.get("user_id")
    
    # Find status record
    status = UserLessonStatus.collection.find_one({
        "_id": ObjectId(lesson_id),
        "user_id": ObjectId(user_id)
    })
    
    if not status:
        return redirect("/dashboard")
    
    lesson = Lesson.find_by_id(status["lesson_id"])
    
    # Mark as read if not already
    if not status.get("read"):
        UserLessonStatus.mark_as_read(lesson_id)
    
    return render_template("lesson_detail.html", lesson=lesson, status=status)


@app.route("/recycle-bin")
@login_required
@no_cache
def recycle_bin():
    """Show deleted lessons in recycle bin"""
    user_id = session.get("user_id")
    deleted_items = UserLessonStatus.get_recycle_bin(user_id)
    
    items_with_content = []
    for item in deleted_items:
        lesson = Lesson.find_by_id(item["lesson_id"])
        items_with_content.append({
            "status": item,
            "lesson": lesson
        })
    
    return render_template("recycle_bin.html", items=items_with_content)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """User settings for email preferences"""
    user_id = session.get("user_id")
    user = User.find_by_id(user_id)
    
    if request.method == "POST":
        settings = {
            "send_daily": request.form.get("send_daily") == "on",
            "send_hour": int(request.form.get("send_hour", SEND_HOUR)),
            "send_minute": int(request.form.get("send_minute", SEND_MINUTE))
        }
        User.update_settings(user_id, settings)
        return redirect("/settings?saved=1")
    
    Topic.ensure_seeded(TOPICS)
    return render_template("settings.html", user=user, now=datetime.now(), topics=Topic.get_all())


@app.route("/api/topics", methods=["POST"])
@login_required
def add_topic():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    category = data.get("category", "").strip()
    query = data.get("query", "").strip()
    if not name or not category or not query:
        return jsonify({"status": "error", "message": "Name, category, and search query are required."}), 400
    Topic.ensure_seeded(TOPICS)
    if Topic.collection.find_one({"name": name}):
        return jsonify({"status": "error", "message": "A topic with that name already exists."}), 409
    Topic.add(name, category, query)
    return jsonify({"status": "created"}), 201


@app.route("/api/topics/<topic_id>", methods=["PUT"])
@login_required
def update_topic(topic_id):
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    category = data.get("category", "").strip()
    query = data.get("query", "").strip()
    if not name or not category or not query:
        return jsonify({"status": "error", "message": "Name, category, and search query are required."}), 400
    Topic.update(topic_id, name, category, query)
    return jsonify({"status": "updated"})


@app.route("/api/topics/<topic_id>", methods=["DELETE"])
@login_required
def delete_topic(topic_id):
    Topic.delete(topic_id)
    return jsonify({"status": "deleted"})


# ============ ACTIONS ============
@app.route("/api/mark-as-read/<status_id>", methods=["POST"])
@login_required
def mark_as_read(status_id):
    """Mark lesson as read"""
    UserLessonStatus.mark_as_read(status_id)
    return jsonify({"status": "ok"})


@app.route("/api/mark-all-read", methods=["POST"])
@login_required
def mark_all_read():
    """Mark all lessons as read"""
    user_id = session.get("user_id")
    UserLessonStatus.mark_all_as_read(user_id)
    return jsonify({"status": "ok"})


@app.route("/api/delete/<status_id>", methods=["POST"])
@login_required
def delete_lesson(status_id):
    """Soft delete lesson (to recycle bin)"""
    UserLessonStatus.soft_delete(status_id)
    return jsonify({"status": "deleted"})


@app.route("/api/restore/<status_id>", methods=["POST"])
@login_required
def restore_lesson(status_id):
    """Restore from recycle bin"""
    UserLessonStatus.restore(status_id)
    return jsonify({"status": "restored"})


@app.route("/api/permanent-delete/<status_id>", methods=["POST"])
@login_required
def permanent_delete(status_id):
    """Permanently delete"""
    UserLessonStatus.permanent_delete(status_id)
    return jsonify({"status": "permanently_deleted"})


@app.route("/api/resend/<status_id>", methods=["POST"])
@login_required
def resend_email(status_id):
    """Resend lesson email"""
    user_id = session.get("user_id")
    user = User.find_by_id(user_id)

    status = UserLessonStatus.collection.find_one({
        "_id": ObjectId(status_id),
        "user_id": ObjectId(user_id)
    })
    if not status or not user:
        return jsonify({"status": "error", "message": "Lesson not found"}), 404

    lesson = Lesson.find_by_id(status["lesson_id"])
    if not lesson:
        return jsonify({"status": "error", "message": "Lesson content not found"}), 404
    
    try:
        emailer.send_email(
            SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, 
            user.get("email"),
            lesson,
            lesson.get("video_info", {}),
            lesson.get("wiki_info", {})
        )
        EmailLog.log_email(user_id, status["lesson_id"], user.get("email"), "sent")
        return jsonify({"status": "resent"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/stats")
@login_required
@no_cache
def get_stats():
    """Get user statistics"""
    user_id = session.get("user_id")
    
    all_lessons = UserLessonStatus.get_user_lessons(user_id)
    read_lessons = [l for l in all_lessons if l.get("read")]
    unread_lessons = [l for l in all_lessons if not l.get("read")]
    
    return jsonify({
        "total": len(all_lessons),
        "read": len(read_lessons),
        "unread": len(unread_lessons),
        "in_recycle_bin": len(UserLessonStatus.get_recycle_bin(user_id))
    })


@app.route("/api/lessons")
@login_required
@no_cache
def get_lessons():
    """Return the current user's lessons for the dashboard."""
    user_id = session.get("user_id")
    statuses = UserLessonStatus.get_user_lessons(user_id)
    lessons = []
    for status in statuses:
        lessons.append({
            "status": status,
            "lesson": Lesson.find_by_id(status["lesson_id"])
        })

    return jsonify(json.loads(json.dumps(lessons, default=str)))


# ============ DAILY JOB ============
def run_daily_job(force_user_id=None, target_user_id=None):
    """Main job: Select random topic, fetch content, send to all active users"""
    Topic.ensure_seeded(TOPICS)
    topic = Topic.get_next_for_cycle()
    
    # Check if this lesson already exists
    existing_lesson = Lesson.find_by_query(topic["query"])
    if existing_lesson:
        lesson_id = existing_lesson["_id"]
        video_info = existing_lesson.get("video_info", {})
        wiki_info = existing_lesson.get("wiki_info", {})
    else:
        video_info = youtube.get_video(topic["query"], YOUTUBE_API_KEY) if YOUTUBE_API_KEY else {}
        wiki_info = wiki.get_summary(topic["query"])
        lesson_data = {
            **topic,
            "video_info": video_info,
            "wiki_info": wiki_info
        }
        lesson_id = Lesson.create(lesson_data)
    
    # Get all active users and send
    user_query = {"is_active": True}
    if target_user_id:
        user_query["_id"] = ObjectId(target_user_id)
    active_users = User.collection.find(user_query)
    
    for user in active_users:
        user_id = str(user["_id"])
        email = user["email"]
        prefs = user.get("email_preference", {})
        
        # Check if already sent today
        if force_user_id != user_id and EmailLog.get_today_sent(user_id):
            print(f"[INFO] Email already sent to {email} today, skipping")
            continue
        
        # Record and send
        UserLessonStatus.mark_sent(user_id, lesson_id, email)
        
        if SMTP_USER and SMTP_PASS:
            try:
                emailer.send_email(
                    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, email,
                    topic, video_info, wiki_info
                )
                EmailLog.log_email(user_id, lesson_id, email, "sent")
                print(f"[OK] Sent to {email}: {topic['name']}")
            except Exception as e:
                EmailLog.log_email(user_id, lesson_id, email, "failed")
                print(f"[ERROR] Failed to send to {email}: {e}")
        else:
            print("[INFO] SMTP not configured - recorded but not sent")
    
    return topic


def run_scheduled_job():
    """Send lessons to users whose saved delivery time is now."""
    current_time = datetime.now()
    users = User.collection.find({
        "is_active": True,
        "email_preference.send_daily": True
    })
    for user in users:
        preferences = user.get("email_preference", {})
        hour = int(preferences.get("send_hour", SEND_HOUR))
        minute = int(preferences.get("send_minute", SEND_MINUTE))
        if hour == current_time.hour and minute == current_time.minute:
            run_daily_job(target_user_id=str(user["_id"]))


@app.route("/api/send-now", methods=["POST"])
@login_required
def send_now():
    """Manual trigger to send daily lesson now"""
    try:
        user_id = session.get("user_id")
        topic = run_daily_job(force_user_id=user_id)
        return jsonify({"status": "sent", "topic": topic["name"]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/cron", methods=["GET", "POST"])
def cron_trigger():
    """Run the hosted scheduler when called with the configured secret."""
    expected_secret = os.getenv("CRON_SECRET")
    supplied_secret = request.headers.get("X-Cron-Secret")
    if not supplied_secret:
        authorization = request.headers.get("Authorization", "")
        if authorization.startswith("Bearer "):
            supplied_secret = authorization[7:]
    if not expected_secret or supplied_secret != expected_secret:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    run_scheduled_job()
    return jsonify({"status": "ok"})


def start_scheduler():
    """Start background scheduler for daily emails"""
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(run_scheduled_job, "interval", minutes=1)
        scheduler.start()
        print("[INFO] Scheduler started -- checking each user's delivery time every minute")
    except Exception as e:
        print(f"[WARNING] Scheduler startup warning: {e}")


# ============ PAGES FOR TESTING ============
@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/api/test-email", methods=["POST"])
def test_email():
    """Test email sending"""
    if not (SMTP_USER and SMTP_PASS):
        return jsonify({"status": "error", "message": "SMTP not configured"}), 500
    
    topic = {"name": "Test Email", "category": "Testing"}
    video = {"title": "Test Video", "url": "https://youtube.com"}
    wiki = {"summary": "This is a test email to verify SMTP is working correctly."}
    
    try:
        emailer.send_email(
            SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, TO_EMAIL,
            topic, video, wiki
        )
        return jsonify({"status": "test_email_sent", "to": TO_EMAIL})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html", error=str(e)), 500


# ============ STARTUP ============
if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True, use_reloader=False, port=5000)
