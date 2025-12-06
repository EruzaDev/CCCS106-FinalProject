# HonestBallot - Social Media Platform with Fact-Checking

A cross-platform social media application built with Python Flet framework, featuring AI-powered fact-checking for Filipino news, user posts with engagement features, and comprehensive admin moderation capabilities.

## 🎯 Project Overview

HonestBallot is a social network platform focused on promoting truth and transparency in social media. The system includes fact-checking capabilities that verify posts against Filipino news sources, helping combat misinformation while fostering meaningful social connections.

### Key Features

- **User Posts** - Create posts with text and images
- **Social Network** - Follow users, view their posts
- **Fact-Checking** - AI-powered verification against Filipino news websites (Rappler, Inquirer, PhilStar, GMA News)
- **Admin Panel** - Comprehensive moderation dashboard for reported content
- **Cross-Platform** - Responsive design for mobile portrait and landscape desktop views

## 🚀 Current Implementation Status

### ✅ Completed (Milestone 4 - Core UI Features)
- Post creation with expandable input
- Image upload with preview
- Post cards with like/report interactions
- Profile page with editable sections
- Dark/light mode theming
- Responsive collapsible sidebar
- Settings page with account management
- Notification system
- User search functionality

### 🔄 In Progress
- Data models preparation (User, Post, PostReport)
- Database integration planning

### 📋 Planned Features
- Firebase Authentication (Email/Password, Google, Apple)
- Firestore database integration
- Firebase Storage for images
- AI fact-checking system
- Admin panel with RBAC
- 2FA via email
- Following/followers system

## 🛠️ Technology Stack

### Current Implementation
- **Framework:** Python Flet (Flutter-based UI)
- **Language:** Python 3.11+
- **Architecture:** Component-based with MVC pattern

### Planned Production Stack
- **Backend:** Firebase (Firestore, Auth, Storage)
- **Admin Backend:** Flask + SQLite (RBAC, 2FA)
- **Fact-Checking:** Hybrid NLP + RSS feeds
- **News Sources:** Rappler, Inquirer, PhilStar, GMA News
- **Image Processing:** Pillow for compression

## 📁 Project Structure

```
CCCS106-FinalProject/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── assets/                      # Images and static files
├── components/                  # Reusable UI components
│   ├── __init__.py
│   ├── sidebar.py              # Navigation sidebar
│   ├── top_taskbar.py          # Header with search/notifications
│   ├── post_creator.py         # Post input interface
│   ├── post_card.py            # Individual post display
│   ├── post_container.py       # Posts feed container
│   ├── right_sidebar.py        # Suggestions sidebar
│   └── notification_dropdown.py # Notifications panel
├── pages/                       # Main application pages
│   ├── __init__.py
│   ├── login_page.py           # User login
│   ├── signup_page.py          # User registration
│   ├── home_page.py            # Main feed
│   ├── profile_page.py         # User profile
│   └── settings_page.py        # User settings
└── models/                      # Data models (NEW)
    ├── __init__.py
    ├── user.py                 # User & UserProfile models
    └── post.py                 # Post & PostReport models
```

## 📋 SDLC Model: Iterative Development Approach

This project follows an **Iterative and Incremental Development Model**, allowing for continuous refinement and feature expansion through defined milestones.

---

## Milestone 1: Project Planning & Setup

### Objectives
- Define system requirements for a social media platform with fact-checking
- Establish project structure and development environment
- Create initial wireframes and designs

### Deliverables
- ✅ Project charter and requirements document
- ✅ Technology stack selection (Python Flet)
- ✅ Git repository setup
- ✅ Development roadmap (18 milestones)

---

## Milestone 2: Authentication & User Management

### Objectives
- Implement user authentication system
- Create login and signup pages
- Set up user session management

### Planned Features
- Email/Password authentication via Firebase
- Google Sign-In integration
- Apple Sign-In integration
- Session persistence
- Logout functionality

### Status
🔄 **Partially Complete** - UI pages built, Firebase integration pending

---

## Milestone 3: Database Design & Integration

### Objectives
- Design database schema for users, posts, and interactions
- Integrate Firebase Firestore
- Set up Firebase Storage for images

### Data Models Created
✅ **User Model** (`models/user.py`)
- UserProfile: username, email, handle, bio, stats
- User: authentication data, admin flags, account status

✅ **Post Model** (`models/post.py`)
- Post: content, images, likes, fact-check status
- PostReport: moderation reports with reasons
- FactCheckStatus: True, Somewhat True, False, Pending, Not Applicable

### Status
🔄 **In Progress** - Models defined, Firebase integration pending

---

## Milestone 4: Core UI Features ✅ COMPLETED

### Implemented Features
✅ **Post Creation**
- Expandable input interface
- Text editor with character limit
- Image upload with file picker
- Image preview with remove option
- Submit and cancel buttons

✅ **Post Display**
- Post cards with user info
- Like button with count
- Report menu for moderation
- Image display support
- Timestamp formatting

✅ **Profile Page**
- Editable "About Me" section
- Editable location & contact info
- Profile stats (Following, Followers, Likes)
- User posts feed

✅ **Settings Page**
- Dark/Light mode toggle with live switching
- Delete account option with confirmation
- Simplified UI (removed unnecessary features)

✅ **Responsive Design**
- Collapsible sidebar for mobile/tablet
- Icon-only sidebar mode
- Responsive breakpoints (768px mobile, 1024px tablet)

✅ **Theme System**
- Light and dark mode support
- Theme-aware component backgrounds
- Persistent theme preference

---

## Milestone 5: Social Features (Next)

### Planned Features
- Following/Followers system
- User search and discovery
- Friend suggestions
- User profiles with posts
- Activity feed

---

## Milestone 6: Fact-Checking System

### Planned Architecture
**Hybrid NLP + RSS Approach**

1. **Content Analysis**
   - Extract claims from posts
   - Identify news-worthy content
   - Filter personal opinions

2. **News Source Integration**
   - Rappler RSS feeds
   - Philippine Daily Inquirer
   - PhilStar
   - GMA News
   - Real-time article scraping

3. **Verification Levels**
   - ✅ **True** - Verified accurate
   - ⚠️ **Somewhat True** - Partially accurate
   - ❌ **False** - Contains misinformation
   - ⏳ **Pending** - Under review
   - ➖ **Not Applicable** - Personal content

4. **Display Integration**
   - Fact-check badges on posts
   - Source links for verification
   - Summary of findings

---

## Milestone 7-10: Admin Panel & Moderation

### Features
- Report management dashboard
- User moderation tools
- Content flagging system
- Analytics and insights
- RBAC (Role-Based Access Control)
- 2FA for admin users

---

## Milestone 11-15: Advanced Features

### Planned Enhancements
- Real-time notifications
- Image compression and optimization
- Search functionality
- Post sharing
- Comment system
- Direct messaging

---

## Milestone 16-18: Testing & Deployment

### Testing Strategy
- Unit tests for components
- Integration tests for Firebase
- User acceptance testing
- Performance optimization
- Security audit

### Deployment
- Web deployment via Flet
- Desktop builds (Windows, macOS, Linux)
- Mobile builds (Android, iOS)

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Quick Start

```bash
# Clone repository
git clone https://github.com/EruzaDev/CCCS106-FinalProject.git
cd CCCS106-FinalProject

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Development Setup

```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python main.py
```

### Dependencies

```txt
flet>=0.21.0
Pillow>=10.0.0
```

### Test Credentials (Firebase integration pending)
- **Email:** test@example.com
- **Password:** password123

---

## 🎨 Application Structure

### Components Overview

#### `components/sidebar.py`
- Navigation sidebar with Profile, Find Friends, Settings, Log Out
- Collapsible design for mobile/tablet views
- Icon-only mode for compact display

#### `components/top_taskbar.py`
- Search bar for finding users
- User info display
- Settings button
- Notifications dropdown
- Clickable logo to return home

#### `components/post_creator.py`
- Expandable post input
- Text field with placeholder
- Image upload functionality
- Submit and cancel buttons

#### `components/post_card.py`
- User avatar and info
- Post content display
- Image preview
- Like button with count
- Report menu for moderation

#### `components/notification_dropdown.py`
- List of post notifications
- "See previous" button
- Clean, minimal design

### Pages Overview

#### `pages/login_page.py`
- Email/password input
- Social sign-in buttons (Google, Apple)
- "Create Account" link

#### `pages/signup_page.py`
- Account registration form
- Social sign-up options
- Terms acceptance

#### `pages/home_page.py`
- Main feed with posts
- Post creator at top
- Left sidebar navigation
- Right sidebar with suggestions

#### `pages/profile_page.py`
- User profile header with cover photo
- Editable "About Me" section
- Editable location & info
- User's posts feed

#### `pages/settings_page.py`
- Dark/Light mode toggle
- Delete account option
- Simplified settings UI

### Data Models

#### `models/user.py`
```python
@dataclass
class UserProfile:
    username: str
    email: str
    handle: str
    about_me: str
    profile_picture_url: Optional[str]
    location: str
    following_count: int
    followers_count: int
    likes_count: int
    theme: str  # "light" or "dark"
```

#### `models/post.py`
```python
@dataclass
class Post:
    post_id: str
    author_uid: str
    content: str
    image_url: Optional[str]
    likes_count: int
    fact_check_status: FactCheckStatus
    created_at: datetime

class FactCheckStatus(Enum):
    TRUE = "true"
    SOMEWHAT_TRUE = "somewhat_true"
    FALSE = "false"
    PENDING = "pending"
    NOT_APPLICABLE = "not_applicable"
```

---

## 🚀 Deployment Options

### Web Deployment
```bash
# Build for web
flet build web

# The output will be in build/web directory
# Deploy to any static hosting service
```

### Desktop Applications
```bash
# Windows
flet build windows

# macOS
flet build macos

# Linux
flet build linux
```

### Mobile Applications
```bash
# Android APK
flet build apk

# iOS (requires macOS with Xcode)
flet build ipa
```

### Hosting Recommendations
- **Web:** GitHub Pages, Netlify, Vercel
- **Desktop:** Direct distribution or Microsoft Store / Mac App Store
- **Mobile:** Google Play Store, Apple App Store

---

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use type hints where applicable
- Write descriptive docstrings
- Keep components modular and reusable
- Test on both light and dark modes

### Branch Strategy
- `main` - Production-ready code
- `milestone-X-...` - Feature branches for each milestone
- Use descriptive branch names

---

## 🐛 Known Issues

1. Dark mode needs further refinement for some components
2. Firebase integration not yet implemented
3. Image compression needs optimization
4. Fact-checking system pending implementation

---

## 📝 Changelog

### Milestone 4 (Current)
- ✅ Implemented core UI components
- ✅ Added dark/light mode theming
- ✅ Created responsive sidebar
- ✅ Built post creation and display
- ✅ Added settings and profile pages
- ✅ Implemented notification system

### Milestone 3
- ✅ Designed data models
- ✅ Created User and Post structures
- ✅ Defined fact-checking enums

### Milestone 2
- ✅ Built authentication UI pages
- ✅ Created login and signup forms

### Milestone 1
- ✅ Project setup and planning
- ✅ Technology selection
- ✅ Repository initialization

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Authors

- **EruzaDev** - Project Lead & Development

---

## 🙏 Acknowledgments

- Built with [Flet](https://flet.dev/) - A framework for building Flutter apps in Python
- Inspired by the need for truth in social media
- Filipino news sources for fact-checking integration
- Open source community for tools and resources

---

## 📞 Support

For questions or support:
- Create an issue on [GitHub Issues](https://github.com/EruzaDev/CCCS106-FinalProject/issues)
- Email: support@eutable.example.com

---

## 🗺️ Roadmap

### Version 1.0 (In Development)
- [x] Core UI implementation
- [x] Theme system
- [x] Data models
- [ ] Firebase integration
- [ ] User authentication
- [ ] Post creation/deletion
- [ ] Like/unlike functionality

### Version 2.0 (Planned)
- [ ] Fact-checking system integration
- [ ] Following/followers system
- [ ] Real-time notifications
- [ ] Comment system on posts
- [ ] Direct messaging
- [ ] User search and discovery

### Version 3.0 (Future)
- [ ] Admin panel with RBAC
- [ ] Content moderation dashboard
- [ ] Analytics and insights
- [ ] Multi-language support (English, Filipino)
- [ ] Advanced fact-checking with AI
- [ ] API for third-party integrations

---

**Built with 🐍 Python and ❤️ for truth in social media**
