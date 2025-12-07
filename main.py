import flet as ft
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.views.login_page import LoginPage
from app.views.signup_page import SignupPage
from app.views.home_page import HomePage
from app.views.settings_page import SettingsPage
from app.views.profile_page import ProfilePage
from app.views.comelec_dashboard import ComelecDashboard
from app.views.user_management import UserManagement
from app.views.election_results import ElectionResults
from app.views.voter_dashboard import VoterDashboard
from app.views.politician_profile import PoliticianProfile
from app.views.candidate_comparison import CandidateComparison
from app.views.voting_page import VotingPage
from app.views.politician_dashboard import PoliticianDashboard
from app.views.nbi_dashboard import NBIDashboard
from app.views.audit_log_page import AuditLogPage
from app.views.analytics_page import AnalyticsPage
from app.storage.database import init_demo_data
from app.state.session_manager import SessionManager
from app.security_logger import auth_logger


class HonestBallotApp:
    """Main application class for local voting app with session management"""
    
    def __init__(self):
        self.page = None
        self.current_session = None
        self.session_manager = SessionManager()
        self.db = None
    
    def main(self, page: ft.Page):
        """Main entry point for the Flet app"""
        self.page = page
        
        # Initialize database with demo data
        self.db = init_demo_data()
        
        # Page configuration
        page.title = "HonestBallot - Local Voting App"
        page.bgcolor = ft.Colors.GREY_100
        page.window.width = 1280
        page.window.height = 800
        page.window.min_width = 1024
        page.window.min_height = 600
        page.padding = 0
        page.spacing = 0
        
        # Store session manager in page data
        page.session.set("session_manager", self.session_manager)
        page.session.set("db", self.db)
        
        # Start with login page
        self.show_login_page()
    
    def show_login_page(self):
        """Show the login page"""
        self.page.clean()
        
        login_page = LoginPage(
            on_login=self.handle_login,
            on_create_account=self.show_signup_page,
            on_forgot_password=self.handle_forgot_password,
        )
        
        self.page.add(login_page)
        self.page.update()
    
    def show_signup_page(self):
        """Show the signup page"""
        self.page.clean()
        
        signup_page = SignupPage(
            on_google_signin=self.handle_google_signin,
            on_apple_signin=self.handle_apple_signin,
            on_create_account=self.handle_create_account,
            on_signin=self.show_login_page,
        )
        
        self.page.add(signup_page)
        self.page.update()
    
    def show_home_page(self):
        """Show the main home page - now voter dashboard"""
        self.page.clean()
        self.page.overlay.clear()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        # Check if voting is active
        voting_status = self.db.get_voting_status() if self.db else {"is_active": False}
        
        if voting_status.get("is_active", False):
            # Show voting page when voting is active
            voting_page = VotingPage(
                user_id=self.current_session["user_id"],
                username=self.current_session["username"],
                db=self.db,
                on_logout=self.handle_logout,
                on_view_profile=self.show_politician_profile,
                on_voting_stopped=self.show_home_page,  # Auto-refresh when voting stops
            )
            self.page.add(voting_page)
        else:
            # Show voter dashboard when not voting time
            dashboard = VoterDashboard(
                username=self.current_session["username"],
                db=self.db,
                on_logout=self.handle_logout,
                on_profile_view=self.show_politician_profile,
                on_compare=self.show_candidate_comparison,
                on_voting_started=self.show_home_page,  # Auto-refresh when voting starts
            )
            self.page.add(dashboard)
        
        self.page.update()
    
    def show_politician_profile(self, politician_id):
        """Show politician profile page"""
        self.page.clean()
        self.page.overlay.clear()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        profile_page = PoliticianProfile(
            politician_id=politician_id,
            db=self.db,
            on_back=self.show_home_page,
            on_logout=self.handle_logout,
            username=self.current_session["username"],
        )
        
        self.page.add(profile_page)
        self.page.update()
    
    def show_candidate_comparison(self, candidate1_id, candidate2_id):
        """Show candidate comparison page"""
        self.page.clean()
        self.page.overlay.clear()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        comparison_page = CandidateComparison(
            candidate1_id=candidate1_id,
            candidate2_id=candidate2_id,
            db=self.db,
            on_back=self.show_home_page,
            on_logout=self.handle_logout,
            username=self.current_session["username"],
        )
        
        self.page.add(comparison_page)
        self.page.update()
    
    def show_politician_dashboard(self):
        """Show the Politician dashboard"""
        self.page.clean()
        self.page.overlay.clear()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        dashboard = PoliticianDashboard(
            user_id=self.current_session["user_id"],
            username=self.current_session["username"],
            db=self.db,
            on_logout=self.handle_logout,
            on_audit_log=self.show_audit_log,
        )
        
        # Add file picker to page overlay
        self.page.overlay.append(dashboard.file_picker)
        
        self.page.add(dashboard)
        self.page.update()
    
    def show_comelec_dashboard(self):
        """Show the COMELEC dashboard"""
        self.page.clean()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        dashboard = ComelecDashboard(
            username=self.current_session["username"],
            db=self.db,
            on_logout=self.handle_logout,
            on_user_management=self.show_user_management,
            on_election_results=self.show_election_results,
            on_candidates=lambda: self.show_error_dialog("Info", "Verified Candidates - Coming Soon"),
            current_user_id=self.current_session["user_id"],
            on_audit_log=self.show_audit_log,
            on_analytics=self.show_analytics_page,
        )
        
        self.page.add(dashboard)
        self.page.update()
    
    def show_nbi_dashboard(self):
        """Show the NBI Officer dashboard"""
        self.page.clean()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        dashboard = NBIDashboard(
            username=self.current_session["username"],
            db=self.db,
            on_logout=self.handle_logout,
            current_user_id=self.current_session["user_id"],
            on_audit_log=self.show_audit_log,
        )
        
        self.page.add(dashboard)
        self.page.update()
    
    def show_audit_log(self):
        """Show the Audit Log page"""
        self.page.clean()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        # Determine which dashboard to go back to
        role = self.current_session["role"]
        if role == "comelec":
            on_back = self.show_comelec_dashboard
        elif role == "nbi":
            on_back = self.show_nbi_dashboard
        elif role == "politician":
            on_back = self.show_politician_dashboard
        else:
            on_back = self.show_home_page
        
        audit_page = AuditLogPage(
            username=self.current_session["username"],
            db=self.db,
            user_role=role,
            on_back=on_back,
            current_user_id=self.current_session["user_id"],
        )
        
        self.page.add(audit_page)
        self.page.update()
    
    def show_analytics_page(self):
        """Show the Analytics Dashboard page"""
        self.page.clean()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        analytics_page = AnalyticsPage(
            username=self.current_session["username"],
            db=self.db,
            user_role=self.current_session["role"],
            on_back=self.show_comelec_dashboard,
            on_logout=self.handle_logout,
        )
        
        self.page.add(analytics_page)
        self.page.update()
    
    def show_election_results(self):
        """Show the Election Results page"""
        self.page.clean()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        results_page = ElectionResults(
            username=self.current_session["username"],
            db=self.db,
            on_logout=self.handle_logout,
            on_back=self.show_comelec_dashboard,
        )
        
        self.page.add(results_page)
        self.page.update()
    
    def show_user_management(self):
        """Show the User Management page"""
        self.page.clean()
        # Clear any existing overlays
        self.page.overlay.clear()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        user_mgmt = UserManagement(
            username=self.current_session["username"],
            db=self.db,
            on_logout=self.handle_logout,
            on_back=self.show_comelec_dashboard,
        )
        
        # Add file picker to page overlay
        self.page.overlay.append(user_mgmt.file_picker)
        
        self.page.add(user_mgmt)
        self.page.update()
    
    def handle_login(self, username, password):
        """Handle login attempt with credential stuffing protection"""
        if not username or not password:
            self.show_error_dialog("Login Error", "Please enter both username and password.")
            return
        
        # Check if account is locked due to too many failed attempts
        identifier = username.lower()
        if self.db.is_account_locked(identifier):
            remaining_time = self.db.get_lockout_remaining_time(identifier)
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            self.show_error_dialog(
                "Account Locked", 
                f"Too many failed login attempts. Please try again in {minutes}m {seconds}s."
            )
            return
        
        # Verify credentials from database (try username first, then email)
        user = self.session_manager.db.verify_user_by_username(username, password)
        if not user:
            user = self.session_manager.db.verify_user(username, password)
        
        if user:
            # Record successful login and clear failed attempts
            self.db.record_login_attempt(identifier, success=True)
            self.db.clear_failed_attempts(identifier)
            
            # Create session
            session_token = self.session_manager.create_session(
                user["id"],
                user["username"],
                user["email"],
                user["role"]
            )
            
            # Store session
            self.current_session = {
                "token": session_token,
                "user_id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "role": user["role"]
            }
            
            # Log the login action to database
            self.db.log_action(
                action=f"User {user['username']} logged in",
                action_type="login",
                description=f"Successful login for {user['email']}",
                user_id=user["id"],
                user_role=user["role"],
            )
            
            # Log to security logger
            auth_logger.login_success(
                username=user["username"],
                user_id=user["id"],
                role=user["role"]
            )
            
            # Store in page session
            self.page.session.set("current_session", self.current_session)
            
            # Route based on role
            if user["role"] == "comelec":
                self.show_comelec_dashboard()
            elif user["role"] == "nbi":
                self.show_nbi_dashboard()
            elif user["role"] == "politician":
                self.show_politician_dashboard()
            else:
                self.show_home_page()
        else:
            # Record failed login attempt
            self.db.record_login_attempt(identifier, success=False)
            
            # Log the failed attempt to database
            self.db.log_action(
                action=f"Failed login attempt for {username}",
                action_type="login_failed",
                description=f"Invalid credentials provided",
                user_id=None,
                user_role=None,
            )
            
            # Check if account just got locked
            if self.db.is_account_locked(identifier):
                # Log account lockout to security logger
                auth_logger.account_locked(
                    username=username,
                    duration_minutes=self.db.LOCKOUT_DURATION_MINUTES
                )
                self.show_error_dialog(
                    "Account Locked", 
                    f"Too many failed attempts. Account locked for {self.db.LOCKOUT_DURATION_MINUTES} minutes."
                )
            else:
                attempts_remaining = self.db.MAX_LOGIN_ATTEMPTS - self.db.get_failed_attempts_count(identifier)
                # Log failed login to security logger
                auth_logger.login_failed(
                    username=username,
                    reason="Invalid credentials",
                    attempts_remaining=attempts_remaining
                )
                self.show_error_dialog(
                    "Login Failed", 
                    f"Invalid email or password. {attempts_remaining} attempts remaining."
                )
    
    def handle_create_account(self, username, email, password):
        """Handle create account"""
        if not username or not email or not password:
            self.show_error_dialog("Signup Error", "Please fill all fields.")
            return
        
        # Create user in database
        if self.session_manager.db.create_user(username, email, password, "voter"):
            # Log new account creation
            auth_logger.account_created(
                username=username,
                user_id=None,  # Will be set after login
                role="voter"
            )
            # Auto-login after signup
            self.handle_login(email, password)
        else:
            self.show_error_dialog("Signup Failed", "Email or username already exists.")
    
    def handle_google_signin(self):
        """Handle Google sign in"""
        self.show_error_dialog("Info", "Google Sign-in not available in local mode.")
    
    def handle_apple_signin(self):
        """Handle Apple sign in"""
        self.show_error_dialog("Info", "Apple Sign-in not available in local mode.")
    
    def handle_forgot_password(self):
        """Handle forgot password click"""
        self.show_error_dialog("Forgot Password", "Password reset functionality coming soon!")
    
    def handle_logout(self):
        """Handle logout"""
        if self.current_session:
            # Log the logout action to database
            self.db.log_action(
                action=f"User {self.current_session['username']} logged out",
                action_type="logout",
                description=f"User logged out",
                user_id=self.current_session["user_id"],
                user_role=self.current_session["role"],
            )
            
            # Log to security logger
            auth_logger.logout(
                username=self.current_session["username"],
                user_id=self.current_session["user_id"]
            )
            
            self.session_manager.end_session(self.current_session["token"])
        
        self.current_session = None
        self.page.session.set("current_session", None)
        self.show_login_page()
    
    def handle_settings(self):
        """Handle settings click - show settings page"""
        self.show_settings_page()
    
    def show_profile_page(self):
        """Show the profile page"""
        self.page.clean()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        profile_page = ProfilePage(
            username=self.current_session["username"],
            user_handle=f"@{self.current_session['username'].lower()}",
            on_logout=self.handle_logout,
            on_settings=self.handle_settings,
            on_home=self.show_home_page,
        )
        
        self.page.add(profile_page)
        self.page.update()
    
    def show_settings_page(self):
        """Show the settings page"""
        self.page.clean()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        settings_page = SettingsPage(
            username=self.current_session["username"],
            user_handle=f"@{self.current_session['username'].lower()}",
            on_save=lambda settings: self.handle_settings_save(settings),
            on_cancel=self.show_home_page,
            on_back=self.show_home_page,
            on_logout=self.handle_logout,
            on_profile=self.show_profile_page,
        )
        
        self.page.add(settings_page)
        self.page.update()
    
    def handle_settings_save(self, settings_data):
        """Handle saving settings and return to home"""
        print(f"Settings saved: {settings_data}")
        self.show_home_page()
    
    def show_error_dialog(self, title, message):
        """Show error dialog"""
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.close_dialog(dialog)),
            ],
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def close_dialog(self, dialog):
        """Close a dialog"""
        dialog.open = False
        self.page.update()


def main(page: ft.Page):
    """Main function to run the app"""
    app = HonestBallotApp()
    app.main(page)


if __name__ == "__main__":
    ft.app(target=main)
