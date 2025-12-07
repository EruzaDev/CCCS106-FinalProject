"""
Unit Tests for Password Policy Module
Tests password validation, strength calculation, and policy enforcement
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.password_policy import PasswordPolicy


class TestPasswordValidation(unittest.TestCase):
    """Test cases for password validation"""
    
    def test_valid_password(self):
        """Test that a valid password passes all checks"""
        is_valid, errors = PasswordPolicy.validate("SecureP@ss123")
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_password_too_short(self):
        """Test that short passwords are rejected"""
        is_valid, errors = PasswordPolicy.validate("Aa1!")
        self.assertFalse(is_valid)
        self.assertTrue(any("at least" in e for e in errors))
    
    def test_password_no_uppercase(self):
        """Test that passwords without uppercase are rejected"""
        is_valid, errors = PasswordPolicy.validate("password123!")
        self.assertFalse(is_valid)
        self.assertTrue(any("uppercase" in e for e in errors))
    
    def test_password_no_lowercase(self):
        """Test that passwords without lowercase are rejected"""
        is_valid, errors = PasswordPolicy.validate("PASSWORD123!")
        self.assertFalse(is_valid)
        self.assertTrue(any("lowercase" in e for e in errors))
    
    def test_password_no_digit(self):
        """Test that passwords without digits are rejected"""
        is_valid, errors = PasswordPolicy.validate("Password!")
        self.assertFalse(is_valid)
        self.assertTrue(any("number" in e for e in errors))
    
    def test_password_no_special(self):
        """Test that passwords without special chars are rejected"""
        is_valid, errors = PasswordPolicy.validate("Password123")
        self.assertFalse(is_valid)
        self.assertTrue(any("special" in e for e in errors))
    
    def test_weak_password_rejected(self):
        """Test that common weak passwords are rejected"""
        # "password" is in the weak passwords list
        is_valid, errors = PasswordPolicy.validate("password")
        self.assertFalse(is_valid)
        self.assertTrue(any("common" in e.lower() or "weak" in e.lower() for e in errors))
    
    def test_password_contains_username(self):
        """Test that passwords containing username are rejected"""
        is_valid, errors = PasswordPolicy.validate("MyUsername123!", username="myusername")
        self.assertFalse(is_valid)
        self.assertTrue(any("username" in e for e in errors))
    
    def test_password_contains_email(self):
        """Test that passwords containing email name are rejected"""
        is_valid, errors = PasswordPolicy.validate("JohnDoe123!@#", email="johndoe@test.com")
        self.assertFalse(is_valid)
        self.assertTrue(any("email" in e for e in errors))


class TestPasswordStrength(unittest.TestCase):
    """Test cases for password strength calculation"""
    
    def test_empty_password_zero_strength(self):
        """Test that empty password has zero strength"""
        score = PasswordPolicy.get_strength("")
        self.assertEqual(score, 0)
    
    def test_weak_password_low_strength(self):
        """Test that weak passwords have low strength"""
        score = PasswordPolicy.get_strength("abc")
        self.assertLess(score, 30)
    
    def test_strong_password_high_strength(self):
        """Test that strong passwords have high strength"""
        score = PasswordPolicy.get_strength("V3ryStr0ng!P@ssw0rd#2024")
        self.assertGreater(score, 70)
    
    def test_strength_label_weak(self):
        """Test weak password label"""
        label, color = PasswordPolicy.get_strength_label("abc")
        self.assertEqual(label, "Weak")
    
    def test_strength_label_strong(self):
        """Test strong password label"""
        label, color = PasswordPolicy.get_strength_label("V3ryStr0ng!P@ss#2024")
        self.assertIn(label, ["Strong", "Very Strong"])
    
    def test_sequential_chars_penalty(self):
        """Test that sequential characters reduce strength"""
        score_with = PasswordPolicy.get_strength("abc123Pass!")
        score_without = PasswordPolicy.get_strength("xyzqwrPass!")
        # Sequential 'abc' and '123' should reduce score
        self.assertLessEqual(score_with, score_without)
    
    def test_repeated_chars_penalty(self):
        """Test that repeated characters reduce strength"""
        score_with = PasswordPolicy.get_strength("Paaass111!!!")
        score_without = PasswordPolicy.get_strength("Pabcde123!@#")
        self.assertLess(score_with, score_without)


class TestPasswordRequirements(unittest.TestCase):
    """Test password requirements text generation"""
    
    def test_requirements_list(self):
        """Test that requirements list is generated"""
        requirements = PasswordPolicy.get_requirements_text()
        self.assertIsInstance(requirements, list)
        self.assertGreater(len(requirements), 0)
    
    def test_requirements_include_length(self):
        """Test that length requirement is included"""
        requirements = PasswordPolicy.get_requirements_text()
        self.assertTrue(any("character" in r.lower() for r in requirements))


if __name__ == "__main__":
    unittest.main()
