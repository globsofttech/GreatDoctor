#!/usr/bin/env python3
"""
DEPLOYMENT & TESTING CHECKLIST
Medical Knowledge Portal
"""

CHECKLIST = """
╔════════════════════════════════════════════════════════════════════════╗
║        🏥 MEDICAL KNOWLEDGE PORTAL - DEPLOYMENT CHECKLIST             ║
╚════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════
PHASE 1: LOCAL TESTING (Your Computer)
═══════════════════════════════════════════════════════════════════════════

□ Prerequisites
  □ Python 3.8+ installed
  □ MongoDB Atlas account created (free)
  □ Gmail account with app password ready
  
□ Setup
  □ Clone/download project
  □ Run setup.bat (Windows) or setup.sh (Mac/Linux)
  □ Create .env file from .env.example_enhanced
  □ Fill in MongoDB URI
  □ Fill in Gmail SMTP credentials
  □ Generate Flask secret key
  
□ Testing Database Connection
  □ MongoDB connection string correct format
  □ IP whitelist set to 0.0.0.0/0 in MongoDB Atlas
  □ Can connect to database from Python

□ Testing Email
  □ Gmail account has 2-factor auth enabled
  □ Generated app password (16 characters)
  □ SMTP credentials added to .env
  □ Test with POST /api/test-email
  □ Email received in inbox

□ Testing Application
  □ python app_enhanced.py starts without errors
  □ http://localhost:5000/register accessible
  □ Can create new user account
  □ Can login with credentials
  □ Can access /dashboard
  □ Click "Send Now" button works
  □ Email received in inbox
  □ Email contains lesson details
  □ Portal link in email works

□ Testing Portal Features
  □ Dashboard shows statistics
  □ Search functionality works
  □ Click "View" lesson opens details
  □ "Mark as Read" button works
  □ "Delete" moves to recycle bin
  □ "Resend" sends email again
  □ Recycle bin shows deleted items
  □ Can restore from recycle bin
  □ Settings page loads
  □ Can toggle email preferences
  □ Can change repeat interval

□ Testing Scheduler
  □ Scheduler starts without errors
  □ Logs show: "[INFO] Scheduler started"
  □ Wait until scheduled time (SEND_HOUR:SEND_MINUTE)
  □ Email sent automatically
  □ Lesson appears in portal

═══════════════════════════════════════════════════════════════════════════
PHASE 2: VERCEL DEPLOYMENT (Free Cloud)
═══════════════════════════════════════════════════════════════════════════

□ Prepare Repository
  □ Git initialized
  □ All files committed
  □ Repository pushed to GitHub
  □ .env file NOT in git (add to .gitignore)

□ Create Vercel Project
  □ Sign up at vercel.com
  □ Import GitHub repository
  □ Select project root: disease-reminder/disease-reminder
  □ Project name set (e.g., medical-portal)

□ Set Environment Variables in Vercel Dashboard
  □ MONGO_URI = [your MongoDB connection string]
  □ FLASK_SECRET_KEY = [random 64-char string]
  □ FLASK_ENV = production
  □ SMTP_HOST = smtp.gmail.com
  □ SMTP_PORT = 587
  □ SMTP_USER = [your Gmail]
  □ SMTP_PASS = [app password]
  □ TO_EMAIL = [your Gmail]
  □ SEND_HOUR = 1 (for India time)
  □ SEND_MINUTE = 30 (for India time)
  □ YOUTUBE_API_KEY = [optional]

□ Deploy
  □ Click "Deploy" button
  □ Wait for deployment to complete
  □ No build errors
  □ Deployment URL provided

□ Test Deployed App
  □ Visit deployment URL
  □ Can register new account
  □ Can login
  □ POST /api/test-email works (verify SMTP)
  □ Can send lesson manually
  □ Email received from cloud instance
  □ All features work same as local

□ Set Up External Scheduler
  □ Visit easycron.com or cron-job.org
  □ Create free account
  □ Set webhook URL: https://your-vercel-url/api/send-now
  □ Set method: POST
  □ Set frequency: Daily at 1:30 AM UTC (7 AM IST)
  □ Save and enable

□ Test Scheduler
  □ Wait for scheduled time
  □ Email should arrive automatically
  □ Lesson appears in portal
  □ Verify it works daily

═══════════════════════════════════════════════════════════════════════════
PHASE 3: PRODUCTION HARDENING
═══════════════════════════════════════════════════════════════════════════

□ Security
  □ FLASK_SECRET_KEY is strong random string
  □ MongoDB password is strong
  □ Gmail app password is unique (not main password)
  □ No credentials in code or git
  □ HTTPS enabled on Vercel (automatic)
  □ Session timeout configured
  □ CORS properly configured (if needed)

□ Database
  □ MongoDB backups enabled
  □ Database indexed for performance
  □ Retention policy set (optional)
  □ Growth monitoring configured

□ Email
  □ Gmail account secure
  □ Backup email set up
  □ Test email sending regularly
  □ Monitor email logs

□ Monitoring
  □ Vercel monitoring enabled
  □ Error logging configured
  □ Performance metrics tracked
  □ Alerts set for failures

□ Scaling
  □ Application tested with 100+ users
  □ Database can handle growth
  □ Email rate limits checked
  □ MongoDB connection pool configured

═══════════════════════════════════════════════════════════════════════════
PHASE 4: USER ACCEPTANCE
═══════════════════════════════════════════════════════════════════════════

□ User Testing
  □ Share deployment URL with test user
  □ User can register account
  □ User can receive daily emails
  □ User can view in portal
  □ User can mark as read
  □ User can delete and restore
  □ User can search lessons
  □ User can change settings
  □ UI is intuitive and clear

□ Documentation
  □ SETUP_GUIDE.md reviewed and accurate
  □ README_ENHANCED.md has correct URLs
  □ API_DOCUMENTATION.md complete
  □ Troubleshooting section covers common issues
  □ Installation scripts tested

□ Education
  □ User knows how to set up locally
  □ User knows how to deploy to cloud
  □ User knows how to use portal
  □ User knows how to customize topics
  □ User has contact for support

═══════════════════════════════════════════════════════════════════════════
PHASE 5: ONGOING MAINTENANCE
═══════════════════════════════════════════════════════════════════════════

□ Daily
  □ Check that email sent (easycron logs)
  □ Verify email received in inbox
  □ Spot check portal is accessible

□ Weekly
  □ Review Vercel logs for errors
  □ Check MongoDB storage usage
  □ Verify scheduler is working

□ Monthly
  □ Review application performance
  □ Update topics if needed
  □ Check for any user-reported issues
  □ Test disaster recovery (backup restore)

□ Quarterly
  □ Review dependencies for updates
  □ Test major workflows end-to-end
  □ Review security practices
  □ Plan new features

═══════════════════════════════════════════════════════════════════════════
TROUBLESHOOTING REFERENCE
═══════════════════════════════════════════════════════════════════════════

Issue: Email not sending on schedule
Solution:
  ✓ Check easycron logs to verify webhook called
  ✓ Check Vercel logs for 500 errors
  ✓ Test POST /api/test-email manually
  ✓ Verify SMTP credentials in Vercel environment
  ✓ Restart scheduler or redeploy

Issue: Users can't login
Solution:
  ✓ Check MongoDB connection in logs
  ✓ Verify IP whitelist includes Vercel IPs
  ✓ Check Flask secret key is consistent
  ✓ Clear browser cookies and try again

Issue: Lessons not appearing in portal
Solution:
  ✓ Verify email was sent (check EmailLog collection)
  ✓ Check UserLessonStatus collection has records
  ✓ Try refreshing browser
  ✓ Check browser console for errors
  ✓ Verify user is logged in correctly

Issue: 500 Internal Server Error
Solution:
  ✓ Check Vercel logs for stack trace
  ✓ Check MongoDB connection
  ✓ Look for typos in code
  ✓ Test locally to reproduce
  ✓ Redeploy if code changed

Issue: Scheduler running but not sending emails
Solution:
  ✓ Check APScheduler is running (application logs)
  ✓ Verify SEND_HOUR and SEND_MINUTE are set correctly
  ✓ Account for timezone (UTC vs local)
  ✓ Check SMTP credentials
  ✓ Use external cron service (more reliable)

═══════════════════════════════════════════════════════════════════════════
TESTING COMMANDS (When Deployed)
═══════════════════════════════════════════════════════════════════════════

Test email sending:
  curl -X POST https://your-url.vercel.app/api/test-email

Manual trigger send:
  curl -X POST https://your-url.vercel.app/api/send-now -H "Cookie: session=..."

Get stats:
  curl -X GET https://your-url.vercel.app/api/stats -H "Cookie: session=..."

═══════════════════════════════════════════════════════════════════════════
FINAL VERIFICATION BEFORE GOING LIVE
═══════════════════════════════════════════════════════════════════════════

□ Registration works and creates user
□ Login works with correct credentials
□ Login fails with wrong credentials
□ Dashboard displays correctly
□ Email sends when triggered
□ Email content is complete and formatted
□ Email links work
□ Lessons appear in portal after email
□ Read/unread tracking works
□ Delete moves to recycle bin (soft delete)
□ Restore works from recycle bin
□ Permanent delete works
□ Search filters correctly
□ Settings save preferences
□ Stats display correct numbers
□ Scheduler runs automatically at scheduled time
□ No sensitive data in logs
□ HTTPS working on all pages
□ Mobile responsive on all pages
□ Error pages display correctly
□ Database backups working
□ Monitoring alerts configured

═══════════════════════════════════════════════════════════════════════════
SIGN OFF
═══════════════════════════════════════════════════════════════════════════

Name: ________________________    Date: ____________

Testing completed: ☐ YES    ☐ NO

Ready for production: ☐ YES    ☐ NO

Notes: ________________________________________________________________

_____________________________________________________________________

═══════════════════════════════════════════════════════════════════════════

If all checkboxes are checked, your Medical Knowledge Portal is ready! 🎉

Good luck with your MBBS journey! 🏥📚
"""

if __name__ == "__main__":
    print(CHECKLIST)
