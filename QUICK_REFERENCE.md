# HonestBallot - Quick Reference Card

## 🚀 GETTING STARTED

```bash
pip install -r requirements.txt
python setup_db.py
python main.py
```

---

## 👥 DEMO USERS

| Email | Password |
|-------|----------|
| alice@honestballot.local | password123 |
| bob@honestballot.local | password123 |
| charlie@honestballot.local | password123 |
| diana@honestballot.local | password123 |
| eve@honestballot.local | password123 |

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `main.py` | Application entry point |
| `setup_db.py` | Initialize database |
| `models/database.py` | SQLite management |
| `models/session_manager.py` | Session handling |
| `pages/login_page.py` | Login UI |

---

## 🔄 WORKFLOW

```
Start App
  ↓
Login with Email + Password
  ↓
Session Token Created (UUID)
  ↓
Token Stored in DB + Memory
  ↓
User Logged In (Home Page)
  ↓
Can Vote, View Profile, Settings
  ↓
Logout or 8-hour Timeout
  ↓
Session Terminated
```

---

## 💾 DATABASE

**Tables:**
- `users` - User accounts
- `user_sessions` - Active sessions
- `votes` - Cast votes
- `candidates` - Candidate info
- `election_sessions` - Election info

**File:** `voting_app.db` (SQLite)

---

## 🔐 SECURITY

✅ SHA-256 password hashing
✅ UUID session tokens
✅ One-vote-per-position
✅ 8-hour session timeout
✅ Email uniqueness

---

## 🧪 TESTING MULTI-USER

### Terminal Method
```bash
# Terminal 1
python main.py
# Login as: alice

# Terminal 2
python main.py
# Login as: bob

# Terminal 3
python main.py
# Login as: charlie
```

### Browser Tab Method
```
1. python main.py
2. Login as: alice
3. New tab: http://localhost:8550
4. Login as: bob
5. New tab: http://localhost:8550
6. Login as: charlie
```

---

## 🐛 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| flet not found | `pip install -r requirements.txt` |
| Database locked | Close other instances |
| Login fails | `python setup_db.py` |
| Port in use | Flet auto-selects next |

---

## 📊 SESSION INFO

- **Token Type:** UUID (Unique)
- **Timeout:** 8 hours inactivity
- **Storage:** Memory + Database
- **Max Users:** 5 (configurable)
- **Concurrent Sessions:** Unlimited

---

## 🎯 FEATURES

✅ Local-only (no internet)
✅ Multi-user support
✅ Unique sessions per user
✅ Vote recording
✅ User authentication
✅ Password hashing
✅ Session persistence

---

## 📚 DOCUMENTATION

| File | Content |
|------|---------|
| `README.md` | Full guide |
| `QUICKSTART.md` | 3-step setup |
| `SESSION_MANAGEMENT.md` | Technical details |
| `ARCHITECTURE.md` | System design |
| `IMPLEMENTATION.md` | What's built |

---

## 🔧 COMMON COMMANDS

```bash
# Initialize
python setup_db.py

# Run app
python main.py

# Reset database
del voting_app.db
python setup_db.py

# Check Python version
python --version  # Need 3.11+

# Check dependencies
pip list | grep flet
```

---

## 📝 CODE SNIPPETS

### Check Active Sessions
```python
from models.session_manager import SessionManager
sm = SessionManager()
sessions = sm.get_all_sessions()
for token, session in sessions.items():
    print(f"{session['username']}: {session['last_activity']}")
```

### Reset Database
```python
import os
os.remove('voting_app.db')
from models.database import init_demo_data
init_demo_data()
```

### Test Login
```python
from models.database import Database
db = Database()
user = db.verify_user('alice@honestballot.local', 'password123')
print(user)  # Should print: {'id': 1, 'username': 'alice_smith', ...}
```

---

## 🎓 LEARNING PATHS

### Path 1: Setup & Run
1. Read: QUICKSTART.md
2. Run: `python setup_db.py`
3. Run: `python main.py`
4. Test multi-user

### Path 2: Understand Sessions
1. Read: SESSION_MANAGEMENT.md
2. Review: models/session_manager.py
3. Review: models/database.py
4. Test: Check active sessions

### Path 3: Full Architecture
1. Read: ARCHITECTURE.md
2. Read: IMPLEMENTATION.md
3. Read: main.py
4. Read: pages/*.py

---

## ✅ CHECKLIST

- [ ] Python 3.11+ installed
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Can login with demo credentials
- [ ] Multiple concurrent users work
- [ ] Logout terminates session

---

## 🚀 NEXT STEPS

1. ✅ Setup & run app
2. ✅ Test login/logout
3. ✅ Test multi-user
4. Add voting interface
5. Add results display
6. Deploy to production

---

## 📞 SUPPORT

**Error?** Check `TROUBLESHOOTING.md`
**Question?** See `README.md`
**Technical?** See `SESSION_MANAGEMENT.md`
**Architecture?** See `ARCHITECTURE.md`

---

**Version:** 1.0 - Local Multi-User Alpha
**Last Updated:** December 7, 2025
**Status:** ✅ Ready for Testing

Enjoy! 🗳️
