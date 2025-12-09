import flet as ft
from app.theme import AppTheme


class CandidateComparison(ft.Column):
    """Candidate Comparison page - Compare two candidates side by side"""
    
    def __init__(self, candidate1_id, candidate2_id, db, on_back, on_logout, username):
        super().__init__()
        self.candidate1_id = candidate1_id
        self.candidate2_id = candidate2_id
        self.db = db
        self.on_back = on_back
        self.on_logout = on_logout
        self.username = username
        
        # Get candidate data
        self.candidate1 = self._get_candidate_data(candidate1_id)
        self.candidate2 = self._get_candidate_data(candidate2_id)
        
        # Build UI
        self._build_ui()
    
    def _get_candidate_data(self, candidate_id):
        """Get candidate data from database"""
        if self.db:
            users = self.db.get_all_users()
            for user in users:
                if user[0] == candidate_id:
                    # Get achievements
                    verifications = self.db.get_verifications_by_politician(candidate_id)
                    verified = [v for v in verifications if v[4] == 'verified']
                    pending = [v for v in verifications if v[4] == 'pending']
                    
                    return {
                        "id": user[0],
                        "username": user[1],
                        "email": user[2],
                        "role": user[3],
                        "full_name": user[5],
                        "status": user[6],
                        "position": user[7],
                        "party": user[8],
                        "biography": user[9],
                        "profile_image": user[10],
                        "verified_achievements": verified,
                        "pending_achievements": pending,
                    }
        return None
    
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
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[AppTheme.BG_SECONDARY, AppTheme.BG_PRIMARY],
                ),
                padding=20,
            ),
        ]
        
        self.expand = True
        self.spacing = 0
    
    def _build_header(self):
        """Build the header"""
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
        if not self.candidate1 or not self.candidate2:
            return ft.Container(
                content=ft.Text("One or both candidates not found", color="#666666"),
                padding=40,
                alignment=ft.alignment.center,
            )
        
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
                # Title
                ft.Text("Candidate Comparison", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                # Comparison cards side by side
                ft.Row(
                    [
                        self._build_candidate_card(self.candidate1),
                        self._build_candidate_card(self.candidate2),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        )
    
    def _build_candidate_card(self, candidate):
        """Build comparison card for a candidate"""
        name = candidate["full_name"] or candidate["username"]
        position = candidate["position"] or "Politician"
        party = candidate["party"] or "Independent"
        image = candidate["profile_image"]
        verified_count = len(candidate["verified_achievements"])
        pending_count = len(candidate["pending_achievements"])
        total_achievements = verified_count + pending_count
        
        # Profile image
        if image:
            profile_pic = ft.Container(
                content=ft.Image(
                    src_base64=image,
                    fit=ft.ImageFit.COVER,
                    width=200,
                    height=180,
                ),
                width=200,
                height=180,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                border_radius=ft.border_radius.only(top_left=12, top_right=12),
            )
        else:
            profile_pic = ft.Container(
                content=ft.Icon(ft.Icons.PERSON, size=60, color="#CCCCCC"),
                width=200,
                height=180,
                bgcolor="#E8EAF6",
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
        
        # Build achievements list
        achievements_list = []
        for achievement in candidate["verified_achievements"][:3]:  # Show max 3
            achievements_list.append(
                ft.Row(
                    [
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color="#4CAF50", size=14),
                        ft.Text(achievement[1], size=11, color="#666666"),  # title
                    ],
                    spacing=8,
                )
            )
        
        # Check for any legal issues (placeholder - could be from NBI)
        has_legal_issues = False  # This could come from database
        
        return ft.Container(
            content=ft.Column(
                [
                    # Image with badge overlay
                    ft.Stack(
                        [
                            profile_pic,
                            ft.Container(
                                content=verification_badge,
                                left=10,
                                top=10,
                            ),
                        ],
                    ),
                    # Info section
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(name, size=16, weight=ft.FontWeight.BOLD),
                                ft.Text(position, size=12, color="#5C6BC0"),
                                ft.Text(party, size=11, color="#666666"),
                                ft.Divider(height=16),
                                # Stats
                                ft.Row(
                                    [
                                        ft.Text("Verified Status:", size=12, color="#666666"),
                                        ft.Container(
                                            content=ft.Row(
                                                [
                                                    ft.Icon(ft.Icons.VERIFIED, color="#4CAF50", size=14),
                                                    ft.Text("Verified", size=11, color="#4CAF50"),
                                                ],
                                                spacing=4,
                                            ),
                                            bgcolor="#E8F5E9",
                                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                            border_radius=8,
                                        ) if verified_count > 0 else ft.Text("Pending", size=11, color="#FF9800"),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Container(height=8),
                                ft.Row(
                                    [
                                        ft.Text("COMELEC Approved:", size=12, color="#666666"),
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.CHECK_CIRCLE, color="#4CAF50", size=14),
                                                ft.Text("Yes", size=11, color="#4CAF50"),
                                            ],
                                            spacing=4,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Container(height=8),
                                ft.Row(
                                    [
                                        ft.Text("Achievements:", size=12, color="#666666"),
                                        ft.Text(
                                            f"{verified_count}/{total_achievements} verified",
                                            size=11,
                                            color="#5C6BC0",
                                            weight=ft.FontWeight.W_500,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                # Pending issues
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Text("Pending Issues", size=12, color="#666666"),
                                            ft.Text(str(pending_count), size=11, color="#FF9800"),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    visible=pending_count > 0,
                                    margin=ft.margin.only(top=8),
                                ),
                                ft.Divider(height=16),
                                # Key Achievements
                                ft.Text("Key Achievements", size=12, weight=ft.FontWeight.BOLD, color="#333333"),
                                ft.Container(height=8),
                                ft.Column(
                                    achievements_list if achievements_list else [
                                        ft.Text("No verified achievements yet", size=11, color="#999999")
                                    ],
                                    spacing=4,
                                ),
                                # Legal issues warning
                                ft.Container(
                                    content=ft.Container(
                                        content=ft.Text(
                                            "✓ Legal record on file",
                                            size=11,
                                            color="#4CAF50",
                                        ),
                                        bgcolor="#E8F5E9",
                                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                        border_radius=8,
                                    ),
                                    margin=ft.margin.only(top=12),
                                ),
                            ],
                        ),
                        padding=16,
                    ),
                ],
                spacing=0,
            ),
            width=280,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
