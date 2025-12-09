import flet as ft
from app.theme import AppTheme


class PoliticianProfile(ft.Column):
    """Politician Profile page - View detailed profile and achievements"""
    
    def __init__(self, politician_id, db, on_back, on_logout, username):
        super().__init__()
        self.politician_id = politician_id
        self.db = db
        self.on_back = on_back
        self.on_logout = on_logout
        self.username = username
        
        # Get politician data
        self.politician = self._get_politician_data()
        self.achievements = self._get_achievements()
        
        # Build UI
        self._build_ui()
    
    def _get_politician_data(self):
        """Get politician data from database"""
        if self.db:
            users = self.db.get_all_users()
            for user in users:
                if user[0] == self.politician_id:
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
                    }
        return None
    
    def _get_achievements(self):
        """Get verified achievements for this politician"""
        if self.db:
            verifications = self.db.get_verifications_by_politician(self.politician_id)
            return verifications
        return []
    
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
        if not self.politician:
            return ft.Container(
                content=ft.Text("Politician not found", color="#666666"),
                padding=40,
                alignment=ft.alignment.center,
            )
        
        name = self.politician["full_name"] or self.politician["username"]
        position = self.politician["position"] or "Politician"
        party = self.politician["party"] or "Independent"
        biography = self.politician["biography"] or "No biography available."
        image = self.politician["profile_image"]
        
        # Count verified achievements
        verified_count = len([a for a in self.achievements if a[4] == 'verified'])
        
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
                # Profile card
                ft.Container(
                    content=ft.Column(
                        [
                            # Profile header with gradient
                            self._build_profile_header(name, position, party, image, verified_count),
                            # Biography
                            ft.Container(
                                content=ft.Text(
                                    biography,
                                    size=14,
                                    color="#666666",
                                ),
                                padding=24,
                            ),
                        ],
                        spacing=0,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    ),
                ),
                ft.Container(height=20),
                # Achievements section
                self._build_achievements_section(),
            ],
        )
    
    def _build_profile_header(self, name, position, party, image, verified_count):
        """Build profile header with gradient background"""
        # Profile image
        if image:
            profile_pic = ft.Container(
                content=ft.Image(
                    src_base64=image,
                    fit=ft.ImageFit.COVER,
                    width=120,
                    height=120,
                ),
                width=120,
                height=120,
                border_radius=8,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                border=ft.border.all(4, ft.Colors.WHITE),
            )
        else:
            profile_pic = ft.Container(
                content=ft.Icon(ft.Icons.PERSON, size=60, color="#666666"),
                width=120,
                height=120,
                bgcolor="#E8EAF6",
                border_radius=8,
                alignment=ft.alignment.center,
                border=ft.border.all(4, ft.Colors.WHITE),
            )
        
        return ft.Stack(
            [
                # Gradient background
                ft.Container(
                    height=180,
                    border_radius=ft.border_radius.only(top_left=12, top_right=12),
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.center_left,
                        end=ft.alignment.center_right,
                        colors=["#7C4DFF", "#536DFE"],
                    ),
                ),
                # Profile image positioned at bottom
                ft.Container(
                    content=profile_pic,
                    left=24,
                    top=100,
                ),
                # Name and info
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(name, size=22, weight=ft.FontWeight.BOLD, color="#333333"),
                                    ft.Container(
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
                                    ),
                                ],
                                spacing=12,
                            ),
                            ft.Text(position, size=14, color="#5C6BC0"),
                            ft.Text(party, size=12, color="#666666"),
                        ],
                        spacing=4,
                    ),
                    left=160,
                    top=190,
                ),
            ],
            height=260,
        )
    
    def _build_achievements_section(self):
        """Build achievements and contributions section"""
        verified_achievements = [a for a in self.achievements if a[4] == 'verified']
        
        achievement_items = []
        for achievement in verified_achievements:
            # achievement: (id, title, description, evidence_url, status, created_at)
            achievement_id, title, description, evidence_url, status, created_at = achievement
            
            achievement_items.append(
                self._build_achievement_item(title, description, created_at, status)
            )
        
        if not achievement_items:
            achievement_items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.VERIFIED_USER, size=48, color="#CCCCCC"),
                            ft.Text("No verified achievements yet", color="#666666"),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Achievements & Contributions",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=16),
                    *achievement_items,
                ],
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def _build_achievement_item(self, title, description, created_at, status):
        """Build an achievement item"""
        # Parse date if available
        date_str = ""
        if created_at:
            try:
                date_str = created_at.split(" ")[0] if " " in created_at else created_at
            except:
                date_str = ""
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color="#333333"),
                            ft.Text(description if description else "", size=12, color="#666666"),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=12, color="#999999"),
                                    ft.Text(date_str, size=11, color="#999999"),
                                    ft.Text(" • ", color="#999999"),
                                    ft.Icon(ft.Icons.VERIFIED_USER, size=12, color="#999999"),
                                    ft.Text("Verified by: COMELEC Official", size=11, color="#999999"),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.CHECK_CIRCLE, color="#4CAF50", size=14),
                                ft.Text("Verified", size=12, color="#4CAF50"),
                            ],
                            spacing=4,
                        ),
                        bgcolor="#E8F5E9",
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=16,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=16,
            border=ft.border.only(bottom=ft.BorderSide(1, "#F0F0F0")),
        )
