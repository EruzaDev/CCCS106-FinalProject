import sqlite3
import os
import hashlib
import json
from datetime import datetime
from pathlib import Path


class Database:
    """Local SQLite database manager for the voting application"""
    
    def __init__(self, db_name="voting_app.db"):
        """Initialize database connection"""
        self.db_path = Path(db_name)
        self.connection = None
        self.cursor = None
        self.initialize_db()
    
    def initialize_db(self):
        """Initialize database and create tables if they don't exist"""
        self.connection = sqlite3.connect(str(self.db_path))
        self.cursor = self.connection.cursor()
        
        # Create users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'voter',
                status TEXT DEFAULT 'active',
                position TEXT,
                party TEXT,
                biography TEXT,
                profile_image TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create votes table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voter_id INTEGER NOT NULL,
                candidate_id INTEGER NOT NULL,
                position TEXT NOT NULL,
                election_session_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (voter_id) REFERENCES users(id),
                UNIQUE(voter_id, position, election_session_id)
            )
        ''')
        
        # Create candidates table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                party TEXT,
                bio TEXT,
                image_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create election sessions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS election_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                is_active BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user sessions table for tracking unique sessions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.connection.commit()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password, role="voter"):
        """Create a new user"""
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute('''
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, role))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def verify_user(self, email, password):
        """Verify user credentials"""
        password_hash = self.hash_password(password)
        self.cursor.execute('''
            SELECT id, username, email, role FROM users
            WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))
        
        user = self.cursor.fetchone()
        if user:
            # Update last login
            self.cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user[0],))
            self.connection.commit()
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[3]
            }
        return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        self.cursor.execute('''
            SELECT id, username, email, role FROM users WHERE email = ?
        ''', (email,))
        user = self.cursor.fetchone()
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[3]
            }
        return None
    
    def create_user_session(self, user_id, session_token):
        """Create a new user session"""
        try:
            self.cursor.execute('''
                INSERT INTO user_sessions (user_id, session_token)
                VALUES (?, ?)
            ''', (user_id, session_token))
            self.connection.commit()
            return session_token
        except sqlite3.IntegrityError:
            return None
    
    def verify_session(self, session_token):
        """Verify if session is active"""
        self.cursor.execute('''
            SELECT user_id FROM user_sessions
            WHERE session_token = ? AND is_active = 1
        ''', (session_token,))
        result = self.cursor.fetchone()
        if result:
            # Update last activity
            self.cursor.execute('''
                UPDATE user_sessions SET last_activity = CURRENT_TIMESTAMP
                WHERE session_token = ?
            ''', (session_token,))
            self.connection.commit()
            return result[0]
        return None
    
    def end_session(self, session_token):
        """End a user session"""
        self.cursor.execute('''
            UPDATE user_sessions SET is_active = 0
            WHERE session_token = ?
        ''', (session_token,))
        self.connection.commit()
    
    def cast_vote(self, voter_id, candidate_id, position, election_session_id=None):
        """Record a vote"""
        try:
            self.cursor.execute('''
                INSERT INTO votes (voter_id, candidate_id, position, election_session_id)
                VALUES (?, ?, ?, ?)
            ''', (voter_id, candidate_id, position, election_session_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            # User already voted for this position
            return False
    
    def get_votes_by_position(self, position, election_session_id=None):
        """Get vote counts by position"""
        if election_session_id:
            self.cursor.execute('''
                SELECT candidate_id, COUNT(*) as count
                FROM votes
                WHERE position = ? AND election_session_id = ?
                GROUP BY candidate_id
                ORDER BY count DESC
            ''', (position, election_session_id))
        else:
            self.cursor.execute('''
                SELECT candidate_id, COUNT(*) as count
                FROM votes
                WHERE position = ?
                GROUP BY candidate_id
                ORDER BY count DESC
            ''', (position,))
        return self.cursor.fetchall()
    
    def get_candidates_by_position(self, position):
        """Get all candidates for a position"""
        self.cursor.execute('''
            SELECT id, name, position, party, bio FROM candidates
            WHERE position = ?
        ''', (position,))
        return self.cursor.fetchall()
    
    def add_candidate(self, name, position, party, bio=""):
        """Add a new candidate"""
        self.cursor.execute('''
            INSERT INTO candidates (name, position, party, bio)
            VALUES (?, ?, ?, ?)
        ''', (name, position, party, bio))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def create_election_session(self, name):
        """Create an election session"""
        self.cursor.execute('''
            INSERT INTO election_sessions (name, is_active)
            VALUES (?, 1)
        ''', (name,))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_all_users(self):
        """Get all users (for admin purposes)"""
        self.cursor.execute('''
            SELECT id, username, email, role, created_at, full_name, status, position, party, biography, profile_image FROM users
        ''')
        return self.cursor.fetchall()
    
    def get_users_by_role(self, role):
        """Get all users by role"""
        self.cursor.execute('''
            SELECT id, username, email, role, created_at, full_name, status, position, party, biography, profile_image 
            FROM users WHERE role = ?
        ''', (role,))
        return self.cursor.fetchall()
    
    def create_voter(self, username, email, password, full_name):
        """Create a new voter account"""
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, role, status)
                VALUES (?, ?, ?, ?, 'voter', 'active')
            ''', (username, email, password_hash, full_name))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def create_politician(self, username, email, password, full_name, position, party, biography, profile_image=None):
        """Create a new politician account"""
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, role, status, position, party, biography, profile_image)
                VALUES (?, ?, ?, ?, 'politician', 'active', ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, position, party, biography, profile_image))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_user_status(self, user_id, status):
        """Update user status (active/inactive)"""
        self.cursor.execute('''
            UPDATE users SET status = ? WHERE id = ?
        ''', (status, user_id))
        self.connection.commit()
    
    def update_voter(self, user_id, full_name, email, username):
        """Update voter account without changing password"""
        try:
            self.cursor.execute('''
                UPDATE users SET full_name = ?, email = ?, username = ? WHERE id = ?
            ''', (full_name, email, username, user_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_voter_with_password(self, user_id, full_name, email, username, password):
        """Update voter account with new password"""
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute('''
                UPDATE users SET full_name = ?, email = ?, username = ?, password_hash = ? WHERE id = ?
            ''', (full_name, email, username, password_hash, user_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_politician(self, user_id, full_name, email, username, position, party, biography, profile_image=None):
        """Update politician account without changing password"""
        try:
            if profile_image:
                self.cursor.execute('''
                    UPDATE users SET full_name = ?, email = ?, username = ?, position = ?, party = ?, biography = ?, profile_image = ? WHERE id = ?
                ''', (full_name, email, username, position, party, biography, profile_image, user_id))
            else:
                self.cursor.execute('''
                    UPDATE users SET full_name = ?, email = ?, username = ?, position = ?, party = ?, biography = ? WHERE id = ?
                ''', (full_name, email, username, position, party, biography, user_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_politician_with_password(self, user_id, full_name, email, username, position, party, biography, password, profile_image=None):
        """Update politician account with new password"""
        try:
            password_hash = self.hash_password(password)
            if profile_image:
                self.cursor.execute('''
                    UPDATE users SET full_name = ?, email = ?, username = ?, position = ?, party = ?, biography = ?, password_hash = ?, profile_image = ? WHERE id = ?
                ''', (full_name, email, username, position, party, biography, password_hash, profile_image, user_id))
            else:
                self.cursor.execute('''
                    UPDATE users SET full_name = ?, email = ?, username = ?, position = ?, party = ?, biography = ?, password_hash = ? WHERE id = ?
                ''', (full_name, email, username, position, party, biography, password_hash, user_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def delete_user(self, user_id):
        """Delete a user"""
        self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.connection.commit()
        return self.cursor.fetchall()
    
    def verify_user_by_username(self, username, password):
        """Verify user credentials by username"""
        password_hash = self.hash_password(password)
        self.cursor.execute('''
            SELECT id, username, email, role FROM users
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = self.cursor.fetchone()
        if user:
            # Update last login
            self.cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user[0],))
            self.connection.commit()
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[3]
            }
        return None
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()


def init_demo_data():
    """Initialize database with demo users and candidates"""
    db = Database()
    
    # Check if users already exist
    existing_users = db.get_all_users()
    if len(existing_users) > 0:
        return db  # Database already initialized, return open connection
    
    # Create role-based demo users
    demo_users = [
        # Voter accounts
        ("voter1", "voter1@honestballot.local", "voter123", "voter"),
        ("voter2", "voter2@honestballot.local", "voter123", "voter"),
        ("voter3", "voter3@honestballot.local", "voter123", "voter"),
        # Politician account
        ("politician1", "politician1@honestballot.local", "pol123", "politician"),
        # NBI Officer account
        ("nbi1", "nbi1@honestballot.local", "nbi123", "nbi"),
        # COMELEC account
        ("comelec1", "comelec1@honestballot.local", "com123", "comelec"),
    ]
    
    for username, email, password, role in demo_users:
        db.create_user(username, email, password, role)
    
    # Create sample candidates
    candidates = [
        ("Juan Dela Cruz", "President", "Party A", "Experienced leader with 20 years in politics"),
        ("Maria Santos", "President", "Party B", "Business executive focused on economy"),
        ("Pedro Lopez", "Vice President", "Party A", "Former military general"),
        ("Rosa Garcia", "Vice President", "Party B", "Healthcare advocate"),
        ("Miguel Torres", "Senator", "Party A", "Education specialist"),
        ("Ana Reyes", "Senator", "Party B", "Environmental activist"),
    ]
    
    for name, position, party, bio in candidates:
        db.add_candidate(name, position, party, bio)
    
    # Create an election session
    db.create_election_session("2025 General Election")
    
    return db  # Return the open database connection
