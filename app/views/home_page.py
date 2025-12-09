import flet as ft
from app.theme import AppTheme


class HomePage(ft.Column):
    """Main home page for authenticated users"""
    
    def __init__(self, username, user_handle, on_logout, on_settings, on_profile):
        super().__init__()
        self.username = username
        self.user_handle = user_handle
        self.on_logout = on_logout
        self.on_settings = on_settings
        self.on_profile = on_profile
        
        # Build UI
        self.controls = [
            self._build_top_bar(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f"Welcome, {self.username}!",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            f"User: {self.user_handle}",
                            size=14,
                            color=AppTheme.TEXT_SECONDARY,
                        ),
                        ft.Divider(height=30, color=AppTheme.BORDER_COLOR),
                        ft.Text(
                            "Voting System Features:",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    self._create_feature_card(
                                        ft.Icons.HOW_TO_VOTE,
                                        "Cast Your Vote",
                                        "Vote for your preferred candidates"
                                    ),
                                    self._create_feature_card(
                                        ft.Icons.BAR_CHART,
                                        "View Results",
                                        "See real-time voting results"
                                    ),
                                    self._create_feature_card(
                                        ft.Icons.PERSON,
                                        "View Candidates",
                                        "Browse candidate information"
                                    ),
                                ]
                            )
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
                    ft.Text(
                        "HonestBallot",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.PRIMARY,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.PERSON,
                        icon_color=AppTheme.PRIMARY,
                        on_click=lambda e: self.on_profile(),
                        tooltip="Profile",
                    ),
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
                color=ft.Colors.with_opacity(0.1, AppTheme.PRIMARY),
            ),
        )
    
    def _create_feature_card(self, icon, title, description):
        """Create a feature card"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icon, size=36, color=ft.Colors.WHITE),
                        bgcolor=AppTheme.PRIMARY,
                        border_radius=12,
                        padding=12,
                    ),
                    ft.Column(
                        [
                            ft.Text(title, weight=ft.FontWeight.BOLD, color=AppTheme.TEXT_PRIMARY),
                            ft.Text(description, size=12, color=AppTheme.TEXT_SECONDARY),
                        ]
                    ),
                ],
                spacing=15,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.08, AppTheme.PRIMARY),
            ),
            border=ft.border.all(1, AppTheme.BORDER_COLOR),
        )
