import uuid
from datetime import datetime, timedelta
from models.database import Database


class SessionManager:
    """Manages user sessions with unique tokens"""
    
    def __init__(self):
        self.db = Database()
        self.sessions = {}  # In-memory session cache
        self.session_timeout = timedelta(hours=8)  # Session timeout
    
    def create_session(self, user_id, username, email, role):
        """Create a new session for a user"""
        session_token = str(uuid.uuid4())
        
        # Store in database
        self.db.create_user_session(user_id, session_token)
        
        # Store in memory
        self.sessions[session_token] = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "role": role,
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        
        return session_token
    
    def verify_session(self, session_token):
        """Verify if a session is valid"""
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        # Check if session has expired
        if datetime.now() - session["created_at"] > self.session_timeout:
            self.end_session(session_token)
            return None
        
        # Update last activity
        session["last_activity"] = datetime.now()
        self.db.verify_session(session_token)
        
        return session
    
    def end_session(self, session_token):
        """End a user session"""
        if session_token in self.sessions:
            del self.sessions[session_token]
        self.db.end_session(session_token)
    
    def get_session_user(self, session_token):
        """Get user info from session"""
        session = self.verify_session(session_token)
        if session:
            return {
                "user_id": session["user_id"],
                "username": session["username"],
                "email": session["email"],
                "role": session["role"]
            }
        return None
    
    def get_all_sessions(self):
        """Get all active sessions"""
        active_sessions = {}
        for token, session in self.sessions.items():
            if datetime.now() - session["created_at"] <= self.session_timeout:
                active_sessions[token] = session
        return active_sessions
    
    def close(self):
        """Close database connection"""
        self.db.close()
