# 🏥 Medical Knowledge Portal - Enhanced Version

**Daily automated medical lessons to your inbox + Personal learning portal with tracking, recycle bin, and 150-day spaced repetition.**

Perfect for MBBS students to build comprehensive medical knowledge with daily reinforcement.

---

## ✨ Features

### 📧 **Daily Email Lessons**
- Automated email every morning (customizable time)
- Covers: diseases, surgeries, diagnosis, treatment drugs, symptoms, ADRs
- Content from Wikipedia + YouTube educational videos
- No repetition same day
- Auto-repeat after 150 days

### 📚 **Personal Learning Portal**
- Login/Register with secure authentication
- View all received lessons in beautiful UI
- Track read/unread status
- Search and filter by disease name or category
- Sort by date received
- View lesson details with full medical information
- Educational videos embedded

### 🗑️ **Soft Delete & Recycle Bin**
- Delete lessons to recycle bin (not permanent)
- Recover deleted lessons anytime
- Permanently delete when ready
- Track deletion dates

### 🔄 **Smart Repeat Cycle**
- Automatically repeat lessons after 150 days
- Customizable repeat interval (30-365 days)
- Can toggle auto-repeat on/off
- Manually pause/resume anytime

### ⚙️ **User Settings**
- Control daily email sending
- Enable/disable auto-repeat
- Customize repeat interval
- View learning statistics
- Change email preferences

### 📊 **Dashboard Statistics**
- Total lessons received
- Lessons read vs unread
- Items in recycle bin
- Learning streak
- Study progress

---

## 🚀 Quick Start

### **Local Setup (5 minutes)**

#### 1. **Windows Users**
```cmd
cd disease-reminder\disease-reminder
setup.bat
```

#### 2. **Mac/Linux Users**
```bash
cd disease-reminder/disease-reminder
chmod +x setup.sh
./setup.sh
```

#### 3. **Manual Setup**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements_enhanced.txt
cp .env.example_enhanced .env
# Edit .env with your credentials
python app_enhanced.py
```

Then visit: **http://localhost:5000/register**

---

## 🔧 Configuration

### **Required: MongoDB**
1. Create free account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Get connection string: `mongodb+srv://user:pass@cluster.mongodb.net/medical_portal`
4. Add to `.env` as `MONGO_URI`

### **Required: Gmail SMTP**
1. Enable 2-factor authentication on Gmail
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Generate app password for "Mail" + "Windows Computer"
4. Copy 16-char password → `.env` as `SMTP_PASS`

### **Optional: YouTube API**
1. Create project at [console.cloud.google.com](https://console.cloud.google.com)
2. Enable YouTube Data API v3
3. Create API key
4. Add to `.env` as `YOUTUBE_API_KEY`

### **Schedule Configuration**
```env
SEND_HOUR=7        # Hour (0-23, in UTC)
SEND_MINUTE=0      # Minute (0-59)

# For 7 AM India Time (IST):
SEND_HOUR=1
SEND_MINUTE=30
```

---

## 🌍 Deploy to Vercel (Free)

### **Step 1: Prepare Code**
```bash
git init
git add .
git commit -m "Medical Portal"
git remote add origin https://github.com/USERNAME/medical-portal.git
git push origin main
```

### **Step 2: Deploy**
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import GitHub repository
3. Set project root: `disease-reminder/disease-reminder`
4. Add environment variables from `.env.example_enhanced`
5. Click **Deploy**

### **Step 3: Get URL**
After deployment: `https://your-project.vercel.app`

### **Step 4: Set Scheduler (Important)**
Vercel serverless functions have limitations. Use external cron:
- [EasyCron](https://www.easycron.com) - FREE
- [cron-job.org](https://cron-job.org) - FREE

Set webhook: `POST` → `https://your-project.vercel.app/api/send-now`

**Schedule**: Daily at your preferred time

---

## 📱 How to Use

### **First Login**
1. Visit your deployed URL or `http://localhost:5000`
2. Click "Register here"
3. Enter name, email, password
4. You're in! ✅

### **Dashboard**
- See all lessons with read/unread badges
- Search by disease name or category
- Click "View" for full details
- Click "Delete" to move to trash
- Click "Resend" to get email again

### **Lesson Details**
- Full medical information
- Wikipedia summary
- Educational video link
- Diagnostic criteria
- Treatment protocols
- Drug doses & ADRs
- Print or download

### **Recycle Bin**
- See deleted lessons
- "Restore" to get back
- "Delete Forever" for permanent removal

### **Settings**
- Toggle daily emails on/off
- Enable/disable auto-repeat
- Change repeat interval (30-365 days)
- View learning statistics

---

## 📧 Email Format

Each daily email includes:

```
Subject: 📚 Daily Medical Lesson - [Disease Name]

---

🏥 MEDICAL KNOWLEDGE PORTAL
Daily Lesson - [Date]

📌 Today's Topic: Anaphylactic Shock
🏷️ Category: Emergency Medicine

📖 Overview:
[Wikipedia summary of condition]

🎬 Educational Video:
[YouTube link for visual learning]

🔍 Key Points:
• Pathophysiology and epidemiology
• Diagnostic criteria
• Treatment protocols
• Drug management & doses
• Adverse reactions
• Clinical warning signs

💊 Common Medications:
[Drug names and doses]

⚠️ Adverse Drug Reactions:
[Common ADRs]

---

👁️ View online: https://your-portal.com/lesson/[ID]
📱 Open in portal for full details and to mark as read

---
```

---

## 🎓 Medical Topics Covered

### Emergency Medicine (6)
- Anaphylactic Shock
- Cardiogenic Shock
- Septic Shock
- Status Epilepticus
- ARDS
- Diabetic Ketoacidosis

### Internal Medicine (14)
- Myocardial Infarction
- Heart Failure
- Chronic Kidney Disease
- Pulmonary Embolism
- COPD
- Rheumatoid Arthritis
- Tuberculosis
- Anemia
- Hypothyroidism
- Hyperthyroidism
- Cirrhosis
- Peptic Ulcer
- Stroke
- SLE

### Surgery (9)
- Acute Appendicitis
- Cholecystitis
- Inguinal Hernia
- Bowel Obstruction
- Peritonitis
- Breast Cancer (Surgical)
- Thyroid Nodule
- Burns Management
- Compartment Syndrome

### Pediatrics
- Neonatal Jaundice
- Measles
- Cerebral Palsy
- [+ 20+ more]

### And more...
**Total: 200+ topics** - Edit `topics.py` to add more!

---

## 🔐 Security

- ✅ Password hashing (Werkzeug)
- ✅ Secure session tokens
- ✅ MongoDB password protected
- ✅ HTTPS on Vercel
- ✅ Only you can see your data
- ✅ No third-party tracking

---

## 📊 Database Schema

### Users
```json
{
  "_id": ObjectId,
  "email": "student@medical.edu",
  "password": "hashed",
  "name": "Dr. Student",
  "created_at": Datetime,
  "email_preference": {
    "send_daily": true,
    "auto_repeat_enabled": true,
    "repeat_after_days": 150
  }
}
```

### Lessons
```json
{
  "_id": ObjectId,
  "name": "Anaphylactic Shock",
  "category": "Emergency Medicine",
  "query": "Anaphylactic shock",
  "video_info": {...},
  "wiki_info": {...},
  "created_at": Datetime,
  "sent_count": 12
}
```

### UserLessonStatus
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "lesson_id": ObjectId,
  "sent_at": Datetime,
  "read": true,
  "read_at": Datetime,
  "deleted": false,
  "deleted_at": Datetime,
  "in_recycle_bin": false
}
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Email not sending | Check SMTP credentials, verify Gmail app password |
| Login fails | Clear browser cookies, check MongoDB connection |
| Scheduler not working on Vercel | Use external cron service (EasyCron) |
| MongoDB connection error | Check IP whitelist, verify URI format |
| Lessons not showing | Check if admin user registered first |

---

## 🎯 Study Tips

1. **Read Every Morning**: Set a calendar reminder
2. **Mark Lessons**: Mark as read after studying
3. **Review Before Exams**: Search topics by category
4. **Use Portal**: Bookmark for quick access
5. **Watch Videos**: Click YouTube links for visual learning
6. **Take Notes**: Print or PDF for your study notes
7. **Study Groups**: Share portal with classmates

---

## 📈 Advanced Features (Coming Soon)

- [ ] PDF export of lessons
- [ ] Quiz generator from lessons
- [ ] Spaced repetition algorithm
- [ ] Study streaks & achievements
- [ ] Progress analytics & charts
- [ ] Dark mode
- [ ] Mobile app
- [ ] Study groups / sharing

---

## 📝 Customization

### **Add More Medical Topics**
Edit `topics.py`:
```python
TOPICS = [
    {"name": "New Disease", "category": "Medicine", "query": "disease name"},
    # ... add more
]
```

### **Change Email Time**
Edit `.env`:
```env
SEND_HOUR=8      # 8 AM
SEND_MINUTE=30   # 8:30 AM
```

### **Change Repeat Interval**
In Settings page → change "Repeat lessons after X days"

---

## 💡 Architecture

```
Medical Portal
├── Backend (Flask)
│   ├── app_enhanced.py (main app with routes)
│   ├── models.py (MongoDB schema)
│   ├── utils/ (email, youtube, wiki)
│   └── topics.py (500+ medical topics)
├── Frontend (HTML/CSS/JS)
│   ├── login.html
│   ├── dashboard.html
│   ├── lesson_detail.html
│   ├── recycle_bin.html
│   └── settings.html
└── Database
    └── MongoDB Atlas (Cloud)
```

**Hosting**: Vercel (Serverless)

---

## 📞 Support

Facing issues?
1. Check error messages on dashboard
2. Test email with `/api/test-email`
3. Verify `.env` configuration
4. Check MongoDB connectivity
5. Review logs on Vercel dashboard

---

## 📄 Files Included

```
disease-reminder/
├── disease-reminder/
│   ├── app_enhanced.py ⭐ (Main enhanced app)
│   ├── models.py ⭐ (Database models)
│   ├── requirements_enhanced.txt (Dependencies)
│   ├── .env.example_enhanced (.env template)
│   ├── setup.sh (Linux setup script)
│   ├── setup.bat (Windows setup script)
│   ├── templates/
│   │   ├── login.html ⭐
│   │   ├── register.html ⭐
│   │   ├── dashboard.html ⭐
│   │   ├── lesson_detail.html ⭐
│   │   ├── recycle_bin.html ⭐
│   │   ├── settings.html ⭐
│   │   ├── 404.html
│   │   └── 500.html
│   └── utils/ (existing email, youtube, wiki utils)
├── SETUP_GUIDE.md (Detailed setup instructions)
└── vercel_enhanced.json (Vercel config)

⭐ = New files for enhanced version
```

---

## 🎓 Perfect For

- ✅ MBBS students (1st, 2nd, 3rd, 4th year)
- ✅ Medical interns & residents
- ✅ Medical competitive exams (NEET, PG)
- ✅ Quick medical knowledge review
- ✅ Daily learning habit building
- ✅ Medical school coursework tracking

---

## 📜 License

Open source - feel free to modify and use!

---

**Happy Learning! 🏥📚**

Start receiving your daily medical lessons today and build comprehensive medical knowledge month by month.

**Time to register: http://localhost:5000/register** ⏰
