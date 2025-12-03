import flet as ft
from .notification_dropdown import NotificationDropdown


class TopTaskbar(ft.Container):
    """Top taskbar with search, user info, settings, location, and notifications"""
    
    def __init__(self, username="EUTABLE", user_handle="@CUTIE_EUTABLE",
                 on_settings=None, on_location=None, on_notifications=None,
                 on_search=None):
        super().__init__()
        self.username = username
        self.user_handle = user_handle
        self.on_settings = on_settings
        self.on_location = on_location
        self.on_notifications = on_notifications
        self.on_search = on_search
        
        # Create notification dropdown
        self.notification_dropdown = NotificationDropdown(
            on_close=self._close_notifications,
        )
        
        # Search field
        self.search_field = ft.TextField(
            hint_text="Search for post here...",
            border_radius=25,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.BLUE_400,
            bgcolor=ft.Colors.WHITE,
            height=45,
            text_size=14,
            prefix_icon=ft.Icons.SEARCH,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
            expand=True,
            on_submit=self._handle_search,
        )
        
        # Build the UI
        self.content = self._build_ui()
        self.bgcolor = "#B3E5FC"  # Light cyan blue like in screenshot
        self.padding = ft.padding.symmetric(horizontal=20, vertical=10)
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=5,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        )
    
    def _build_ui(self):
        """Build the top taskbar UI"""
        
        # Logo from assets
        logo = ft.Container(
            content=ft.Image(
                src="assets/fd875946-c220-48f7-a5db-e8e1d3e0a2a0.jpg",
                width=50,
                height=50,
                fit=ft.ImageFit.CONTAIN,
            ),
            width=50,
            height=50,
            border_radius=25,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )
        
        # Search bar container
        search_container = ft.Container(
            content=self.search_field,
            width=350,
        )
        
        # User info section
        user_info = ft.Row(
            controls=[
                # User avatar
                ft.Container(
                    content=ft.Text(
                        self.username[0],
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    width=40,
                    height=40,
                    bgcolor=ft.Colors.BLUE_400,
                    border_radius=20,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            self.username,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Text(
                            self.user_handle,
                            size=11,
                            color=ft.Colors.GREY_600,
                        ),
                    ],
                    spacing=2,
                ),
            ],
            spacing=10,
        )
        
        # Action buttons
        settings_btn = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            icon_size=22,
            icon_color=ft.Colors.GREY_700,
            bgcolor=ft.Colors.GREY_100,
            on_click=self._handle_settings,
        )
        
        location_btn = ft.IconButton(
            icon=ft.Icons.LOCATION_ON,
            icon_size=22,
            icon_color=ft.Colors.RED_400,
            bgcolor=ft.Colors.GREY_100,
            on_click=self._handle_location,
        )
        
        notification_btn = ft.IconButton(
            icon=ft.Icons.NOTIFICATIONS,
            icon_size=22,
            icon_color=ft.Colors.GREY_700,
            bgcolor=ft.Colors.GREY_100,
            on_click=self._handle_notifications,
        )
        
        # Notification button with dropdown
        notification_stack = ft.Stack(
            controls=[
                notification_btn,
                # Notification badge
                ft.Container(
                    content=ft.Text("2", size=10, color=ft.Colors.WHITE),
                    width=16,
                    height=16,
                    bgcolor=ft.Colors.RED_400,
                    border_radius=8,
                    alignment=ft.alignment.center,
                    right=5,
                    top=5,
                ),
            ],
            width=45,
            height=45,
        )
        
        # Main row layout
        main_row = ft.Row(
            controls=[
                logo,
                ft.Container(width=20),
                search_container,
                ft.Container(expand=True),
                user_info,
                ft.Container(width=15),
                settings_btn,
                location_btn,
                notification_stack,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        return main_row
    
    def _handle_search(self, e):
        """Handle search submit"""
        if self.on_search:
            self.on_search(self.search_field.value)
    
    def _handle_settings(self, e):
        """Handle settings button click"""
        if self.on_settings:
            self.on_settings()
    
    def _handle_location(self, e):
        """Handle location button click"""
        if self.on_location:
            self.on_location()
    
    def _handle_notifications(self, e):
        """Handle notifications button click"""
        self.notification_dropdown.toggle()
        if self.on_notifications:
            self.on_notifications()
    
    def _close_notifications(self):
        """Close notification dropdown"""
        self.notification_dropdown.hide()
    
    def get_notification_dropdown(self):
        """Get the notification dropdown widget for overlay"""
        return self.notification_dropdown
