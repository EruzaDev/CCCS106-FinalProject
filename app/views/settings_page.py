import flet as ft
from app.theme import AppTheme


class SettingsPage(ft.Column):
    """Settings page for user preferences"""
    
    def __init__(self, username, user_handle, on_save, on_cancel, on_back, on_logout, on_profile):
        super().__init__()
        self.username = username
        self.user_handle = user_handle
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.on_back = on_back
        self.on_logout = on_logout
        self.on_profile = on_profile
        
        # Theme settings
        self.theme_dropdown = ft.Dropdown(
            label="Theme",
            options=[
                ft.dropdown.Option("light", "Light Mode"),
                ft.dropdown.Option("dark", "Dark Mode"),
                ft.dropdown.Option("auto", "Auto"),
            ],
            value="light",
            width=200,
            border_color=AppTheme.BORDER_COLOR,
            focused_border_color=AppTheme.PRIMARY,
        )
        
        # Notification settings
        self.notifications_switch = ft.Switch(
            label="Enable Notifications",
            value=True,
            active_color=AppTheme.PRIMARY,
        )
        
        # Build UI
        self.controls = [
            self._build_top_bar(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Settings",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Divider(height=20, color=AppTheme.BORDER_COLOR),
                        ft.Text(
                            "Appearance",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        self.theme_dropdown,
                        ft.Divider(height=20, color=AppTheme.BORDER_COLOR),
                        ft.Text(
                            "Notifications",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        self.notifications_switch,
                        ft.Divider(height=30, color=AppTheme.BORDER_COLOR),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text="Save",
                                    bgcolor=AppTheme.PRIMARY,
                                    color=ft.Colors.WHITE,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=self._handle_save,
                                ),
                                ft.TextButton(
                                    text="Cancel",
                                    style=ft.ButtonStyle(color=AppTheme.PRIMARY),
                                    on_click=lambda e: self.on_cancel(),
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=10,
                ),
                padding=30,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[AppTheme.BG_SECONDARY, AppTheme.BG_PRIMARY],
                ),
                expand=True,
            ),
        ]
        
        self.expand = True
        self.spacing = 0
    
    def _build_top_bar(self):
        """Build top navigation bar"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=AppTheme.PRIMARY,
                        on_click=lambda e: self.on_back(),
                        tooltip="Back",
                    ),
                    ft.Text(
                        "Settings",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.LOGOUT,
                        icon_color=AppTheme.PRIMARY,
                        on_click=lambda e: self.on_logout(),
                        tooltip="Logout",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.08, AppTheme.PRIMARY),
            ),
        )
    
    def _handle_save(self, e):
        """Handle save settings"""
        settings_data = {
            "theme": self.theme_dropdown.value,
            "notifications": self.notifications_switch.value,
        }
        self.on_save(settings_data)
