"""
Tests for VoterDashboard and VotingPage pubsub subscription behavior
Tests that did_mount and will_unmount properly handle pubsub subscriptions
"""

import unittest
import os
import sys
from unittest.mock import Mock, MagicMock, patch, call

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.views.voter_dashboard import VoterDashboard
from app.views.voting_page import VotingPage


class TestVoterDashboardPubSub(unittest.TestCase):
    """Test pubsub subscription and lifecycle methods in VoterDashboard"""
    
    def setUp(self):
        """Set up test environment"""
        self.mock_db = Mock()
        self.mock_db.get_voting_status.return_value = {"is_active": False}
        self.mock_db.get_users_by_role.return_value = []
        
        self.on_logout = Mock()
        self.on_profile_view = Mock()
        self.on_compare = Mock()
        self.on_voting_started = Mock()
    
    def test_did_mount_subscribes_to_pubsub(self):
        """Test that did_mount subscribes to pubsub when page is available"""
        dashboard = VoterDashboard(
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_profile_view=self.on_profile_view,
            on_compare=self.on_compare,
            on_voting_started=self.on_voting_started,
        )
        
        # Create mock page with pubsub
        mock_page = Mock()
        mock_pubsub = Mock()
        mock_page.pubsub = mock_pubsub
        dashboard.page = mock_page
        
        # Call did_mount
        dashboard.did_mount()
        
        # Verify subscribe was called with the handler
        mock_pubsub.subscribe.assert_called_once_with(dashboard._on_voting_status_change)
    
    def test_did_mount_handles_no_page(self):
        """Test that did_mount handles case when page is not available"""
        dashboard = VoterDashboard(
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_profile_view=self.on_profile_view,
            on_compare=self.on_compare,
            on_voting_started=self.on_voting_started,
        )
        
        # No page assigned
        dashboard.page = None
        
        # Call did_mount - should not raise error
        try:
            dashboard.did_mount()
        except Exception as e:
            self.fail(f"did_mount should not raise exception when page is None: {e}")
    
    def test_will_unmount_unsubscribes_from_pubsub(self):
        """Test that will_unmount properly unsubscribes with handler"""
        dashboard = VoterDashboard(
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_profile_view=self.on_profile_view,
            on_compare=self.on_compare,
            on_voting_started=self.on_voting_started,
        )
        
        # Create mock page with pubsub
        mock_page = Mock()
        mock_pubsub = Mock()
        mock_page.pubsub = mock_pubsub
        dashboard.page = mock_page
        
        # Call will_unmount
        dashboard.will_unmount()
        
        # Verify unsubscribe was called with the handler
        mock_pubsub.unsubscribe.assert_called_once_with(dashboard._on_voting_status_change)
    
    def test_will_unmount_handles_no_page(self):
        """Test that will_unmount handles case when page is not available"""
        dashboard = VoterDashboard(
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_profile_view=self.on_profile_view,
            on_compare=self.on_compare,
            on_voting_started=self.on_voting_started,
        )
        
        # No page assigned
        dashboard.page = None
        
        # Call will_unmount - should not raise error
        try:
            dashboard.will_unmount()
        except Exception as e:
            self.fail(f"will_unmount should not raise exception when page is None: {e}")
    
    def test_on_voting_status_change_triggers_callback_when_voting_starts(self):
        """Test that voting status change triggers the on_voting_started callback"""
        dashboard = VoterDashboard(
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_profile_view=self.on_profile_view,
            on_compare=self.on_compare,
            on_voting_started=self.on_voting_started,
        )
        
        # Initial state: voting not active
        dashboard.voting_active = False
        
        # Simulate voting status change message
        message = {
            "type": "voting_status_changed",
            "is_active": True
        }
        
        dashboard._on_voting_status_change(message)
        
        # Verify callback was triggered
        self.on_voting_started.assert_called_once()
        self.assertTrue(dashboard.voting_active)
    
    def test_on_voting_status_change_refreshes_when_voting_stops(self):
        """Test that voting status change refreshes dashboard when voting stops"""
        dashboard = VoterDashboard(
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_profile_view=self.on_profile_view,
            on_compare=self.on_compare,
            on_voting_started=self.on_voting_started,
        )
        
        # Set up mock page
        mock_page = Mock()
        dashboard.page = mock_page
        
        # Initial state: voting active
        dashboard.voting_active = True
        
        # Simulate voting status change message
        message = {
            "type": "voting_status_changed",
            "is_active": False
        }
        
        dashboard._on_voting_status_change(message)
        
        # Verify voting state changed
        self.assertFalse(dashboard.voting_active)
        # Verify page.update was called
        mock_page.update.assert_called_once()
    
    def test_on_voting_status_change_ignores_non_dict_messages(self):
        """Test that non-dict messages are ignored"""
        dashboard = VoterDashboard(
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_profile_view=self.on_profile_view,
            on_compare=self.on_compare,
            on_voting_started=self.on_voting_started,
        )
        
        # Try with various non-dict messages
        dashboard._on_voting_status_change("string message")
        dashboard._on_voting_status_change(123)
        dashboard._on_voting_status_change(None)
        
        # Verify callbacks were not triggered
        self.on_voting_started.assert_not_called()
    
    def test_on_voting_status_change_ignores_wrong_message_type(self):
        """Test that messages with wrong type are ignored"""
        dashboard = VoterDashboard(
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_profile_view=self.on_profile_view,
            on_compare=self.on_compare,
            on_voting_started=self.on_voting_started,
        )
        
        # Message with wrong type
        message = {
            "type": "some_other_event",
            "is_active": True
        }
        
        dashboard._on_voting_status_change(message)
        
        # Verify callbacks were not triggered
        self.on_voting_started.assert_not_called()


class TestVotingPagePubSub(unittest.TestCase):
    """Test pubsub subscription and lifecycle methods in VotingPage"""
    
    def setUp(self):
        """Set up test environment"""
        self.mock_db = Mock()
        self.mock_db.get_users_by_role.return_value = []
        self.mock_db.get_votes_by_voter.return_value = []
        
        self.on_logout = Mock()
        self.on_view_profile = Mock()
        self.on_voting_stopped = Mock()
    
    def test_did_mount_subscribes_to_pubsub(self):
        """Test that did_mount subscribes to pubsub when page is available"""
        voting_page = VotingPage(
            user_id=1,
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_view_profile=self.on_view_profile,
            on_voting_stopped=self.on_voting_stopped,
        )
        
        # Create mock page with pubsub
        mock_page = Mock()
        mock_pubsub = Mock()
        mock_page.pubsub = mock_pubsub
        voting_page.page = mock_page
        
        # Call did_mount
        voting_page.did_mount()
        
        # Verify subscribe was called with the handler
        mock_pubsub.subscribe.assert_called_once_with(voting_page._on_voting_status_change)
    
    def test_will_unmount_unsubscribes_from_pubsub(self):
        """Test that will_unmount properly unsubscribes with handler"""
        voting_page = VotingPage(
            user_id=1,
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_view_profile=self.on_view_profile,
            on_voting_stopped=self.on_voting_stopped,
        )
        
        # Create mock page with pubsub
        mock_page = Mock()
        mock_pubsub = Mock()
        mock_page.pubsub = mock_pubsub
        voting_page.page = mock_page
        
        # Call will_unmount
        voting_page.will_unmount()
        
        # Verify unsubscribe was called with the handler
        mock_pubsub.unsubscribe.assert_called_once_with(voting_page._on_voting_status_change)
    
    def test_on_voting_status_change_triggers_callback_when_voting_stops(self):
        """Test that voting status change triggers the on_voting_stopped callback"""
        voting_page = VotingPage(
            user_id=1,
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_view_profile=self.on_view_profile,
            on_voting_stopped=self.on_voting_stopped,
        )
        
        # Simulate voting status change message
        message = {
            "type": "voting_status_changed",
            "is_active": False
        }
        
        voting_page._on_voting_status_change(message)
        
        # Verify callback was triggered
        self.on_voting_stopped.assert_called_once()
    
    def test_on_voting_status_change_ignores_when_voting_starts(self):
        """Test that voting page doesn't react when voting starts (already voting)"""
        voting_page = VotingPage(
            user_id=1,
            username="test_user",
            db=self.mock_db,
            on_logout=self.on_logout,
            on_view_profile=self.on_view_profile,
            on_voting_stopped=self.on_voting_stopped,
        )
        
        # Message indicating voting started
        message = {
            "type": "voting_status_changed",
            "is_active": True
        }
        
        voting_page._on_voting_status_change(message)
        
        # Verify callback was not triggered (page doesn't care about voting starting)
        self.on_voting_stopped.assert_not_called()


if __name__ == "__main__":
    unittest.main()
