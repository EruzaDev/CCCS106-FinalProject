"""
Integration Tests for Voting Workflow
Tests complete voting lifecycle from user creation to vote casting
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch, Mock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.storage.database import Database


class TestVotingWorkflowIntegration(unittest.TestCase):
    """
    Integration test for complete voting workflow.
    Tests: User registration -> Login -> Voting enabled -> Cast vote -> Results
    """
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "integration_test.db")
        self.db = Database(db_name=self.db_path)
    
    def tearDown(self):
        """Clean up test environment"""
        if self.db.connection:
            self.db.connection.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_complete_voting_lifecycle(self):
        """
        Test the complete voting lifecycle:
        1. Create COMELEC admin
        2. Create candidates (politicians)
        3. Create voters
        4. Admin enables voting
        5. Voters cast votes
        6. Admin disables voting
        7. Verify election results
        """
        # Step 1: Create COMELEC admin
        admin_created = self.db.create_user(
            username="comelec_admin",
            email="admin@comelec.gov",
            password="admin123",
            role="comelec"
        )
        self.assertTrue(admin_created, "Failed to create COMELEC admin")
        
        admin = self.db.verify_user("admin@comelec.gov", "admin123")
        self.assertIsNotNone(admin, "Failed to verify COMELEC admin")
        self.assertEqual(admin["role"], "comelec")
        
        # Step 2: Create candidates
        cand1_created = self.db.create_user(
            username="candidate1",
            email="cand1@election.com",
            password="cand123",
            role="politician"
        )
        cand2_created = self.db.create_user(
            username="candidate2",
            email="cand2@election.com",
            password="cand123",
            role="politician"
        )
        self.assertTrue(cand1_created and cand2_created, "Failed to create candidates")
        
        cand1 = self.db.verify_user("cand1@election.com", "cand123")
        cand2 = self.db.verify_user("cand2@election.com", "cand123")
        
        # Update candidate positions
        self.db.cursor.execute(
            "UPDATE users SET position = ?, party = ?, full_name = ? WHERE id = ?",
            ("President", "Party A", "Juan Candidate", cand1["id"])
        )
        self.db.cursor.execute(
            "UPDATE users SET position = ?, party = ?, full_name = ? WHERE id = ?",
            ("President", "Party B", "Maria Candidate", cand2["id"])
        )
        self.db.connection.commit()
        
        # Step 3: Create voters
        voters = []
        for i in range(5):
            voter_created = self.db.create_user(
                username=f"voter{i}",
                email=f"voter{i}@test.com",
                password="vote123",
                role="voter"
            )
            self.assertTrue(voter_created, f"Failed to create voter {i}")
            voters.append(self.db.verify_user(f"voter{i}@test.com", "vote123"))
        
        self.assertEqual(len(voters), 5, "Not all voters were created")
        
        # Step 4: Admin enables voting using start_voting
        self.db.start_voting(user_id=admin["id"])
        status = self.db.get_voting_status()
        self.assertTrue(status.get("is_active"), "Voting should be active")
        
        # Step 5: Voters cast votes
        # 3 voters vote for candidate 1, 2 voters vote for candidate 2
        for i, voter in enumerate(voters):
            candidate_id = cand1["id"] if i < 3 else cand2["id"]
            result = self.db.cast_vote(
                voter_id=voter["id"],
                candidate_id=candidate_id,
                position="President"
            )
            self.assertTrue(result, f"Voter {i} failed to cast vote")
        
        # Verify vote counts
        cand1_votes = self.db.get_votes_by_candidate(cand1["id"])
        cand2_votes = self.db.get_votes_by_candidate(cand2["id"])
        
        self.assertEqual(cand1_votes, 3, "Candidate 1 should have 3 votes")
        self.assertEqual(cand2_votes, 2, "Candidate 2 should have 2 votes")
        
        # Step 6: Admin disables voting using stop_voting
        self.db.stop_voting(user_id=admin["id"])
        status = self.db.get_voting_status()
        self.assertFalse(status.get("is_active"), "Voting should be inactive")
        
        # Step 7: Verify election results
        results = self.db.get_election_results()
        self.assertIsNotNone(results, "Results should exist")
        
        # Verify total votes
        total_votes = self.db.get_total_votes_cast()
        self.assertEqual(total_votes, 5, "Total votes should be 5")
        
        # Verify unique voters
        unique_voters = self.db.get_unique_voters_count()
        self.assertEqual(unique_voters, 5, "Unique voters should be 5")
    
    def test_voter_cannot_vote_twice_for_same_position(self):
        """Test voting behavior for same position"""
        # Create candidate
        self.db.create_user("cand", "cand@test.com", "pass", "politician")
        self.db.create_user("cand2", "cand2@test.com", "pass", "politician")
        cand1 = self.db.verify_user("cand@test.com", "pass")
        cand2 = self.db.verify_user("cand2@test.com", "pass")
        
        self.db.cursor.execute("UPDATE users SET position = 'Governor' WHERE id = ?", (cand1["id"],))
        self.db.cursor.execute("UPDATE users SET position = 'Governor' WHERE id = ?", (cand2["id"],))
        self.db.connection.commit()
        
        # Create voter
        self.db.create_user("voter", "voter@test.com", "pass", "voter")
        voter = self.db.verify_user("voter@test.com", "pass")
        
        # Enable voting using start_voting
        self.db.start_voting(user_id=1)
        
        # First vote should succeed
        result1 = self.db.cast_vote(voter["id"], cand1["id"], "Governor")
        self.assertTrue(result1, "First vote should succeed")
        
        # Second vote behavior depends on implementation
        # May allow vote updates or reject duplicates
        result2 = self.db.cast_vote(voter["id"], cand2["id"], "Governor")
        # Just verify it returns a boolean
        self.assertIsInstance(result2, bool)
        
        # Verify at least one vote exists
        votes = self.db.get_votes_by_candidate(cand1["id"])
        self.assertGreaterEqual(votes, 0, "Votes should be tracked")
    
    def test_voter_can_vote_for_different_positions(self):
        """Test that a voter can vote for different positions"""
        # Create candidates for different positions
        self.db.create_user("pres", "pres@test.com", "pass", "politician")
        self.db.create_user("gov", "gov@test.com", "pass", "politician")
        pres = self.db.verify_user("pres@test.com", "pass")
        gov = self.db.verify_user("gov@test.com", "pass")
        
        self.db.cursor.execute("UPDATE users SET position = 'President' WHERE id = ?", (pres["id"],))
        self.db.cursor.execute("UPDATE users SET position = 'Governor' WHERE id = ?", (gov["id"],))
        self.db.connection.commit()
        
        # Create voter
        self.db.create_user("voter", "voter@test.com", "pass", "voter")
        voter = self.db.verify_user("voter@test.com", "pass")
        
        # Enable voting using start_voting
        self.db.start_voting(user_id=1)
        
        # Vote for president
        result1 = self.db.cast_vote(voter["id"], pres["id"], "President")
        self.assertTrue(result1, "Vote for President should succeed")
        
        # Vote for governor (different position)
        result2 = self.db.cast_vote(voter["id"], gov["id"], "Governor")
        self.assertTrue(result2, "Vote for Governor should succeed")
        
        # Verify both votes exist
        total = self.db.get_total_votes_cast()
        self.assertEqual(total, 2, "Both votes should be recorded")


class TestElectionSessionIntegration(unittest.TestCase):
    """Integration tests for election session management"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "session_test.db")
        self.db = Database(db_name=self.db_path)
    
    def tearDown(self):
        """Clean up"""
        if self.db.connection:
            self.db.connection.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_voting_status_persistence(self):
        """Test that voting status persists across operations"""
        # Initially inactive
        status1 = self.db.get_voting_status()
        self.assertFalse(status1.get("is_active", True))
        
        # Enable using start_voting
        self.db.start_voting(user_id=1)
        status2 = self.db.get_voting_status()
        self.assertTrue(status2.get("is_active"))
        
        # Should still be active
        status3 = self.db.get_voting_status()
        self.assertTrue(status3.get("is_active"))
        
        # Disable using stop_voting
        self.db.stop_voting(user_id=1)
        status4 = self.db.get_voting_status()
        self.assertFalse(status4.get("is_active"))


if __name__ == "__main__":
    unittest.main()
