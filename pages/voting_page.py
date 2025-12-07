import flet as ft


class VotingPage(ft.Column):
    """Voting Page - Cast votes when voting is active with collapsible position sections"""
    
    def __init__(self, user_id, username, db, on_logout, on_view_profile=None, on_voting_stopped=None):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.db = db
        self.on_logout = on_logout
        self.on_view_profile = on_view_profile
        self.on_voting_stopped = on_voting_stopped
        
        # Track votes and UI state
        self.votes = {}  # position -> candidate_id
        self.submitted_positions = set()
        self.expanded_positions = set()  # Track which positions are expanded
        self.selected_candidates = {}  # position -> candidate_id (before submit)
        self.change_vote_mode = set()  # Positions where user is changing their vote
        
        # Get candidates grouped by position
        self.candidates_by_position = self._get_candidates_by_position()
        
        # Check for existing votes
        self._load_existing_votes()
        
        # Build UI
        self._build_ui()
    
    def did_mount(self):
        """Called when the control is added to the page - subscribe to voting updates"""
        if self.page:
            self.page.pubsub.subscribe(self._on_voting_status_change)
    
    def will_unmount(self):
        """Called when the control is about to be removed - unsubscribe"""
        if self.page:
            self.page.pubsub.unsubscribe()
    
    def _on_voting_status_change(self, message):
        """Handle voting status change broadcast from COMELEC"""
        if isinstance(message, dict) and message.get("type") == "voting_status_changed":
            is_active = message.get("is_active", False)
            if not is_active:
                # Voting stopped - go back to dashboard
                if self.on_voting_stopped:
                    self.on_voting_stopped()
    
    def _get_candidates_by_position(self):
        """Get all candidates grouped by position"""
        candidates = {}
        if self.db:
            politicians = self.db.get_users_by_role("politician")
            for politician in politicians:
                user_id, username, email, role, created_at, full_name, status, position, party, biography, profile_image = politician
                if position:
                    if position not in candidates:
                        candidates[position] = []
                    
                    # Get verification info
                    verifications = self.db.get_verifications_by_politician(user_id) if self.db else []
                    verified_count = len([v for v in verifications if v[4] == 'verified'])
                    total_achievements = len(verifications)
                    
                    # Get any records (placeholder for NBI integration)
                    records_count = 1 if user_id % 3 == 0 else 0  # Demo: some have records
                    
                    candidates[position].append({
                        "id": user_id,
                        "name": full_name if full_name else username,
                        "party": party if party else "Independent",
                        "image": profile_image,
                        "verified": verified_count > 0,
                        "achievements": total_achievements,
                        "records": records_count,
                    })
        return candidates
    
    def _load_existing_votes(self):
        """Load existing votes for this user from database"""
        if self.db:
            existing_votes = self.db.get_votes_by_voter(self.user_id)
            for position, candidate_id in existing_votes:
                self.votes[position] = candidate_id
                self.submitted_positions.add(position)
    
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
        """Build the header with voting active badge"""
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
                            ft.Container(
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
                            ),
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
        total_positions = len(self.candidates_by_position)
        voted_positions = len(self.submitted_positions)
        all_voted = voted_positions == total_positions and total_positions > 0
        
        position_cards = []
        for position, candidates in sorted(self.candidates_by_position.items()):
            position_cards.append(self._build_position_section(position, candidates))
        
        return ft.Column(
            [
                # Cast Your Vote header
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.HOW_TO_VOTE, color=ft.Colors.WHITE, size=20),
                                    ft.Text(
                                        "Cast Your Vote",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE,
                                    ),
                                ],
                                spacing=8,
                            ),
                            ft.Text(
                                "Select one candidate for each position and submit your vote. You can only vote once per position.",
                                size=12,
                                color=ft.Colors.WHITE70,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=20,
                    bgcolor="#F44336",
                    border_radius=12,
                ),
                ft.Container(height=20),
                # Voting Progress
                self._build_voting_progress(voted_positions, total_positions),
                ft.Container(height=20),
                # Position sections (collapsible)
                *position_cards,
                # Voting complete message
                self._build_voting_complete() if all_voted else ft.Container(),
            ],
        )
    
    def _build_voting_progress(self, voted, total):
        """Build voting progress bar"""
        progress = voted / total if total > 0 else 0
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Voting Progress", size=14, weight=ft.FontWeight.W_500),
                            ft.Text(f"{voted} / {total}", size=14, color="#666666"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=8),
                    ft.ProgressBar(
                        value=progress,
                        height=8,
                        color="#4CAF50" if progress == 1 else "#5C6BC0",
                        bgcolor="#E0E0E0",
                    ),
                ],
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            ),
        )
    
    def _build_position_section(self, position, candidates):
        """Build a collapsible section for a voting position"""
        is_voted = position in self.submitted_positions
        is_expanded = position in self.expanded_positions
        
        # Header row
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.CHECK_BOX if is_voted else ft.Icons.CHECK_BOX_OUTLINE_BLANK,
                                    color="#5C6BC0" if is_voted else "#666666",
                                    size=24,
                                ),
                                bgcolor="#E8EAF6" if is_voted else None,
                                border_radius=4,
                            ),
                            ft.Column(
                                [
                                    ft.Text(position, size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{len(candidates)} candidates", size=12, color="#666666"),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Row(
                        [
                            ft.TextButton(
                                "Change Vote" if is_voted and position not in self.change_vote_mode else "",
                                style=ft.ButtonStyle(color="#FF9800"),
                                on_click=lambda e, pos=position: self._enable_change_vote(pos),
                                visible=is_voted and position not in self.change_vote_mode,
                            ),
                            ft.TextButton(
                                "Collapse" if is_expanded else "Vote Now" if not is_voted else "Changing..." if position in self.change_vote_mode else "Vote Submitted",
                                style=ft.ButtonStyle(
                                    color="#FF9800" if position in self.change_vote_mode else "#5C6BC0" if not is_voted else "#4CAF50",
                                ),
                                on_click=lambda e, pos=position: self._toggle_position(pos),
                            ),
                        ],
                        spacing=0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=16,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.only(top_left=12, top_right=12) if is_expanded else 12,
            ink=True,
            on_click=lambda e, pos=position: self._toggle_position(pos),
        )
        
        # Candidates list (only if expanded)
        if is_expanded:
            candidate_cards = [
                self._build_candidate_card(candidate, position, is_voted)
                for candidate in candidates
            ]
            
            candidates_section = ft.Container(
                content=ft.Column(
                    candidate_cards,
                    spacing=0,
                ),
                bgcolor=ft.Colors.WHITE,
                padding=ft.padding.only(left=16, right=16, bottom=16),
                border_radius=ft.border_radius.only(bottom_left=12, bottom_right=12),
            )
            
            return ft.Container(
                content=ft.Column(
                    [header, candidates_section],
                    spacing=0,
                ),
                margin=ft.margin.only(bottom=12),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                ),
                border_radius=12,
                border=ft.border.all(2, "#4CAF50") if is_voted else None,
            )
        else:
            return ft.Container(
                content=header,
                margin=ft.margin.only(bottom=12),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                ),
                border_radius=12,
                border=ft.border.all(2, "#4CAF50") if is_voted else None,
            )
    
    def _build_candidate_card(self, candidate, position, is_voted):
        """Build a clickable candidate card"""
        is_changing = position in self.change_vote_mode
        is_selected = self.selected_candidates.get(position) == candidate["id"]
        is_submitted = position in self.submitted_positions and self.votes.get(position) == candidate["id"]
        
        # Profile image
        if candidate.get("image"):
            avatar = ft.Container(
                content=ft.Image(
                    src_base64=candidate["image"],
                    fit=ft.ImageFit.COVER,
                    width=50,
                    height=50,
                ),
                width=50,
                height=50,
                border_radius=25,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )
        else:
            avatar = ft.CircleAvatar(
                content=ft.Text(candidate["name"][0].upper() if candidate["name"] else "?", size=18),
                bgcolor="#E8EAF6",
                radius=25,
            )
        
        # Determine card styling based on state
        if is_submitted and not is_changing:
            bg_color = "#E8F5E9"
            border_color = "#4CAF50"
            border_width = 2
        elif is_submitted and is_changing:
            # Current vote while changing - show as orange
            bg_color = "#FFF3E0"
            border_color = "#FF9800"
            border_width = 2
        elif is_selected:
            bg_color = "#E8EAF6"
            border_color = "#5C6BC0"
            border_width = 2
        else:
            bg_color = "#FAFAFA"
            border_color = "#E0E0E0"
            border_width = 1
        
        return ft.Container(
            content=ft.Row(
                [
                    avatar,
                    ft.Column(
                        [
                            ft.Text(candidate["name"], size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(candidate["party"], size=12, color="#666666"),
                            ft.Row(
                                [
                                    # Verified badge
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.VERIFIED, color="#4CAF50", size=12),
                                                ft.Text("Verified", size=10, color="#4CAF50"),
                                            ],
                                            spacing=2,
                                        ),
                                        visible=candidate.get("verified", False),
                                    ),
                                    # Achievements
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.EMOJI_EVENTS, color="#666666", size=12),
                                            ft.Text(f"{candidate.get('achievements', 0)} Achievements", size=10, color="#666666"),
                                        ],
                                        spacing=2,
                                    ),
                                    # Records (if any)
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.WARNING, color="#FF9800", size=12),
                                                ft.Text(f"{candidate.get('records', 0)} Record", size=10, color="#FF9800"),
                                            ],
                                            spacing=2,
                                        ),
                                        visible=candidate.get("records", 0) > 0,
                                    ),
                                ],
                                spacing=12,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    # View profile button (always visible)
                    ft.IconButton(
                        icon=ft.Icons.VISIBILITY,
                        icon_color="#5C6BC0",
                        icon_size=20,
                        tooltip="View Profile",
                        on_click=lambda e, cid=candidate["id"]: self._view_profile(cid),
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=12,
            bgcolor=bg_color,
            border=ft.border.all(border_width, border_color),
            border_radius=8,
            margin=ft.margin.only(bottom=8),
            ink=True,
            on_click=lambda e, cid=candidate["id"], pos=position: self._select_candidate(cid, pos) if (not is_voted or is_changing) else None,
        )
    
    def _enable_change_vote(self, position):
        """Enable change vote mode for a position"""
        self.change_vote_mode.add(position)
        # Also expand the position
        self.expanded_positions.add(position)
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _toggle_position(self, position):
        """Toggle expand/collapse for a position"""
        if position in self.expanded_positions:
            self.expanded_positions.remove(position)
            # Also exit change mode when collapsing
            self.change_vote_mode.discard(position)
        else:
            self.expanded_positions.add(position)
        
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _select_candidate(self, candidate_id, position):
        """Select a candidate for voting"""
        is_changing = position in self.change_vote_mode
        
        if position in self.submitted_positions and not is_changing:
            return  # Can't change vote unless in change mode
        
        # If changing vote and clicking same candidate, cancel change mode
        if is_changing and self.votes.get(position) == candidate_id:
            self.change_vote_mode.discard(position)
            self._build_ui()
            if self.page:
                self.page.update()
            return
        
        # Toggle selection or select new
        if self.selected_candidates.get(position) == candidate_id:
            # Deselect
            del self.selected_candidates[position]
        else:
            # Select and submit immediately
            self.selected_candidates[position] = candidate_id
            self._submit_vote(position, candidate_id, is_update=is_changing)
    
    def _submit_vote(self, position, candidate_id, is_update=False):
        """Submit vote for a position"""
        # Record the vote
        self.votes[position] = candidate_id
        self.submitted_positions.add(position)
        
        # Save to database
        if self.db:
            try:
                if is_update:
                    self.db.update_vote(self.user_id, candidate_id, position)
                else:
                    self.db.cast_vote(self.user_id, candidate_id, position)
            except Exception as e:
                print(f"Error casting vote: {e}")
        
        # Exit change vote mode if active
        self.change_vote_mode.discard(position)
        
        # Collapse the section after voting
        if position in self.expanded_positions:
            self.expanded_positions.remove(position)
        
        # Clear selection
        if position in self.selected_candidates:
            del self.selected_candidates[position]
        
        # Rebuild UI
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _view_profile(self, candidate_id):
        """View politician profile"""
        if self.on_view_profile:
            self.on_view_profile(candidate_id)
    
    def _build_voting_complete(self):
        """Build voting complete message"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color="#4CAF50", size=24),
                    ft.Column(
                        [
                            ft.Text(
                                "Voting Complete!",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color="#4CAF50",
                            ),
                            ft.Text(
                                "Thank you for participating in the election. Your votes have been recorded.",
                                size=12,
                                color="#666666",
                            ),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                ],
                spacing=16,
            ),
            padding=20,
            bgcolor="#E8F5E9",
            border_radius=12,
            border=ft.border.all(1, "#4CAF50"),
            margin=ft.margin.only(top=8),
        )
