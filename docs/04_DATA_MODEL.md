# Data Model - Entity Relationship Diagram

## Database Schema Overview

The HonestBallot application uses **SQLite** as its database engine with the following tables:

## Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              HONESTBALLOT ERD                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐         ┌─────────────────────┐         ┌─────────────────┐
│       USERS         │         │        VOTES        │         │   CANDIDATES    │
├─────────────────────┤         ├─────────────────────┤         ├─────────────────┤
│ PK id              │◄────────┤ FK voter_id         │         │ FK user_id      │
│    username        │         │ FK candidate_id     │────────►│    position     │
│    email           │         │    position         │         │    party        │
│    password_hash   │         │    election_session │         │    biography    │
│    role            │         │    created_at       │         │    profile_image│
│    full_name       │         └─────────────────────┘         └─────────────────┘
│    position        │                                                    │
│    party           │         ┌─────────────────────┐                   │
│    biography       │         │   LEGAL_RECORDS     │                   │
│    profile_image   │         ├─────────────────────┤                   │
│    created_at      │◄────────┤ FK politician_id    │◄──────────────────┘
└─────────────────────┘         │    record_type      │
         │                      │    title            │
         │                      │    description      │
         │                      │    record_date      │
         │                      │    status           │
         │                      │ FK added_by         │
         │                      │ FK verified_by      │
         │                      │    created_at       │
         │                      └─────────────────────┘
         │
         │                      ┌─────────────────────┐
         │                      │    AUDIT_LOGS       │
         │                      ├─────────────────────┤
         └─────────────────────►│ FK user_id          │
                                │    action           │
                                │    action_type      │
                                │    description      │
                                │    user_role        │
                                │    target_type      │
                                │    target_id        │
                                │    details (JSON)   │
                                │    ip_address       │
                                │    created_at       │
                                └─────────────────────┘

┌─────────────────────┐         ┌─────────────────────┐
│   VOTING_STATUS     │         │ ELECTION_SESSIONS   │
├─────────────────────┤         ├─────────────────────┤
│ PK id              │         │ PK id              │
│    is_active       │         │    name             │
│    started_at      │         │    description      │
│    ended_at        │         │    start_date       │
│ FK updated_by      │         │    end_date         │
└─────────────────────┘         │    status           │
                                │ FK created_by       │
┌─────────────────────┐         │    created_at       │
│   USER_SESSIONS     │         └─────────────────────┘
├─────────────────────┤
│ PK id              │         ┌─────────────────────┐
│ FK user_id         │         │ACHIEVEMENT_VERIFY   │
│    session_token   │         ├─────────────────────┤
│    is_active       │         │ PK id              │
│    created_at      │         │ FK politician_id    │
│    last_activity   │         │    achievement_title│
└─────────────────────┘         │    description      │
                                │    evidence_url     │
                                │    status           │
                                │ FK verified_by      │
                                │    created_at       │
                                └─────────────────────┘
```

## Table Definitions

### 1. USERS Table
Primary table storing all user accounts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| username | TEXT | UNIQUE, NOT NULL | Login username |
| email | TEXT | UNIQUE, NOT NULL | User email address |
| password_hash | TEXT | NOT NULL | Hashed password (SHA-256) |
| role | TEXT | NOT NULL | One of: voter, politician, comelec, nbi |
| full_name | TEXT | | User's full name |
| position | TEXT | | Political position (for politicians) |
| party | TEXT | | Political party affiliation |
| biography | TEXT | | User biography/platform |
| profile_image | TEXT | | Path to profile image |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation time |

### 2. VOTES Table
Stores all cast votes.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique vote identifier |
| voter_id | INTEGER | FOREIGN KEY → users.id | Who cast the vote |
| candidate_id | INTEGER | FOREIGN KEY → users.id | Who received the vote |
| position | TEXT | NOT NULL | Position being voted for |
| election_session_id | INTEGER | FOREIGN KEY | Election session reference |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Vote timestamp |

**Constraint**: UNIQUE(voter_id, position, election_session_id) - One vote per position per election

### 3. LEGAL_RECORDS Table
NBI-managed legal records for politicians.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Record identifier |
| politician_id | INTEGER | FOREIGN KEY → users.id | Associated politician |
| record_type | TEXT | NOT NULL | Type: Case Filing, Investigation, etc. |
| title | TEXT | NOT NULL | Record title |
| description | TEXT | | Detailed description |
| record_date | TEXT | | Date of the record |
| status | TEXT | DEFAULT 'pending' | pending, verified, rejected |
| added_by | INTEGER | FOREIGN KEY → users.id | NBI officer who added |
| verified_by | INTEGER | FOREIGN KEY → users.id | Verifying officer |
| verified_at | TIMESTAMP | | Verification timestamp |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |

### 4. AUDIT_LOGS Table
Complete action audit trail.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Log entry identifier |
| action | TEXT | NOT NULL | Action performed |
| action_type | TEXT | NOT NULL | Category: login, vote, etc. |
| description | TEXT | | Detailed description |
| user_id | INTEGER | FOREIGN KEY → users.id | User who performed action |
| user_role | TEXT | | Role at time of action |
| target_type | TEXT | | Type of target entity |
| target_id | INTEGER | | ID of target entity |
| details | TEXT | | JSON-encoded extra details |
| ip_address | TEXT | | Client IP address |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Log timestamp |

### 5. VOTING_STATUS Table
Election voting period control.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Status entry ID |
| is_active | INTEGER | DEFAULT 0 | 1 = voting open, 0 = closed |
| started_at | TIMESTAMP | | When voting started |
| ended_at | TIMESTAMP | | When voting ended |
| updated_by | INTEGER | FOREIGN KEY → users.id | COMELEC admin who changed |

### 6. USER_SESSIONS Table
Active user session tracking.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Session ID |
| user_id | INTEGER | FOREIGN KEY → users.id | Session owner |
| session_token | TEXT | UNIQUE | UUID session token |
| is_active | INTEGER | DEFAULT 1 | Session active status |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Session start |
| last_activity | TIMESTAMP | | Last activity time |

## Relationships Summary

| Relationship | Type | Description |
|-------------|------|-------------|
| Users → Votes | 1:N | One voter can cast multiple votes (different positions) |
| Users → Legal_Records | 1:N | One politician can have multiple legal records |
| Users → Audit_Logs | 1:N | One user can generate multiple audit entries |
| Users → User_Sessions | 1:N | One user can have multiple session history |
| Voting_Status → Users | N:1 | Status changes tracked by user |

---

*Document Version: 1.0*  
*Last Updated: December 2025*
