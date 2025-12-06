# Session Management Guide

## Overview

HonestBallot uses a local session management system that creates unique tokens for each user login. This allows multiple users to interact with the voting system simultaneously while maintaining separate sessions.

## How Sessions Work

### Session Creation

When a user logs in:

```python
# 1. User credentials are verified against the database
user = db.verify_user(email, password)

# 2. A unique session token is generated (UUID)
session_token = session_manager.create_session(
    user_id,
    username,
    email,
    role
)

# 3. Session is stored in both:
#    - Database (for persistence)
#    - In-memory cache (for fast access)
```

### Session Validation

On each user action:

```python
# The session token is verified
session = session_manager.verify_session(session_token)

# If valid, last_activity is updated
# If expired (>8 hours), session is terminated
```

### Session Termination

When user logs out:

```python
session_manager.end_session(session_token)
# - Session is removed from in-memory cache
# - Session is marked as inactive in database
```

## Multiple Concurrent Sessions

### Scenario: 5 Users Voting Simultaneously

```
┌─────────────────────────────────────────────┐
│         HonestBallot Local Database         │
├─────────────────────────────────────────────┤
│                                             │
│  User Sessions:                             │
│  ├─ alice_smith (token: uuid-1234...)      │
│  ├─ bob_johnson (token: uuid-5678...)      │
│  ├─ charlie_brown (token: uuid-9abc...)    │
│  ├─ diana_prince (token: uuid-def0...)     │
│  └─ eve_wilson (token: uuid-1234...)       │
│                                             │
│  Each session:                              │
│  ├─ Has unique session token               │
│  ├─ Maintains own state                    │
│  ├─ Can cast votes independently           │
│  └─ All votes recorded in shared database  │
│                                             │
└─────────────────────────────────────────────┘
```

## Session Data Structure

```python
{
    "token": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": 1,
    "username": "alice_smith",
    "email": "alice@honestballot.local",
    "role": "voter",
    "created_at": "2025-12-07T10:30:00",
    "last_activity": "2025-12-07T10:35:45"
}
```

## Implementation Details

### Database Layer (`models/database.py`)

```python
class Database:
    def create_user_session(self, user_id, session_token):
        """Create session record in database"""
        
    def verify_session(self, session_token):
        """Check if session is active"""
        
    def end_session(self, session_token):
        """Mark session as inactive"""
```

### Session Manager (`models/session_manager.py`)

```python
class SessionManager:
    def __init__(self):
        self.sessions = {}  # In-memory cache
        self.session_timeout = timedelta(hours=8)
        
    def create_session(self, user_id, username, email, role):
        """Create new session and store in memory + database"""
        
    def verify_session(self, session_token):
        """Validate session and check expiration"""
        
    def end_session(self, session_token):
        """Terminate session"""
```

### Main Application (`main.py`)

```python
class HonestBallotApp:
    def __init__(self):
        self.session_manager = SessionManager()
        self.current_session = None
        
    def handle_login(self, email, password):
        # Verify credentials
        user = self.session_manager.db.verify_user(email, password)
        
        # Create session
        session_token = self.session_manager.create_session(...)
        
        # Store current session
        self.current_session = {
            "token": session_token,
            "user_id": user["id"],
            ...
        }
```

## Flet Session Integration

Flet's built-in session storage is used to persist session data:

```python
# Store session in Flet page
page.session.set("current_session", self.current_session)
page.session.set("session_manager", self.session_manager)
page.session.set("db", self.db)

# Retrieve session
current_session = page.session.get("current_session")
session_manager = page.session.get("session_manager")
db = page.session.get("db")
```

## Testing Multiple Sessions

### Test Case 1: Concurrent Voting
```
1. Start 5 instances of the application
2. Login each with different user
3. Each user votes in home_page
4. Check database: voting_app.db
5. All votes should be recorded with correct user_id
```

### Test Case 2: Session Timeout
```
1. Login user
2. Wait >8 hours (or modify timeout in session_manager.py)
3. Try to perform action
4. Session should be expired and redirect to login
```

### Test Case 3: One Vote Per Position
```
1. User votes for President
2. User tries to vote again for President
3. Database constraint prevents duplicate vote
4. User gets error: "You have already voted for this position"
```

## Security Considerations

### Current Implementation
- Sessions use UUID tokens (cryptographically secure)
- Passwords hashed with SHA-256
- Session timeout: 8 hours of inactivity
- One-vote-per-position enforced at database level

### Future Enhancements
- SSL/TLS for network communication
- Rate limiting on login attempts
- Two-factor authentication
- Audit logging
- Session revocation capability
- IP address tracking per session

## Troubleshooting

### Session Not Persisting
- Check that `voting_app.db` exists and is readable
- Verify database tables were created: `python setup_db.py`
- Check session timeout hasn't been exceeded

### Login Always Failing
- Verify user exists: Check `voting_app.db` with SQLite browser
- Reset password: Delete database and reinitialize
- Check email format matches database

### Can't Run Multiple Sessions
- Each instance needs separate port (Flet handles this)
- Ensure database is not locked: Close other instances
- Try restarting all instances

## Advanced Usage

### Custom Session Timeout
Edit `models/session_manager.py`:
```python
self.session_timeout = timedelta(hours=8)  # Change to desired duration
```

### Add New User Roles
Edit `models/database.py`:
```python
# In create_user method, add role options:
db.create_user(username, email, password, role="admin")
```

### Monitor Active Sessions
```python
active_sessions = session_manager.get_all_sessions()
for token, session in active_sessions.items():
    print(f"{session['username']} - Active: {session['last_activity']}")
```

## Database Locking

SQLite handles concurrent access, but for best performance with multiple users:

```python
# In models/database.py
self.connection = sqlite3.connect(
    str(self.db_path),
    timeout=10.0,  # 10 second lock timeout
    check_same_thread=False  # Allow use across threads
)
```

## Performance Notes

- Session lookup: O(1) in-memory cache
- Database writes: Committed immediately
- Concurrent votes: SQLite handles with ACID transactions
- Maximum concurrent sessions: Limited by system resources

---

For more information, see README.md
