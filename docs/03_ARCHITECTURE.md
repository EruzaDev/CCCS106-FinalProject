# Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           HONESTBALLOT SYSTEM                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         PRESENTATION LAYER                              │ │
│  │                           (Flet Framework)                              │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │ │
│  │  │  Login Page  │ │  Home Page   │ │ Profile Page │ │ Settings Page│  │ │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘  │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │ │
│  │  │COMELEC Dash  │ │  NBI Dash    │ │ Analytics Pg │ │  Audit Logs  │  │ │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                         │
│                                    ▼                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                          COMPONENT LAYER                                │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │ │
│  │  │   Sidebar    │ │  Top Taskbar │ │  Post Cards  │ │    Charts    │  │ │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                         │
│                                    ▼                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      APPLICATION SERVICE LAYER                          │ │
│  │  ┌─────────────────────────┐    ┌─────────────────────────────────┐   │ │
│  │  │     Session Manager     │    │         AI Service              │   │ │
│  │  │  • Create/Verify Session│    │  • Theme Extraction             │   │ │
│  │  │  • Token Management     │    │  • Sentiment Analysis           │   │ │
│  │  │  • Session Timeout      │    │  • Compatibility Scoring        │   │ │
│  │  └─────────────────────────┘    │  • Candidate Recommendations    │   │ │
│  │                                  └─────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                         │
│                                    ▼                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                          DATA ACCESS LAYER                              │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │                       Database Class                             │   │ │
│  │  │  • User Operations (CRUD, Authentication)                        │   │ │
│  │  │  • Voting Operations (Cast, Count, Results)                      │   │ │
│  │  │  • Audit Logging (Log, Query, Filter)                            │   │ │
│  │  │  • Legal Records (Create, Update, Verify)                        │   │ │
│  │  │  • Election Management (Start, Stop, Status)                     │   │ │
│  │  └─────────────────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                         │
│                                    ▼                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         PERSISTENCE LAYER                               │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │                    SQLite Database                               │   │ │
│  │  │                    (voting_app.db)                               │   │ │
│  │  └─────────────────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Folder Structure

```
CCCS106-FinalProject/
├── main.py                 # Application entry point
├── setup_db.py             # Database initialization
├── requirements.txt        # Python dependencies
├── voting_app.db           # SQLite database file
│
├── app/                    # Main application code
│   ├── __init__.py
│   ├── views/              # Page/View components
│   │   ├── login_page.py
│   │   ├── signup_page.py
│   │   ├── home_page.py
│   │   ├── profile_page.py
│   │   ├── settings_page.py
│   │   ├── comelec_dashboard.py
│   │   ├── nbi_dashboard.py
│   │   ├── audit_logs_page.py
│   │   └── analytics_page.py
│   │
│   ├── components/         # Reusable UI components
│   │   ├── sidebar.py
│   │   ├── top_taskbar.py
│   │   ├── post_card.py
│   │   ├── post_container.py
│   │   ├── charts.py
│   │   └── ...
│   │
│   ├── services/           # Business logic services
│   │   └── ai_service.py   # AI-powered analysis
│   │
│   ├── state/              # Application state management
│   │   └── session_manager.py
│   │
│   └── storage/            # Data persistence
│       └── database.py
│
├── tests/                  # Test suite
│   ├── test_ai_service.py
│   ├── test_database.py
│   ├── test_session_manager.py
│   ├── test_voting_integration.py
│   └── test_audit_integration.py
│
├── assets/                 # Static assets
│   └── images/
│
└── docs/                   # Documentation
    └── *.md
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     TECHNOLOGY STACK                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  FRONTEND/UI          BACKEND            EMERGING TECH       │
│  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐    │
│  │    Flet      │    │   Python     │   │ Rule-Based   │    │
│  │  (Flutter)   │    │   3.11+      │   │     AI       │    │
│  │              │    │              │   │              │    │
│  │ • Material   │    │ • SQLite     │   │ • NLP-like   │    │
│  │   Design     │    │ • bcrypt     │   │   Analysis   │    │
│  │ • Cross-     │    │ • hashlib    │   │ • Keyword    │    │
│  │   platform   │    │ • UUID       │   │   Matching   │    │
│  └──────────────┘    └──────────────┘   │ • Scoring    │    │
│                                          │   Algorithms │    │
│  DATA VIZ                                └──────────────┘    │
│  ┌──────────────┐    TESTING                                 │
│  │   Charts     │    ┌──────────────┐                        │
│  │  (Custom)    │    │   pytest     │                        │
│  │              │    │   unittest   │                        │
│  │ • Bar Charts │    │   mock       │                        │
│  │ • Donut      │    └──────────────┘                        │
│  │ • Stat Cards │                                            │
│  └──────────────┘                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────┐     ┌─────────────┐     ┌─────────────┐     ┌──────────┐
│  User   │────▶│  Flet UI    │────▶│   Service   │────▶│ Database │
│ Action  │     │   Layer     │     │   Layer     │     │  Layer   │
└─────────┘     └─────────────┘     └─────────────┘     └──────────┘
                      │                    │                   │
                      │                    ▼                   │
                      │            ┌─────────────┐            │
                      │            │ AI Service  │            │
                      │            │ (Analysis)  │            │
                      │            └─────────────┘            │
                      │                    │                   │
                      ▼                    ▼                   ▼
               ┌─────────────────────────────────────────────────┐
               │              Response to User                    │
               │  (Updated UI, Analytics, Recommendations)        │
               └─────────────────────────────────────────────────┘
```

---

*Document Version: 1.0*  
*Last Updated: December 2025*
