# Setup & Run Instructions

## Prerequisites

Before running HonestBallot, ensure you have the following installed:

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.11 or higher | Runtime environment |
| pip | Latest | Package management |
| Git | Any | Version control (optional) |

### Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Windows 10/11 | ✅ Fully Supported | Primary development platform |
| macOS | ✅ Supported | Tested on macOS 12+ |
| Linux | ✅ Supported | Tested on Ubuntu 22.04 |

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/EruzaDev/CCCS106-FinalProject.git
cd CCCS106-FinalProject
```

Or download the ZIP file and extract it.

### Step 2: Create Virtual Environment (Recommended)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `flet` - UI framework
- `bcrypt` - Password hashing
- `pytest` - Testing framework

### Step 4: Initialize Database (Optional)

The database is automatically created on first run. To reset or reinitialize:

```bash
python setup_db.py
```

This creates `voting_app.db` with sample data.

### Step 5: Run the Application

```bash
python main.py
```

The application will open in a native desktop window.

## Quick Start Commands

### One-liner Setup (Windows PowerShell)

```powershell
git clone https://github.com/EruzaDev/CCCS106-FinalProject.git; cd CCCS106-FinalProject; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt; python main.py
```

### One-liner Setup (macOS/Linux)

```bash
git clone https://github.com/EruzaDev/CCCS106-FinalProject.git && cd CCCS106-FinalProject && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py
```

## Configuration

### Environment Variables (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `FLET_SECRET_KEY` | (auto-generated) | Session encryption key |
| `DB_PATH` | `voting_app.db` | Database file location |

### Database Location

By default, the SQLite database is created in the project root:
```
CCCS106-FinalProject/
└── voting_app.db
```

## Test Accounts

After running `setup_db.py`, these accounts are available:

| Role | Email | Password |
|------|-------|----------|
| COMELEC Admin | admin@comelec.gov | admin123 |
| NBI Officer | nbi@gov.ph | nbi123 |
| Voter | voter@test.com | voter123 |
| Politician | politician@test.com | pol123 |

## Running Tests

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test File
```bash
python -m pytest tests/test_ai_service.py -v
```

### Run with Coverage (if installed)
```bash
pip install pytest-cov
python -m pytest tests/ --cov=app --cov-report=html
```

## Troubleshooting

### Common Issues

#### 1. "Module not found" Error
```
ModuleNotFoundError: No module named 'flet'
```
**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt
```

#### 2. "Permission denied" on Database
```
sqlite3.OperationalError: unable to open database file
```
**Solution**: Check write permissions in the project folder.

#### 3. Flet Window Not Opening
**Solution**: Try running as desktop mode explicitly:
```bash
flet run main.py --desktop
```

#### 4. Port Already in Use
**Solution**: Kill existing Python processes or change port:
```bash
flet run main.py --port 8551
```

### Platform-Specific Notes

#### Windows
- Use PowerShell for best compatibility
- Run as Administrator if permission issues occur

#### macOS
- May need to allow app in Security & Privacy settings
- Use `python3` instead of `python`

#### Linux
- Install additional dependencies for GTK:
  ```bash
  sudo apt-get install libgtk-3-dev
  ```

## Development Mode

### Hot Reload
For development with auto-reload:
```bash
flet run main.py -d
```

### Debug Mode
Enable verbose logging:
```bash
python main.py --debug
```

## Building Executables (Optional)

### Windows EXE
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### macOS App
```bash
flet pack main.py --icon assets/icon.icns
```

## Folder Structure After Setup

```
CCCS106-FinalProject/
├── venv/                    # Virtual environment (created)
├── voting_app.db            # SQLite database (created on first run)
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── app/                     # Application code
├── tests/                   # Test suite
├── assets/                  # Static files
└── docs/                    # Documentation
```

---

*Document Version: 1.0*  
*Last Updated: December 2025*
