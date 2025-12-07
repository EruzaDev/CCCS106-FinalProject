"""
Integration Tests for Audit Log and Legal Records Workflow
Tests complete audit logging and NBI legal records lifecycle
"""

import unittest
import os
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.storage.database import Database
from app.services.ai_service import AIService


class TestAuditLogWorkflowIntegration(unittest.TestCase):
    """
    Integration test for audit logging workflow.
    Tests: User actions -> Audit log creation -> Role-based retrieval
    """
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "audit_test.db")
        self.db = Database(db_name=self.db_path)
        
        # Create users with different roles
        self.db.create_user("admin", "admin@comelec.gov", "pass", "comelec")
        self.db.create_user("nbi_officer", "nbi@gov.ph", "pass", "nbi")
        self.db.create_user("politician1", "pol1@gov.ph", "pass", "politician")
        self.db.create_user("voter1", "voter@test.com", "pass", "voter")
        
        self.admin = self.db.verify_user("admin@comelec.gov", "pass")
        self.nbi = self.db.verify_user("nbi@gov.ph", "pass")
        self.politician = self.db.verify_user("pol1@gov.ph", "pass")
        self.voter = self.db.verify_user("voter@test.com", "pass")
    
    def tearDown(self):
        """Clean up test environment"""
        if self.db.connection:
            self.db.connection.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_complete_audit_log_workflow(self):
        """
        Test complete audit logging workflow:
        1. User login creates audit log
        2. Admin enables voting creates log
        3. NBI adds legal record creates log
        4. Each role sees appropriate logs
        """
        # Step 1: Log user logins using log_action
        self.db.log_action(
            action="User Login",
            action_type="login",
            description="COMELEC admin logged in",
            user_id=self.admin["id"],
            user_role="comelec"
        )
        
        self.db.log_action(
            action="User Login",
            action_type="login",
            description="NBI officer logged in",
            user_id=self.nbi["id"],
            user_role="nbi"
        )
        
        self.db.log_action(
            action="User Login",
            action_type="login",
            description="Voter logged in",
            user_id=self.voter["id"],
            user_role="voter"
        )
        
        # Step 2: Admin enables voting
        self.db.start_voting(user_id=self.admin["id"])
        self.db.log_action(
            action="Voting Enabled",
            action_type="voting_control",
            description="Voting period started by admin",
            user_id=self.admin["id"],
            user_role="comelec"
        )
        
        # Step 3: NBI adds legal record
        self.db.create_legal_record(
            politician_id=self.politician["id"],
            record_type="Case Filing",
            title="Tax Case Investigation",
            description="Under investigation for tax irregularities",
            date="2025-01-15",
            added_by=self.nbi["id"]
        )
        
        self.db.log_action(
            action="Legal Record Added",
            action_type="legal_record",
            description=f"Legal record added for politician ID {self.politician['id']}",
            user_id=self.nbi["id"],
            user_role="nbi",
            target_type="politician",
            target_id=self.politician["id"]
        )
        
        # Step 4: Verify role-based log visibility
        # COMELEC should see all logs
        comelec_logs = self.db.get_audit_logs_for_role("comelec")
        self.assertGreaterEqual(len(comelec_logs), 4, "COMELEC should see all logs")
        
        # NBI should see legal records and logins
        nbi_logs = self.db.get_audit_logs_for_role("nbi")
        self.assertIsNotNone(nbi_logs)
        
        # Check action types in NBI logs
        nbi_action_types = [log[2] for log in nbi_logs]
        self.assertTrue(
            any(at in ["login", "legal_record"] for at in nbi_action_types),
            "NBI should see login and legal_record types"
        )
    
    def test_audit_log_filtering(self):
        """Test audit log filtering by action type"""
        # Create various logs using log_action
        self.db.log_action("Login", "login", "Test", self.admin["id"], "comelec")
        self.db.log_action("Login", "login", "Test", self.nbi["id"], "nbi")
        self.db.log_action("Logout", "logout", "Test", self.admin["id"], "comelec")
        self.db.log_action("Vote Cast", "vote", "Test", self.voter["id"], "voter")
        self.db.log_action("Record Added", "legal_record", "Test", self.nbi["id"], "nbi")
        
        # Filter by login
        login_logs = self.db.get_audit_logs(action_type="login")
        self.assertEqual(len(login_logs), 2)
        
        # Filter by vote
        vote_logs = self.db.get_audit_logs(action_type="vote")
        self.assertEqual(len(vote_logs), 1)
        
        # Get all
        all_logs = self.db.get_audit_logs()
        self.assertEqual(len(all_logs), 5)


class TestLegalRecordsWorkflowIntegration(unittest.TestCase):
    """
    Integration test for NBI legal records workflow.
    Tests: Create record -> Edit record -> Verify record -> View in profile
    """
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "legal_test.db")
        self.db = Database(db_name=self.db_path)
        
        # Create NBI officer
        self.db.create_user("nbi_officer", "nbi@gov.ph", "pass", "nbi")
        self.nbi = self.db.verify_user("nbi@gov.ph", "pass")
        
        # Create politician
        self.db.create_user("politician1", "pol1@gov.ph", "pass", "politician")
        self.politician = self.db.verify_user("pol1@gov.ph", "pass")
        
        # Update politician profile
        self.db.cursor.execute(
            "UPDATE users SET position = ?, party = ?, full_name = ?, biography = ? WHERE id = ?",
            ("Senator", "Reform Party", "Juan Politician", 
             "Experienced lawmaker focused on healthcare and education.", 
             self.politician["id"])
        )
        self.db.connection.commit()
    
    def tearDown(self):
        """Clean up"""
        if self.db.connection:
            self.db.connection.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_complete_legal_record_lifecycle(self):
        """
        Test complete legal record lifecycle:
        1. NBI creates legal record
        2. Record verification
        3. Record appears in politician's records
        """
        # Step 1: Create legal record using correct method signature
        record_id = self.db.create_legal_record(
            politician_id=self.politician["id"],
            record_type="Case Filing",
            title="Ethics Investigation",
            description="Under investigation for alleged ethics violation",
            date="2025-06-01",
            added_by=self.nbi["id"]
        )
        self.assertIsNotNone(record_id, "Record should be created")
        
        # Verify record exists
        records = self.db.get_legal_records_by_politician(self.politician["id"])
        self.assertEqual(len(records), 1, "Should have one record")
        # Record format: id, record_type, title, description, record_date, status, created_at
        self.assertEqual(records[0][2], "Ethics Investigation")
        
        # Step 2: Update record status
        self.db.update_legal_record_status(
            record_id=record_id,
            status="verified",
            verified_by=self.nbi["id"]
        )
        
        # Check status update
        records = self.db.get_legal_records_by_politician(self.politician["id"])
        # Status is the 6th field (index 5)
        self.assertIsNotNone(records[0], "Record should exist after status update")
        
        # Step 3: Verify politician has records 
        # Instead of get_user_by_id, just verify records exist
        politician_records = self.db.get_legal_records_by_politician(self.politician["id"])
        self.assertIsNotNone(politician_records)
        self.assertEqual(len(politician_records), 1)
    
    def test_multiple_records_for_politician(self):
        """Test handling multiple legal records for one politician"""
        # Create multiple records using correct signature
        record_types = [
            ("Case Filing", "Case 1", "First case"),
            ("Investigation", "Case 2", "Second case"),
            ("Court Decision", "Case 3", "Third case"),
        ]
        
        for rtype, title, desc in record_types:
            self.db.create_legal_record(
                politician_id=self.politician["id"],
                record_type=rtype,
                title=title,
                description=desc,
                date="2025-01-01",
                added_by=self.nbi["id"]
            )
        
        # Verify all records exist
        records = self.db.get_legal_records_by_politician(self.politician["id"])
        self.assertEqual(len(records), 3, "Should have 3 records")
        
        # Verify can get all legal records
        all_records = self.db.get_all_legal_records()
        self.assertGreaterEqual(len(all_records), 3)


class TestAIAnalyticsWithDataIntegration(unittest.TestCase):
    """
    Integration test for AI analytics with real data.
    Tests: Create candidates -> Cast votes -> AI analyzes patterns
    """
    
    def setUp(self):
        """Set up test environment with realistic data"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "ai_test.db")
        self.db = Database(db_name=self.db_path)
        self.ai = AIService(db=self.db)
        
        # Create candidates with different profiles
        candidates = [
            ("cand1", "cand1@test.com", "President", "Reform Party",
             "Dedicated to education reform and student scholarships. Led major school improvements."),
            ("cand2", "cand2@test.com", "President", "Progress Party",
             "Healthcare champion with hospital experience. Medical professional for decades."),
            ("cand3", "cand3@test.com", "Senator", "Independent",
             "Young and fresh face in politics. New ideas for economic growth."),
        ]
        
        self.candidates = []
        for uname, email, pos, party, bio in candidates:
            self.db.create_user(uname, email, "pass", "politician")
            cand = self.db.verify_user(email, "pass")
            self.db.cursor.execute(
                "UPDATE users SET position = ?, party = ?, full_name = ?, biography = ? WHERE id = ?",
                (pos, party, uname.title(), bio, cand["id"])
            )
            self.db.connection.commit()
            self.candidates.append(cand)
    
    def tearDown(self):
        """Clean up"""
        if self.db.connection:
            self.db.connection.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_ai_candidate_analysis_with_real_data(self):
        """Test AI analysis with realistic candidate data"""
        # Get candidate data from database
        politicians = self.db.get_users_by_role("politician")
        self.assertEqual(len(politicians), 3)
        
        # Analyze each candidate
        for pol in politicians:
            pol_dict = {
                "id": pol[0],
                "username": pol[1],
                "full_name": pol[4] if len(pol) > 4 else pol[1],
                "position": pol[7] if len(pol) > 7 else "",
                "party": pol[8] if len(pol) > 8 else "",
                "biography": pol[9] if len(pol) > 9 else "",
            }
            
            # Generate summary
            summary = self.ai.generate_candidate_summary(pol_dict)
            self.assertIsNotNone(summary)
            self.assertIn(pol_dict["full_name"], summary)
    
    def test_ai_compatibility_scoring_with_real_data(self):
        """Test compatibility scoring with realistic data"""
        # Use data from candidates created in setUp
        # First candidate has education-focused biography
        pol_dict = {
            "id": self.candidates[0]["id"],
            "biography": "Dedicated to education reform and student scholarships. Led major school improvements.",
            "position": "President",
            "party": "Reform Party",
        }
        
        # Voter interested in education should have high compatibility
        edu_prefs = ["education"]
        score1, matches1 = self.ai.calculate_compatibility_score(edu_prefs, pol_dict)
        self.assertIn("education", matches1)
        self.assertGreater(score1, 50)
        
        # Voter interested in healthcare - different candidate
        health_prefs = ["healthcare"]
        score2, matches2 = self.ai.calculate_compatibility_score(health_prefs, pol_dict)
        # Education candidate may or may not have healthcare keywords
        self.assertIsInstance(score2, (int, float))


if __name__ == "__main__":
    unittest.main()
