"""
Secure Configuration Module for HonestBallot
Loads configuration from environment variables or .env file
"""

import os
from pathlib import Path


def load_dotenv():
    """Load environment variables from .env file if it exists"""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key not in os.environ:  # Don't override existing env vars
                        os.environ[key] = value


# Load .env file on module import
load_dotenv()


class Config:
    """Application configuration from environment variables"""
    
    # Application Settings
    APP_NAME = os.getenv("APP_NAME", "HonestBallot")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    
    # Security Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production-to-a-secure-random-key")
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
    MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    LOCKOUT_DURATION_MINUTES = int(os.getenv("LOCKOUT_DURATION_MINUTES", "15"))
    
    # Database Settings
    DATABASE_NAME = os.getenv("DATABASE_NAME", "voting_app.db")
    
    # Password Hashing
    BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))
    
    # Logging Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "app.log")
    
    @classmethod
    def is_production(cls):
        """Check if running in production mode"""
        return not cls.DEBUG
    
    @classmethod
    def validate(cls):
        """Validate critical configuration settings"""
        warnings = []
        
        if cls.SECRET_KEY == "change-this-in-production-to-a-secure-random-key":
            warnings.append("WARNING: Using default SECRET_KEY. Set a secure key in production!")
        
        if len(cls.SECRET_KEY) < 32:
            warnings.append("WARNING: SECRET_KEY should be at least 32 characters long.")
        
        if cls.DEBUG and cls.is_production():
            warnings.append("WARNING: DEBUG mode should be disabled in production.")
        
        return warnings
    
    @classmethod
    def to_dict(cls):
        """Export non-sensitive config as dictionary"""
        return {
            "app_name": cls.APP_NAME,
            "app_version": cls.APP_VERSION,
            "debug": cls.DEBUG,
            "session_timeout_minutes": cls.SESSION_TIMEOUT_MINUTES,
            "max_login_attempts": cls.MAX_LOGIN_ATTEMPTS,
            "lockout_duration_minutes": cls.LOCKOUT_DURATION_MINUTES,
            "database_name": cls.DATABASE_NAME,
            "log_level": cls.LOG_LEVEL,
        }


# Export config instance
config = Config()
