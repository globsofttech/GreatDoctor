"""
API Documentation - Medical Knowledge Portal
All endpoints with request/response examples
"""

# ============================================================
# AUTHENTICATION ENDPOINTS
# ============================================================

## POST /register
"""
Create new user account

Request:
  POST /register
  Content-Type: application/x-www-form-urlencoded
  
  Parameters:
  - name: string (user's full name)
  - email: string (unique email address)
  - password: string (secure password)

Response (Success):
  Redirect: /dashboard
  Sets: session["user_id"], session["email"]

Response (Error):
  400: "Email already registered" | "All fields required"
"""

## POST /login
"""
Authenticate user with email and password

Request:
  POST /login
  Content-Type: application/x-www-form-urlencoded
  
  Parameters:
  - email: string
  - password: string

Response (Success):
  Redirect: /dashboard
  Sets: session["user_id"], session["email"]

Response (Error):
  400: "Invalid email or password"
"""

## GET /logout
"""
Logout user and clear session

Response:
  Redirect: /login
  Clears: session data
"""

# ============================================================
# DASHBOARD & VIEWING ENDPOINTS
# ============================================================

## GET /dashboard
"""
Main dashboard - view all lessons

Authentication: Required (login_required)

Response:
  HTML page with:
  - List of all lessons with read/unread status
  - Search functionality
  - Statistics (total, read, unread, trash)
  - Action buttons (view, delete, resend)
  
  Variables passed to template:
  - lessons: List[{status: dict, lesson: dict}]
"""

## GET /lesson/<lesson_id>
"""
View full details of a single lesson

Authentication: Required
Parameters:
  - lesson_id: string (MongoDB ObjectId)

Response:
  HTML page with:
  - Full lesson content
  - Wikipedia summary
  - YouTube video link
  - Medical information (diagnosis, treatment, drugs)
  - Marks lesson as read automatically
  - Action buttons (mark read, resend, delete, print)

Response (Error):
  404: If lesson not found for user
"""

## GET /recycle-bin
"""
View all deleted lessons

Authentication: Required

Response:
  HTML page with:
  - Table of deleted items
  - Deletion date for each
  - Restore button
  - Permanent delete button
  - Empty state if no deleted items
"""

## GET /settings
"""
User settings and preferences page

Authentication: Required

Response (GET):
  HTML form with:
  - Toggle: Daily email sending
  - Toggle: Auto-repeat enabled
  - Input: Repeat after N days (30-365)
  - Display: Account stats (email, created_at, duration)
  - Submit button

Response (POST):
  Redirect: /settings?saved=1
  Updates: User.email_preference in MongoDB
"""

# ============================================================
# API ENDPOINTS (JSON)
# ============================================================

## GET /api/stats
"""
Get user learning statistics

Authentication: Required
Method: GET
Content-Type: application/json

Response (200):
{
  "total": 45,        # Total lessons received
  "read": 32,         # Lessons marked as read
  "unread": 13,       # Lessons not yet read
  "in_recycle_bin": 5 # Deleted but not permanently removed
}
"""

## POST /api/mark-as-read/<status_id>
"""
Mark a single lesson as read

Authentication: Required
Method: POST
Parameters:
  - status_id: string (MongoDB ObjectId of UserLessonStatus)

Response (200):
{
  "status": "ok"
}
"""

## POST /api/mark-all-read
"""
Mark ALL lessons as read in one action

Authentication: Required
Method: POST

Response (200):
{
  "status": "ok"
}
"""

## POST /api/delete/<status_id>
"""
Soft delete - move lesson to recycle bin

Authentication: Required
Method: POST
Parameters:
  - status_id: string

Response (200):
{
  "status": "deleted"
}

Note: Data is not permanently deleted, can be restored
"""

## POST /api/restore/<status_id>
"""
Restore lesson from recycle bin

Authentication: Required
Method: POST
Parameters:
  - status_id: string

Response (200):
{
  "status": "restored"
}
"""

## POST /api/permanent-delete/<status_id>
"""
Permanently delete lesson (cannot be recovered)

Authentication: Required
Method: POST
Parameters:
  - status_id: string

Response (200):
{
  "status": "permanently_deleted"
}

⚠️ WARNING: This action cannot be undone
"""

## POST /api/resend/<status_id>
"""
Resend lesson to user's email

Authentication: Required
Method: POST
Parameters:
  - status_id: string

Response (200):
{
  "status": "resent"
}

Response (500):
{
  "status": "error",
  "message": "SMTP error details"
}
"""

## POST /api/send-now
"""
Manually trigger the daily lesson to be sent immediately

Authentication: Required
Method: POST

Response (200):
{
  "status": "sent",
  "topic": "Anaphylactic Shock"
}

Response (500):
{
  "status": "error",
  "message": "Error details"
}

Note: Can be used to test email sending
"""

## POST /api/test-email
"""
Send test email to verify SMTP configuration

Authentication: Not required (but optional)
Method: POST

Response (200):
{
  "status": "test_email_sent",
  "to": "info.drrajanpoudel@gmail.com"
}

Response (500):
{
  "status": "error",
  "message": "SMTP not configured" | "SMTP error"
}

Use this to verify Gmail SMTP is working correctly
"""

# ============================================================
# PAGE ROUTES
# ============================================================

## GET /
"""
Root redirect

Response:
  - If logged in: Redirect to /dashboard
  - If not logged in: Redirect to /login
"""

## GET /404 (Automatic)
"""
404 Not Found error page

Trigger:
  - Visit non-existent route
  
Response:
  HTML error page with link back to dashboard
"""

## GET /500 (Automatic)
"""
500 Server Error page

Trigger:
  - Unhandled exception during request
  - Database error
  - SMTP error
  
Response:
  HTML error page with error details
"""

# ============================================================
# SCHEDULED JOBS (Automatic)
# ============================================================

## Background Job: run_daily_job()
"""
Runs automatically at scheduled time (SEND_HOUR:SEND_MINUTE)

Triggered by: APScheduler background task
Frequency: Once per day

Process:
1. Select random medical topic
2. Fetch video info from YouTube
3. Fetch summary from Wikipedia
4. Create/find Lesson in database
5. For each active user:
   - Check if already sent today
   - Check if should repeat (150-day cycle)
   - Record in UserLessonStatus
   - Send email via SMTP
   - Log in EmailLog

Returns:
  {topic_name: str, sent_to: int}

Can also be manually triggered via:
  POST /api/send-now
"""

# ============================================================
# DATABASE OPERATIONS
# ============================================================

## User.create(email, password_hash, name)
"""
Create new user in database

Parameters:
  - email: str
  - password_hash: str (hashed with werkzeug)
  - name: str

Returns:
  ObjectId (inserted user ID)

Fields created:
  - _id (auto)
  - email
  - password (hashed)
  - name
  - created_at
  - email_preference (defaults)
  - is_active: true
"""

## User.find_by_email(email)
"""
Find user by email address

Returns:
  dict (user document) or None

Used for: Login validation
"""

## User.find_by_id(user_id)
"""
Find user by MongoDB ObjectId

Parameters:
  - user_id: str or ObjectId

Returns:
  dict (user document) or None
"""

## Lesson.create(topic_data)
"""
Create new lesson from topic

Parameters:
  - topic_data: dict with:
    - name: str
    - category: str
    - query: str
    - content: dict (optional)
    - video_info: dict (optional)
    - wiki_info: dict (optional)

Returns:
  ObjectId (inserted lesson ID)
"""

## UserLessonStatus.mark_sent(user_id, lesson_id, email_address)
"""
Record that a lesson was sent to a user

Parameters:
  - user_id: str or ObjectId
  - lesson_id: str or ObjectId
  - email_address: str

Creates document with:
  - sent_at: Datetime
  - read: false
  - deleted: false
  - repeat_cycle_count: 0
"""

## UserLessonStatus.mark_as_read(status_id)
"""
Mark lesson as read with timestamp

Updates:
  - read: true
  - read_at: Datetime.now()
"""

## UserLessonStatus.soft_delete(status_id)
"""
Move lesson to recycle bin (not permanent)

Updates:
  - deleted: true
  - in_recycle_bin: true
  - deleted_at: Datetime.now()
"""

## UserLessonStatus.restore(status_id)
"""
Restore lesson from recycle bin

Updates:
  - deleted: false
  - in_recycle_bin: false
"""

## UserLessonStatus.permanent_delete(status_id)
"""
Permanently delete from database

Removes: Document completely
"""

## UserLessonStatus.should_repeat(user_id, lesson_id, repeat_after_days=150)
"""
Check if lesson should be sent again based on repeat cycle

Calculates:
  days_passed = now - sent_at
  
Returns:
  True if days_passed >= repeat_after_days
  False otherwise
"""

# ============================================================
# ERROR RESPONSES
# ============================================================

"""
Common error responses:

400 Bad Request:
  - Missing required form fields
  - Invalid email format
  - Invalid ObjectId format

401 Unauthorized:
  - Not logged in (missing session)
  - Session expired

403 Forbidden:
  - Trying to access other user's data

404 Not Found:
  - Lesson/status not found for user
  - Invalid route

500 Internal Server Error:
  - MongoDB connection failed
  - SMTP error
  - Unhandled exception

"""

# ============================================================
# EXAMPLE WORKFLOWS
# ============================================================

"""
WORKFLOW 1: New User Registration & First Lesson
1. User visits /register
2. POST /register with (name, email, password)
3. User created in MongoDB
4. Redirect to /dashboard
5. Dashboard shows empty state with "Send First Lesson" button
6. User clicks button → POST /api/send-now
7. Lesson generated and emailed
8. Email contains portal link
9. User reads lesson in portal
10. Status marked as read

WORKFLOW 2: Daily Automated Email
1. Time reaches SEND_HOUR:SEND_MINUTE
2. APScheduler triggers run_daily_job()
3. Random topic selected from TOPICS
4. YouTube & Wikipedia data fetched
5. Lesson created in database
6. For each active user:
   a. Check if already sent today → skip if yes
   b. Check 150-day repeat rule → skip if not time
   c. Create UserLessonStatus record
   d. Send email with lesson details
7. User receives email next morning
8. Email contains link to portal

WORKFLOW 3: Lesson Review (150-day Repeat)
Day 1: Lesson "Anaphylactic Shock" sent
...
Day 150: 
1. Scheduler triggers job
2. Randomly selects topic
3. Runs should_repeat() → True (150 days passed)
4. Sends same topic again
5. User sees duplicate in portal
6. Can view, delete, or mark as read again

WORKFLOW 4: Recycle Bin Recovery
1. User views lesson → clicks "Delete"
2. POST /api/delete/<id>
3. Lesson moved to recycle bin (soft delete)
4. Dashboard no longer shows it
5. User visits /recycle-bin
6. Can see deleted lesson
7. User clicks "Restore"
8. POST /api/restore/<id>
9. Lesson back in main dashboard
10. Read status preserved

"""

# ============================================================
# TESTING ENDPOINTS
# ============================================================

"""
Test with curl or Postman:

1. Test user registration:
   curl -X POST http://localhost:5000/register \\
     -d "name=Test&email=test@example.com&password=pass123"

2. Test login:
   curl -X POST http://localhost:5000/login \\
     -d "email=test@example.com&password=pass123" \\
     -c cookies.txt

3. Test email sending:
   curl -X POST http://localhost:5000/api/test-email

4. Test stats API:
   curl -X GET http://localhost:5000/api/stats \\
     -b cookies.txt

5. Test send now:
   curl -X POST http://localhost:5000/api/send-now \\
     -b cookies.txt
"""
