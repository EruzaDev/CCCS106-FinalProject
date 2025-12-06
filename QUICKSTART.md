# Quick Start Guide - HonestBallot Local Voting App

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python setup_db.py
```

Output:
```
Initializing HonestBallot Local Database...
--------------------------------------------------
✅ Database initialized successfully!

Demo Users Created:
--------------------------------------------------
  ID: 1
  Username: alice_smith
  Email: alice@honestballot.local
  Role: voter

  ID: 2
  Username: bob_johnson
  Email: bob@honestballot.local
  Role: voter

... (5 users total)

--------------------------------------------------
✅ All 5 demo users created with password: password123

You can now run: python main.py
```

### Step 3: Run the Application
```bash
python main.py
```

The app will open in your default browser or as a desktop application.

---

## 📝 Demo Credentials

Use any of these to login:

| Email | Password |
|-------|----------|
| alice@honestballot.local | password123 |
| bob@honestballot.local | password123 |
| charlie@honestballot.local | password123 |
| diana@honestballot.local | password123 |
| eve@honestballot.local | password123 |

---

## 🔄 Testing Multiple Users

### Option A: Multiple Browser Tabs (Recommended)
1. Run: `python main.py`
2. Login with alice's credentials
3. Open a new browser tab: `http://localhost:8550` (or whatever port is shown)
4. Login with bob's credentials
5. Each tab has its own session!

### Option B: Multiple Terminal Instances
1. Terminal 1: `python main.py` → Login as alice
2. Terminal 2: `python main.py` → Login as bob
3. Terminal 3: `python main.py` → Login as charlie
4. Each runs independently with unique session

### Option C: Multiple Machines
- Each computer runs `python main.py`
- Each has its own SQLite database (voting_app.db)
- Can share vote results by copying the database file

---

## 📂 Project Structure

```
.
├── main.py                    ← Run this
├── setup_db.py               ← Run first to initialize
├── requirements.txt
├── voting_app.db             ← Auto-created database
├── SESSION_MANAGEMENT.md     ← Advanced guide
├── models/
│   ├── database.py          ← SQLite management
│   └── session_manager.py   ← User sessions
└── pages/
    ├── login_page.py        ← Login screen
    ├── signup_page.py       ← Registration
    ├── home_page.py         ← Main dashboard
    ├── profile_page.py      ← User profile
    └── settings_page.py     ← Settings
```

---

## 🔑 Key Features

✅ **Local-Only** - No internet required, SQLite database
✅ **Multi-User** - Up to 5 simultaneous sessions
✅ **Unique Sessions** - Each user gets unique token
✅ **Vote Recording** - All votes saved in database
✅ **User Authentication** - Email/password login
✅ **Session Timeout** - 8 hours of inactivity
✅ **One Vote Per Position** - Database enforces rules

---

## 💡 Useful Commands

### Check Active Sessions
```python
# In Python shell after importing
from models.session_manager import SessionManager
sm = SessionManager()
sessions = sm.get_all_sessions()
for token, session in sessions.items():
    print(f"{session['username']}: {session['last_activity']}")
```

### View Database
```bash
# Using SQLite CLI
sqlite3 voting_app.db
sqlite> SELECT * FROM users;
sqlite> SELECT * FROM user_sessions;
sqlite> SELECT * FROM votes;
```

### Reset Everything
```bash
# Delete database
del voting_app.db  # Windows
# or
rm voting_app.db   # Mac/Linux

# Reinitialize
python setup_db.py

# Run again
python main.py
```

---

## 🐛 Troubleshooting

**Problem: "ModuleNotFoundError: No module named 'flet'"**
- Solution: `pip install -r requirements.txt`

**Problem: "Database locked" error**
- Solution: Close other running instances of the app

**Problem: Can't login with demo credentials**
- Solution: Run `python setup_db.py` to reinitialize database

**Problem: "Port already in use"**
- Solution: This is normal - Flet finds next available port automatically

---

## 📚 Learn More

- **Session Details**: See `SESSION_MANAGEMENT.md`
- **Full Documentation**: See `README.md`
- **Database Schema**: See `models/database.py`

---

## 🎯 Next Steps

1. ✅ Initialize database
2. ✅ Run application
3. ✅ Login with demo credentials
4. ✅ Test multiple users
5. Add voting functionality
6. Customize candidates
7. Deploy to production

---

Happy Voting! 🗳️
