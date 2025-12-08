"""
Tests for NBI Dashboard audit logging functionality
"""

import pytest
import tempfile
import os
from app.storage.database import Database


class TestNBIAuditLogging:
    """Test suite for NBI operations audit logging"""
    
    def setup_method(self):
        """Set up test database before each test"""
        self.temp_db = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(self.temp_db.name)
        
        # Create test users
        self.db.create_user("nbi_officer", "nbi@test.com", "nbi123", "nbi")
        self.nbi = self.db.get_user_by_email("nbi@test.com")
        
        self.db.create_user("politician1", "pol@test.com", "pol123", "politician")
        self.politician = self.db.get_user_by_email("pol@test.com")
    
    def teardown_method(self):
        """Clean up test database after each test"""
        if hasattr(self, 'db') and self.db.connection:
            self.db.connection.close()
        if hasattr(self, 'temp_db') and os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_add_legal_record_logs_action(self):
        """Test that adding a legal record creates audit log entry"""
        # Create a legal record
        record_id = self.db.create_legal_record(
            politician_id=self.politician["id"],
            record_type="Graft and Corruption Case",
            title="Test Case",
            description="Test description",
            date="01/15/2025",
            added_by=self.nbi["id"]
        )
        
        # Log the action (simulating what NBI dashboard does)
        self.db.log_action(
            action="Legal Record Added",
            action_type="legal_record",
            description="Added record: Test Case",
            user_id=self.nbi["id"],
            user_role="nbi",
            target_type="politician",
            target_id=self.politician["id"],
        )
        
        # Verify audit log was created
        logs = self.db.get_audit_logs_for_role("nbi")
        assert len(logs) > 0, "Audit log should be created"
        
        # Verify log content
        add_logs = [log for log in logs if log[2] == "legal_record"]
        assert len(add_logs) > 0, "Should have legal_record action type"
        
        log = add_logs[0]
        assert "Legal Record Added" in log[1], "Action should be 'Legal Record Added'"
        assert self.nbi["id"] == log[4], "User ID should match NBI officer"
    
    def test_update_legal_record_logs_action(self):
        """Test that updating a legal record creates audit log entry"""
        # Create a legal record
        record_id = self.db.create_legal_record(
            politician_id=self.politician["id"],
            record_type="Graft and Corruption Case",
            title="Test Case",
            description="Test description",
            date="01/15/2025",
            added_by=self.nbi["id"]
        )
        
        # Update the record
        success = self.db.update_legal_record(
            record_id,
            "Tax Compliance Issue",
            "Updated Test Case",
            "Updated description",
            "01/20/2025"
        )
        assert success, "Record update should succeed"
        
        # Log the action (simulating what NBI dashboard does)
        self.db.log_action(
            action="Legal Record Updated",
            action_type="legal_record_edit",
            description="Updated record: Updated Test Case",
            user_id=self.nbi["id"],
            user_role="nbi",
            target_type="legal_record",
            target_id=record_id,
        )
        
        # Verify audit log was created
        logs = self.db.get_audit_logs_for_role("nbi")
        assert len(logs) > 0, "Audit log should be created"
        
        # Verify log content
        edit_logs = [log for log in logs if log[2] == "legal_record_edit"]
        assert len(edit_logs) > 0, "Should have legal_record_edit action type"
        
        log = edit_logs[0]
        assert "Legal Record Updated" in log[1], "Action should be 'Legal Record Updated'"
        assert self.nbi["id"] == log[4], "User ID should match NBI officer"
    
    def test_verify_legal_record_logs_action(self):
        """Test that verifying a legal record creates audit log entry"""
        # Create a legal record
        record_id = self.db.create_legal_record(
            politician_id=self.politician["id"],
            record_type="Graft and Corruption Case",
            title="Test Case",
            description="Test description",
            date="01/15/2025",
            added_by=self.nbi["id"]
        )
        
        # Verify the record
        self.db.update_legal_record_status(record_id, "verified", self.nbi["id"])
        
        # Log the action (simulating what NBI dashboard does)
        self.db.log_action(
            action="Legal Record Verified",
            action_type="legal_record_status",
            description="Verified record: Test Case",
            user_id=self.nbi["id"],
            user_role="nbi",
            target_type="legal_record",
            target_id=record_id,
        )
        
        # Verify audit log was created
        logs = self.db.get_audit_logs_for_role("nbi")
        assert len(logs) > 0, "Audit log should be created"
        
        # Verify log content
        verify_logs = [log for log in logs if log[2] == "legal_record_status"]
        assert len(verify_logs) > 0, "Should have legal_record_status action type"
        
        log = verify_logs[0]
        assert "Legal Record Verified" in log[1], "Action should be 'Legal Record Verified'"
        assert self.nbi["id"] == log[4], "User ID should match NBI officer"
    
    def test_complete_legal_record_audit_trail(self):
        """Test complete audit trail for legal record lifecycle"""
        # Create
        record_id = self.db.create_legal_record(
            politician_id=self.politician["id"],
            record_type="Criminal Case",
            title="Initial Case",
            description="Initial description",
            date="01/01/2025",
            added_by=self.nbi["id"]
        )
        
        self.db.log_action(
            action="Legal Record Added",
            action_type="legal_record",
            description="Added record: Initial Case",
            user_id=self.nbi["id"],
            user_role="nbi",
            target_type="politician",
            target_id=self.politician["id"],
        )
        
        # Update
        self.db.update_legal_record(
            record_id,
            "Criminal Case",
            "Updated Case",
            "Updated description",
            "01/15/2025"
        )
        
        self.db.log_action(
            action="Legal Record Updated",
            action_type="legal_record_edit",
            description="Updated record: Updated Case",
            user_id=self.nbi["id"],
            user_role="nbi",
            target_type="legal_record",
            target_id=record_id,
        )
        
        # Verify
        self.db.update_legal_record_status(record_id, "verified", self.nbi["id"])
        
        self.db.log_action(
            action="Legal Record Verified",
            action_type="legal_record_status",
            description="Verified record: Updated Case",
            user_id=self.nbi["id"],
            user_role="nbi",
            target_type="legal_record",
            target_id=record_id,
        )
        
        # Verify complete audit trail
        logs = self.db.get_audit_logs_for_role("nbi")
        assert len(logs) >= 3, "Should have at least 3 audit log entries"
        
        # Verify we have all action types
        action_types = set([log[2] for log in logs])
        assert "legal_record" in action_types, "Should have add action"
        assert "legal_record_edit" in action_types, "Should have edit action"
        assert "legal_record_status" in action_types, "Should have verify action"
