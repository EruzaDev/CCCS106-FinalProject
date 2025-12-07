import flet as ft


class ElectionResults(ft.Column):
    """Election Results page - Shows voting results grouped by position"""
    
    def __init__(self, username, db, on_logout, on_back):
        super().__init__()
        self.username = username
        self.db = db
        self.on_logout = on_logout
        self.on_back = on_back
        
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
        # Get election data
        total_votes = self.db.get_total_votes_cast() if self.db else 0
        unique_voters = self.db.get_unique_voters_count() if self.db else 0
        positions_count = self.db.get_positions_count() if self.db else 0
        
        # Get results by position
        results = self.db.get_election_results() if self.db else []
        
        # Group results by position
        results_by_position = {}
        for result in results:
            user_id, full_name, username, position, party, profile_image, vote_count = result
            if position:
                if position not in results_by_position:
                    results_by_position[position] = []
                results_by_position[position].append({
                    "id": user_id,
                    "name": full_name if full_name else username,
                    "party": party if party else "Independent",
                    "votes": vote_count,
                    "image": profile_image,
                })
        
        # Calculate total votes per position for percentage
        position_totals = {}
        for pos, candidates in results_by_position.items():
            position_totals[pos] = sum(c["votes"] for c in candidates)
        
        return ft.Column(
            [
                # Back button
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.ARROW_BACK, size=16, color="#5C6BC0"),
                            ft.TextButton(
                                "Back to Dashboard",
                                on_click=lambda e: self.on_back(),
                                style=ft.ButtonStyle(color="#5C6BC0"),
                            ),
                        ],
                        spacing=4,
                    ),
                    margin=ft.margin.only(bottom=16),
                ),
                # Election Results Header Card
                self._build_results_header(total_votes, unique_voters, positions_count),
                ft.Container(height=20),
                # Results by position
                *[self._build_position_results(pos, candidates, position_totals.get(pos, 0)) 
                  for pos, candidates in sorted(results_by_position.items())],
                # No votes message
                self._build_no_votes_message() if total_votes == 0 else ft.Container(),
            ],
        )
    
    def _build_results_header(self, total_votes, unique_voters, positions):
        """Build the election results header card"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.BAR_CHART, color=ft.Colors.WHITE, size=24),
                            ft.Text(
                                "Election Results",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=16),
                    ft.Row(
                        [
                            self._build_stat_box("Total Votes Cast", str(total_votes)),
                            self._build_stat_box("Unique Voters", str(unique_voters)),
                            self._build_stat_box("Positions", str(positions)),
                        ],
                        spacing=12,
                    ),
                ],
            ),
            padding=24,
            border_radius=12,
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#7C4DFF", "#536DFE"],
            ),
        )
    
    def _build_stat_box(self, label, value):
        """Build a statistics box"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(label, size=11, color=ft.Colors.WHITE70),
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ],
                spacing=4,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            border_radius=8,
            expand=True,
        )
    
    def _build_position_results(self, position, candidates, total_votes):
        """Build results card for a position"""
        # Sort candidates by votes (descending)
        sorted_candidates = sorted(candidates, key=lambda x: x["votes"], reverse=True)
        
        candidate_rows = []
        for rank, candidate in enumerate(sorted_candidates, 1):
            percentage = (candidate["votes"] / total_votes * 100) if total_votes > 0 else 0
            candidate_rows.append(
                self._build_candidate_row(rank, candidate, percentage)
            )
        
        return ft.Container(
            content=ft.Column(
                [
                    # Position header
                    ft.Row(
                        [
                            ft.Text(position, size=14, weight=ft.FontWeight.BOLD, color="#333333"),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.PEOPLE, size=14, color="#5C6BC0"),
                                    ft.Text(
                                        f"{total_votes} votes cast",
                                        size=12,
                                        color="#5C6BC0",
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=1, color="#E0E0E0"),
                    # Candidate rows
                    *candidate_rows,
                ],
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            margin=ft.margin.only(bottom=16),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def _build_candidate_row(self, rank, candidate, percentage):
        """Build a row for a candidate with their votes"""
        # Determine rank badge color
        rank_colors = {1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32"}
        rank_color = rank_colors.get(rank, "#E8EAF6")
        rank_text_color = "#333333" if rank <= 3 else "#666666"
        
        # Create avatar
        if candidate.get("image"):
            avatar = ft.Container(
                content=ft.Image(
                    src_base64=candidate["image"],
                    fit=ft.ImageFit.COVER,
                    width=44,
                    height=44,
                ),
                width=44,
                height=44,
                border_radius=22,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )
        else:
            avatar = ft.CircleAvatar(
                content=ft.Text(candidate["name"][0].upper() if candidate["name"] else "?"),
                bgcolor="#E8EAF6",
                radius=22,
            )
        
        return ft.Container(
            content=ft.Row(
                [
                    # Rank badge
                    ft.Container(
                        content=ft.Text(str(rank), size=12, weight=ft.FontWeight.BOLD, color=rank_text_color),
                        width=28,
                        height=28,
                        bgcolor=rank_color,
                        border_radius=14,
                        alignment=ft.alignment.center,
                    ),
                    # Avatar
                    avatar,
                    # Name and party
                    ft.Column(
                        [
                            ft.Text(candidate["name"], size=14, weight=ft.FontWeight.W_500),
                            ft.Text(candidate["party"], size=11, color="#666666"),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    # Votes count
                    ft.Column(
                        [
                            ft.Text(str(candidate["votes"]), size=16, weight=ft.FontWeight.BOLD),
                            ft.Text("votes", size=10, color="#666666"),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                    # Percentage bar
                    ft.Column(
                        [
                            ft.Text(f"{percentage:.1f}%", size=12, weight=ft.FontWeight.W_500),
                            ft.ProgressBar(
                                value=percentage / 100,
                                width=100,
                                height=6,
                                color="#7C4DFF",
                                bgcolor="#E8EAF6",
                            ),
                        ],
                        spacing=4,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                spacing=16,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=12),
            border=ft.border.only(bottom=ft.BorderSide(1, "#F5F5F5")),
        )
    
    def _build_no_votes_message(self):
        """Build message when no votes have been cast"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.HOW_TO_VOTE, size=64, color="#CCCCCC"),
                    ft.Container(height=16),
                    ft.Text("No Votes Yet", size=18, weight=ft.FontWeight.BOLD, color="#666666"),
                    ft.Container(height=8),
                    ft.Text(
                        "No votes have been cast yet. Results will appear once voting begins.",
                        size=14,
                        color="#999999",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=60,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            margin=ft.margin.only(top=20),
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
