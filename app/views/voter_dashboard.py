import flet as ft
from app.components.news_feed import NewsFeed
from app.theme import AppTheme


class VoterDashboard(ft.Column):
    """Voter Dashboard - Main dashboard for voters to view candidates and vote"""
    
    def __init__(self, username, db, on_logout, on_profile_view=None, on_compare=None, on_voting_started=None):
        super().__init__()
        self.username = username
        self.db = db
        self.on_logout = on_logout
        self.on_profile_view = on_profile_view
        self.on_compare = on_compare
        self.on_voting_started = on_voting_started
        self.search_query = ""
        self.selected_for_compare = None  # Single candidate selected for comparison {"id": x, "position": y}
        self.compare_mode = False  # When true, filter to same position only
        self.current_tab = "candidates"  # "candidates" or "news"
        
        # UI component references for dynamic updates
        self.search_field = None
        self.candidate_grid_container = None
        self.compare_banner_container = None
        self.content_column = None
        self.news_feed = None
        
        # Get voting status
        self.voting_active = self._get_voting_status()
        
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
            if is_active and not self.voting_active:
                # Voting just started - redirect to voting page
                self.voting_active = True
                if self.on_voting_started:
                    self.on_voting_started()
            elif not is_active and self.voting_active:
                # Voting stopped - refresh dashboard
                self.voting_active = False
                self._build_ui()
                if self.page:
                    self.page.update()
    
    def _get_voting_status(self):
        """Get current voting status from database"""
        if self.db:
            status = self.db.get_voting_status()
            return status.get("is_active", False)
        return False
    
    def _build_ui(self):
        """Build the main UI"""
        # Determine content based on current tab
        if self.current_tab == "news":
            main_content = self._build_news_feed_content()
        elif self.current_tab == "records":
            main_content = self._build_legal_records_content()
        else:
            main_content = self._build_candidates_content()
        
        self.controls = [
            self._build_header(),
            self._build_tab_bar(),
            ft.Container(
                content=ft.Column(
                    [
                        main_content,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                expand=True,
                bgcolor=AppTheme.BG_PRIMARY,
                padding=20,
            ),
        ]
        
        self.expand = True
        self.spacing = 0
    
    def _build_news_feed_content(self):
        """Build the news feed tab content"""
        self.news_feed = NewsFeed(self.db)
        return self.news_feed
    
    def _build_legal_records_content(self):
        """Build the legal records tab content (read-only view for voters)"""
        # Get all legal records
        records = self.db.get_all_legal_records() if self.db else []
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.GAVEL, color=AppTheme.PRIMARY, size=28),
                    ft.Text(
                        "Politician Legal Records",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                ], spacing=12),
                ft.Text(
                    "View verified and pending legal records of politicians. These records are maintained by NBI officers.",
                    size=14,
                    color=AppTheme.TEXT_MUTED,
                ),
            ], spacing=8),
            padding=ft.padding.only(bottom=20),
        )
        
        # Stats row
        verified_count = len([r for r in records if r[6] == "verified"])
        pending_count = len([r for r in records if r[6] == "pending"])
        dismissed_count = len([r for r in records if r[6] == "dismissed"])
        
        stats_row = ft.Container(
            content=ft.Row([
                self._build_record_stat_card("Total Records", len(records), ft.Icons.DESCRIPTION, AppTheme.PRIMARY),
                self._build_record_stat_card("Verified", verified_count, ft.Icons.VERIFIED, "#4CAF50"),
                self._build_record_stat_card("Pending", pending_count, ft.Icons.PENDING, "#FF9800"),
                self._build_record_stat_card("Dismissed", dismissed_count, ft.Icons.CANCEL, "#9E9E9E"),
            ], spacing=16, wrap=True),
            padding=ft.padding.only(bottom=24),
        )
        
        # Records list
        if not records:
            records_content = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=48, color=AppTheme.TEXT_MUTED),
                    ft.Text(
                        "No legal records found",
                        size=16,
                        color=AppTheme.TEXT_MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=40,
                alignment=ft.alignment.center,
            )
        else:
            record_cards = []
            for record in records:
                # record: (id, politician_id, record_type, title, description, record_date, status, created_at, full_name, username, position, party, profile_image)
                record_id = record[0]
                record_type = record[2]
                title = record[3]
                description = record[4]
                record_date = record[5]
                status = record[6]
                politician_name = record[8] or record[9] or "Unknown"
                position = record[10] or "N/A"
                party = record[11] or "N/A"
                
                # Status styling
                if status == "verified":
                    status_color = "#4CAF50"
                    status_icon = ft.Icons.VERIFIED
                    status_bg = "#E8F5E9"
                elif status == "dismissed":
                    status_color = "#9E9E9E"
                    status_icon = ft.Icons.CANCEL
                    status_bg = "#F5F5F5"
                else:  # pending
                    status_color = "#FF9800"
                    status_icon = ft.Icons.PENDING
                    status_bg = "#FFF3E0"
                
                # Record type styling
                type_colors = {
                    "criminal": "#F44336",
                    "civil": "#2196F3",
                    "administrative": "#FF9800",
                    "regulatory": "#9C27B0",
                }
                type_color = type_colors.get(record_type, "#757575")
                
                card = ft.Container(
                    content=ft.Column([
                        # Header row with politician info and status
                        ft.Row([
                            ft.Column([
                                ft.Text(
                                    politician_name,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=AppTheme.TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    f"{position} • {party}",
                                    size=12,
                                    color=AppTheme.TEXT_MUTED,
                                ),
                            ], spacing=2, expand=True),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(status_icon, size=14, color=status_color),
                                    ft.Text(status.capitalize(), size=12, color=status_color, weight=ft.FontWeight.W_500),
                                ], spacing=4),
                                bgcolor=status_bg,
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=12,
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Divider(height=1, color=AppTheme.BORDER_LIGHT),
                        
                        # Record details
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    record_type.capitalize() if record_type else "Unknown",
                                    size=11,
                                    color=ft.Colors.WHITE,
                                    weight=ft.FontWeight.W_500,
                                ),
                                bgcolor=type_color,
                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                border_radius=4,
                            ),
                            ft.Text(f"Date: {record_date or 'N/A'}", size=12, color=AppTheme.TEXT_MUTED),
                        ], spacing=12),
                        
                        ft.Text(
                            title or "No Title",
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        
                        ft.Text(
                            description or "No description available",
                            size=13,
                            color=AppTheme.TEXT_SECONDARY,
                        ),
                    ], spacing=10),
                    bgcolor=ft.Colors.WHITE,
                    padding=16,
                    border_radius=12,
                    border=ft.border.all(1, AppTheme.BORDER_LIGHT),
                )
                record_cards.append(card)
            
            records_content = ft.Column(record_cards, spacing=12)
        
        return ft.Column([
            header,
            stats_row,
            records_content,
        ], spacing=0)
    
    def _build_record_stat_card(self, label, count, icon, color):
        """Build a stat card for legal records"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=color, size=20),
                    bgcolor=f"{color}20",
                    padding=8,
                    border_radius=8,
                ),
                ft.Column([
                    ft.Text(str(count), size=20, weight=ft.FontWeight.BOLD, color=AppTheme.TEXT_PRIMARY),
                    ft.Text(label, size=11, color=AppTheme.TEXT_MUTED),
                ], spacing=0),
            ], spacing=12),
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            border_radius=10,
            border=ft.border.all(1, AppTheme.BORDER_LIGHT),
        )

    def _build_candidates_content(self):
        """Build the candidates tab content (original _build_content)"""
        # Get filtered politicians
        politicians = self._get_filtered_politicians()
        
        # Create search bar with stored reference
        self.search_field = ft.TextField(
            hint_text="Search candidates by name, position, or party...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=12,
            height=50,
            bgcolor=AppTheme.BG_CARD,
            border_color=AppTheme.BORDER_LIGHT,
            focused_border_color=AppTheme.PRIMARY,
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
            bgcolor=AppTheme.SUCCESS,
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
                                bgcolor=AppTheme.PRIMARY,
                                border_radius=10,
                                padding=10,
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=8,
                                    color=ft.Colors.with_opacity(0.3, AppTheme.PRIMARY),
                                ),
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "HonestBallot",
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        f"Welcome, {self.username}",
                                        size=12,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=14,
                    ),
                    ft.Row(
                        [
                            voting_badge,
                            ft.Container(width=16),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.LOGOUT, color=AppTheme.PRIMARY, size=18),
                                        ft.Text("Logout", color=AppTheme.PRIMARY, size=14),
                                    ],
                                    spacing=6,
                                ),
                                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                border_radius=20,
                                bgcolor=AppTheme.SURFACE_LIGHT,
                                on_click=lambda e: self.on_logout(),
                                ink=True,
                            ),
                        ],
                        spacing=4,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            bgcolor=AppTheme.BG_CARD,
            border=ft.border.only(bottom=ft.BorderSide(1, AppTheme.BORDER_LIGHT)),
        )
    
    def _build_tab_bar(self):
        """Build the tab bar for switching between Candidates and News Feed"""
        def create_tab(icon, label, tab_id):
            is_selected = self.current_tab == tab_id
            return ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            icon,
                            color=AppTheme.PRIMARY if is_selected else AppTheme.TEXT_MUTED,
                            size=20,
                        ),
                        ft.Text(
                            label,
                            size=14,
                            weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL,
                            color=AppTheme.PRIMARY if is_selected else AppTheme.TEXT_MUTED,
                        ),
                    ],
                    spacing=8,
                ),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                border=ft.border.only(
                    bottom=ft.BorderSide(3, AppTheme.PRIMARY) if is_selected else None
                ),
                bgcolor=AppTheme.SURFACE_LIGHT if is_selected else None,
                on_click=lambda e, t=tab_id: self._switch_tab(t),
                ink=True,
            )
        
        return ft.Container(
            content=ft.Row(
                [
                    create_tab(ft.Icons.PEOPLE, "Candidates", "candidates"),
                    create_tab(ft.Icons.NEWSPAPER, "News Feed", "news"),
                    create_tab(ft.Icons.GAVEL, "Legal Records", "records"),
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(bottom=ft.BorderSide(1, AppTheme.BORDER_COLOR)),
            padding=ft.padding.only(left=24),
        )
    
    def _switch_tab(self, tab_id):
        """Switch between tabs"""
        if self.current_tab != tab_id:
            self.current_tab = tab_id
            self._build_ui()
            if self.page:
                self.page.update()
    
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
                            ft.Icon(ft.Icons.COMPARE_ARROWS, color=AppTheme.PRIMARY, size=24),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Compare Mode Active",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        f"Select another {self.selected_for_compare['position']} candidate to compare with {selected_name}",
                                        size=12,
                                        color=AppTheme.TEXT_SECONDARY,
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
            bgcolor=AppTheme.BG_PRIMARY,
            border_radius=12,
            border=ft.border.all(2, AppTheme.PRIMARY),
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
        """Build responsive grid of candidate cards"""
        if not politicians:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=64, color=AppTheme.BORDER_COLOR),
                        ft.Text("No candidates found", size=16, color=AppTheme.TEXT_SECONDARY),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                padding=40,
                alignment=ft.alignment.center,
            )
        
        # Create responsive cards using ResponsiveRow
        # col breakpoints: xs (extra small), sm (small), md (medium), lg (large), xl (extra large)
        # Values represent number of columns out of 12
        cards = []
        
        for politician in politicians:
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
            
            # Wrap card in responsive container
            # xs=12 (1 card per row on phones)
            # sm=6 (2 cards per row on small tablets)
            # md=4 (3 cards per row on tablets/small desktops)
            # lg=3 (4 cards per row on desktops)
            # xl=2 (6 cards per row on large screens)
            responsive_card = ft.Container(
                content=card,
                col={"xs": 12, "sm": 6, "md": 4, "lg": 3, "xl": 2},
            )
            cards.append(responsive_card)
        
        return ft.ResponsiveRow(cards, spacing=16, run_spacing=16)
    
    def _build_candidate_card(self, user_id, name, position, party, biography, image, verified_count, pending_count, is_selected=False):
        """Build a candidate card with consistent sizing"""
        # Fixed dimensions for consistent card layout
        CARD_IMAGE_HEIGHT = 140
        CARD_MIN_HEIGHT = 380
        
        # Create avatar/image with fixed height
        if image:
            profile_image = ft.Container(
                content=ft.Image(
                    src_base64=image,
                    fit=ft.ImageFit.COVER,
                    width=float("inf"),
                    height=CARD_IMAGE_HEIGHT,
                ),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                border_radius=ft.border_radius.only(top_left=12, top_right=12),
                height=CARD_IMAGE_HEIGHT,
            )
        else:
            profile_image = ft.Container(
                content=ft.Icon(ft.Icons.PERSON, size=60, color=AppTheme.BORDER_COLOR),
                bgcolor=AppTheme.BG_PRIMARY,
                height=CARD_IMAGE_HEIGHT,
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
        compare_icon_color = ft.Colors.WHITE if is_selected else AppTheme.PRIMARY
        compare_bg = AppTheme.PRIMARY if is_selected else ft.Colors.with_opacity(0.9, ft.Colors.WHITE)
        
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
        card_border = ft.border.all(3, AppTheme.PRIMARY) if is_selected else None
        card_shadow_color = ft.Colors.with_opacity(0.3, AppTheme.PRIMARY) if is_selected else ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
        
        # Truncate biography to consistent length
        bio_display = biography[:70] + "..." if len(biography) > 70 else biography
        if not bio_display:
            bio_display = "No biography available."
        
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
                        ],
                        height=CARD_IMAGE_HEIGHT,
                    ),
                    # Info section with fixed height
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    name, 
                                    size=14, 
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(position, size=12, color=AppTheme.PRIMARY),
                                ft.Text(party, size=11, color=AppTheme.TEXT_SECONDARY),
                                ft.Container(height=4),
                                ft.Text(
                                    bio_display,
                                    size=11,
                                    color=AppTheme.TEXT_SECONDARY,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Container(height=4),
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.VERIFIED, color="#4CAF50", size=14),
                                        ft.Text(f"{verified_count} Verified", size=11, color=AppTheme.TEXT_SECONDARY),
                                    ],
                                    spacing=4,
                                ),
                                ft.Container(expand=True),  # Spacer to push buttons to bottom
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "View Profile",
                                            icon=ft.Icons.PERSON,
                                            bgcolor=AppTheme.PRIMARY,
                                            color=ft.Colors.WHITE,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                            ),
                                            expand=True,
                                            on_click=lambda e, uid=user_id: self._view_profile(uid),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.CHECK if is_selected else ft.Icons.COMPARE_ARROWS,
                                            icon_color=ft.Colors.WHITE if is_selected else AppTheme.PRIMARY,
                                            bgcolor=AppTheme.PRIMARY if is_selected else None,
                                            tooltip="Remove from compare" if is_selected else "Compare",
                                            on_click=lambda e, uid=user_id, pos=position: self._toggle_compare(uid, pos),
                                        ),
                                    ],
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        padding=12,
                        bgcolor=AppTheme.BG_PRIMARY if is_selected else None,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            height=CARD_MIN_HEIGHT,
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
