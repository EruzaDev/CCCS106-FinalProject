import flet as ft


class VoterDashboard(ft.Column):
    """Voter Dashboard - Main dashboard for voters to view candidates and vote"""
    
    def __init__(self, username, db, on_logout, on_profile_view=None, on_compare=None):
        super().__init__()
        self.username = username
        self.db = db
        self.on_logout = on_logout
        self.on_profile_view = on_profile_view
        self.on_compare = on_compare
        self.search_query = ""
        self.selected_for_compare = None  # Single candidate selected for comparison {"id": x, "position": y}
        self.compare_mode = False  # When true, filter to same position only
        
        # UI component references for dynamic updates
        self.search_field = None
        self.candidate_grid_container = None
        self.compare_banner_container = None
        self.content_column = None
        
        # Get voting status
        self.voting_active = self._get_voting_status()
        
        # Build UI
        self._build_ui()
    
    def _get_voting_status(self):
        """Get current voting status from database"""
        if self.db:
            status = self.db.get_voting_status()
            return status.get("is_active", False)
        return False
    
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
        """Build the header with HonestBallot branding"""
        voting_badge = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE, size=14),
                    ft.Text("Voting Active", size=12, color=ft.Colors.WHITE),
                ],
                spacing=4,
            ),
            bgcolor="#4CAF50",
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=16,
            visible=self.voting_active,
        )
        
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
                                bgcolor="#5C6BC0",
                                border_radius=8,
                                padding=8,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "HonestBallot",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color="#333333",
                                    ),
                                    ft.Text(
                                        f"Welcome, {self.username}",
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
                            voting_badge,
                            ft.Container(width=16),
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
        # Get filtered politicians
        politicians = self._get_filtered_politicians()
        
        # Create search bar with stored reference
        self.search_field = ft.TextField(
            hint_text="Search candidates by name, position, or party...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=8,
            height=45,
            bgcolor=ft.Colors.WHITE,
            border_color="#E0E0E0",
            focused_border_color="#5C6BC0",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            on_change=self._on_search_change,
            value=self.search_query,
            disabled=self.compare_mode,
        )
        
        search_container = ft.Container(content=self.search_field)
        
        # Compare banner container (initially empty or with banner)
        self.compare_banner_container = ft.Container(
            content=self._build_compare_banner() if self.compare_mode and self.selected_for_compare else None,
            margin=ft.margin.only(bottom=20) if self.compare_mode else None,
        )
        
        # Candidate grid container with stored reference
        self.candidate_grid_container = ft.Container(
            content=self._build_candidate_grid(politicians),
        )
        
        # Store reference to content column for updates
        self.content_column = ft.Column([
            search_container,
            ft.Container(height=20),
            self.compare_banner_container,
            self.candidate_grid_container,
        ])
        
        return self.content_column
    
    def _get_filtered_politicians(self):
        """Get politicians filtered by search query and compare mode"""
        politicians = self.db.get_users_by_role("politician") if self.db else []
        
        # Filter by search query
        if self.search_query:
            politicians = [p for p in politicians if 
                          self.search_query.lower() in (p[5] or p[1] or "").lower() or
                          self.search_query.lower() in (p[7] or "").lower() or
                          self.search_query.lower() in (p[8] or "").lower()]
        
        # If in compare mode, filter to same position only
        if self.compare_mode and self.selected_for_compare:
            target_position = self.selected_for_compare["position"]
            politicians = [p for p in politicians if p[7] == target_position]
        
        return politicians
    
    def _build_compare_banner(self):
        """Build comparison mode banner"""
        # Get selected candidate name
        selected_name = "Unknown"
        if self.db and self.selected_for_compare:
            users = self.db.get_all_users()
            for user in users:
                if user[0] == self.selected_for_compare["id"]:
                    selected_name = user[5] if user[5] else user[1]
                    break
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.COMPARE_ARROWS, color="#5C6BC0", size=24),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Compare Mode Active",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color="#333333",
                                    ),
                                    ft.Text(
                                        f"Select another {self.selected_for_compare['position']} candidate to compare with {selected_name}",
                                        size=12,
                                        color="#666666",
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.ElevatedButton(
                        "Cancel",
                        icon=ft.Icons.CLOSE,
                        bgcolor="#F44336",
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=lambda e: self._cancel_compare(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=16,
            bgcolor="#E8EAF6",
            border_radius=12,
            border=ft.border.all(2, "#5C6BC0"),
        )
    
    def _on_search_change(self, e):
        """Handle search input change - dynamically update grid only"""
        self.search_query = e.control.value
        self._update_candidate_grid()
    
    def _update_candidate_grid(self):
        """Update only the candidate grid without rebuilding entire UI"""
        if self.candidate_grid_container:
            politicians = self._get_filtered_politicians()
            self.candidate_grid_container.content = self._build_candidate_grid(politicians)
            if self.page:
                self.page.update()
    
    def _build_candidate_grid(self, politicians):
        """Build grid of candidate cards"""
        if not politicians:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=64, color="#CCCCCC"),
                        ft.Text("No candidates found", size=16, color="#666666"),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                padding=40,
                alignment=ft.alignment.center,
            )
        
        # Create rows of 3 cards each
        rows = []
        cards = []
        
        for i, politician in enumerate(politicians):
            user_id, username, email, role, created_at, full_name, status, position, party, biography, profile_image = politician
            
            # Get verification count for this politician
            verifications = self.db.get_verifications_by_politician(user_id) if self.db else []
            verified_count = len([v for v in verifications if v[4] == 'verified'])
            pending_count = len([v for v in verifications if v[4] == 'pending'])
            
            # Check if this candidate is selected for comparison
            is_selected = (self.selected_for_compare and 
                          self.selected_for_compare["id"] == user_id)
            
            card = self._build_candidate_card(
                user_id=user_id,
                name=full_name if full_name else username,
                position=position if position else "Politician",
                party=party if party else "Independent",
                biography=biography if biography else "",
                image=profile_image,
                verified_count=verified_count,
                pending_count=pending_count,
                is_selected=is_selected,
            )
            cards.append(card)
            
            # Create row every 3 cards
            if len(cards) == 3:
                rows.append(ft.Row(cards, spacing=16))
                cards = []
        
        # Add remaining cards
        if cards:
            rows.append(ft.Row(cards, spacing=16))
        
        return ft.Column(rows, spacing=16)
    
    def _build_candidate_card(self, user_id, name, position, party, biography, image, verified_count, pending_count, is_selected=False):
        """Build a candidate card"""
        # Create avatar/image
        if image:
            profile_image = ft.Container(
                content=ft.Image(
                    src_base64=image,
                    fit=ft.ImageFit.COVER,
                    width=280,
                    height=160,
                ),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                border_radius=ft.border_radius.only(top_left=12, top_right=12),
            )
        else:
            profile_image = ft.Container(
                content=ft.Icon(ft.Icons.PERSON, size=60, color="#CCCCCC"),
                bgcolor="#E8EAF6",
                height=160,
                alignment=ft.alignment.center,
                border_radius=ft.border_radius.only(top_left=12, top_right=12),
            )
        
        # Verification badge
        verification_badge = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.VERIFIED, color=ft.Colors.WHITE, size=12),
                    ft.Text("Verified", size=10, color=ft.Colors.WHITE),
                ],
                spacing=4,
            ),
            bgcolor="#4CAF50",
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=12,
            visible=verified_count > 0,
        )
        
        # Pending badge
        pending_badge = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.PENDING, color=ft.Colors.WHITE, size=12),
                    ft.Text("Pending", size=10, color=ft.Colors.WHITE),
                ],
                spacing=4,
            ),
            bgcolor="#FF9800",
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=12,
            visible=pending_count > 0 and verified_count == 0,
        )
        
        # Compare button - different style when selected
        compare_icon_color = ft.Colors.WHITE if is_selected else "#5C6BC0"
        compare_bg = "#5C6BC0" if is_selected else ft.Colors.with_opacity(0.9, ft.Colors.WHITE)
        
        compare_checkbox = ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.CHECK if is_selected else ft.Icons.COMPARE_ARROWS,
                icon_color=compare_icon_color,
                icon_size=20,
                tooltip="Remove from compare" if is_selected else "Add to compare",
                on_click=lambda e, uid=user_id, pos=position: self._toggle_compare(uid, pos),
            ),
            bgcolor=compare_bg,
            border_radius=20,
        )
        
        # Card styling - highlight if selected
        card_border = ft.border.all(3, "#5C6BC0") if is_selected else None
        card_shadow_color = ft.Colors.with_opacity(0.3, "#5C6BC0") if is_selected else ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
        
        return ft.Container(
            content=ft.Column(
                [
                    # Image with badges overlay
                    ft.Stack(
                        [
                            profile_image,
                            ft.Container(
                                content=ft.Row(
                                    [verification_badge, pending_badge],
                                    spacing=4,
                                ),
                                left=10,
                                top=10,
                            ),
                            ft.Container(
                                content=compare_checkbox,
                                right=10,
                                top=10,
                            ),
                            # Selected overlay
                            ft.Container(
                                bgcolor=ft.Colors.with_opacity(0.1, "#5C6BC0") if is_selected else None,
                                border_radius=ft.border_radius.only(top_left=12, top_right=12),
                                height=160,
                                width=280,
                            ) if is_selected else ft.Container(),
                        ],
                    ),
                    # Info section
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(name, size=16, weight=ft.FontWeight.BOLD, expand=True),
                                        ft.Container(
                                            content=ft.Text("SELECTED", size=9, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                            bgcolor="#5C6BC0",
                                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                            border_radius=8,
                                            visible=is_selected,
                                        ),
                                    ],
                                ),
                                ft.Text(position, size=12, color="#5C6BC0"),
                                ft.Text(party, size=11, color="#666666"),
                                ft.Container(height=8),
                                ft.Text(
                                    biography[:80] + "..." if len(biography) > 80 else biography,
                                    size=11,
                                    color="#666666",
                                ),
                                ft.Container(height=8),
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.VERIFIED, color="#4CAF50", size=14),
                                        ft.Text(f"{verified_count} Verified", size=11, color="#666666"),
                                    ],
                                    spacing=4,
                                ),
                                ft.Container(height=12),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "View Profile",
                                            icon=ft.Icons.PERSON,
                                            bgcolor="#5C6BC0",
                                            color=ft.Colors.WHITE,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                            ),
                                            expand=True,
                                            on_click=lambda e, uid=user_id: self._view_profile(uid),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.CHECK if is_selected else ft.Icons.COMPARE_ARROWS,
                                            icon_color=ft.Colors.WHITE if is_selected else "#5C6BC0",
                                            bgcolor="#5C6BC0" if is_selected else None,
                                            tooltip="Remove from compare" if is_selected else "Compare",
                                            on_click=lambda e, uid=user_id, pos=position: self._toggle_compare(uid, pos),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        padding=16,
                        bgcolor="#F5F5FF" if is_selected else None,
                    ),
                ],
                spacing=0,
            ),
            width=280,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=card_border,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12 if is_selected else 8,
                color=card_shadow_color,
            ),
        )
    
    def _view_profile(self, user_id):
        """View politician profile"""
        if self.on_profile_view:
            self.on_profile_view(user_id)
    
    def _toggle_compare(self, user_id, position):
        """Toggle candidate selection for comparison"""
        # If clicking on already selected candidate, deselect and exit compare mode
        if self.selected_for_compare and self.selected_for_compare["id"] == user_id:
            self._cancel_compare()
            return
        
        # If no candidate selected yet, select this one and enter compare mode
        if not self.selected_for_compare:
            self.selected_for_compare = {"id": user_id, "position": position}
            self.compare_mode = True
            self._update_compare_ui()
            return
        
        # If a candidate is selected and clicking another one with same position
        if self.selected_for_compare["position"] == position:
            # Trigger comparison
            if self.on_compare:
                self.on_compare(self.selected_for_compare["id"], user_id)
            # Reset compare mode
            self._cancel_compare()
        else:
            # Different position - show error
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Can only compare candidates for the same position"),
                    bgcolor="#F44336",
                )
                self.page.snack_bar.open = True
                self.page.update()
    
    def _cancel_compare(self):
        """Cancel comparison mode"""
        self.selected_for_compare = None
        self.compare_mode = False
        self._update_compare_ui()
    
    def _update_compare_ui(self):
        """Update UI for compare mode changes without losing search state"""
        # Update search field disabled state
        if self.search_field:
            self.search_field.disabled = self.compare_mode
        
        # Update compare banner
        if self.compare_banner_container:
            if self.compare_mode and self.selected_for_compare:
                self.compare_banner_container.content = self._build_compare_banner()
                self.compare_banner_container.margin = ft.margin.only(bottom=20)
            else:
                self.compare_banner_container.content = None
                self.compare_banner_container.margin = None
        
        # Update candidate grid
        self._update_candidate_grid()
        
        if self.page:
            self.page.update()
