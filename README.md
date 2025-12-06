# HonestBallot - Voting Application

A cross-platform voting application built with Python Flet framework, designed to provide transparent and secure voting mechanisms with comprehensive election management capabilities.

## 🎯 Project Overview

HonestBallot is a voting platform that demonstrates how technology can support electoral transparency. The system supports multiple user roles with specialized dashboards for different voting participants.

### User Roles

1. **Voters** - Cast votes, view election results
2. **Candidates** - Manage profiles and campaign information
3. **Election Officials** - Manage voting process, view real-time results
4. **Administrators** - System oversight and configuration

## 🚀 Features

### Core Features
- ✅ User authentication and role-based access control
- ✅ Secure voting mechanism with integrity checks
- ✅ Real-time vote counting and results display
- ✅ Candidate profile management
- ✅ Responsive cross-platform design

### Voting System
- ✅ Position-based voting interface
- ✅ One vote per position enforcement
- ✅ Vote submission with confirmation
- ✅ Real-time vote tallying
- ✅ Results dashboard with analytics

### Administrative Features
- ✅ Election session management
- ✅ Voter registration
- ✅ Results verification
- ✅ Audit trails and logging

## 🛠️ Technology Stack

### Current Implementation
- **Framework:** Python Flet (Flutter-based)
- **Language:** Python 3.11+
- **Database:** SQLite (Local)
- **Architecture:** Component-based with MVC pattern
- **Session Management:** Unique user sessions with token-based authentication

### Key Features
- **Local-Only:** Runs completely offline with SQLite database
- **Multi-User Sessions:** Up to 5 simultaneous users with unique sessions
- **Pre-Configured Users:** 5 demo users ready to use
- **Session Tokens:** Each user gets a unique session token

### Planned Production Stack
- **Backend:** Firebase or Node.js + Express
- **Database:** Firestore or PostgreSQL
- **Authentication:** Firebase Auth or JWT
- **Hosting:** Docker, Heroku, or AWS


## 📁 Project Structure

```
CCCS106-FinalProject/
├── main.py                    # Application entry point
├── setup_db.py                # Database initialization script
├── requirements.txt           # Python dependencies
├── voting_app.db              # Local SQLite database (auto-created)
├── pages/                     # Main application pages
│   ├── __init__.py
│   ├── login_page.py         # User login
│   ├── signup_page.py        # User registration
│   ├── home_page.py          # Main dashboard
│   ├── profile_page.py       # User profile
│   └── settings_page.py      # User settings
└── models/                    # Data models and database
    ├── __init__.py
    ├── database.py           # SQLite database manager
    └── session_manager.py    # User session management
```

## 📋 Development Roadmap

### Phase 1: Foundation (Current)
- [ ] Project setup and architecture
- [ ] Authentication pages (login/signup)
- [ ] User role management
- [ ] Basic UI components

### Phase 2: Core Features
- [ ] Candidate management
- [ ] Voting interface
- [ ] Vote submission and validation
- [ ] Real-time vote counting

### Phase 3: Results & Admin
- [ ] Results dashboard
- [ ] Election analytics
- [ ] Admin panel
- [ ] Audit trails

### Phase 4: Polish & Deployment
- [ ] Testing and optimization
- [ ] Security hardening
- [ ] Performance tuning
- [ ] Production deployment

## 📦 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Quick Start

```bash
# Clone repository
git clone https://github.com/EruzaDev/CCCS106-FinalProject.git
cd CCCS106-FinalProject

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with demo data
python setup_db.py

# Run the application
python main.py
```

### Demo User Credentials

The application comes with 5 pre-configured users. Each can be logged in separately to create unique sessions:

```
Email: alice@honestballot.local
Password: password123

Email: bob@honestballot.local
Password: password123

Email: charlie@honestballot.local
Password: password123

Email: diana@honestballot.local
Password: password123

Email: eve@honestballot.local
Password: password123
```

### Dependencies

```txt
flet>=0.21.0
```

## 🎨 Application Structure

### Local Database System

The application uses SQLite for local data storage with the following tables:

#### Users Table
- Stores user credentials and roles
- Password hashing with SHA-256
- Role-based access control

#### User Sessions Table
- Tracks active user sessions
- Each session has a unique token
- Session timeout after 8 hours of inactivity
- Supports multiple simultaneous sessions

#### Votes Table
- Records all cast votes
- Ensures one vote per user per position
- Timestamps for audit trails

#### Candidates Table
- Stores candidate information
- Positions and party affiliation

#### Election Sessions Table
- Manages voting sessions
- Start/end times and active status

### Session Management

Each user login creates a unique session:

```python
# Session structure
{
    "token": "unique-uuid-token",
    "user_id": 1,
    "username": "alice_smith",
    "email": "alice@honestballot.local",
    "role": "voter",
    "created_at": "2025-12-07T10:30:00",
    "last_activity": "2025-12-07T10:35:00"
}
```

### Core Components

#### `pages/login_page.py`
- User authentication with email/password
- Form validation
- Demo credentials reference

#### `pages/signup_page.py`
- New user registration
- Password confirmation
- Validation checks

#### `pages/home_page.py`
- Main dashboard
- Navigation to features
- User welcome screen

#### `pages/profile_page.py`
- User information display
- Account details

#### `pages/settings_page.py`
- User preferences
- Theme and notification settings

## 🚀 Running the Application

### Development Mode (Single Instance)
```bash
python main.py
```

The Flet application will open in your default web browser or as a desktop app.

### Running Multiple User Sessions

Since the app runs locally with SQLite, you can create multiple instances to simulate multiple users:

#### Method 1: Multiple Browser Tabs (Web Mode)
```bash
# First instance
python main.py

# In your terminal, Flet will display a URL like:
# http://localhost:8550

# Open the same URL in multiple browser tabs to simulate different sessions
# Each tab will be a separate session
```

#### Method 2: Multiple Desktop Instances (Desktop Mode)
```bash
# Terminal 1
python main.py

# Terminal 2
python main.py

# Terminal 3
python main.py

# Each instance runs independently with its own session
```

#### Method 3: Multiple Machines on Same Network
Since the database is local to each machine, each computer can run the app independently:

```bash
# Machine 1
python main.py

# Machine 2
python main.py

# Machine 3
python main.py
```

### Testing Multiple Concurrent Users

Example workflow with 5 users:

1. **Open Terminal 1:**
   ```bash
   python main.py
   # Login as: alice@honestballot.local / password123
   ```

2. **Open Terminal 2 (in new PowerShell window):**
   ```bash
   cd C:\Users\Cjay Lavapie\Downloads\CCCS106-FinalProject
   python main.py
   # Login as: bob@honestballot.local / password123
   ```

3. **Open Terminal 3:**
   ```bash
   cd C:\Users\Cjay Lavapie\Downloads\CCCS106-FinalProject
   python main.py
   # Login as: charlie@honestballot.local / password123
   ```

4. **Repeat for diana@honestballot.local and eve@honestballot.local**

Each session maintains its own state with a unique token, and all votes are recorded in the shared local database.

### Build for Distribution
```bash
# Web
flet build web

# Desktop (Windows)
flet build windows

# Desktop (macOS)
flet build macos

# Desktop (Linux)
flet build linux

# Mobile (Android)
flet build apk

# Mobile (iOS)
flet build ipa
```

## 💾 Database Management

### Initialize Database
```bash
python setup_db.py
```

This creates the SQLite database with:
- 5 demo users
- Sample candidates
- Election session

### Database Location
```
voting_app.db (in project root)
```

### Reset Database
```bash
# Delete the database file to reset
rm voting_app.db
# or
del voting_app.db  # Windows

# Then reinitialize
python setup_db.py
```

### Database Schema

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'voter',
    created_at TIMESTAMP,
    last_login TIMESTAMP
);

-- User Sessions table
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    session_token TEXT UNIQUE NOT NULL,
    login_time TIMESTAMP,
    last_activity TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Votes table
CREATE TABLE votes (
    id INTEGER PRIMARY KEY,
    voter_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL,
    position TEXT NOT NULL,
    election_session_id INTEGER,
    timestamp TIMESTAMP,
    UNIQUE(voter_id, position, election_session_id),
    FOREIGN KEY (voter_id) REFERENCES users(id)
);

-- Candidates table
CREATE TABLE candidates (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    party TEXT,
    bio TEXT,
    created_at TIMESTAMP
);

-- Election Sessions table
CREATE TABLE election_sessions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    is_active BOOLEAN DEFAULT 0,
    created_at TIMESTAMP
);
```

## 🤝 Contributing

### Development Workflow
1. Create feature branch: `git checkout -b feature/YourFeature`
2. Commit changes: `git commit -m 'Add YourFeature'`
3. Push to branch: `git push origin feature/YourFeature`
4. Open Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use type hints where applicable
- Write clear docstrings
- Keep components modular and reusable

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **EruzaDev** - Project Lead & Development

## 🙏 Acknowledgments

- Built with [Flet](https://flet.dev/) - A framework for building Flutter apps in Python
- Inspired by the need for transparent voting systems
- Open source community for tools and resources

## 📞 Support

For questions or issues:
- Create an issue on [GitHub Issues](https://github.com/EruzaDev/CCCS106-FinalProject/issues)
- Contact: support@honestballot.example.com

---

**Built with 🐍 Python for transparent voting**