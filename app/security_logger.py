"""
Security Logging Module for HonestBallot
Provides structured logging for authentication events and security monitoring
"""

import logging
import os
from datetime import datetime
from pathlib import Path


# Configure logging
def setup_logger():
    """Set up the application logger with file and console handlers"""
    try:
        from app.config import Config
        log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
        log_file = Config.LOG_FILE
    except ImportError:
        log_level = logging.INFO
        log_file = "app.log"
    
    # Create logger
    logger = logging.getLogger("honestballot")
    logger.setLevel(log_level)
    
    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(levelname)-8s | %(message)s'
    )
    
    # File handler
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass  # Skip file logging if unable to create file
    
    # Console handler (for DEBUG mode only)
    try:
        from app.config import Config
        if Config.DEBUG:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
    except ImportError:
        pass
    
    return logger


# Initialize logger
logger = setup_logger()


class AuthLogger:
    """Specialized logger for authentication events"""
    
    @staticmethod
    def _format_details(**kwargs):
        """Format additional details as key=value pairs"""
        return " | ".join(f"{k}={v}" for k, v in kwargs.items() if v is not None)
    
    @staticmethod
    def login_success(username, user_id, role, ip_address=None):
        """Log successful login attempt"""
        details = AuthLogger._format_details(
            user_id=user_id, 
            role=role, 
            ip=ip_address
        )
        logger.info(f"LOGIN_SUCCESS | user={username} | {details}")
    
    @staticmethod
    def login_failed(username, reason="Invalid credentials", ip_address=None, attempts_remaining=None):
        """Log failed login attempt"""
        details = AuthLogger._format_details(
            reason=reason,
            ip=ip_address,
            attempts_remaining=attempts_remaining
        )
        logger.warning(f"LOGIN_FAILED | user={username} | {details}")
    
    @staticmethod
    def account_locked(username, duration_minutes, ip_address=None):
        """Log account lockout event"""
        details = AuthLogger._format_details(
            duration=f"{duration_minutes}m",
            ip=ip_address
        )
        logger.warning(f"ACCOUNT_LOCKED | user={username} | {details}")
    
    @staticmethod
    def logout(username, user_id, reason="user_initiated"):
        """Log logout event"""
        details = AuthLogger._format_details(
            user_id=user_id,
            reason=reason
        )
        logger.info(f"LOGOUT | user={username} | {details}")
    
    @staticmethod
    def session_expired(username, user_id):
        """Log session expiration"""
        details = AuthLogger._format_details(user_id=user_id)
        logger.info(f"SESSION_EXPIRED | user={username} | {details}")
    
    @staticmethod
    def password_changed(username, user_id, changed_by=None):
        """Log password change event"""
        details = AuthLogger._format_details(
            user_id=user_id,
            changed_by=changed_by or "self"
        )
        logger.info(f"PASSWORD_CHANGED | user={username} | {details}")
    
    @staticmethod
    def account_created(username, user_id, role, created_by=None):
        """Log new account creation"""
        details = AuthLogger._format_details(
            user_id=user_id,
            role=role,
            created_by=created_by or "self_registration"
        )
        logger.info(f"ACCOUNT_CREATED | user={username} | {details}")
    
    @staticmethod
    def privilege_escalation(username, user_id, old_role, new_role, changed_by):
        """Log role/privilege changes"""
        details = AuthLogger._format_details(
            user_id=user_id,
            old_role=old_role,
            new_role=new_role,
            changed_by=changed_by
        )
        logger.warning(f"PRIVILEGE_CHANGE | user={username} | {details}")
    
    @staticmethod
    def security_event(event_type, description, user=None, severity="INFO"):
        """Log general security events"""
        level = getattr(logging, severity.upper(), logging.INFO)
        details = AuthLogger._format_details(user=user)
        logger.log(level, f"SECURITY_EVENT | type={event_type} | {description} | {details}")


# Export convenience functions
auth_logger = AuthLogger()
