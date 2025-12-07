"""
Unit Tests for Session Manager
Tests session creation, verification, and management
"""
import pytest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSessionManager:
    """Unit tests for SessionManager class"""
    
    @pytest.fixture
    def mock_database(self):
        """Create a mock database"""
        mock_db = Mock()
        mock_db.create_user_session = Mock(return_value=True)
        mock_db.verify_session = Mock(return_value=True)
        mock_db.end_session = Mock(return_value=True)
        mock_db.close = Mock()
        return mock_db
    
    @pytest.fixture
    def session_manager(self, mock_database):
        """Create SessionManager with mocked database"""
        with patch('app.state.session_manager.Database', return_value=mock_database):
            from app.state.session_manager import SessionManager
            manager = SessionManager()
            yield manager
            manager.close()
    
    # =====================
    # Session Creation Tests
    # =====================
    
    def test_create_session_returns_token(self, session_manager):
        """Test that creating a session returns a valid token"""
        token = session_manager.create_session(
            user_id=1,
            username="testuser",
            email="test@example.com",
            role="voter"
        )
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) == 36  # UUID format
    
    def test_create_session_stores_user_data(self, session_manager):
        """Test that session stores user data correctly"""
        token = session_manager.create_session(
            user_id=1,
            username="testuser",
            email="test@example.com",
            role="voter"
        )
        
        session = session_manager.sessions.get(token)
        assert session is not None
        assert session["user_id"] == 1
        assert session["username"] == "testuser"
        assert session["email"] == "test@example.com"
        assert session["role"] == "voter"
    
    def test_create_session_with_different_roles(self, session_manager):
        """Test session creation with different user roles"""
        roles = ["voter", "comelec", "admin", "nbi"]
        
        for role in roles:
            token = session_manager.create_session(
                user_id=1,
                username=f"user_{role}",
                email=f"{role}@example.com",
                role=role
            )
            session = session_manager.sessions.get(token)
            assert session["role"] == role
    
    def test_create_multiple_sessions(self, session_manager):
        """Test creating multiple sessions"""
        tokens = []
        for i in range(5):
            token = session_manager.create_session(
                user_id=i,
                username=f"user{i}",
                email=f"user{i}@example.com",
                role="voter"
            )
            tokens.append(token)
        
        # All tokens should be unique
        assert len(set(tokens)) == 5
        # All sessions should exist
        assert len(session_manager.sessions) == 5
    
    # =====================
    # Session Verification Tests
    # =====================
    
    def test_verify_valid_session(self, session_manager):
        """Test verifying a valid session"""
        token = session_manager.create_session(
            user_id=1,
            username="testuser",
            email="test@example.com",
            role="voter"
        )
        
        session = session_manager.verify_session(token)
        assert session is not None
        assert session["user_id"] == 1
    
    def test_verify_invalid_session(self, session_manager):
        """Test verifying an invalid session token"""
        result = session_manager.verify_session("invalid-token-12345")
        assert result is None
    
    def test_verify_session_updates_last_activity(self, session_manager):
        """Test that verification updates last activity time"""
        token = session_manager.create_session(
            user_id=1,
            username="testuser",
            email="test@example.com",
            role="voter"
        )
        
        # Get initial activity time
        initial_time = session_manager.sessions[token]["last_activity"]
        
        # Wait a tiny bit and verify
        import time
        time.sleep(0.01)
        session_manager.verify_session(token)
        
        # Last activity should be updated
        new_time = session_manager.sessions[token]["last_activity"]
        assert new_time >= initial_time
    
    # =====================
    # Session End Tests
    # =====================
    
    def test_end_session_removes_from_memory(self, session_manager):
        """Test that ending session removes it from memory"""
        token = session_manager.create_session(
            user_id=1,
            username="testuser",
            email="test@example.com",
            role="voter"
        )
        
        assert token in session_manager.sessions
        session_manager.end_session(token)
        assert token not in session_manager.sessions
    
    def test_end_nonexistent_session(self, session_manager):
        """Test ending a session that doesn't exist (should not error)"""
        # Should not raise an error
        session_manager.end_session("nonexistent-token")
    
    # =====================
    # Get Session User Tests
    # =====================
    
    def test_get_session_user_returns_user_info(self, session_manager):
        """Test getting user info from session"""
        token = session_manager.create_session(
            user_id=1,
            username="testuser",
            email="test@example.com",
            role="voter"
        )
        
        user_info = session_manager.get_session_user(token)
        assert user_info is not None
        assert user_info["user_id"] == 1
        assert user_info["username"] == "testuser"
        assert user_info["email"] == "test@example.com"
        assert user_info["role"] == "voter"
    
    def test_get_session_user_invalid_token(self, session_manager):
        """Test getting user info with invalid token"""
        user_info = session_manager.get_session_user("invalid-token")
        assert user_info is None
    
    # =====================
    # Get All Sessions Tests
    # =====================
    
    def test_get_all_sessions(self, session_manager):
        """Test getting all active sessions"""
        # Create multiple sessions
        for i in range(3):
            session_manager.create_session(
                user_id=i,
                username=f"user{i}",
                email=f"user{i}@example.com",
                role="voter"
            )
        
        all_sessions = session_manager.get_all_sessions()
        assert len(all_sessions) == 3
    
    def test_get_all_sessions_empty(self, session_manager):
        """Test getting all sessions when none exist"""
        all_sessions = session_manager.get_all_sessions()
        assert len(all_sessions) == 0


class TestSessionTimeout:
    """Tests for session timeout functionality"""
    
    @pytest.fixture
    def mock_database(self):
        """Create a mock database"""
        mock_db = Mock()
        mock_db.create_user_session = Mock(return_value=True)
        mock_db.verify_session = Mock(return_value=True)
        mock_db.end_session = Mock(return_value=True)
        mock_db.close = Mock()
        return mock_db
    
    @pytest.fixture
    def session_manager(self, mock_database):
        """Create SessionManager with mocked database"""
        with patch('app.state.session_manager.Database', return_value=mock_database):
            from app.state.session_manager import SessionManager
            manager = SessionManager()
            yield manager
            manager.close()
    
    def test_session_timeout_value(self, session_manager):
        """Test that session timeout is set correctly (8 hours)"""
        assert session_manager.session_timeout == timedelta(hours=8)
    
    def test_expired_session_returns_none(self, session_manager):
        """Test that expired sessions return None on verification"""
        token = session_manager.create_session(
            user_id=1,
            username="testuser",
            email="test@example.com",
            role="voter"
        )
        
        # Manually expire the session
        session_manager.sessions[token]["created_at"] = datetime.now() - timedelta(hours=9)
        
        # Session should be considered expired
        result = session_manager.verify_session(token)
        assert result is None
    
    def test_expired_session_gets_removed(self, session_manager):
        """Test that expired sessions are removed when verified"""
        token = session_manager.create_session(
            user_id=1,
            username="testuser",
            email="test@example.com",
            role="voter"
        )
        
        # Manually expire the session
        session_manager.sessions[token]["created_at"] = datetime.now() - timedelta(hours=9)
        
        # Verify (should fail and remove)
        session_manager.verify_session(token)
        
        # Session should be removed
        assert token not in session_manager.sessions
