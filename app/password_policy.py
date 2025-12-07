"""
Password Policy Module for HonestBallot
Enforces password complexity, prevents reuse, and validates passwords
"""

import re
from datetime import datetime, timedelta


class PasswordPolicy:
    """Password policy enforcement"""
    
    # Policy settings
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL = True
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    MAX_REUSE_CHECK = 5  # Check last 5 passwords
    
    # Common weak passwords to reject
    WEAK_PASSWORDS = [
        "password", "password123", "123456", "12345678", "qwerty",
        "abc123", "letmein", "welcome", "admin", "login",
        "passw0rd", "Password1", "iloveyou", "sunshine", "princess",
    ]
    
    @classmethod
    def validate(cls, password, username=None, email=None):
        """
        Validate password against policy.
        Returns (is_valid, list of errors)
        """
        errors = []
        
        if not password:
            return False, ["Password is required"]
        
        # Length check
        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Password must be at least {cls.MIN_LENGTH} characters")
        
        if len(password) > cls.MAX_LENGTH:
            errors.append(f"Password must be less than {cls.MAX_LENGTH} characters")
        
        # Complexity checks
        if cls.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if cls.REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if cls.REQUIRE_DIGIT and not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        if cls.REQUIRE_SPECIAL and not any(c in cls.SPECIAL_CHARS for c in password):
            errors.append("Password must contain at least one special character (!@#$%^&*)")
        
        # Check for weak passwords
        if password.lower() in [p.lower() for p in cls.WEAK_PASSWORDS]:
            errors.append("Password is too common. Please choose a stronger password")
        
        # Check if password contains username or email
        if username and username.lower() in password.lower():
            errors.append("Password cannot contain your username")
        
        if email:
            email_name = email.split('@')[0].lower()
            if len(email_name) > 3 and email_name in password.lower():
                errors.append("Password cannot contain your email")
        
        return len(errors) == 0, errors
    
    @classmethod
    def get_strength(cls, password):
        """
        Calculate password strength score (0-100)
        """
        if not password:
            return 0
        
        score = 0
        
        # Length scoring (up to 30 points)
        length_score = min(len(password) * 2, 30)
        score += length_score
        
        # Character variety (up to 40 points)
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'\d', password):
            score += 10
        if any(c in cls.SPECIAL_CHARS for c in password):
            score += 10
        
        # Bonus for mixing (up to 20 points)
        unique_chars = len(set(password))
        score += min(unique_chars, 20)
        
        # Penalty for common patterns
        if password.lower() in [p.lower() for p in cls.WEAK_PASSWORDS]:
            score = max(0, score - 50)
        
        # Penalty for sequential characters
        if re.search(r'(012|123|234|345|456|567|678|789|abc|bcd|cde|def)', password.lower()):
            score = max(0, score - 10)
        
        # Penalty for repeated characters
        if re.search(r'(.)\1{2,}', password):
            score = max(0, score - 10)
        
        return min(100, score)
    
    @classmethod
    def get_strength_label(cls, password):
        """Get human-readable strength label"""
        score = cls.get_strength(password)
        
        if score < 30:
            return "Weak", "#F44336"  # Red
        elif score < 50:
            return "Fair", "#FF9800"  # Orange
        elif score < 70:
            return "Good", "#FFC107"  # Yellow
        elif score < 90:
            return "Strong", "#8BC34A"  # Light Green
        else:
            return "Very Strong", "#4CAF50"  # Green
    
    @classmethod
    def get_requirements_text(cls):
        """Get formatted password requirements text"""
        requirements = [f"At least {cls.MIN_LENGTH} characters"]
        
        if cls.REQUIRE_UPPERCASE:
            requirements.append("One uppercase letter (A-Z)")
        if cls.REQUIRE_LOWERCASE:
            requirements.append("One lowercase letter (a-z)")
        if cls.REQUIRE_DIGIT:
            requirements.append("One number (0-9)")
        if cls.REQUIRE_SPECIAL:
            requirements.append("One special character (!@#$%^&*)")
        
        return requirements


class PasswordHistory:
    """Track password history to prevent reuse"""
    
    def __init__(self, db):
        self.db = db
        self._ensure_table()
    
    def _ensure_table(self):
        """Create password history table if not exists"""
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        self.db.connection.commit()
    
    def add_password(self, user_id, password_hash):
        """Add a password to history"""
        self.db.cursor.execute('''
            INSERT INTO password_history (user_id, password_hash)
            VALUES (?, ?)
        ''', (user_id, password_hash))
        self.db.connection.commit()
        
        # Keep only last N passwords
        self.db.cursor.execute('''
            DELETE FROM password_history 
            WHERE user_id = ? AND id NOT IN (
                SELECT id FROM password_history 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            )
        ''', (user_id, user_id, PasswordPolicy.MAX_REUSE_CHECK))
        self.db.connection.commit()
    
    def is_password_reused(self, user_id, password, db):
        """Check if password was recently used"""
        self.db.cursor.execute('''
            SELECT password_hash FROM password_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, PasswordPolicy.MAX_REUSE_CHECK))
        
        old_hashes = self.db.cursor.fetchall()
        
        for (old_hash,) in old_hashes:
            if db.verify_password(password, old_hash):
                return True
        
        return False
