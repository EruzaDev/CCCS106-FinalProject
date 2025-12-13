import sqlite3
import os
import bcrypt
import json
import threading
from datetime import datetime
from pathlib import Path

# Import configuration
try:
    from app.config import Config
except ImportError:
    # Fallback for direct module execution
    Config = None


class Database:
    """Local SQLite database manager for the voting application"""
    
    # Class-level lock shared across all instances for thread safety
    _db_lock = threading.RLock()
    
    def __init__(self, db_name=None):
        """Initialize database connection"""
        # Use config if available, otherwise use default
        if db_name is None:
            db_name = Config.DATABASE_NAME if Config else "voting_app.db"
        self.db_path = Path(db_name)
        self.connection = None
        self.cursor = None
        self.initialize_db()
    
    def _get_cursor(self):
        """Get the cursor, creating a new one if needed. Use within _db_lock context."""
        if self.cursor is None:
            self.cursor = self.connection.cursor()
        return self.cursor
    
    def initialize_db(self):
        """Initialize database and create tables if they don't exist"""
        # Enable check_same_thread=False to allow cross-thread access (safe for this app)
        self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
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
        
        # Create achievement verifications table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievement_verifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                politician_id INTEGER NOT NULL,
                achievement_title TEXT NOT NULL,
                achievement_description TEXT,
                evidence_url TEXT,
                status TEXT DEFAULT 'pending',
                verified_by INTEGER,
                verified_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (politician_id) REFERENCES users(id),
                FOREIGN KEY (verified_by) REFERENCES users(id)
            )
        ''')
        
        # Create voting status table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS voting_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                is_active BOOLEAN DEFAULT 0,
                started_at TIMESTAMP,
                ended_at TIMESTAMP,
                updated_by INTEGER,
                FOREIGN KEY (updated_by) REFERENCES users(id)
            )
        ''')
        
        # Create legal records table (NBI)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS legal_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                politician_id INTEGER NOT NULL,
                record_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                record_date TEXT,
                status TEXT DEFAULT 'pending',
                added_by INTEGER,
                verified_by INTEGER,
                verified_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (politician_id) REFERENCES users(id),
                FOREIGN KEY (added_by) REFERENCES users(id),
                FOREIGN KEY (verified_by) REFERENCES users(id)
            )
        ''')
        
        # Create audit logs table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                action_type TEXT NOT NULL,
                description TEXT,
                user_id INTEGER,
                user_role TEXT,
                target_type TEXT,
                target_id INTEGER,
                details TEXT,
                ip_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Create login_attempts table for credential stuffing protection
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identifier TEXT NOT NULL,
                attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN DEFAULT 0,
                ip_address TEXT
            )
        ''')
        
        # Create news_posts table for updates from politicians, NBI, and COMELEC
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_id INTEGER NOT NULL,
                author_role TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                is_pinned BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users(id)
            )
        ''')
        
        self.connection.commit()
    
    def hash_password(self, password):
        """Hash password using bcrypt (secure, salted hashing)"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, password_hash):
        """Verify password against bcrypt hash"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(password_hash, str):
            password_hash = password_hash.encode('utf-8')
        try:
            return bcrypt.checkpw(password, password_hash)
        except Exception:
            return False
    
    def create_user(self, username, email, password, role="voter"):
        """Create a new user"""
        with Database._db_lock:
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
        """Verify user credentials using bcrypt"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT id, username, email, role, password_hash FROM users
                WHERE email = ?
            ''', (email,))
        
            user = self.cursor.fetchone()
            if user and self.verify_password(password, user[4]):
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
        with Database._db_lock:
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
        with Database._db_lock:
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
        with Database._db_lock:
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
        with Database._db_lock:
            self.cursor.execute('''
                UPDATE user_sessions SET is_active = 0
                WHERE session_token = ?
            ''', (session_token,))
            self.connection.commit()
    
    # =====================
    # User Activity Monitoring
    # =====================
    
    def get_user_activity(self, user_id):
        """Get comprehensive user activity data"""
        with Database._db_lock:
            # Get user basic info with last login
            self.cursor.execute('''
                SELECT id, username, email, role, status, created_at, last_login
                FROM users WHERE id = ?
            ''', (user_id,))
            user = self.cursor.fetchone()
        
            if not user:
                return None
        
            # Get failed login attempts in last 24 hours
            failed_attempts = self.get_failed_attempts_count(user[2], minutes=1440)  # 24 hours
        
            # Get recent login history from audit logs
            self.cursor.execute('''
                SELECT action, created_at FROM audit_logs
                WHERE user_id = ? AND action_type IN ('login', 'logout', 'login_failed')
                ORDER BY created_at DESC LIMIT 10
            ''', (user_id,))
            login_history = self.cursor.fetchall()
        
            # Get active sessions count
            self.cursor.execute('''
                SELECT COUNT(*) FROM user_sessions
                WHERE user_id = ? AND is_active = 1
            ''', (user_id,))
            active_sessions = self.cursor.fetchone()[0]
        
            # Get total actions by this user
            self.cursor.execute('''
                SELECT COUNT(*) FROM audit_logs WHERE user_id = ?
            ''', (user_id,))
            total_actions = self.cursor.fetchone()[0]
        
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[3],
                "status": user[4],
                "created_at": user[5],
                "last_login": user[6],
                "failed_attempts_24h": failed_attempts,
                "login_history": login_history,
                "active_sessions": active_sessions,
                "total_actions": total_actions,
            }
    
    def get_all_user_activities(self, role_filter=None, limit=50):
        """Get activity summary for all users (admin view)"""
        with Database._db_lock:
            query = '''
                SELECT u.id, u.username, u.email, u.role, u.status, u.last_login,
                       (SELECT COUNT(*) FROM audit_logs WHERE user_id = u.id) as action_count,
                       (SELECT COUNT(*) FROM user_sessions WHERE user_id = u.id AND is_active = 1) as active_sessions
                FROM users u
                WHERE 1=1
            '''
            params = []
        
            if role_filter:
                query += " AND u.role = ?"
                params.append(role_filter)
        
            query += " ORDER BY u.last_login DESC NULLS LAST LIMIT ?"
            params.append(limit)
        
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
        
            return [{
                "id": r[0],
                "username": r[1],
                "email": r[2],
                "role": r[3],
                "status": r[4],
                "last_login": r[5],
                "action_count": r[6],
                "active_sessions": r[7],
            } for r in results]
    
    def cast_vote(self, voter_id, candidate_id, position, election_session_id=None):
        """Record a vote"""
        with Database._db_lock:
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
    
    def update_vote(self, voter_id, candidate_id, position):
        """Update an existing vote for a position"""
        with Database._db_lock:
            try:
                self.cursor.execute('''
                    UPDATE votes 
                    SET candidate_id = ?, voted_at = CURRENT_TIMESTAMP
                    WHERE voter_id = ? AND position = ?
                ''', (candidate_id, voter_id, position))
                self.connection.commit()
                return self.cursor.rowcount > 0
            except Exception as e:
                print(f"Error updating vote: {e}")
                return False
    
    def get_votes_by_position(self, position, election_session_id=None):
        """Get vote counts by position"""
        with Database._db_lock:
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
    
    def get_votes_by_voter(self, voter_id):
        """Get all votes cast by a specific voter"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT position, candidate_id FROM votes
                WHERE voter_id = ?
            ''', (voter_id,))
            return self.cursor.fetchall()
    
    def has_voted_for_position(self, voter_id, position):
        """Check if voter has already voted for a position"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT COUNT(*) FROM votes
                WHERE voter_id = ? AND position = ?
            ''', (voter_id, position))
            result = self.cursor.fetchone()
            return result[0] > 0 if result else False
    
    def get_candidates_by_position(self, position):
        """Get all candidates for a position"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT id, name, position, party, bio FROM candidates
                WHERE position = ?
            ''', (position,))
            return self.cursor.fetchall()
    
    def add_candidate(self, name, position, party, bio=""):
        """Add a new candidate"""
        with Database._db_lock:
            self.cursor.execute('''
                INSERT INTO candidates (name, position, party, bio)
                VALUES (?, ?, ?, ?)
            ''', (name, position, party, bio))
            self.connection.commit()
            return self.cursor.lastrowid
    
    def create_election_session(self, name):
        """Create an election session"""
        with Database._db_lock:
            self.cursor.execute('''
                INSERT INTO election_sessions (name, is_active)
                VALUES (?, 1)
            ''', (name,))
            self.connection.commit()
            return self.cursor.lastrowid
    
    def get_all_users(self):
        """Get all users (for admin purposes)"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT id, username, email, role, created_at, full_name, status, position, party, biography, profile_image FROM users
            ''')
            return self.cursor.fetchall()
    
    def get_users_by_role(self, role):
        """Get all users by role"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT id, username, email, role, created_at, full_name, status, position, party, biography, profile_image 
                FROM users WHERE role = ?
            ''', (role,))
            return self.cursor.fetchall()
    
    def create_voter(self, username, email, password, full_name):
        """Create a new voter account"""
        with Database._db_lock:
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
        with Database._db_lock:
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
        with Database._db_lock:
            self.cursor.execute('''
                UPDATE users SET status = ? WHERE id = ?
            ''', (status, user_id))
            self.connection.commit()
    
    def update_voter(self, user_id, full_name, email, username):
        """Update voter account without changing password"""
        with Database._db_lock:
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
        with Database._db_lock:
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
        with Database._db_lock:
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
        with Database._db_lock:
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
        with Database._db_lock:
            self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            self.connection.commit()
            return self.cursor.fetchall()
    
    # Achievement Verification Methods
    def create_achievement_verification(self, politician_id, title, description, evidence_url=None):
        """Create a new achievement verification request"""
        with Database._db_lock:
            try:
                self.cursor.execute('''
                    INSERT INTO achievement_verifications (politician_id, achievement_title, achievement_description, evidence_url)
                    VALUES (?, ?, ?, ?)
                ''', (politician_id, title, description, evidence_url))
                self.connection.commit()
                return self.cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
    
    def get_pending_verifications(self):
        """Get all pending achievement verifications"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT av.id, av.politician_id, av.achievement_title, av.achievement_description, 
                       av.evidence_url, av.status, av.created_at, u.full_name, u.username, u.position
                FROM achievement_verifications av
                JOIN users u ON av.politician_id = u.id
                WHERE av.status = 'pending'
                ORDER BY av.created_at DESC
            ''')
            return self.cursor.fetchall()
    
    def get_all_verifications(self):
        """Get all achievement verifications"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT av.id, av.politician_id, av.achievement_title, av.achievement_description, 
                       av.evidence_url, av.status, av.created_at, u.full_name, u.username, u.position
                FROM achievement_verifications av
                JOIN users u ON av.politician_id = u.id
                ORDER BY av.created_at DESC
            ''')
            return self.cursor.fetchall()
    
    def verify_achievement(self, verification_id, verified_by_id, status='verified'):
        """Verify or reject an achievement"""
        with Database._db_lock:
            self.cursor.execute('''
                UPDATE achievement_verifications 
                SET status = ?, verified_by = ?, verified_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, verified_by_id, verification_id))
            self.connection.commit()
    
    def get_verifications_by_politician(self, politician_id):
        """Get all verifications for a specific politician"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT id, achievement_title, achievement_description, evidence_url, status, created_at
                FROM achievement_verifications
                WHERE politician_id = ?
                ORDER BY created_at DESC
            ''', (politician_id,))
            return self.cursor.fetchall()
    
    # Voting Status Methods
    def get_voting_status(self):
        """Get current voting status"""
        with Database._db_lock:
            self.cursor.execute('SELECT is_active, started_at, ended_at FROM voting_status ORDER BY id DESC LIMIT 1')
            result = self.cursor.fetchone()
            if result:
                return {"is_active": bool(result[0]), "started_at": result[1], "ended_at": result[2]}
            return {"is_active": False, "started_at": None, "ended_at": None}
    
    def start_voting(self, user_id):
        """Start voting session"""
        with Database._db_lock:
            self.cursor.execute('''
                INSERT INTO voting_status (is_active, started_at, updated_by)
                VALUES (1, CURRENT_TIMESTAMP, ?)
            ''', (user_id,))
            self.connection.commit()
            return True
    
    def stop_voting(self, user_id):
        """Stop voting session"""
        with Database._db_lock:
            self.cursor.execute('''
                UPDATE voting_status SET is_active = 0, ended_at = CURRENT_TIMESTAMP, updated_by = ?
                WHERE id = (SELECT MAX(id) FROM voting_status)
            ''', (user_id,))
            self.connection.commit()
            return True
    
    # Election Results Methods
    def get_election_results(self):
        """Get election results grouped by position"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT u.id, u.full_name, u.username, u.position, u.party, u.profile_image,
                       COUNT(v.id) as vote_count
                FROM users u
                LEFT JOIN votes v ON u.id = v.candidate_id
                WHERE u.role = 'politician'
                GROUP BY u.id
                ORDER BY u.position, vote_count DESC
            ''')
            return self.cursor.fetchall()
    
    def get_total_votes_cast(self):
        """Get total number of votes cast"""
        with Database._db_lock:
            self.cursor.execute('SELECT COUNT(*) FROM votes')
            result = self.cursor.fetchone()
            return result[0] if result else 0
    
    def get_unique_voters_count(self):
        """Get count of unique voters who have voted"""
        with Database._db_lock:
            self.cursor.execute('SELECT COUNT(DISTINCT voter_id) FROM votes')
            result = self.cursor.fetchone()
            return result[0] if result else 0
    
    def get_positions_count(self):
        """Get count of unique positions being voted on"""
        with Database._db_lock:
            self.cursor.execute('SELECT COUNT(DISTINCT position) FROM users WHERE role = "politician"')
            result = self.cursor.fetchone()
            return result[0] if result else 0
    
    def get_votes_by_candidate(self, candidate_id):
        """Get vote count for a specific candidate"""
        with Database._db_lock:
            self.cursor.execute('SELECT COUNT(*) FROM votes WHERE candidate_id = ?', (candidate_id,))
            result = self.cursor.fetchone()
            return result[0] if result else 0
    
    def verify_user_by_username(self, username, password):
        """Verify user credentials by username using bcrypt"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT id, username, email, role, password_hash FROM users
                WHERE username = ?
            ''', (username,))
        
            user = self.cursor.fetchone()
            if user and self.verify_password(password, user[4]):
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
    
    # Credential Stuffing Protection Methods
    # Use config values if available, otherwise use defaults
    @property
    def MAX_LOGIN_ATTEMPTS(self):
        return Config.MAX_LOGIN_ATTEMPTS if Config else 5
    
    @property
    def LOCKOUT_DURATION_MINUTES(self):
        return Config.LOCKOUT_DURATION_MINUTES if Config else 15
    
    def record_login_attempt(self, identifier, success=False, ip_address=None):
        """Record a login attempt for rate limiting"""
        with Database._db_lock:
            self.cursor.execute('''
                INSERT INTO login_attempts (identifier, success, ip_address)
                VALUES (?, ?, ?)
            ''', (identifier.lower(), success, ip_address))
            self.connection.commit()
    
    def get_failed_attempts_count(self, identifier, minutes=15):
        """Get the number of failed login attempts in the last N minutes"""
        with Database._db_lock:
            self.cursor.execute(f'''
                SELECT COUNT(*) FROM login_attempts
                WHERE identifier = ? 
                AND success = 0
                AND attempt_time > datetime('now', '-{int(minutes)} minutes')
            ''', (identifier.lower(),))
            result = self.cursor.fetchone()
            return result[0] if result else 0
    
    def is_account_locked(self, identifier):
        """Check if account is locked due to too many failed attempts"""
        failed_attempts = self.get_failed_attempts_count(
            identifier, 
            self.LOCKOUT_DURATION_MINUTES
        )
        return failed_attempts >= self.MAX_LOGIN_ATTEMPTS
    
    def get_lockout_remaining_time(self, identifier):
        """Get remaining lockout time in seconds"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT attempt_time FROM login_attempts
                WHERE identifier = ? AND success = 0
                ORDER BY attempt_time DESC
                LIMIT 1
            ''', (identifier.lower(),))
            result = self.cursor.fetchone()
            if result:
                from datetime import timedelta
                last_attempt = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
                lockout_end = last_attempt + timedelta(minutes=self.LOCKOUT_DURATION_MINUTES)
                remaining = (lockout_end - datetime.now()).total_seconds()
                return max(0, int(remaining))
            return 0
    
    def clear_failed_attempts(self, identifier):
        """Clear failed login attempts after successful login"""
        with Database._db_lock:
            self.cursor.execute('''
                DELETE FROM login_attempts
                WHERE identifier = ? AND success = 0
            ''', (identifier.lower(),))
            self.connection.commit()
    
    def cleanup_old_login_attempts(self, hours=24):
        """Clean up old login attempts (older than N hours)"""
        with Database._db_lock:
            self.cursor.execute(f'''
                DELETE FROM login_attempts
                WHERE attempt_time < datetime('now', '-{int(hours)} hours')
            ''')
            self.connection.commit()
    
    # Legal Records Methods (NBI)
    def create_legal_record(self, politician_id, record_type, title, description, date, added_by):
        """Create a new legal record for a politician"""
        with Database._db_lock:
            try:
                self.cursor.execute('''
                    INSERT INTO legal_records (politician_id, record_type, title, description, record_date, status, added_by)
                    VALUES (?, ?, ?, ?, ?, 'pending', ?)
                ''', (politician_id, record_type, title, description, date, added_by))
                self.connection.commit()
                return self.cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
    
    def get_all_legal_records(self):
        """Get all legal records with politician info"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT lr.id, lr.politician_id, lr.record_type, lr.title, lr.description, 
                       lr.record_date, lr.status, lr.created_at, u.full_name, u.username, u.position, u.party, u.profile_image
                FROM legal_records lr
                JOIN users u ON lr.politician_id = u.id
                ORDER BY lr.created_at DESC
            ''')
            return self.cursor.fetchall()
    
    def get_legal_records_by_politician(self, politician_id):
        """Get all legal records for a specific politician"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT id, record_type, title, description, record_date, status, created_at
                FROM legal_records
                WHERE politician_id = ?
                ORDER BY created_at DESC
            ''', (politician_id,))
            return self.cursor.fetchall()
    
    def update_legal_record_status(self, record_id, status, verified_by):
        """Update the status of a legal record"""
        with Database._db_lock:
            self.cursor.execute('''
                UPDATE legal_records 
                SET status = ?, verified_by = ?, verified_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, verified_by, record_id))
            self.connection.commit()
    
    def update_legal_record(self, record_id, record_type, title, description, date):
        """Update a legal record's details"""
        with Database._db_lock:
            try:
                self.cursor.execute('''
                    UPDATE legal_records 
                    SET record_type = ?, title = ?, description = ?, record_date = ?
                    WHERE id = ?
                ''', (record_type, title, description, date, record_id))
                self.connection.commit()
                return True
            except Exception as e:
                print(f"Error updating legal record: {e}")
                return False
    
    def get_legal_record_by_id(self, record_id):
        """Get a single legal record by ID"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT id, politician_id, record_type, title, description, record_date, status
                FROM legal_records
                WHERE id = ?
            ''', (record_id,))
            return self.cursor.fetchone()
    
    def delete_legal_record(self, record_id):
        """Delete a legal record"""
        with Database._db_lock:
            self.cursor.execute('DELETE FROM legal_records WHERE id = ?', (record_id,))
            self.connection.commit()
    
    def get_legal_records_stats(self):
        """Get statistics about legal records"""
        with Database._db_lock:
            # Total records
            self.cursor.execute('SELECT COUNT(*) FROM legal_records')
            total = self.cursor.fetchone()[0]
        
            # Verified records
            self.cursor.execute("SELECT COUNT(*) FROM legal_records WHERE status = 'verified'")
            verified = self.cursor.fetchone()[0]
        
            # Pending records
            self.cursor.execute("SELECT COUNT(*) FROM legal_records WHERE status = 'pending'")
            pending = self.cursor.fetchone()[0]
        
            return {"total": total, "verified": verified, "pending": pending}
    
    def search_legal_records(self, query):
        """Search legal records by politician name or record title"""
        with Database._db_lock:
            search_term = f"%{query}%"
            self.cursor.execute('''
                SELECT lr.id, lr.politician_id, lr.record_type, lr.title, lr.description, 
                       lr.record_date, lr.status, lr.created_at, u.full_name, u.username, u.position, u.party, u.profile_image
                FROM legal_records lr
                JOIN users u ON lr.politician_id = u.id
                WHERE u.full_name LIKE ? OR u.username LIKE ? OR lr.title LIKE ?
                ORDER BY lr.created_at DESC
            ''', (search_term, search_term, search_term))
            return self.cursor.fetchall()
    
    # =====================
    # Audit Log Methods
    # =====================
    
    def log_action(self, action, action_type, description=None, user_id=None, user_role=None, 
                   target_type=None, target_id=None, details=None, ip_address=None):
        """Log an action to the audit log"""
        with Database._db_lock:
            try:
                details_json = json.dumps(details) if details else None
                self.cursor.execute('''
                    INSERT INTO audit_logs (action, action_type, description, user_id, user_role, 
                                           target_type, target_id, details, ip_address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (action, action_type, description, user_id, user_role, 
                      target_type, target_id, details_json, ip_address))
                self.connection.commit()
                return self.cursor.lastrowid
            except Exception as e:
                print(f"Error logging action: {e}")
                return None
    
    def get_audit_logs(self, limit=100, offset=0, action_type=None, user_role=None, 
                       date_from=None, date_to=None):
        """Get audit logs with optional filtering including date range"""
        with Database._db_lock:
            query = '''
                SELECT al.id, al.action, al.action_type, al.description, al.user_id, 
                       al.user_role, al.target_type, al.target_id, al.details, 
                       al.ip_address, al.created_at, u.username, u.full_name
                FROM audit_logs al
                LEFT JOIN users u ON al.user_id = u.id
                WHERE 1=1
            '''
            params = []
        
            if action_type:
                query += " AND al.action_type = ?"
                params.append(action_type)
        
            if user_role:
                query += " AND al.user_role = ?"
                params.append(user_role)
        
            if date_from:
                query += " AND al.created_at >= ?"
                params.append(date_from)
        
            if date_to:
                query += " AND al.created_at <= ?"
                params.append(date_to)
        
            query += " ORDER BY al.created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
    
    def get_audit_logs_for_role(self, viewer_role, limit=100, offset=0):
        """Get audit logs filtered by what a role is allowed to see"""
        with Database._db_lock:
            # Define what each role can see
            role_permissions = {
                'comelec': ['all'],  # COMELEC can see everything
                'nbi': ['legal_record', 'legal_record_edit', 'legal_record_status', 'login', 'logout'],  # NBI sees legal records and auth
                'politician': ['verification', 'legal_record', 'legal_record_edit', 'legal_record_status', 'vote_result'],  # Politicians see their related logs
            }
        
            allowed_types = role_permissions.get(viewer_role, [])
        
            if 'all' in allowed_types:
                return self.get_audit_logs(limit, offset)
        
            if not allowed_types:
                return []
        
            placeholders = ','.join(['?' for _ in allowed_types])
            query = f'''
                SELECT al.id, al.action, al.action_type, al.description, al.user_id, 
                       al.user_role, al.target_type, al.target_id, al.details, 
                       al.ip_address, al.created_at, u.username, u.full_name
                FROM audit_logs al
                LEFT JOIN users u ON al.user_id = u.id
                WHERE al.action_type IN ({placeholders})
                ORDER BY al.created_at DESC
                LIMIT ? OFFSET ?
            '''
            params = allowed_types + [limit, offset]
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
    
    def get_audit_log_stats(self):
        """Get audit log statistics"""
        with Database._db_lock:
            stats = {}
        
            # Total logs
            self.cursor.execute("SELECT COUNT(*) FROM audit_logs")
            stats['total'] = self.cursor.fetchone()[0]
        
            # Logs by action type
            self.cursor.execute('''
                SELECT action_type, COUNT(*) FROM audit_logs 
                GROUP BY action_type ORDER BY COUNT(*) DESC
            ''')
            stats['by_type'] = self.cursor.fetchall()
        
            # Logs today
            self.cursor.execute('''
                SELECT COUNT(*) FROM audit_logs 
                WHERE DATE(created_at) = DATE('now')
            ''')
            stats['today'] = self.cursor.fetchone()[0]
        
            return stats
    
    def search_audit_logs(self, query, viewer_role=None, limit=100):
        """Search audit logs by action, description, or username"""
        with Database._db_lock:
            search_term = f"%{query}%"
        
            base_query = '''
                SELECT al.id, al.action, al.action_type, al.description, al.user_id, 
                       al.user_role, al.target_type, al.target_id, al.details, 
                       al.ip_address, al.created_at, u.username, u.full_name
                FROM audit_logs al
                LEFT JOIN users u ON al.user_id = u.id
                WHERE (al.action LIKE ? OR al.description LIKE ? OR u.username LIKE ? OR u.full_name LIKE ?)
            '''
            params = [search_term, search_term, search_term, search_term]
        
            # Apply role-based filtering
            if viewer_role and viewer_role != 'comelec':
                role_permissions = {
                    'nbi': ['legal_record', 'login', 'logout'],
                    'politician': ['verification', 'legal_record', 'vote_result'],
                }
                allowed_types = role_permissions.get(viewer_role, [])
                if allowed_types:
                    placeholders = ','.join(['?' for _ in allowed_types])
                    base_query += f" AND al.action_type IN ({placeholders})"
                    params.extend(allowed_types)
        
            base_query += " ORDER BY al.created_at DESC LIMIT ?"
            params.append(limit)
        
            self.cursor.execute(base_query, params)
            return self.cursor.fetchall()
    
    # =====================
    # News Feed Methods
    # =====================
    
    def create_news_post(self, author_id, author_role, title, content, category='general', is_pinned=False):
        """Create a news post (for politicians, NBI, COMELEC)"""
        with Database._db_lock:
            try:
                self.cursor.execute('''
                    INSERT INTO news_posts (author_id, author_role, title, content, category, is_pinned)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (author_id, author_role, title, content, category, is_pinned))
                self.connection.commit()
                return self.cursor.lastrowid
            except Exception as e:
                print(f"Error creating news post: {e}")
                return None
    
    def get_news_posts(self, limit=50, offset=0, category=None, author_role=None):
        """Get news posts for the feed (voters view)"""
        with Database._db_lock:
            query = '''
                SELECT np.id, np.author_id, np.author_role, np.title, np.content, 
                       np.category, np.is_pinned, np.created_at, np.updated_at,
                       u.username, u.full_name, u.profile_image, u.position, u.party
                FROM news_posts np
                JOIN users u ON np.author_id = u.id
                WHERE 1=1
            '''
            params = []
            
            if category:
                query += " AND np.category = ?"
                params.append(category)
            
            if author_role:
                query += " AND np.author_role = ?"
                params.append(author_role)
            
            # Pinned posts first, then by date
            query += " ORDER BY np.is_pinned DESC, np.created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            
            return [{
                "id": r[0],
                "author_id": r[1],
                "author_role": r[2],
                "title": r[3],
                "content": r[4],
                "category": r[5],
                "is_pinned": bool(r[6]),
                "created_at": r[7],
                "updated_at": r[8],
                "author_username": r[9],
                "author_name": r[10] or r[9],
                "author_image": r[11],
                "author_position": r[12],
                "author_party": r[13],
            } for r in results]
    
    def get_news_posts_by_author(self, author_id, limit=20):
        """Get news posts by a specific author"""
        with Database._db_lock:
            self.cursor.execute('''
                SELECT id, title, content, category, is_pinned, created_at, updated_at
                FROM news_posts
                WHERE author_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (author_id, limit))
            return self.cursor.fetchall()
    
    def update_news_post(self, post_id, title, content, category=None, is_pinned=None):
        """Update a news post"""
        with Database._db_lock:
            try:
                updates = ["title = ?", "content = ?", "updated_at = CURRENT_TIMESTAMP"]
                params = [title, content]
                
                if category is not None:
                    updates.append("category = ?")
                    params.append(category)
                
                if is_pinned is not None:
                    updates.append("is_pinned = ?")
                    params.append(is_pinned)
                
                params.append(post_id)
                
                self.cursor.execute(f'''
                    UPDATE news_posts SET {", ".join(updates)} WHERE id = ?
                ''', params)
                self.connection.commit()
                return True
            except Exception as e:
                print(f"Error updating news post: {e}")
                return False
    
    def delete_news_post(self, post_id):
        """Delete a news post"""
        with Database._db_lock:
            self.cursor.execute('DELETE FROM news_posts WHERE id = ?', (post_id,))
            self.connection.commit()
    
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
        # NBI Officer account
        ("nbi1", "nbi1@honestballot.local", "nbi123", "nbi"),
        # COMELEC account
        ("comelec1", "comelec1@honestballot.local", "com123", "comelec"),
    ]
    
    for username, email, password, role in demo_users:
        db.create_user(username, email, password, role)
    
    # Create sample politician accounts with positions
    politicians_data = [
        # Governor candidates
        ("Roberto Cruz", "rcruz@honestballot.local", "pol123", "Roberto Cruz", "Governor", "United Citizens Party", "Experienced administrator with 15 years in public service"),
        ("Carmen dela Cruz", "cdelacruz@honestballot.local", "pol123", "Carmen dela Cruz", "Governor", "Progressive Alliance", "Former city mayor with focus on infrastructure"),
        # Mayor candidates
        ("Elena Rodriguez", "erodriguez@honestballot.local", "pol123", "Elena Rodriguez", "Mayor", "Green Coalition", "Environmental advocate and community leader"),
        ("Antonio Mendoza", "amendoza@honestballot.local", "pol123", "Antonio Mendoza", "Mayor", "Independent", "Business leader focused on economic growth"),
        # Senator candidates
        ("Maria Santos", "msantos@honestballot.local", "pol123", "Maria Santos", "Senator", "Progressive Alliance", "Education reform champion"),
        ("Miguel Reyes", "mreyes@honestballot.local", "pol123", "Miguel Reyes", "Senator", "Democratic Reform Party", "Healthcare advocate"),
    ]
    
    for username, email, password, full_name, position, party, bio in politicians_data:
        db.create_politician(username, email, password, full_name, position, party, bio)
    
    # Create sample candidates (legacy table)
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
    
    # Create sample achievement verifications for politicians
    politicians = db.get_users_by_role("politician")
    if politicians:
        # Add achievement verifications for first few politicians
        for i, politician in enumerate(politicians[:3]):
            politician_id = politician[0]
            full_name = politician[5] if politician[5] else politician[1]
            
            db.create_achievement_verification(
                politician_id,
                "Public Service Achievement",
                f"Successfully led community development projects benefiting local constituents.",
                None
            )
            
            if i == 0:
                db.create_achievement_verification(
                    politician_id,
                    "Educational Reform Initiative",
                    "Implemented scholarship programs for underprivileged students.",
                    None
                )
    
    # Create sample legal records for politicians
    nbi_user = db.cursor.execute("SELECT id FROM users WHERE role = 'nbi' LIMIT 1").fetchone()
    nbi_user_id = nbi_user[0] if nbi_user else None
    
    if politicians and nbi_user_id:
        # Sample legal records data
        legal_records_data = [
            # Roberto Cruz - Governor candidate
            (politicians[0][0], "Conflict of Interest Allegation", "Conflict of Interest Allegation", 
             "Alleged involvement in awarding contracts to family-owned businesses. Investigation ongoing.", 
             "1/10/2024", "pending"),
            # Miguel Reyes - Senator candidate
            (politicians[5][0] if len(politicians) > 5 else politicians[0][0], "Libel Case (Dismissed)", "Libel Case (Dismissed)", 
             "Filed by business mogul. Case dismissed due to lack of evidence.", 
             "3/10/2021", "dismissed"),
            # Antonio Mendoza - Mayor candidate
            (politicians[3][0] if len(politicians) > 3 else politicians[0][0], "Tax Compliance Issue", "Tax Compliance Issue", 
             "Settled previous tax discrepancies from business operations. All penalties paid.", 
             "3/10/2020", "verified"),
        ]
        
        for pol_id, record_type, title, description, date, status in legal_records_data:
            record_id = db.create_legal_record(pol_id, record_type, title, description, date, nbi_user_id)
            if record_id and status != "pending":
                db.update_legal_record_status(record_id, status, nbi_user_id)
    
    return db  # Return the open database connection
