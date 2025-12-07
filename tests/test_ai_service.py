"""
Unit Tests for AI Service Module
Tests AI-powered analysis and recommendation features
"""

import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.ai_service import AIService, RecommendationEngine


class TestAIServiceThemeExtraction(unittest.TestCase):
    """Test cases for theme extraction from candidate biographies"""
    
    def setUp(self):
        """Set up AI service"""
        self.ai = AIService(db=None)
    
    def test_extract_education_theme(self):
        """Test extraction of education-related themes"""
        bio = "I am committed to improving education for all students. I support scholarships and better schools."
        themes = self.ai._extract_themes(bio)
        self.assertIn("Education", themes)
    
    def test_extract_healthcare_theme(self):
        """Test extraction of healthcare-related themes"""
        bio = "Healthcare is my priority. I will improve hospitals and medical services for everyone."
        themes = self.ai._extract_themes(bio)
        self.assertIn("Healthcare", themes)
    
    def test_extract_multiple_themes(self):
        """Test extraction of multiple themes"""
        bio = """
        As your leader, I will focus on:
        - Education reform and scholarships
        - Better healthcare and hospitals
        - Economic growth and job creation
        """
        themes = self.ai._extract_themes(bio)
        self.assertIn("Education", themes)
        self.assertIn("Healthcare", themes)
        self.assertIn("Economy", themes)
    
    def test_extract_no_themes(self):
        """Test with biography containing no matching themes"""
        bio = "I am a good person who loves my country."
        themes = self.ai._extract_themes(bio)
        self.assertEqual(len(themes), 0)
    
    def test_extract_themes_case_insensitive(self):
        """Test that theme extraction is case-insensitive"""
        bio = "EDUCATION is important. HEALTHCARE matters. ECONOMY needs work."
        themes = self.ai._extract_themes(bio)
        self.assertGreater(len(themes), 0)


class TestAIServiceSentimentAnalysis(unittest.TestCase):
    """Test cases for sentiment analysis"""
    
    def setUp(self):
        """Set up AI service"""
        self.ai = AIService(db=None)
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection"""
        bio = "I have achieved great success in my career. I led many successful reforms."
        sentiment = self.ai._analyze_sentiment(bio)
        self.assertGreater(sentiment, 0)
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection"""
        bio = "There were allegations and controversy. The project failed and was rejected."
        sentiment = self.ai._analyze_sentiment(bio)
        self.assertLess(sentiment, 0)
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment"""
        bio = "I was born in Manila. I have two children."
        sentiment = self.ai._analyze_sentiment(bio)
        self.assertEqual(sentiment, 0)
    
    def test_mixed_sentiment(self):
        """Test mixed positive and negative sentiment"""
        bio = "I achieved success but faced allegations. I led reforms but failed in some areas."
        sentiment = self.ai._analyze_sentiment(bio)
        # Should be relatively balanced (may lean slightly positive or negative)
        self.assertGreaterEqual(sentiment, -0.8)
        self.assertLessEqual(sentiment, 0.8)


class TestAIServiceCompatibilityScore(unittest.TestCase):
    """Test cases for voter-candidate compatibility scoring"""
    
    def setUp(self):
        """Set up AI service"""
        self.ai = AIService(db=None)
    
    def test_high_compatibility(self):
        """Test high compatibility when preferences match"""
        voter_prefs = ["education", "healthcare"]
        politician = {
            "id": 1,
            "biography": "I focus on education, schools, healthcare, and hospitals."
        }
        
        score, matches = self.ai.calculate_compatibility_score(voter_prefs, politician)
        self.assertGreater(score, 60)
        self.assertIn("education", matches)
        self.assertIn("healthcare", matches)
    
    def test_low_compatibility(self):
        """Test low compatibility when no preferences match"""
        voter_prefs = ["education", "healthcare"]
        politician = {
            "id": 1,
            "biography": "I love sports and entertainment."
        }
        
        score, matches = self.ai.calculate_compatibility_score(voter_prefs, politician)
        self.assertLessEqual(score, 60)
        self.assertEqual(len(matches), 0)
    
    def test_partial_compatibility(self):
        """Test partial compatibility"""
        voter_prefs = ["education", "healthcare", "economy"]
        politician = {
            "id": 1,
            "biography": "Education is my focus. I support students and schools."
        }
        
        score, matches = self.ai.calculate_compatibility_score(voter_prefs, politician)
        self.assertGreater(score, 50)
        self.assertIn("education", matches)
        self.assertNotIn("healthcare", matches)


class TestAIServiceCandidateSummary(unittest.TestCase):
    """Test cases for candidate summary generation"""
    
    def setUp(self):
        """Set up AI service"""
        self.ai = AIService(db=None)
    
    def test_generate_summary_with_party(self):
        """Test summary generation with party"""
        politician = {
            "full_name": "Juan Dela Cruz",
            "position": "Senator",
            "party": "Reform Party",
            "biography": "Dedicated to education reform and student welfare."
        }
        
        summary = self.ai.generate_candidate_summary(politician)
        self.assertIn("Juan Dela Cruz", summary)
        self.assertIn("Senator", summary)
        self.assertIn("Reform Party", summary)
    
    def test_generate_summary_independent(self):
        """Test summary generation for independent candidate"""
        politician = {
            "full_name": "Maria Santos",
            "position": "Mayor",
            "party": "Independent",
            "biography": "Healthcare advocate with hospital experience."
        }
        
        summary = self.ai.generate_candidate_summary(politician)
        self.assertIn("Maria Santos", summary)
        self.assertIn("Mayor", summary)
    
    def test_generate_summary_with_themes(self):
        """Test that summary includes key themes"""
        politician = {
            "full_name": "Test Candidate",
            "position": "Governor",
            "party": None,
            "biography": "Education expert. Healthcare champion. Economy specialist."
        }
        
        summary = self.ai.generate_candidate_summary(politician)
        self.assertIn("focus areas", summary.lower())


class TestAIServiceExperienceAssessment(unittest.TestCase):
    """Test cases for experience level assessment"""
    
    def setUp(self):
        """Set up AI service"""
        self.ai = AIService(db=None)
    
    def test_high_experience(self):
        """Test high experience detection"""
        bio = "A veteran politician with decades of service and extensive experience."
        exp = self.ai._assess_experience(bio)
        self.assertEqual(exp, "high")
    
    def test_medium_experience(self):
        """Test medium experience detection"""
        bio = "I have years of experience. I served as a former official."
        exp = self.ai._assess_experience(bio)
        self.assertEqual(exp, "medium")
    
    def test_emerging_experience(self):
        """Test emerging/new candidate detection"""
        bio = "A young and fresh face in politics. This is my first-time running."
        exp = self.ai._assess_experience(bio)
        self.assertEqual(exp, "emerging")
    
    def test_unknown_experience(self):
        """Test unknown experience when no indicators present"""
        bio = "I love my country and want to serve."
        exp = self.ai._assess_experience(bio)
        self.assertEqual(exp, "unknown")


class TestAIServiceStrengthIdentification(unittest.TestCase):
    """Test cases for strength identification"""
    
    def setUp(self):
        """Set up AI service"""
        self.ai = AIService(db=None)
    
    def test_leadership_strength(self):
        """Test leadership strength detection"""
        bio = "I led many initiatives and spearheaded major reforms."
        strengths = self.ai._identify_strengths(bio)
        self.assertIn("Leadership", strengths)
    
    def test_reform_strength(self):
        """Test reform-oriented strength detection"""
        bio = "Committed to reform and innovative solutions for change."
        strengths = self.ai._identify_strengths(bio)
        self.assertIn("Reform-oriented", strengths)
    
    def test_multiple_strengths(self):
        """Test detection of multiple strengths"""
        bio = "A community leader who led grassroots initiatives and policy reforms."
        strengths = self.ai._identify_strengths(bio)
        self.assertGreaterEqual(len(strengths), 2)


class TestRecommendationEngine(unittest.TestCase):
    """Test cases for recommendation engine"""
    
    def setUp(self):
        """Set up recommendation engine without database"""
        self.ai = AIService(db=None)
        self.engine = RecommendationEngine(db=None, ai_service=self.ai)
    
    def test_engine_initialization(self):
        """Test engine initializes correctly"""
        self.assertIsNotNone(self.engine)
        self.assertIsNotNone(self.engine.ai)  # Uses self.ai not self.ai_service
    
    def test_get_recommendations_no_db(self):
        """Test recommendations return empty list without database"""
        recs = self.engine.get_recommendations(["education"])
        self.assertEqual(recs, [])


if __name__ == "__main__":
    unittest.main()
