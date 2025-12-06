import flet as ft
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.top_taskbar import TopTaskbar
from components.sidebar import Sidebar
from components.post_container import PostContainer
from components.right_sidebar import RightSidebar
from components.notification_dropdown import NotificationDropdown


class HomePage(ft.Container):
    """Main home page combining all components"""
    
    def __init__(self, username="EUTABLE", user_handle="@CUTIE_EUTABLE",
                 on_logout=None, on_settings=None, on_profile=None):
        super().__init__()
        self.username = username
        self.user_handle = user_handle
        self.on_logout = on_logout
        self.on_settings = on_settings
        self.on_profile_callback = on_profile
        
        # Create components
        self.top_taskbar = TopTaskbar(
            username=username,
            user_handle=user_handle,
            on_settings=self._handle_settings,
            on_location=self._handle_location,
            on_notifications=self._handle_notifications,
            on_search=self._handle_search,
        )
        
        self.sidebar = Sidebar(
            username=username,
            on_profile=self._handle_profile,
            on_find_friends=self._handle_find_friends,
            on_user_analytics=self._handle_analytics,
            on_settings=self._handle_settings,
            on_security=self._handle_security,
            on_logout=self._handle_logout,
        )
        
        self.post_container = PostContainer(
            on_post_submit=self._handle_post_submit,
        )
        
        self.right_sidebar = RightSidebar(
            on_follow=self._handle_follow,
            on_boost=self._handle_boost,
        )
        
        # Notification dropdown
        self.notification_dropdown = self.top_taskbar.get_notification_dropdown()
        
        # Build the UI
        self.content = self._build_ui()
        self.expand = True
        self.bgcolor = "#E1F5FE"  # Very light blue background
    
    def _build_ui(self):
        """Build the home page UI"""
        
        # Main content area (sidebar + posts + right sidebar) - UNDER the taskbar
        main_content = ft.Row(
            controls=[
                # Left sidebar
                self.sidebar,
                # Vertical divider
                ft.VerticalDivider(width=1, color=ft.Colors.GREY_300),
                # Center content (posts)
                ft.Container(
                    content=self.post_container,
                    expand=True,
                    padding=ft.padding.only(top=10),
                ),
                # Vertical divider
                ft.VerticalDivider(width=1, color=ft.Colors.GREY_300),
                # Right sidebar
                ft.Container(
                    content=self.right_sidebar,
                    width=280,
                    bgcolor=ft.Colors.WHITE,
                    padding=ft.padding.only(top=10, right=10),
                ),
            ],
            expand=True,
            spacing=0,
        )
        
        # Full layout with taskbar at TOP spanning full width
        full_layout = ft.Column(
            controls=[
                self.top_taskbar,
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                main_content,
            ],
            spacing=0,
            expand=True,
        )
        
        # Stack for overlaying notification dropdown
        main_stack = ft.Stack(
            controls=[
                full_layout,
                # Notification dropdown overlay
                ft.Container(
                    content=self.notification_dropdown,
                    right=20,
                    top=70,
                ),
                # File picker for post creation (needs to be in page overlay)
                self.post_container.post_creator.file_picker,
            ],
            expand=True,
        )
        
        return main_stack
    
    def _handle_settings(self):
        """Handle settings button click"""
        print("Settings clicked")
        if self.on_settings:
            self.on_settings()
    
    def _handle_location(self):
        """Handle location button click"""
        print("Location clicked")
    
    def _handle_notifications(self):
        """Handle notifications button click"""
        print("Notifications clicked")
    
    def _handle_search(self, query):
        """Handle search submission"""
        print(f"Search: {query}")
    
    def _handle_profile(self):
        """Handle profile click"""
        print("Profile clicked")
        if self.on_profile_callback:
            self.on_profile_callback()
    
    def _handle_find_friends(self):
        """Handle find friends click"""
        print("Find friends clicked")
    
    def _handle_analytics(self):
        """Handle analytics click"""
        print("Analytics clicked")
    
    def _handle_security(self):
        """Handle security click"""
        print("Security clicked")
    
    def _handle_logout(self):
        """Handle logout click"""
        print("Logout clicked")
        if self.on_logout:
            self.on_logout()
    
    def _handle_post_submit(self, content):
        """Handle post submission"""
        print(f"New post: {content}")
        # Post is already added by the post container
    
    def _handle_follow(self, user):
        """Handle follow button click"""
        print(f"Follow: {user}")
    
    def _handle_boost(self):
        """Handle boost button click"""
        print("Boost clicked")
