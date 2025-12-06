# HonestBallot - Visual Architecture Guide

## System Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    Flet UI Framework                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Login Page   │  │  Home Page   │  │ Profile Page │     │
│  │              │  │              │  │              │     │
│  │ • Email      │  │ • Dashboard  │  │ • User Info  │     │
│  │ • Password   │  │ • Navigation │  │ • Settings   │     │
│  │ • Submit     │  │ • Features   │  │ • Back       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│        │                   │                   │            │
│        └───────────────────┴───────────────────┘            │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │ Main.py (App)  │
                    │ Controller     │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ SessionManager   │ │ Database Layer   │ │ Page Session     │
│                  │ │ (SQLite)         │ │ Storage (Flet)   │
│ • Create Session │ │                  │ │                  │
│ • Verify Session │ │ • User Auth      │ │ • Current User   │
│ • End Session    │ │ • Store Sessions │ │ • Session Token  │
│ • Track Active   │ │ • Record Votes   │ │ • Manager Ref    │
│   Sessions       │ │ • Candidates     │ │ • Database Ref   │
└──────────────────┘ └──────────────────┘ └──────────────────┘
        │                   │
        └───────────────────┼───────────────────┐
                            │                   │
                    ┌───────▼─────────────┐     │
                    │  SQLite Database    │     │
                    │  voting_app.db      │     │
                    │                     │     │
                    │ ┌─────────────────┐ │     │
                    │ │ users           │ │     │
                    │ │ user_sessions   │ │     │
                    │ │ votes           │ │     │
                    │ │ candidates      │ │     │
                    │ │ election_       │ │     │
                    │ │   sessions      │ │     │
                    │ └─────────────────┘ │     │
                    └─────────────────────┘     │
                                                │
                    ┌───────────────────────────┘
                    │
                    ▼
        ┌──────────────────────────┐
        │  File System (Local)     │
        │  voting_app.db           │
        │  (All data persisted)    │
        └──────────────────────────┘
```

## Multi-User Session Flow

```
USER 1: Alice                   USER 2: Bob                     USER 3: Charlie
┌─────────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│ Terminal/Browser 1  │    │ Terminal/Browser │    │ Terminal/Browser 3 │
│                     │    │ 2                │    │                    │
│ App Instance 1      │    │ App Instance 2   │    │ App Instance 3     │
└──────────┬──────────┘    └────────┬─────────┘    └──────────┬─────────┘
           │                        │                         │
           │                        │                         │
    ┌──────▼────────┐        ┌──────▼────────┐        ┌──────▼────────┐
    │ Login: alice@ │        │ Login: bob@   │        │ Login:        │
    │ honestballot  │        │ honestballot  │        │ charlie@      │
    │               │        │               │        │ honestballot  │
    │ password123   │        │ password123   │        │               │
    │               │        │               │        │ password123   │
    └──────┬────────┘        └──────┬────────┘        └──────┬────────┘
           │                        │                        │
           │ Verify              │ Verify                │ Verify
           │ Credentials         │ Credentials            │ Credentials
           └────────┬────────────┴────────────┬────────────┘
                    │                        │
                    ▼                        ▼
            ┌─────────────────────┐
            │ SQLite Database     │
            │ (SHARED)            │
            │                     │
            │ ┌─────────────────┐ │
            │ │ users           │ │
            │ │ alice_smith  ✓  │ │
            │ │ bob_johnson  ✓  │ │
            │ │ charlie_brown✓  │ │
            │ └─────────────────┘ │
            └─────────────────────┘
                    │ │ │
        ┌───────────┼─┼─┴───────────┐
        │           │ │             │
        ▼           ▼ ▼             ▼
    ┌────────┐  ┌────────┐      ┌────────┐
    │Session:│  │Session:│      │Session:│
    │Token:  │  │Token:  │      │Token:  │
    │uuid-A  │  │uuid-B  │      │uuid-C  │
    │        │  │        │      │        │
    │ Stored │  │ Stored │      │ Stored │
    │ in:    │  │ in:    │      │ in:    │
    │ Memory │  │ Memory │      │ Memory │
    │ +      │  │ +      │      │ +      │
    │ DB     │  │ DB     │      │ DB     │
    └────────┘  └────────┘      └────────┘
        │           │              │
        └───────────┼──────────────┘
                    │
            ┌───────▼─────────┐
            │ Active Sessions │
            │                 │
            │ Alice: active   │
            │ Bob: active     │
            │ Charlie: active │
            └─────────────────┘
```

## Database Schema Visualization

```
┌─────────────────────────────────────────────────────────┐
│                 SQLite Database                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  USERS TABLE              USER_SESSIONS TABLE          │
│  ┌──────────────────┐     ┌──────────────────────┐     │
│  │ id (PK)          │◄───→│ id (PK)              │     │
│  │ username         │     │ user_id (FK)         │     │
│  │ email            │     │ session_token        │     │
│  │ password_hash    │     │ login_time           │     │
│  │ role             │     │ last_activity        │     │
│  │ created_at       │     │ is_active            │     │
│  │ last_login       │     └──────────────────────┘     │
│  └──────────────────┘                                   │
│           │                       ▲                     │
│           │                       │                     │
│           └───────────────────────┘                     │
│                                                         │
│  VOTES TABLE                CANDIDATES TABLE           │
│  ┌──────────────────────┐  ┌──────────────────┐       │
│  │ id (PK)              │  │ id (PK)          │       │
│  │ voter_id (FK) ────────→ │ position         │       │
│  │ candidate_id (FK) ──────→ name             │       │
│  │ position             │  │ party            │       │
│  │ election_session_id  │  │ bio              │       │
│  │ timestamp            │  │ created_at       │       │
│  │ UNIQUE(voter_id,     │  └──────────────────┘       │
│  │         position,    │                              │
│  │         election_id) │   ELECTION_SESSIONS TABLE    │
│  └──────────────────────┘   ┌──────────────────────┐   │
│           │                 │ id (PK)              │   │
│           │                 │ name                 │   │
│           │                 │ start_time           │   │
│           └────────────────→ │ end_time             │   │
│                             │ is_active            │   │
│                             │ created_at           │   │
│                             └──────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Session Lifecycle Timeline

```
USER ACTION TIMELINE
═══════════════════════════════════════════════════════════════

00:00 ► Application Launched
       ├─ main.py starts
       ├─ Database connection established
       ├─ Session manager initialized
       └─ Login page displayed

00:05 ► User Enters Credentials
       ├─ alice@honestballot.local
       ├─ password123
       └─ Login button clicked

00:06 ► Credentials Verified
       ├─ Database query: SELECT password_hash FROM users WHERE email=?
       ├─ SHA-256 comparison
       ├─ Match found ✓
       └─ User record retrieved

00:07 ► Session Created
       ├─ UUID token generated: uuid-abc123def456
       ├─ Session record inserted in DB
       ├─ Session added to memory cache
       └─ page.session updated

00:08 ► User Logged In
       ├─ Home page displayed
       ├─ Session token active
       ├─ Last activity: 00:08
       └─ Timeout clock starts (8 hours)

04:08 ► User Performs Action
       ├─ last_activity updated: 04:08
       ├─ Timeout clock reset
       └─ Session remains active

08:08 ► TIMEOUT THRESHOLD REACHED
       ├─ Session age: 8 hours
       ├─ Session marked inactive
       ├─ User session terminated
       └─ Next page refresh → login required

08:09 ► User Clicks Logout
       ├─ logout() handler called
       ├─ Session record updated
       ├─ Memory cache cleared
       ├─ Token invalidated
       └─ Login page displayed

08:10 ► Session Completely Removed
       ├─ No active sessions for user
       ├─ Can login again with new token
       └─ Ready for next user

═══════════════════════════════════════════════════════════════
```

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────┐
│                   USER INPUT                             │
│  (Login Form: email + password)                          │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
         ┌──────────────────┐
         │ Validate Input   │
         │ • Non-empty?     │
         │ • Email format?  │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────────────┐
         │ Query Database           │
         │ WHERE email = ?          │
         └────────┬─────────────────┘
                  │
          ┌───────┴────────┐
          │                │
    Found │                │ Not Found
          │                │
          ▼                ▼
    ┌─────────────┐   ┌──────────────┐
    │ Verify Hash │   │ Show Error   │
    │ Match?      │   │ "Invalid     │
    └──┬──────────┘   │ credentials" │
       │              └──────────────┘
    Yes│
       ▼
    ┌─────────────────────────────┐
    │ Generate Session Token      │
    │ token = uuid.uuid4()        │
    └────────┬────────────────────┘
             │
             ▼
    ┌─────────────────────────────┐
    │ Insert Session to Database  │
    └────────┬────────────────────┘
             │
             ▼
    ┌─────────────────────────────┐
    │ Add to Memory Cache         │
    │ sessions[token] = {...}     │
    └────────┬────────────────────┘
             │
             ▼
    ┌─────────────────────────────┐
    │ Store in page.session       │
    │ (Flet session storage)      │
    └────────┬────────────────────┘
             │
             ▼
    ┌─────────────────────────────┐
    │ Redirect to Home Page       │
    └─────────────────────────────┘
```

## File Dependencies

```
main.py (Core App Controller)
│
├──► models/
│    ├── database.py (SQLite Management)
│    │   ├── Initialize DB tables
│    │   ├── User CRUD operations
│    │   ├── Vote management
│    │   └── Session persistence
│    │
│    └── session_manager.py (Session Handling)
│        ├── Create sessions
│        ├── Verify tokens
│        ├── Manage timeouts
│        └── Track active users
│
├──► pages/
│    ├── login_page.py (UI: Login)
│    ├── signup_page.py (UI: Registration)
│    ├── home_page.py (UI: Dashboard)
│    ├── profile_page.py (UI: Profile)
│    └── settings_page.py (UI: Preferences)
│
└──► setup_db.py (Database Initialization)
     └── Creates demo users & data
```

## Session Token Generation

```
user_id=1
username="alice_smith"
email="alice@honestballot.local"
                │
                ▼
    ┌─────────────────────────────┐
    │  uuid.uuid4()               │
    │                             │
    │  Generated Token:           │
    │  550e8400-e29b-41d4-        │
    │  a716-446655440000         │
    │                             │
    └────────────┬────────────────┘
                 │
        ┌────────┴─────────┐
        │                  │
        ▼                  ▼
    Database          Memory Cache
    INSERT INTO       sessions{
    user_sessions       token: {
    VALUES             user_id: 1,
    (1,                username: "alice",
     token,            email: "alice@...",
     now(),            created: now(),
     now(),            last_activity: now()
     1)              }
                     }

    Result:
    ────────────────────────────────
    Session Created
    Token: 550e8400-e29b-41d4-...
    Active: Yes
    Timeout: 8 hours
```

---

For step-by-step instructions, see: **QUICKSTART.md**
For technical details, see: **SESSION_MANAGEMENT.md**
For full documentation, see: **README.md**
