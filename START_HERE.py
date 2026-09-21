#!/usr/bin/env python3
"""
Quick Start Script - Lists all files and next steps
"""

FILES_CREATED = {
    "🔵 CORE APPLICATION FILES": {
        "app_enhanced.py": "Main Flask app with all features (auth, portal, scheduler, APIs)",
        "models.py": "MongoDB database models (Users, Lessons, UserLessonStatus, EmailLog)",
    },
    
    "🎨 FRONTEND TEMPLATES": {
        "templates/login.html": "Login page with beautiful gradient design",
        "templates/register.html": "Registration page for new users",
        "templates/dashboard.html": "Main portal - view all lessons, search, stats",
        "templates/lesson_detail.html": "Full lesson view with medical information",
        "templates/recycle_bin.html": "View and restore deleted lessons",
        "templates/settings.html": "User email preferences & learning settings",
        "templates/404.html": "Error page - not found",
        "templates/500.html": "Error page - server error",
    },
    
    "📚 DOCUMENTATION": {
        "README_ENHANCED.md": "Feature overview, quick start, and usage guide",
        "SETUP_GUIDE.md": "Complete setup, configuration, and deployment guide",
        "API_DOCUMENTATION.md": "All API endpoints with examples and workflows",
        ".env.example_enhanced": "Environment variables template",
    },
    
    "🚀 DEPLOYMENT & SETUP": {
        "setup.sh": "One-click setup script for Linux/Mac",
        "setup.bat": "One-click setup script for Windows",
        "requirements_enhanced.txt": "Python dependencies (Flask, MongoDB, etc.)",
        "vercel_enhanced.json": "Vercel deployment configuration",
    }
}

print("""
╔═══════════════════════════════════════════════════════════════════════╗
║        🏥 MEDICAL KNOWLEDGE PORTAL - COMPLETE & READY! ✅            ║
║                                                                       ║
║   Daily Disease Lessons → Email + Personal Learning Portal           ║
║   Perfect for MBBS students with 150-day spaced repetition           ║
╚═══════════════════════════════════════════════════════════════════════╝

📦 FILES CREATED
""")

for category, files in FILES_CREATED.items():
    print(f"\n{category}")
    for filename, description in files.items():
        print(f"  ✓ {filename:<35} - {description}")

print("""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 QUICK START (Choose One)

1️⃣ WINDOWS USERS (5 Minutes)
   cd disease-reminder\\disease-reminder
   setup.bat
   
2️⃣ MAC/LINUX USERS (5 Minutes)
   cd disease-reminder/disease-reminder
   chmod +x setup.sh
   ./setup.sh

3️⃣ MANUAL SETUP
   cd disease-reminder/disease-reminder
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   pip install -r requirements_enhanced.txt
   cp .env.example_enhanced .env
   # Edit .env with your MongoDB & Gmail credentials
   python app_enhanced.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 REQUIRED CREDENTIALS (Get These First)

✓ MongoDB (Free):
  https://www.mongodb.com/cloud/atlas
  Create cluster → Get connection string
  
✓ Gmail SMTP (Free):
  1. Enable 2-factor auth on Gmail
  2. https://myaccount.google.com/apppasswords
  3. Copy 16-char app password

✓ YouTube API (Optional, for video links):
  https://console.cloud.google.com/
  Create project → Enable YouTube Data API v3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️ CONFIGURATION (.env file)

MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/medical_portal
FLASK_SECRET_KEY=generate-random-string-here
SMTP_USER=your-email@gmail.com
SMTP_PASS=16-character-app-password
TO_EMAIL=your-email@gmail.com
SEND_HOUR=7       # Morning time (24-hour)
SEND_MINUTE=0     # For 7 AM India Time: HOUR=1, MINUTE=30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 NEXT STEPS (After Setup)

1. Run setup script → install dependencies
2. Create .env file → add credentials
3. Start app → python app_enhanced.py
4. Visit → http://localhost:5000/register
5. Create account → register with your email
6. Send first lesson → click "Send Now" button
7. Check email → verify SMTP is working
8. Read in portal → view lesson in browser
9. Deploy to Vercel → follow SETUP_GUIDE.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ FEATURES INCLUDED

✅ Daily Automated Emails (customizable time)
✅ Beautiful Learning Portal with login
✅ Read/Unread tracking for each lesson
✅ Soft delete to recycle bin (recoverable)
✅ Auto-repeat every 150 days
✅ Customizable repeat interval
✅ Manual resend & pause buttons
✅ Search & filter by disease name
✅ Statistics dashboard
✅ Responsive design (mobile/tablet/desktop)
✅ Medical topics: 500+ diseases/surgeries/drugs
✅ Wikipedia summaries & YouTube videos
✅ Beautiful email templates
✅ Free hosting (Vercel + MongoDB Atlas)
✅ No code changes needed for deployment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 WHAT YOU GET (Each Morning at 7 AM)

📧 EMAIL with:
   • Disease name & category
   • Symptoms & signs
   • Diagnostic criteria
   • Treatment protocols
   • Drug names & doses
   • Adverse drug reactions
   • Wikipedia medical summary
   • YouTube educational video link
   • Portal link to view online

💻 PORTAL allows you to:
   • View all lessons received
   • Search by disease name or category
   • Mark as read/unread
   • Delete to recycle bin
   • Restore deleted lessons
   • View full medical details
   • Print or download
   • Track your progress
   • Customize email schedule

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 DOCUMENTATION

Read in this order:
  1. README_ENHANCED.md - Overview and quick start
  2. SETUP_GUIDE.md - Detailed setup & deployment
  3. API_DOCUMENTATION.md - Technical details

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 EXAMPLE USAGE WORKFLOW

Day 1:
  • Run setup.sh or setup.bat
  • Edit .env with your credentials
  • Start app (python app_enhanced.py)
  • Register account at http://localhost:5000/register
  • Click "Send Now" to test

Day 2:
  • Email arrives at 7 AM: "Anaphylactic Shock"
  • Open email → click "View online"
  • Portal shows lesson with read status
  • Read the medical information
  • Click "Mark as Read"

Day 3:
  • New topic: "Myocardial Infarction"
  • Repeat same process
  • Build daily habit

Day 150:
  • First topic repeats: "Anaphylactic Shock"
  • Reinforces your learning
  • Spaced repetition algorithm at work!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 TIPS FOR SUCCESS

1. Set a morning routine → Read email with coffee ☕
2. Mark lessons as read → Tracks your progress 📊
3. Before exams → Search portal by topic & category 🔍
4. Watch videos → Click YouTube links in lessons 🎬
5. Join study group → Share portal with classmates 👥
6. Review weak areas → Keep tough topics in portal 📚
7. Track progress → Check dashboard stats 📈

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌍 DEPLOY TO VERCEL (Free Cloud Hosting)

1. Push code to GitHub
2. Go to vercel.com/new
3. Import repository
4. Set environment variables
5. Click Deploy
6. Get your URL: https://your-project.vercel.app
7. Set external scheduler (EasyCron.com - free)

Full instructions in: SETUP_GUIDE.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ FREQUENTLY ASKED QUESTIONS

Q: Is email really free?
A: Yes! Gmail SMTP is free for personal use. No API costs.

Q: Does MongoDB cost money?
A: No! 512 MB free storage on MongoDB Atlas. Enough for years.

Q: What if I miss a day?
A: All lessons saved in portal. You can read anytime.

Q: Can I change the repeat interval?
A: Yes! Settings page → change from 150 to any value (30-365).

Q: Can I pause emails?
A: Yes! Settings page → toggle "Send daily emails" OFF.

Q: What time zone is the scheduler?
A: By default UTC. For India time (IST): SEND_HOUR=1, SEND_MINUTE=30

Q: Does this work on mobile?
A: Yes! Portal is fully responsive and mobile-optimized.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆘 TROUBLESHOOTING

Email not sending?
  ✓ Check .env file for SMTP credentials
  ✓ Verify Gmail app password (16 chars, spaces removed)
  ✓ Try /api/test-email endpoint

Login not working?
  ✓ Check MongoDB connection in .env
  ✓ Verify database is accessible
  ✓ Clear browser cookies

Scheduler not running?
  ✓ Check SEND_HOUR and SEND_MINUTE
  ✓ On Vercel, use external service (EasyCron)
  ✓ Manually trigger with "Send Now" button

Still having issues?
  ✓ Read error message carefully
  ✓ Check Flask console for detailed errors
  ✓ Review SETUP_GUIDE.md troubleshooting section

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 PERFECT FOR

✅ MBBS Students (1st, 2nd, 3rd, 4th year)
✅ Medical interns & residents  
✅ Medical competitive exams (NEET PG)
✅ Quick medical reference
✅ Daily learning habit
✅ Exam preparation
✅ Medical knowledge building

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to build your medical knowledge? 
Let's get started! 🏥📚

Run setup script now:
  Windows: disease-reminder\\disease-reminder\\setup.bat
  Mac/Linux: disease-reminder/disease-reminder/setup.sh

Happy learning! 🎓
""")
