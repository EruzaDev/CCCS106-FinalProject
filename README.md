# 🗳️ Honest Ballot - Research, Decide, Act

An open-source desktop social media platform designed to help voters make informed decisions during elections — featuring candidate information sharing, community discussions, and voter education tools.

📋 **Project Foundation:** This application is a final project for CCCS106, built using the Flet framework for Python by **Team PowerPuffBoyz**. The platform aims to promote transparent governance and informed voting through social engagement.

## ✨ Features (In Progress)

- **User Authentication:** Login and signup pages with email/password and social login options (Google, Apple)
- **Social Feed:** View and create posts about candidates and election information
- **Post Creation:** Write posts, upload photos, and share videos about candidates
- **User Profiles:** Personalized profiles with avatar and user information
- **Notifications:** Real-time notification system with unread/earlier sections
- **People Suggestions:** Discover and follow other voters in your community
- **Responsive UI:** Modern, clean interface with sidebar navigation

## 🛠️ Tech Stack

### Core
- Python 3.x
- Flet (Cross-platform GUI framework)

### Frontend (GUI)
- Flet 0.28+ (Python UI framework)
- Custom modular components

### Key Dependencies
- `flet` - Cross-platform GUI framework

### Project Structure
```
CCCS106-FinalProject/
├── main.py                    # Main entry point with routing
├── requirements.txt           # Dependencies
├── assets/                    # Images and static files
├── components/                # Reusable UI components
│   ├── top_taskbar.py         # Top bar with search, user info, notifications
│   ├── sidebar.py             # Left sidebar with profile & navigation
│   ├── post_container.py      # Main feed container
│   ├── post_creator.py        # Post creation widget
│   ├── post_card.py           # Individual post card
│   ├── right_sidebar.py       # Right panel with suggestions
│   └── notification_dropdown.py # Notification popup
└── pages/                     # Full page layouts
    ├── login_page.py          # Login screen
    ├── signup_page.py         # Join/Signup screen
    └── home_page.py           # Main home page
```

## 🔄 Development Approach

The project follows a **Modular Component-Based** architecture:
- Each UI component is in a separate file for maintainability
- Components use classes with callbacks for event handling
- Pages combine components to create full layouts
- Separation of concerns ensures easy updates and testing

## 🗂️ Roadmap

### Milestone 1: Project Setup & Foundation ✅
- [x] Initialize repository structure
- [x] Set up virtual environment
- [x] Install core dependencies (flet)
- [x] Create README documentation
- [x] Set up GitHub repository
- [x] Create initial project structure

### Milestone 2: Authentication Pages ✅
- [x] Login page with email/password fields
- [x] Signup page with social login options
- [x] Page routing between login/signup/home
- [x] Custom logo integration

### Milestone 3: Home Page Layout ✅
- [x] Top taskbar with search and user info
- [x] Left sidebar with navigation
- [x] Main post container/feed
- [x] Right sidebar with suggestions
- [x] Notification dropdown

### Milestone 4: Core UI Features ✅
- [x] Post creation functionality with expandable input
- [x] Image upload support with preview and removal
- [x] User profile page with editable about section
- [x] Settings page with dark/light mode toggle
- [x] Responsive design foundation (collapsible sidebar)

### Milestone 5: Backend Foundation & Configuration
- [ ] Create Flask app with factory pattern
- [ ] Set up environment configuration (.env)
- [ ] Initialize SQLAlchemy with SQLite
- [ ] Configure Firebase Admin SDK
- [ ] Set up Flask-Mail for email services
- [ ] Update dependencies in requirements.txt

### Milestone 6: Data Models (SQLite + Firebase)
- [ ] User model (auth, roles, settings)
- [ ] Post model (Firestore schema)
- [ ] Report model for content moderation
- [ ] Audit log model for security tracking
- [ ] Two-factor authentication model

### Milestone 7: Authentication System with Security
- [ ] User registration with password hashing (bcrypt)
- [ ] Login with attempt throttling (5 attempts → 15min lockout)
- [ ] Session management (30min timeout)
- [ ] CSRF protection on all forms
- [ ] Password policy enforcement
- [ ] Audit logging for auth events

### Milestone 8: Two-Factor Authentication (Email)
- [ ] Email verification code generation
- [ ] Flask-Mail integration for sending codes
- [ ] 2FA verification flow in login
- [ ] Enable/disable 2FA in user settings
- [ ] Secure code storage with expiration

### Milestone 9: Role-Based Access Control & Admin Routes
- [ ] Admin and User role definitions
- [ ] @admin_required decorator
- [ ] User management endpoints (CRUD)
- [ ] Report management endpoints
- [ ] Audit log viewing endpoints
- [ ] Dashboard statistics endpoint

### Milestone 10: Profile Management
- [ ] Profile view and edit endpoints
- [ ] Password change with verification
- [ ] Avatar upload with image compression (Pillow)
- [ ] Settings persistence (theme, 2FA)
- [ ] Following/followers system

### Milestone 11: Post System with Image Upload
- [ ] Create/read/delete post endpoints
- [ ] Image upload with compression (max 1080px, WebP)
- [ ] Firebase Storage integration
- [ ] Like and share functionality
- [ ] Report post functionality
- [ ] Feed algorithm (following + trending)

### Milestone 12: AI Fact-Checker (Hybrid NLP + RSS)
- [ ] RSS feed integration (Rappler, Inquirer, PhilStar, GMA)
- [ ] Keyword extraction from posts
- [ ] Content similarity matching
- [ ] Truthfulness scoring (True/Somewhat True/False)
- [ ] Source attribution and display
- [ ] Background processing queue

### Milestone 13: Flet API Client & Integration
- [ ] HTTP client service (httpx)
- [ ] Auth state management
- [ ] Update login/signup pages to use API
- [ ] Flask daemon thread launcher
- [ ] Session persistence and refresh

### Milestone 14: Admin Panel UI (Flet)
- [ ] Admin dashboard with statistics
- [ ] User management page (table, search, actions)
- [ ] Reported posts review page
- [ ] Audit log viewer with filters
- [ ] Conditional admin navigation

### Milestone 15: Responsive Design
- [ ] Breakpoint system (mobile/tablet/desktop)
- [ ] Collapsible sidebar for mobile
- [ ] Adaptive layouts with ResponsiveRow
- [ ] Touch-friendly controls
- [ ] Portrait mode optimization

### Milestone 16: Settings & Theme System
- [ ] Dark/Light mode toggle
- [ ] Theme persistence to Firebase
- [ ] Language settings (English/Filipino)
- [ ] Notification preferences
- [ ] Real-time theme application

### Milestone 17: Testing & Polish
- [ ] Unit tests for auth, admin, posts
- [ ] Loading states and spinners
- [ ] Error handling and user messages
- [ ] Form validation
- [ ] Confirmation dialogs

### Milestone 18: Deployment Preparation
- [ ] Production configuration
- [ ] Firebase security rules
- [ ] Deployment documentation
- [ ] Cross-platform build testing
- [ ] Admin bootstrap script

## 📦 Installation & Setup

### Clone the repository
```bash
git clone https://github.com/EruzaDev/CCCS106-FinalProject.git
cd CCCS106-FinalProject
```

### Set up virtual environment
```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows cmd)
.\venv\Scripts\activate.bat

# Activate (Linux/macOS)
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Run the App

### Run as a desktop app:
```bash
python main.py
```

Or using Flet CLI:
```bash
flet run
```

### Run as a web app:
```bash
flet run --web
```

## 📦 Build the App

### Windows
```bash
flet build windows -v
```

### Linux
```bash
flet build linux -v
```

### macOS
```bash
flet build macos -v
```

## 📚 Documentation

- [Flet Documentation](https://flet.dev/docs/) - GUI framework reference

## 📜 License

MIT

## 👥 Contributors

- **Caldo, John Paul** - Developer
- **Lavapie, Cjay** - Developer
- **Sael, Dexter** - Developer
