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


class EutableApp:
    """Main application class managing page routing"""
    
    def __init__(self):
        self.page = None
        self.current_user = None
    
    def main(self, page: ft.Page):
        """Main entry point for the Flet app"""
        self.page = page
        
        # Page configuration
        page.title = "EUTABLE - Research, Decide, Act"
        page.bgcolor = ft.Colors.GREY_100
        page.window.width = 1280
        page.window.height = 800
        page.window.min_width = 1024
        page.window.min_height = 600
        page.padding = 0
        page.spacing = 0
        
        # Start with signup page
        self.show_signup_page()
    
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
    
    def show_home_page(self, username="EUTABLE", user_handle="@CUTIE_EUTABLE"):
        """Show the main home page"""
        self.page.clean()
        
        home_page = HomePage(
            username=username,
            user_handle=user_handle,
            on_logout=self.handle_logout,
            on_settings=self.handle_settings,
            on_profile=lambda: self.show_profile_page(username, user_handle),
        )
        
        self.page.add(home_page)
        self.page.update()
    
    def handle_login(self, email, password):
        """Handle login attempt"""
        # For demo purposes, accept any login
        if email and password:
            self.current_user = {
                "email": email,
                "username": email.split("@")[0].upper() if "@" in email else email.upper(),
                "handle": f"@{email.split('@')[0]}" if "@" in email else f"@{email}",
            }
            self.show_home_page(
                username=self.current_user["username"],
                user_handle=self.current_user["handle"],
            )
        else:
            # Show error dialog
            dialog = ft.AlertDialog(
                title=ft.Text("Login Error"),
                content=ft.Text("Please enter both email and password."),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: self.close_dialog(dialog)),
                ],
            )
            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()
    
    def handle_google_signin(self):
        """Handle Google sign in"""
        # For demo, go directly to home
        self.current_user = {
            "username": "GOOGLE_USER",
            "handle": "@google_user",
        }
        self.show_home_page(
            username=self.current_user["username"],
            user_handle=self.current_user["handle"],
        )
    
    def handle_apple_signin(self):
        """Handle Apple sign in"""
        # For demo, go directly to home
        self.current_user = {
            "username": "APPLE_USER",
            "handle": "@apple_user",
        }
        self.show_home_page(
            username=self.current_user["username"],
            user_handle=self.current_user["handle"],
        )
    
    def handle_create_account(self):
        """Handle create account click"""
        # For demo, go to login page
        self.show_login_page()
    
    def handle_forgot_password(self):
        """Handle forgot password click"""
        dialog = ft.AlertDialog(
            title=ft.Text("Forgot Password"),
            content=ft.Text("Password reset functionality coming soon!"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.close_dialog(dialog)),
            ],
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def handle_logout(self):
        """Handle logout"""
        self.current_user = None
        self.show_signup_page()
    
    def handle_settings(self):
        """Handle settings click - show settings page"""
        self.show_settings_page()
    
    def show_profile_page(self, username="EUTABLE", user_handle="@CUTIE_EUTABLE"):
        """Show the profile page"""
        self.page.clean()
        
        profile_page = ProfilePage(
            username=username,
            user_handle=user_handle,
            on_logout=self.handle_logout,
            on_settings=lambda: self.show_settings_page(),
            on_home=lambda: self.show_home_page(username, user_handle),
        )
        
        self.page.add(profile_page)
        self.page.update()
    
    def show_settings_page(self):
        """Show the settings page"""
        self.page.clean()
        
        # Get current user info
        username = self.current_user.get("username", "EUTABLE") if self.current_user else "EUTABLE"
        user_handle = self.current_user.get("handle", "@CUTIE_EUTABLE") if self.current_user else "@CUTIE_EUTABLE"
        
        settings_page = SettingsPage(
            username=username,
            user_handle=user_handle,
            on_save=lambda settings: self.handle_settings_save(settings, username, user_handle),
            on_cancel=lambda: self.show_home_page(username, user_handle),
            on_back=lambda: self.show_home_page(username, user_handle),
            on_logout=self.handle_logout,
            on_profile=lambda: self.show_profile_page(username, user_handle),
        )
        
        self.page.add(settings_page)
        self.page.update()
    
    def handle_settings_save(self, settings_data, username, user_handle):
        """Handle saving settings and return to home"""
        print(f"Settings saved: {settings_data}")
        # TODO: Apply theme/settings changes here
        self.show_home_page(username, user_handle)
    
    def close_dialog(self, dialog):
        """Close a dialog"""
        dialog.open = False
        self.page.update()


def main(page: ft.Page):
    """Main function to run the app"""
    app = EutableApp()
    app.main(page)


if __name__ == "__main__":
    ft.app(target=main)
