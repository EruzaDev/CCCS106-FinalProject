import flet as ft
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.home_page import HomePage
from pages.settings_page import SettingsPage
from pages.profile_page import ProfilePage
from models.database import init_demo_data
from models.session_manager import SessionManager


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
        """Show the main home page"""
        self.page.clean()
        
        if not self.current_session:
            self.show_login_page()
            return
        
        home_page = HomePage(
            username=self.current_session["username"],
            user_handle=f"@{self.current_session['username'].lower()}",
            on_logout=self.handle_logout,
            on_settings=self.handle_settings,
            on_profile=self.show_profile_page,
        )
        
        self.page.add(home_page)
        self.page.update()
    
    def handle_login(self, username, password):
        """Handle login attempt"""
        if not username or not password:
            self.show_error_dialog("Login Error", "Please enter both username and password.")
            return
        
        # Verify credentials from database (try username first, then email)
        user = self.session_manager.db.verify_user_by_username(username, password)
        if not user:
            user = self.session_manager.db.verify_user(username, password)
        
        if user:
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
            
            # Store in page session
            self.page.session.set("current_session", self.current_session)
            
            self.show_home_page()
        else:
            self.show_error_dialog("Login Failed", "Invalid email or password.")
    
    def handle_create_account(self, username, email, password):
        """Handle create account"""
        if not username or not email or not password:
            self.show_error_dialog("Signup Error", "Please fill all fields.")
            return
        
        # Create user in database
        if self.session_manager.db.create_user(username, email, password, "voter"):
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
