import flet as ft


class ComelecDashboard(ft.Column):
    """COMELEC Dashboard - Main dashboard for COMELEC administrators"""
    
    def __init__(self, username, db, on_logout, on_user_management, on_election_results, on_candidates):
        super().__init__()
        self.username = username
        self.db = db
        self.on_logout = on_logout
        self.on_user_management = on_user_management
        self.on_election_results = on_election_results
        self.on_candidates = on_candidates
        self.voting_active = False
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the main UI"""
        self.controls = [
            self._build_header(),
            ft.Container(
                content=ft.Column(
                    [
                        self._build_content(),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
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
                ft.Container(height=20),
                # Candidate Management
                self._build_candidate_management(),
                ft.Container(height=20),
                # Pending Achievement Verifications
                self._build_pending_verifications(),
            ],
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
                                        "Voting is currently inactive. Activate voting to allow voters to cast their ballots." if not self.voting_active else "Voting is currently active. Voters can now cast their ballots.",
                                        size=12,
                                        color="#666666",
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.ElevatedButton(
                                "Start Voting" if not self.voting_active else "Stop Voting",
                                icon=ft.Icons.PLAY_ARROW if not self.voting_active else ft.Icons.STOP,
                                bgcolor="#4CAF50" if not self.voting_active else "#F44336",
                                color=ft.Colors.WHITE,
                                on_click=lambda e: self._toggle_voting(),
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
                                "6 verified",
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
        # Get counts from database
        politicians = self.db.get_users_by_role("politician") if self.db else []
        total_candidates = len(politicians)
        
        return ft.Row(
            [
                self._build_stat_card("Total Candidates", str(total_candidates), ft.Icons.PEOPLE, "#4CAF50"),
                self._build_stat_card("Approved", str(total_candidates), ft.Icons.CHECK_CIRCLE, "#4CAF50"),
                self._build_stat_card("Total Votes Cast", "0", ft.Icons.HOW_TO_VOTE, "#5C6BC0"),
                self._build_stat_card("Verified", str(total_candidates), ft.Icons.VERIFIED, "#4CAF50"),
            ],
            spacing=16,
        )
    
    def _build_stat_card(self, label, value, icon, color):
        """Build a statistic card"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(label, size=12, color="#666666"),
                    ft.Container(width=8),
                    ft.Icon(icon, color=color, size=16),
                    ft.Container(width=4),
                    ft.Text(value, size=14, weight=ft.FontWeight.BOLD, color=color),
                ],
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=2,
                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            ),
        )
    
    def _build_candidate_management(self):
        """Build candidate management section"""
        # Get politicians from database
        politicians = self.db.get_users_by_role("politician") if self.db else []
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Candidate Management",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                    ft.Container(height=12),
                    # Search bar
                    ft.TextField(
                        hint_text="Search candidates...",
                        prefix_icon=ft.Icons.SEARCH,
                        border_radius=8,
                        height=40,
                        content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    ),
                    ft.Container(height=16),
                    # Candidates table
                    self._build_candidates_table(politicians),
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
    
    def _build_candidates_table(self, politicians):
        """Build candidates data table"""
        rows = []
        
        for politician in politicians:
            user_id, username, email, role, created_at, full_name, status, position, party, biography, profile_image = politician
            display_name = full_name if full_name else username
            display_status = status if status else "active"
            display_position = position if position else "-"
            display_party = party if party else "-"
            
            # Create avatar with image or icon
            if profile_image:
                avatar = ft.CircleAvatar(
                    foreground_image_src=f"data:image/png;base64,{profile_image}",
                    radius=18,
                )
            else:
                avatar = ft.CircleAvatar(
                    content=ft.Text(display_name[0].upper() if display_name else "?"),
                    bgcolor="#E8EAF6",
                    radius=18,
                )
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Row(
                                [
                                    avatar,
                                    ft.Text(display_name, size=13),
                                ],
                                spacing=10,
                            )
                        ),
                        ft.DataCell(ft.Text(display_position, size=13)),
                        ft.DataCell(ft.Text(display_party, size=13)),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    "Approved" if display_status == "active" else "Pending",
                                    color="#4CAF50" if display_status == "active" else "#FF9800",
                                    size=11,
                                ),
                                bgcolor="#E8F5E9" if display_status == "active" else "#FFF3E0",
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=12,
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.CHECK_CIRCLE, color="#4CAF50", size=16),
                                    ft.Text("Yes", size=12, color="#4CAF50"),
                                ],
                                spacing=4,
                            )
                        ),
                        ft.DataCell(
                            ft.TextButton(
                                "Edit",
                                style=ft.ButtonStyle(color="#5C6BC0"),
                            )
                        ),
                    ],
                )
            )
        
        if not rows:
            return ft.Container(
                content=ft.Text("No candidates found. Add politicians in User Management.", color="#666666"),
                padding=20,
                alignment=ft.alignment.center,
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Candidate", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Position", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Party", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Verified", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD, size=12)),
            ],
            rows=rows,
            border=ft.border.all(1, "#E0E0E0"),
            border_radius=8,
            heading_row_color="#FAFAFA",
            data_row_min_height=50,
            data_row_max_height=60,
            column_spacing=20,
        )
    
    def _build_pending_verifications(self):
        """Build pending achievement verifications section"""
        # Get politicians with achievements to verify
        politicians = self.db.get_users_by_role("politician") if self.db else []
        
        verification_items = []
        for politician in politicians[:2]:  # Show first 2 for demo
            user_id, username, email, role, created_at, full_name, status, position, party, biography, profile_image = politician
            display_name = full_name if full_name else username
            display_position = position if position else "Politician"
            
            verification_items.append(
                self._build_verification_item(
                    display_name,
                    display_position,
                    "Public Service Achievement",
                    "Pending verification of claimed accomplishments and public service record.",
                )
            )
        
        if not verification_items:
            verification_items.append(
                ft.Container(
                    content=ft.Text("No pending verifications", color="#666666"),
                    padding=20,
                    alignment=ft.alignment.center,
                )
            )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Pending Achievement Verifications",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=16),
                    *verification_items,
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
    
    def _build_verification_item(self, name, position, achievement_title, description):
        """Build a verification item card"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(name, weight=ft.FontWeight.BOLD, size=14),
                                    ft.Container(
                                        content=ft.Text(position, size=10, color="#666666"),
                                        bgcolor="#E8EAF6",
                                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                        border_radius=4,
                                    ),
                                ],
                                spacing=8,
                            ),
                            ft.Text(achievement_title, size=13, weight=ft.FontWeight.W_500, color="#333333"),
                            ft.Text(description, size=11, color="#666666"),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.ElevatedButton(
                        "Verify",
                        icon=ft.Icons.CHECK,
                        bgcolor="#4CAF50",
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=16,
            bgcolor="#FAFAFA",
            border_radius=8,
            margin=ft.margin.only(bottom=12),
        )
    
    def _toggle_voting(self):
        """Toggle voting status"""
        self.voting_active = not self.voting_active
        self._build_ui()
        if self.page:
            self.page.update()
