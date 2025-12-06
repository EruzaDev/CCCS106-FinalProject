import flet as ft


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
                        ),
                        ft.Text(
                            f"User: {self.user_handle}",
                            size=14,
                            color=ft.Colors.GREY_700,
                        ),
                        ft.Divider(height=30),
                        ft.Text(
                            "Voting System Features:",
                            size=18,
                            weight=ft.FontWeight.BOLD,
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
                        color=ft.Colors.BLUE,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.PERSON,
                        on_click=lambda e: self.on_profile(),
                        tooltip="Profile",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        on_click=lambda e: self.on_settings(),
                        tooltip="Settings",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.LOGOUT,
                        on_click=lambda e: self.on_logout(),
                        tooltip="Logout",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            bgcolor=ft.Colors.WHITE,
            border_bottom=ft.Border(
                bottom=ft.BorderSide(1, ft.Colors.GREY_300)
            ),
        )
    
    def _create_feature_card(self, icon, title, description):
        """Create a feature card"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=40, color=ft.Colors.BLUE),
                    ft.Column(
                        [
                            ft.Text(title, weight=ft.FontWeight.BOLD),
                            ft.Text(description, size=12, color=ft.Colors.GREY_700),
                        ]
                    ),
                ],
                spacing=15,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            border_radius=10,
            bgcolor=ft.Colors.GREY_100,
            border=ft.Border(
                all=ft.BorderSide(1, ft.Colors.GREY_300)
            ),
        )
