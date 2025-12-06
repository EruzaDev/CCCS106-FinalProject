import flet as ft


class ComelecDashboard(ft.Column):
    """COMELEC Dashboard - Main dashboard for COMELEC administrators"""
    
    def __init__(self, username, on_logout, on_user_management, on_election_results, on_candidates):
        super().__init__()
        self.username = username
        self.on_logout = on_logout
        self.on_user_management = on_user_management
        self.on_election_results = on_election_results
        self.on_candidates = on_candidates
        
        # Build UI
        self.controls = [
            self._build_header(),
            ft.Container(
                content=self._build_content(),
                expand=True,
                bgcolor="#F5F5F5",
                padding=20,
            ),
        ]
        
        self.expand = True
        self.spacing = 0
    
    def _build_header(self):
        """Build the header with COMELEC branding"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.HOW_TO_VOTE,
                                    color=ft.Colors.WHITE,
                                    size=24,
                                ),
                                bgcolor="#4CAF50",
                                border_radius=8,
                                padding=8,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "COMELEC Dashboard",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color="#333333",
                                    ),
                                    ft.Text(
                                        f"Welcome, Commissioner {self.username}",
                                        size=12,
                                        color="#666666",
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LOGOUT, color="#5C6BC0", size=18),
                            ft.TextButton(
                                "Logout",
                                on_click=lambda e: self.on_logout(),
                                style=ft.ButtonStyle(
                                    color="#5C6BC0",
                                ),
                            ),
                        ],
                        spacing=4,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        )
    
    def _build_content(self):
        """Build main content area"""
        return ft.Column(
            [
                # Voting Control Center Card
                self._build_voting_control_card(),
                ft.Container(height=20),
                # Quick Actions
                self._build_quick_actions(),
                ft.Container(height=20),
                # Statistics Row
                self._build_statistics_row(),
            ],
            expand=True,
        )
    
    def _build_voting_control_card(self):
        """Build voting control center card"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Voting Control Center",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Voting is currently inactive. Activate voting to allow voters to cast their ballots.",
                                        size=12,
                                        color="#666666",
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.ElevatedButton(
                                "Start Voting",
                                icon=ft.Icons.PLAY_ARROW,
                                bgcolor="#4CAF50",
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def _build_quick_actions(self):
        """Build quick action buttons"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Quick Actions",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=12),
                    ft.Row(
                        [
                            self._build_action_card(
                                ft.Icons.PEOPLE,
                                "User Management",
                                "Create voters & politicians",
                                lambda e: self.on_user_management(),
                            ),
                            self._build_action_card(
                                ft.Icons.BAR_CHART,
                                "Election Results",
                                "View vote tallies",
                                lambda e: self.on_election_results(),
                            ),
                            self._build_action_card(
                                ft.Icons.VERIFIED_USER,
                                "Verified Candidates",
                                "View all candidates",
                                lambda e: self.on_candidates(),
                            ),
                        ],
                        spacing=16,
                    ),
                ],
            ),
        )
    
    def _build_action_card(self, icon, title, subtitle, on_click):
        """Build a quick action card"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, color="#5C6BC0", size=32),
                    ft.Container(height=8),
                    ft.Text(title, size=14, weight=ft.FontWeight.W_500),
                    ft.Text(subtitle, size=11, color="#666666"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            width=200,
            ink=True,
            on_click=on_click,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def _build_statistics_row(self):
        """Build statistics display row"""
        return ft.Container(
            content=ft.Row(
                [
                    self._build_stat_item("Total Candidates", "0", "#4CAF50"),
                    self._build_stat_item("Approved", "0", "#2196F3"),
                    self._build_stat_item("Total Vote Cast", "0", "#FF9800"),
                    self._build_stat_item("Verified", "0", "#9C27B0"),
                ],
                spacing=24,
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def _build_stat_item(self, label, value, color):
        """Build a statistic item"""
        return ft.Column(
            [
                ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(label, size=12, color="#666666"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
