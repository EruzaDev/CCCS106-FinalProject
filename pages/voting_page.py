import flet as ft


class VotingPage(ft.Column):
    """Voting Page - Cast votes when voting is active"""
    
    def __init__(self, user_id, username, db, on_logout, on_view_profile=None):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.db = db
        self.on_logout = on_logout
        self.on_view_profile = on_view_profile
        
        # Track votes
        self.votes = {}  # position -> candidate_id
        self.submitted_positions = set()
        
        # Get candidates grouped by position
        self.candidates_by_position = self._get_candidates_by_position()
        
        # Check for existing votes
        self._load_existing_votes()
        
        # Build UI
        self._build_ui()
    
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
                    candidates[position].append({
                        "id": user_id,
                        "name": full_name if full_name else username,
                        "party": party if party else "Independent",
                        "image": profile_image,
                    })
        return candidates
    
    def _load_existing_votes(self):
        """Load existing votes for this user"""
        # Check database for existing votes
        # For now, we'll track this session only
        pass
    
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
                # Position cards
                *[self._build_position_card(position, candidates) 
                  for position, candidates in sorted(self.candidates_by_position.items())],
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
    
    def _build_position_card(self, position, candidates):
        """Build a card for a voting position"""
        is_voted = position in self.submitted_positions
        selected_candidate = self.votes.get(position)
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Icon(
                                            ft.Icons.CHECK_CIRCLE if is_voted else ft.Icons.RADIO_BUTTON_UNCHECKED,
                                            color="#4CAF50" if is_voted else "#CCCCCC",
                                            size=20,
                                        ),
                                        bgcolor="#E8F5E9" if is_voted else "#F5F5F5",
                                        border_radius=20,
                                        padding=4,
                                    ),
                                    ft.Text(position, size=16, weight=ft.FontWeight.BOLD),
                                ],
                                spacing=12,
                            ),
                            ft.Text(f"{len(candidates)} candidates", size=12, color="#666666"),
                        ],
                        expand=True,
                    ),
                    ft.ElevatedButton(
                        "Vote Submitted" if is_voted else "Vote Now",
                        icon=ft.Icons.CHECK if is_voted else ft.Icons.HOW_TO_VOTE,
                        bgcolor="#4CAF50" if is_voted else "#5C6BC0",
                        color=ft.Colors.WHITE,
                        disabled=is_voted,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=lambda e, pos=position, cands=candidates: self._show_voting_dialog(pos, cands),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(2, "#4CAF50") if is_voted else None,
            margin=ft.margin.only(bottom=12),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            ),
        )
    
    def _show_voting_dialog(self, position, candidates):
        """Show dialog to vote for a position"""
        selected_id = None
        
        def on_candidate_select(e, candidate_id):
            nonlocal selected_id
            selected_id = candidate_id
            # Update radio buttons visual state
            for control in candidate_list.controls:
                if hasattr(control, 'data') and control.data == candidate_id:
                    control.bgcolor = "#E8EAF6"
                    control.border = ft.border.all(2, "#5C6BC0")
                else:
                    control.bgcolor = ft.Colors.WHITE
                    control.border = ft.border.all(1, "#E0E0E0")
            if self.page:
                self.page.update()
        
        def on_submit(e):
            if selected_id:
                # Cast vote
                self.votes[position] = selected_id
                self.submitted_positions.add(position)
                
                # Save to database
                if self.db:
                    self.db.cast_vote(self.user_id, selected_id, position)
                
                # Close dialog and rebuild UI
                dialog.open = False
                self._build_ui()
                if self.page:
                    self.page.update()
        
        def on_view_profile(e, candidate_id):
            dialog.open = False
            if self.page:
                self.page.update()
            if self.on_view_profile:
                self.on_view_profile(candidate_id)
        
        # Build candidate list
        candidate_controls = []
        for candidate in candidates:
            # Get verification count
            verifications = self.db.get_verifications_by_politician(candidate["id"]) if self.db else []
            verified_count = len([v for v in verifications if v[4] == 'verified'])
            
            # Profile image
            if candidate.get("image"):
                avatar = ft.CircleAvatar(
                    foreground_image_src=f"data:image/png;base64,{candidate['image']}",
                    radius=25,
                )
            else:
                avatar = ft.CircleAvatar(
                    content=ft.Text(candidate["name"][0].upper() if candidate["name"] else "?"),
                    bgcolor="#E8EAF6",
                    radius=25,
                )
            
            candidate_card = ft.Container(
                content=ft.Row(
                    [
                        ft.Radio(value=str(candidate["id"]), fill_color="#5C6BC0"),
                        avatar,
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(candidate["name"], size=14, weight=ft.FontWeight.W_500),
                                        ft.Container(
                                            content=ft.Row(
                                                [
                                                    ft.Icon(ft.Icons.VERIFIED, color=ft.Colors.WHITE, size=10),
                                                    ft.Text("Verified", size=9, color=ft.Colors.WHITE),
                                                ],
                                                spacing=2,
                                            ),
                                            bgcolor="#4CAF50",
                                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                            border_radius=8,
                                            visible=verified_count > 0,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                ft.Text(candidate["party"], size=11, color="#666666"),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.VISIBILITY,
                            icon_color="#5C6BC0",
                            icon_size=20,
                            tooltip="View Profile",
                            on_click=lambda e, cid=candidate["id"]: on_view_profile(e, cid),
                        ),
                    ],
                    spacing=12,
                ),
                padding=12,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, "#E0E0E0"),
                border_radius=8,
                data=candidate["id"],
                ink=True,
                on_click=lambda e, cid=candidate["id"]: on_candidate_select(e, cid),
            )
            candidate_controls.append(candidate_card)
        
        candidate_list = ft.Column(candidate_controls, spacing=8)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Vote for {position}"),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Select your preferred candidate:", size=14, color="#666666"),
                        ft.Container(height=12),
                        candidate_list,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                width=400,
                height=400,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self._close_dialog(dialog)),
                ft.ElevatedButton(
                    "Submit Vote",
                    bgcolor="#5C6BC0",
                    color=ft.Colors.WHITE,
                    on_click=on_submit,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        if self.page:
            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()
    
    def _close_dialog(self, dialog):
        """Close a dialog"""
        dialog.open = False
        if self.page:
            self.page.update()
    
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
