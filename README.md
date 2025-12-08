# HonestBallot - Secure Voting Application

A cross-platform voting application built with Python Flet framework, designed to provide transparent and secure voting mechanisms with comprehensive election management capabilities.

## 🎯 Project Overview

HonestBallot is a **local desktop voting platform** that demonstrates how technology can support electoral transparency. The system supports multiple user roles with specialized dashboards for different voting participants.

### User Roles

| Role | Capabilities |
|------|-------------|
| **Voters** | Cast votes, view election results |
| **Politicians** | Manage profiles and campaign information |
| **COMELEC Officials** | Manage voting process, view real-time results, verify achievements |
| **NBI Officers** | Manage legal records for candidates, verify/track legal cases |

## 🚀 Features

### Core Features
- ✅ User authentication and role-based access control
- ✅ Secure voting mechanism with integrity checks
- ✅ Real-time vote counting and results display
- ✅ Candidate profile management

### Security Features
- ✅ **bcrypt password hashing** (cost factor 12)
- ✅ **Rate limiting** - 5 login attempts, 15-minute lockout
- ✅ **Password policy** - 8+ chars, mixed case, digits, special chars
- ✅ **Audit logging** - All actions logged for accountability
- ✅ **Session management** - 30-minute timeout, secure tokens

### Voting System
- ✅ Position-based voting interface
- ✅ One vote per position enforcement
- ✅ Vote submission with confirmation
- ✅ Real-time vote tallying
- ✅ Results dashboard with analytics

### Administrative Features
- ✅ Election session management
- ✅ Voter registration and management
- ✅ Results verification
- ✅ Audit trails with date range filtering
- ✅ User activity monitoring

### NBI Legal Records Management
- ✅ Legal records tracking for candidates
- ✅ Record types: Graft, Corruption, Tax Issues, Criminal Cases
- ✅ Record status management (pending, verified, dismissed, rejected)
- ✅ Search and filter records by politician

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Framework** | Python Flet (Flutter-based) |
| **Language** | Python 3.11+ |
| **Database** | SQLite (Local) |
| **Password Hashing** | bcrypt |
| **Testing** | pytest |

### Key Characteristics
- **Local-Only:** Runs completely offline with SQLite database
- **Multi-User Sessions:** Unique session tokens per user
- **Pre-Configured Users:** Demo users ready to use
- **Cross-Platform:** Works on Windows, macOS, Linux

## 📁 Project Structure

```
CCCS106-FinalProject/
├── main.py                    # Application entry point
├── setup_db.py                # Database initialization
├── requirements.txt           # Python dependencies
├── .env.example               # Configuration template
├── app/
│   ├── config.py              # Centralized configuration
│   ├── password_policy.py     # Password validation
│   ├── security_logger.py     # Security event logging
│   ├── storage/database.py    # SQLite database manager
│   ├── models/                # Data models
│   ├── views/                 # UI pages
│   ├── components/            # Reusable UI components
│   └── services/              # Business logic
├── tests/                     # Unit tests (90+ tests)
└── docs/                      # Documentation
```

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
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with demo data
python setup_db.py

# Run the application
python main.py
```

### Demo User Credentials

| Role | Username | Password |
|------|-------|----------|
| COMELEC | comelec1 | com123 |
| NBI | nbi1 | nbi123 |
| Voter | voter1 | voter123 |
| Politician | *(any politician name)* | pol123 |

### Dependencies

```txt
flet>=0.28.3
bcrypt>=4.0.0
pytest>=8.0.0
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_database.py
```

**Test Coverage:** 90+ tests covering authentication, voting, security features, and more.

## 💾 Database Management

### Initialize Database
```bash
python setup_db.py
```

### Reset Database
```bash
# Delete the database file
del voting_app.db    # Windows
rm voting_app.db     # macOS/Linux

# Reinitialize
python setup_db.py
```

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

| Document | Description |
|----------|-------------|
| `01_PROJECT_OVERVIEW.md` | Project goals and scope |
| `02_FEATURE_LIST.md` | Complete feature breakdown |
| `03_ARCHITECTURE.md` | System design and patterns |
| `04_DATA_MODEL.md` | Database schema |
| `05_EMERGING_TECH.md` | Technologies used |
| `06_SETUP_INSTRUCTIONS.md` | Installation guide |
| `07_TESTING_SUMMARY.md` | Test coverage report |
| `SECURITY_ENGINEERING.md` | Security analysis (STRIDE, OWASP) |

## 🤝 Contributing

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

- **C-jay B. Lavapie** - Product Lead / Vision & Feature Prioritization, Lead Developer (Flet Architecture), & Data & Integration Engineer (storage + emerging tech)
- **John Paul Caldo** - UI/UX & Accessibility Designer, QA / Test Coordinator
- **Marc Dexter Sael** - Documentation & Release Manager

---

**Built with 🐍 Python and Flet for transparent voting**
