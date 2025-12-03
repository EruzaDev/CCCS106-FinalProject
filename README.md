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

### Milestone 2: Authentication Pages (In Progress)
- [x] Login page with email/password fields
- [x] Signup page with social login options
- [x] Page routing between login/signup/home
- [x] Custom logo integration

### Milestone 3: Home Page Layout (In Progress)
- [x] Top taskbar with search and user info
- [x] Left sidebar with navigation
- [x] Main post container/feed
- [x] Right sidebar with suggestions
- [x] Notification dropdown

### Milestone 4: Core Features (In Progress)
- [ ] Post creation functionality
- [ ] Image/video upload support
- [ ] User profile page
- [ ] Settings page
- [ ] Security data page

### Milestone 5: Backend Integration (Planned)
- [ ] Database setup (Firebase/SQLite)
- [ ] User authentication backend
- [ ] Post storage and retrieval
- [ ] Real-time notifications

### Milestone 6: Polish & Distribution (Planned)
- [ ] Error handling and validation
- [ ] Loading states and animations
- [ ] Package for distribution
- [ ] Cross-platform testing

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
