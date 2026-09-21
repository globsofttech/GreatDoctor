"""
Database models for the Medical Knowledge Portal
"""
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import random
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "medical_portal")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


class User:
    collection = db["users"]
    
    @staticmethod
    def create(email, password_hash, name):
        """Create new user"""
        user = {
            "email": email,
            "password": password_hash,
            "name": name,
            "created_at": datetime.now(),
            "email_preference": {
                "send_daily": True,
                "auto_repeat_enabled": True,
                "send_hour": 7,
                "send_minute": 0
            },
            "is_active": True
        }
        result = User.collection.insert_one(user)
        return result.inserted_id
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        return User.collection.find_one({"email": email})
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        return User.collection.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def update_settings(user_id, settings):
        """Update user email preferences"""
        User.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"email_preference": settings}}
        )


class Lesson:
    collection = db["lessons"]
    
    @staticmethod
    def create(topic_data):
        """Create lesson from daily topic"""
        lesson = {
            "name": topic_data.get("name"),
            "category": topic_data.get("category"),
            "query": topic_data.get("query"),
            "content": topic_data.get("content", {}),
            "video_info": topic_data.get("video_info", {}),
            "wiki_info": topic_data.get("wiki_info", {}),
            "created_at": datetime.now(),
            "sent_count": 0
        }
        result = Lesson.collection.insert_one(lesson)
        return result.inserted_id
    
    @staticmethod
    def find_all():
        """Get all lessons"""
        return list(Lesson.collection.find())
    
    @staticmethod
    def find_by_id(lesson_id):
        """Get lesson by ID"""
        return Lesson.collection.find_one({"_id": ObjectId(lesson_id)})
    
    @staticmethod
    def find_by_query(query):
        """Find lesson by query to avoid duplicates"""
        return Lesson.collection.find_one({"query": query})


class Topic:
    collection = db["topics"]
    seed_collection = db["topic_settings"]
    cycle_collection = db["topic_cycle"]

    @staticmethod
    def ensure_seeded(default_topics):
        if Topic.seed_collection.find_one({"_id": "initial_seed_complete"}):
            return
        existing_names = {topic["name"] for topic in Topic.collection.find({}, {"name": 1})}
        missing_topics = [
            {"name": topic["name"], "category": topic["category"], "query": topic["query"]}
            for topic in default_topics
            if topic["name"] not in existing_names
        ]
        if missing_topics:
            Topic.collection.insert_many(missing_topics)
        Topic.seed_collection.insert_one({"_id": "initial_seed_complete"})

    @staticmethod
    def get_all():
        topics = list(Topic.collection.find().sort("name", 1))
        for topic in topics:
            topic["id"] = str(topic.pop("_id"))
        return topics

    @staticmethod
    def add(name, category, query):
        return Topic.collection.insert_one({"name": name, "category": category, "query": query})

    @staticmethod
    def update(topic_id, name, category, query):
        return Topic.collection.update_one(
            {"_id": ObjectId(topic_id)},
            {"$set": {"name": name, "category": category, "query": query}}
        )

    @staticmethod
    def delete(topic_id):
        return Topic.collection.delete_one({"_id": ObjectId(topic_id)})

    @staticmethod
    def get_next_for_cycle():
        topics = Topic.get_all()
        if not topics:
            raise RuntimeError("No topics are configured")

        topic_by_name = {topic["name"]: topic for topic in topics}
        topic_names = set(topic_by_name)
        cycle = Topic.cycle_collection.find_one({"_id": "current"}) or {}
        queue = [name for name in cycle.get("queue", []) if name in topic_names]
        stored_names = set(cycle.get("topic_names", []))
        added_names = topic_names - stored_names

        if not queue and stored_names:
            queue = list(topic_names)
            random.shuffle(queue)
        elif added_names:
            queue.extend(added_names)
            random.shuffle(queue)

        if not queue:
            queue = list(topic_names)
            random.shuffle(queue)
            last_name = cycle.get("last_name")
            if queue[0] == last_name and len(queue) > 1:
                queue[0], queue[1] = queue[1], queue[0]

        next_name = queue.pop(0)
        Topic.cycle_collection.replace_one(
            {"_id": "current"},
            {
                "_id": "current",
                "topic_names": sorted(topic_names),
                "queue": queue,
                "last_name": next_name
            },
            upsert=True
        )
        return topic_by_name[next_name]


class UserLessonStatus:
    collection = db["user_lesson_status"]
    
    @staticmethod
    def mark_sent(user_id, lesson_id, email_address):
        """Record that a lesson was sent to user"""
        status = {
            "user_id": ObjectId(user_id),
            "lesson_id": ObjectId(lesson_id),
            "sent_at": datetime.now(),
            "read": False,
            "deleted": False,
            "in_recycle_bin": False,
            "repeat_cycle_count": 0,
            "email_address": email_address
        }
        UserLessonStatus.collection.insert_one(status)
    
    @staticmethod
    def get_user_lessons(user_id, include_deleted=False):
        """Get all lessons for a user"""
        query = {"user_id": ObjectId(user_id), "deleted": False}
        if include_deleted:
            query = {"user_id": ObjectId(user_id)}
        
        lessons = list(UserLessonStatus.collection.find(query).sort("sent_at", -1))
        return lessons
    
    @staticmethod
    def get_recycle_bin(user_id):
        """Get deleted lessons (recycle bin)"""
        return list(UserLessonStatus.collection.find({
            "user_id": ObjectId(user_id),
            "in_recycle_bin": True
        }).sort("sent_at", -1))
    
    @staticmethod
    def mark_as_read(status_id):
        """Mark lesson as read"""
        UserLessonStatus.collection.update_one(
            {"_id": ObjectId(status_id)},
            {"$set": {"read": True, "read_at": datetime.now()}}
        )
    
    @staticmethod
    def soft_delete(status_id):
        """Soft delete - move to recycle bin"""
        UserLessonStatus.collection.update_one(
            {"_id": ObjectId(status_id)},
            {"$set": {"deleted": True, "in_recycle_bin": True, "deleted_at": datetime.now()}}
        )
    
    @staticmethod
    def restore(status_id):
        """Restore from recycle bin"""
        UserLessonStatus.collection.update_one(
            {"_id": ObjectId(status_id)},
            {"$set": {"deleted": False, "in_recycle_bin": False}}
        )
    
    @staticmethod
    def permanent_delete(status_id):
        """Permanently delete"""
        UserLessonStatus.collection.delete_one({"_id": ObjectId(status_id)})
    
    @staticmethod
    def mark_all_as_read(user_id):
        """Mark all lessons as read"""
        UserLessonStatus.collection.update_many(
            {"user_id": ObjectId(user_id), "deleted": False},
            {"$set": {"read": True, "read_at": datetime.now()}}
        )
    
    @staticmethod
    def check_if_already_sent_today(user_id, query):
        """Check if this topic was already sent today"""
        today = datetime.now().date()
        return UserLessonStatus.collection.find_one({
            "user_id": ObjectId(user_id),
            "sent_at": {
                "$gte": datetime.combine(today, datetime.min.time()),
                "$lte": datetime.combine(today, datetime.max.time())
            }
        })
    
    @staticmethod
    def should_repeat(user_id, lesson_id, repeat_after_days=150):
        """Check if lesson should be repeated (150 days later)"""
        status = UserLessonStatus.collection.find_one({
            "user_id": ObjectId(user_id),
            "lesson_id": ObjectId(lesson_id)
        })
        
        if not status:
            return False
        
        days_passed = (datetime.now() - status["sent_at"]).days
        return days_passed >= repeat_after_days


class EmailLog:
    collection = db["email_logs"]
    
    @staticmethod
    def log_email(user_id, lesson_id, email_address, status="sent"):
        """Log email send event"""
        log = {
            "user_id": ObjectId(user_id),
            "lesson_id": ObjectId(lesson_id),
            "email_address": email_address,
            "sent_at": datetime.now(),
            "status": status
        }
        EmailLog.collection.insert_one(log)
    
    @staticmethod
    def get_today_sent(user_id):
        """Get emails sent today to user"""
        today = datetime.now().date()
        return list(EmailLog.collection.find({
            "user_id": ObjectId(user_id),
            "sent_at": {
                "$gte": datetime.combine(today, datetime.min.time()),
                "$lte": datetime.combine(today, datetime.max.time())
            },
            "status": "sent"
        }))
