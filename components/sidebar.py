import flet as ft


class Sidebar(ft.Container):
    """Left sidebar with profile, explore panel, and settings sections"""
    
    def __init__(self, username="EUTABLE", avatar_url=None,
                 on_profile=None, on_find_friends=None, on_user_analytics=None,
                 on_settings=None, on_security=None, on_logout=None):
        super().__init__()
        self.username = username
        self.avatar_url = avatar_url
        self.on_profile = on_profile
        self.on_find_friends = on_find_friends
        self.on_user_analytics = on_user_analytics
        self.on_settings = on_settings
        self.on_security = on_security
        self.on_logout = on_logout
        
        # Track active item
        self.active_item = "profile"
        
        # Build the UI
        self.content = self._build_ui()
        self.width = 200
        self.padding = ft.padding.all(15)
        self.bgcolor = ft.Colors.WHITE
    
    def _build_ui(self):
        """Build the sidebar UI"""
        
        # Profile avatar section with logo
        avatar_section = ft.Column(
            controls=[
                # Large avatar with logo
                ft.Container(
                    content=ft.Container(
                        content=ft.Image(
                            src="assets/fd875946-c220-48f7-a5db-e8e1d3e0a2a0.jpg",
                            width=100,
                            height=100,
                            fit=ft.ImageFit.COVER,
                        ),
                        width=100,
                        height=100,
                        border_radius=50,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    ),
                    border=ft.border.all(3, ft.Colors.BLUE_400),
                    border_radius=55,
                    padding=5,
                ),
                ft.Container(height=10),
                ft.Text(
                    self.username,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Explore panel section
        explore_section = ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Text(
                    "Explore panel",
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.BLUE_400,
                ),
                ft.Container(height=10),
                self._build_nav_item(
                    icon=ft.Icons.PERSON_OUTLINE,
                    text="Profile",
                    key="profile",
                    on_click=self.on_profile,
                ),
                self._build_nav_item(
                    icon=ft.Icons.PEOPLE_OUTLINE,
                    text="Find friends",
                    key="find_friends",
                    on_click=self.on_find_friends,
                ),
                self._build_nav_item(
                    icon=ft.Icons.ANALYTICS_OUTLINED,
                    text="User analytics",
                    key="analytics",
                    on_click=self.on_user_analytics,
                ),
            ],
            spacing=5,
        )
        
        # Settings section
        settings_section = ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Text(
                    "Settings",
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.BLUE_400,
                ),
                ft.Container(height=10),
                self._build_nav_item(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    text="Settings",
                    key="settings",
                    on_click=self.on_settings,
                ),
                self._build_nav_item(
                    icon=ft.Icons.SECURITY_OUTLINED,
                    text="Security data",
                    key="security",
                    on_click=self.on_security,
                ),
                ft.Container(height=10),
                self._build_nav_item(
                    icon=ft.Icons.LOGOUT,
                    text="Log out",
                    key="logout",
                    on_click=self.on_logout,
                    is_logout=True,
                ),
            ],
            spacing=5,
        )
        
        return ft.Column(
            controls=[
                avatar_section,
                explore_section,
                settings_section,
                ft.Container(expand=True),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def _build_nav_item(self, icon, text, key, on_click=None, is_logout=False):
        """Build a navigation item"""
        is_active = self.active_item == key
        
        text_color = ft.Colors.RED_400 if is_logout else (
            ft.Colors.BLUE_400 if is_active else ft.Colors.GREY_700
        )
        icon_color = ft.Colors.RED_400 if is_logout else (
            ft.Colors.BLUE_400 if is_active else ft.Colors.GREY_600
        )
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, size=20, color=icon_color),
                    ft.Container(width=10),
                    ft.Text(
                        text,
                        size=13,
                        color=text_color,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
            padding=ft.padding.symmetric(vertical=8, horizontal=10),
            border_radius=8,
            bgcolor=ft.Colors.BLUE_50 if is_active else ft.Colors.TRANSPARENT,
            ink=True,
            on_click=lambda e, k=key, cb=on_click: self._handle_nav_click(k, cb),
        )
    
    def _handle_nav_click(self, key, callback):
        """Handle navigation item click"""
        if key != "logout":
            self.active_item = key
            self.content = self._build_ui()
            self.update()
        
        if callback:
            callback()
    
    def set_active(self, key):
        """Set the active navigation item"""
        self.active_item = key
        self.content = self._build_ui()
        self.update()
