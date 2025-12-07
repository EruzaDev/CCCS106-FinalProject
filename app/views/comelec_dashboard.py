import flet as ft
from app.components.news_post_creator import NewsPostCreator, MyPostsList


class ComelecDashboard(ft.Column):
    """COMELEC Dashboard - Main dashboard for COMELEC administrators"""
    
    def __init__(self, username, db, on_logout, on_user_management, on_election_results, on_candidates, current_user_id=None, on_audit_log=None, on_analytics=None):
        super().__init__()
        self.username = username
        self.db = db
        self.on_logout = on_logout
        self.on_user_management = on_user_management
        self.on_election_results = on_election_results
        self.on_candidates = on_candidates
        self.current_user_id = current_user_id
        self.on_audit_log = on_audit_log
        self.on_analytics = on_analytics
        
        # Dialog reference
        self.edit_dialog = None
        
        # Search state
        self.candidate_search_query = ""
        self.candidates_table_container = None
        
        # Get voting status from database
        status = self.db.get_voting_status() if self.db else {"is_active": False}
        self.voting_active = status["is_active"]
        
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
                            ft.IconButton(
                                icon=ft.Icons.ANALYTICS,
                                icon_color="#4CAF50",
                                tooltip="Election Analytics",
                                on_click=lambda e: self.on_analytics() if self.on_analytics else None,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.HISTORY,
                                icon_color="#5C6BC0",
                                tooltip="Audit Logs",
                                on_click=lambda e: self.on_audit_log() if self.on_audit_log else None,
                            ),
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
                ft.Container(height=20),
                # News Post Creator
                self._build_news_section(),
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
        # Get filtered politicians
        politicians = self._get_filtered_candidates()
        
        # Create candidates table container with stored reference
        self.candidates_table_container = ft.Container(
            content=self._build_candidates_table(politicians),
        )
        
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
                    # Search bar with handler
                    ft.TextField(
                        hint_text="Search candidates by name, position, or party...",
                        prefix_icon=ft.Icons.SEARCH,
                        border_radius=8,
                        height=40,
                        content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
                        value=self.candidate_search_query,
                        on_change=self._on_candidate_search_change,
                    ),
                    ft.Container(height=16),
                    # Candidates table (dynamic)
                    self.candidates_table_container,
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
    
    def _get_filtered_candidates(self):
        """Get candidates filtered by search query"""
        politicians = self.db.get_users_by_role("politician") if self.db else []
        
        if self.candidate_search_query:
            query = self.candidate_search_query.lower()
            politicians = [p for p in politicians if 
                          query in (p[5] or p[1] or "").lower() or  # full_name or username
                          query in (p[7] or "").lower() or  # position
                          query in (p[8] or "").lower()]  # party
        
        return politicians
    
    def _on_candidate_search_change(self, e):
        """Handle candidate search input change"""
        self.candidate_search_query = e.control.value
        self._update_candidates_table()
    
    def _update_candidates_table(self):
        """Update only the candidates table without rebuilding entire UI"""
        if self.candidates_table_container:
            politicians = self._get_filtered_candidates()
            self.candidates_table_container.content = self._build_candidates_table(politicians)
            if self.page:
                self.page.update()
    
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
                avatar = ft.Container(
                    content=ft.Image(
                        src_base64=profile_image,
                        fit=ft.ImageFit.COVER,
                        width=36,
                        height=36,
                    ),
                    width=36,
                    height=36,
                    border_radius=18,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                )
            else:
                avatar = ft.CircleAvatar(
                    content=ft.Text(display_name[0].upper() if display_name else "?"),
                    bgcolor="#E8EAF6",
                    radius=18,
                )
            
            # Get verification info for this candidate
            verifications = self.db.get_verifications_by_politician(user_id) if self.db else []
            verified_count = len([v for v in verifications if v[4] == 'verified'])
            total_count = len(verifications)
            
            # Verification badge
            if verified_count > 0:
                verified_cell = ft.Row(
                    [
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color="#4CAF50", size=16),
                        ft.Text(f"{verified_count}/{total_count}", size=12, color="#4CAF50"),
                    ],
                    spacing=4,
                )
            elif total_count > 0:
                verified_cell = ft.Row(
                    [
                        ft.Icon(ft.Icons.PENDING, color="#FF9800", size=16),
                        ft.Text(f"0/{total_count}", size=12, color="#FF9800"),
                    ],
                    spacing=4,
                )
            else:
                verified_cell = ft.Row(
                    [
                        ft.Icon(ft.Icons.REMOVE_CIRCLE_OUTLINE, color="#999999", size=16),
                        ft.Text("None", size=12, color="#999999"),
                    ],
                    spacing=4,
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
                        ft.DataCell(verified_cell),
                        ft.DataCell(
                            ft.TextButton(
                                "Edit",
                                style=ft.ButtonStyle(color="#5C6BC0"),
                                on_click=lambda e, uid=user_id, name=display_name, pos=display_position: self._show_edit_candidate_dialog(uid, name, pos),
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
        # Get pending verifications from database
        pending_verifications = self.db.get_pending_verifications() if self.db else []
        
        verification_items = []
        for verification in pending_verifications:
            ver_id, politician_id, title, description, evidence_url, status, created_at, full_name, username, position = verification
            display_name = full_name if full_name else username
            display_position = position if position else "Politician"
            
            verification_items.append(
                self._build_verification_item(
                    ver_id,
                    display_name,
                    display_position,
                    title,
                    description if description else "Pending verification of claimed accomplishments.",
                )
            )
        
        if not verification_items:
            verification_items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.VERIFIED, color="#CCCCCC", size=48),
                            ft.Text("No pending verifications", color="#666666", size=14),
                            ft.Text("All achievements have been reviewed.", color="#999999", size=12),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    padding=40,
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
    
    def _build_verification_item(self, verification_id, name, position, achievement_title, description):
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
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Verify",
                                icon=ft.Icons.CHECK,
                                bgcolor="#4CAF50",
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e, vid=verification_id: self._verify_achievement(vid, "verified"),
                            ),
                            ft.OutlinedButton(
                                "Reject",
                                icon=ft.Icons.CLOSE,
                                style=ft.ButtonStyle(
                                    color="#F44336",
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e, vid=verification_id: self._verify_achievement(vid, "rejected"),
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=16,
            bgcolor="#FAFAFA",
            border_radius=8,
            margin=ft.margin.only(bottom=12),
        )
    
    def _verify_achievement(self, verification_id, status):
        """Verify or reject an achievement"""
        if self.db:
            self.db.verify_achievement(verification_id, self.current_user_id, status)
            # Rebuild UI to reflect changes
            self._build_ui()
            if self.page:
                self.page.update()
    
    def _build_news_section(self):
        """Build news post creator section for COMELEC announcements"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "News & Announcements",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Create election updates and announcements for voters",
                        size=12,
                        color="#666666",
                    ),
                    ft.Container(height=16),
                    NewsPostCreator(
                        db=self.db,
                        author_id=self.current_user_id,
                        author_role="comelec",
                        on_post_created=self._on_news_post_created,
                    ),
                    ft.Container(height=16),
                    MyPostsList(
                        db=self.db,
                        author_id=self.current_user_id,
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
    
    def _on_news_post_created(self):
        """Handle news post created event"""
        # Rebuild UI to show updated posts
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _toggle_voting(self):
        """Toggle voting status"""
        if self.db:
            if self.voting_active:
                self.db.stop_voting(self.current_user_id)
                # Log the action
                self.db.log_action(
                    action="Voting Stopped",
                    action_type="voting",
                    description="COMELEC stopped the voting session",
                    user_id=self.current_user_id,
                    user_role="comelec",
                )
            else:
                self.db.start_voting(self.current_user_id)
                # Log the action
                self.db.log_action(
                    action="Voting Started",
                    action_type="voting",
                    description="COMELEC started a new voting session",
                    user_id=self.current_user_id,
                    user_role="comelec",
                )
        
        self.voting_active = not self.voting_active
        
        # Broadcast voting status change to all connected clients
        if self.page:
            self.page.pubsub.send_all({
                "type": "voting_status_changed",
                "is_active": self.voting_active
            })
        
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _show_edit_candidate_dialog(self, user_id, name, position):
        """Show dialog to edit candidate verifications"""
        # Get verifications for this candidate
        verifications = self.db.get_verifications_by_politician(user_id) if self.db else []
        
        # Build verification items
        verification_items = []
        for v in verifications:
            ver_id, title, description, evidence_url, status, created_at = v
            
            # Status badge
            if status == "verified":
                status_badge = ft.Container(
                    content=ft.Text("Verified", size=10, color=ft.Colors.WHITE),
                    bgcolor="#4CAF50",
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=8,
                )
            elif status == "rejected":
                status_badge = ft.Container(
                    content=ft.Text("Rejected", size=10, color=ft.Colors.WHITE),
                    bgcolor="#F44336",
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=8,
                )
            else:
                status_badge = ft.Container(
                    content=ft.Text("Pending", size=10, color=ft.Colors.WHITE),
                    bgcolor="#FF9800",
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=8,
                )
            
            verification_items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(title, weight=ft.FontWeight.BOLD, size=13, expand=True),
                                    status_badge,
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(description if description else "No description", size=11, color="#666666"),
                            ft.Container(height=8),
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Verify",
                                        icon=ft.Icons.CHECK,
                                        bgcolor="#4CAF50",
                                        color=ft.Colors.WHITE,
                                        height=32,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=6),
                                            padding=ft.padding.symmetric(horizontal=12),
                                        ),
                                        on_click=lambda e, vid=ver_id, uid=user_id, n=name, p=position: self._update_verification_status(vid, "verified", uid, n, p),
                                    ),
                                    ft.OutlinedButton(
                                        "Reject",
                                        icon=ft.Icons.CLOSE,
                                        height=32,
                                        style=ft.ButtonStyle(
                                            color="#F44336",
                                            shape=ft.RoundedRectangleBorder(radius=6),
                                            padding=ft.padding.symmetric(horizontal=12),
                                        ),
                                        on_click=lambda e, vid=ver_id, uid=user_id, n=name, p=position: self._update_verification_status(vid, "rejected", uid, n, p),
                                    ),
                                    ft.OutlinedButton(
                                        "Pending",
                                        icon=ft.Icons.PENDING,
                                        height=32,
                                        style=ft.ButtonStyle(
                                            color="#FF9800",
                                            shape=ft.RoundedRectangleBorder(radius=6),
                                            padding=ft.padding.symmetric(horizontal=12),
                                        ),
                                        on_click=lambda e, vid=ver_id, uid=user_id, n=name, p=position: self._update_verification_status(vid, "pending", uid, n, p),
                                    ),
                                ],
                                spacing=8,
                            ),
                        ],
                    ),
                    padding=12,
                    bgcolor="#FAFAFA",
                    border_radius=8,
                    margin=ft.margin.only(bottom=8),
                )
            )
        
        # If no verifications, show message
        if not verification_items:
            verification_items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.INFO_OUTLINE, color="#999999", size=32),
                            ft.Text("No achievements submitted", color="#666666", size=12),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    padding=24,
                    alignment=ft.alignment.center,
                )
            )
        
        # Create dialog
        self.edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.EDIT, color="#5C6BC0", size=24),
                    ft.Column(
                        [
                            ft.Text(f"Edit Candidate: {name}", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(position, size=12, color="#666666"),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=12,
            ),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Achievement Verifications", size=14, weight=ft.FontWeight.W_500),
                        ft.Container(height=8),
                        ft.Column(
                            verification_items,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                    ],
                    spacing=8,
                ),
                width=500,
                height=400,
            ),
            actions=[
                ft.TextButton("Close", on_click=self._close_edit_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        if self.page:
            self.page.overlay.append(self.edit_dialog)
            self.edit_dialog.open = True
            self.page.update()
    
    def _update_verification_status(self, verification_id, status, user_id, name, position):
        """Update verification status and refresh dialog"""
        if self.db:
            self.db.verify_achievement(verification_id, self.current_user_id, status)
        
        # Close current dialog and reopen with updated data
        self._close_edit_dialog(None)
        self._show_edit_candidate_dialog(user_id, name, position)
        
        # Also rebuild main UI to reflect changes
        self._build_ui()
    
    def _close_edit_dialog(self, e):
        """Close the edit dialog"""
        if self.edit_dialog and self.page:
            self.edit_dialog.open = False
            self.page.update()
