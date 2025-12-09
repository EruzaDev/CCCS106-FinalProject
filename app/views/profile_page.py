import flet as ft
from app.theme import AppTheme


class ProfilePage(ft.Column):
    """User profile page"""
    
    def __init__(self, username, user_handle, on_logout, on_settings, on_home):
        super().__init__()
        self.username = username
        self.user_handle = user_handle
        self.on_logout = on_logout
        self.on_settings = on_settings
        self.on_home = on_home
        
        # Build UI
        self.controls = [
            self._build_top_bar(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=80, color=AppTheme.PRIMARY),
                        ft.Text(
                            self.username,
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            self.user_handle,
                            size=14,
                            color=AppTheme.TEXT_SECONDARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Divider(height=30, color=AppTheme.BORDER_COLOR),
                        ft.Text(
                            "Profile Information",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text("Role:", weight=ft.FontWeight.BOLD, width=100, color=AppTheme.TEXT_PRIMARY),
                                            ft.Text("Voter", color=AppTheme.TEXT_SECONDARY),
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text("Status:", weight=ft.FontWeight.BOLD, width=100, color=AppTheme.TEXT_PRIMARY),
                                            ft.Text("Active", color="#4CAF50"),
                                        ]
                                    ),
                                ]
                            ),
                            padding=15,
                            bgcolor=AppTheme.BG_PRIMARY,
                            border_radius=10,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
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
                        on_click=lambda e: self.on_home(),
                        tooltip="Back",
                    ),
                    ft.Text(
                        "Profile",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        icon_color=AppTheme.PRIMARY,
                        on_click=lambda e: self.on_settings(),
                        tooltip="Settings",
                    ),
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
