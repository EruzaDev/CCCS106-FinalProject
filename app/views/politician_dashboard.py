import flet as ft
from datetime import datetime
from app.components.news_post_creator import NewsPostCreator, MyPostsList
from app.theme import AppTheme
from components.date_picker_field import DatePickerField


class PoliticianDashboard(ft.Column):
    """Politician Dashboard - View and manage politician profile and achievements"""
    
    def __init__(self, user_id, username, db, on_logout, on_audit_log=None):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.db = db
        self.on_logout = on_logout
        self.on_audit_log = on_audit_log
        
        # Get politician data
        self.politician = self._get_politician_data()
        self.achievements = self._get_achievements()
        
        # Form state
        self.show_add_form = False
        self.show_edit_profile = False
        
        # Form fields
        self.title_field = None
        self.description_field = None
        self.date_field = None
        
        # Edit profile fields
        self.edit_full_name = None
        self.edit_username = None
        self.edit_password = None
        self.edit_confirm_password = None
        self.edit_position = None
        self.edit_party = None
        self.edit_biography = None
        self.edit_image_data = None
        
        # File picker for profile image
        self.file_picker = ft.FilePicker(on_result=self._on_image_selected)
        
        # Build UI
        self._build_ui()
    
    def _get_politician_data(self):
        """Get politician data from database"""
        if self.db:
            users = self.db.get_all_users()
            for user in users:
                if user[0] == self.user_id:
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
        """Get achievements for this politician"""
        if self.db:
            verifications = self.db.get_verifications_by_politician(self.user_id)
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
                                content=ft.Text(
                                    (self.politician["full_name"] or self.username)[0].upper(),
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ) if not self.politician.get("profile_image") else ft.Image(
                                    src_base64=self.politician["profile_image"],
                                    fit=ft.ImageFit.COVER,
                                    width=40,
                                    height=40,
                                ),
                                width=40,
                                height=40,
                                bgcolor=AppTheme.PRIMARY if not self.politician.get("profile_image") else None,
                                border_radius=20,
                                alignment=ft.alignment.center,
                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Politician Dashboard",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        f"Welcome, {self.politician['full_name'] or self.username}",
                                        size=12,
                                        color=AppTheme.TEXT_SECONDARY,
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
                                icon=ft.Icons.HISTORY,
                                icon_color=AppTheme.PRIMARY,
                                tooltip="Audit Logs",
                                on_click=lambda e: self.on_audit_log() if self.on_audit_log else None,
                            ),
                            ft.Icon(ft.Icons.LOGOUT, color=AppTheme.PRIMARY, size=18),
                            ft.TextButton(
                                "Logout",
                                on_click=lambda e: self.on_logout(),
                                style=ft.ButtonStyle(
                                    color=AppTheme.PRIMARY,
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
            border=ft.border.only(bottom=ft.BorderSide(1, AppTheme.BORDER_COLOR)),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.08, AppTheme.PRIMARY),
            ),
        )
    
    def _build_content(self):
        """Build main content area"""
        if not self.politician:
            return ft.Container(
                content=ft.Text("Politician data not found", color=AppTheme.TEXT_SECONDARY),
                padding=40,
                alignment=ft.alignment.center,
            )
        
        return ft.Column(
            [
                # Profile Card
                self._build_profile_card(),
                ft.Container(height=20),
                # Statistics Row
                self._build_statistics_row(),
                ft.Container(height=20),
                # Achievements Section
                self._build_achievements_section(),
                ft.Container(height=20),
                # News Post Creator
                self._build_news_section(),
            ],
        )
    
    def _build_profile_card(self):
        """Build the profile card with politician info"""
        name = self.politician["full_name"] or self.username
        position = self.politician["position"] or "Politician"
        party = self.politician["party"] or "Independent"
        biography = self.politician["biography"] or "No biography available."
        image = self.politician["profile_image"]
        status = self.politician["status"]
        
        # Profile image
        if image:
            profile_pic = ft.Container(
                content=ft.Image(
                    src_base64=image,
                    fit=ft.ImageFit.COVER,
                    width=80,
                    height=80,
                ),
                width=80,
                height=80,
                border_radius=40,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )
        else:
            profile_pic = ft.Container(
                content=ft.Text(
                    name[0].upper() if name else "?",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                width=80,
                height=80,
                bgcolor=AppTheme.PRIMARY,
                border_radius=40,
                alignment=ft.alignment.center,
            )
        
        # Verified badge
        verified_count = len([a for a in self.achievements if a[4] == 'verified'])
        verified_badge = ft.Container(
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
        
        # Status badge
        status_badge = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE, size=12),
                    ft.Text("COMELEC Approved", size=10, color=ft.Colors.WHITE),
                ],
                spacing=4,
            ),
            bgcolor="#2196F3",
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=12,
            visible=status == "active",
        )
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            profile_pic,
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                                            verified_badge,
                                            status_badge,
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Text(position, size=14, color=AppTheme.PRIMARY),
                                    ft.Text(party, size=12, color=AppTheme.TEXT_SECONDARY),
                                    ft.Container(height=4),
                                    ft.Text(
                                        biography[:100] + "..." if len(biography) > 100 else biography,
                                        size=12,
                                        color=AppTheme.TEXT_SECONDARY,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=16,
                        expand=True,
                    ),
                    ft.TextButton(
                        "Edit Profile",
                        icon=ft.Icons.EDIT,
                        style=ft.ButtonStyle(color=AppTheme.PRIMARY),
                        on_click=lambda e: self._toggle_edit_profile(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, AppTheme.PRIMARY),
            ),
        )
    
    def _build_statistics_row(self):
        """Build responsive statistics row"""
        total = len(self.achievements)
        verified = len([a for a in self.achievements if a[4] == 'verified'])
        records = 0  # Placeholder for NBI records
        
        return ft.ResponsiveRow(
            [
                ft.Container(
                    content=self._build_stat_card("Total Achievements", str(total), ft.Icons.EMOJI_EVENTS, AppTheme.PRIMARY),
                    col={"xs": 12, "sm": 6, "md": 4},
                ),
                ft.Container(
                    content=self._build_stat_card("Verified Achievements", str(verified), ft.Icons.VERIFIED, "#4CAF50"),
                    col={"xs": 12, "sm": 6, "md": 4},
                ),
                ft.Container(
                    content=self._build_stat_card("Records on File", str(records), ft.Icons.DESCRIPTION, "#FF9800"),
                    col={"xs": 12, "sm": 12, "md": 4},
                ),
            ],
            spacing=16,
            run_spacing=16,
        )
    
    def _build_stat_card(self, label, value, icon, color):
        """Build a statistic card"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(label, size=12, color=AppTheme.TEXT_SECONDARY),
                    ft.Container(height=8),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(icon, color=color, size=24),
                                bgcolor=ft.Colors.with_opacity(0.1, color),
                                border_radius=20,
                                padding=8,
                            ),
                            ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=color),
                        ],
                        spacing=12,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            ),
        )
    
    def _build_achievements_section(self):
        """Build achievements section"""
        achievement_items = []
        
        # Add achievement form if visible
        if self.show_add_form:
            achievement_items.append(self._build_add_achievement_form())
            achievement_items.append(ft.Container(height=16))
        
        # Edit profile form if visible
        if self.show_edit_profile:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "Edit Profile",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                        ft.Container(height=16),
                        self._build_edit_profile_form(),
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
        
        # Achievement items
        for achievement in self.achievements:
            ver_id, title, description, evidence_url, status, created_at = achievement
            achievement_items.append(
                self._build_achievement_item(ver_id, title, description, status, created_at)
            )
        
        if not self.achievements and not self.show_add_form:
            achievement_items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.EMOJI_EVENTS, color=AppTheme.BORDER_COLOR, size=48),
                            ft.Text("No achievements yet", color=AppTheme.TEXT_SECONDARY, size=14),
                            ft.Text("Click 'Add Achievement' to submit your first achievement.", color=AppTheme.TEXT_SECONDARY, size=12),
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
                    ft.Row(
                        [
                            ft.Text(
                                "My Achievements",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.ElevatedButton(
                                "Add Achievement",
                                icon=ft.Icons.ADD,
                                bgcolor="#4CAF50",
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e: self._toggle_add_form(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
                blur_radius=4,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def _build_add_achievement_form(self):
        """Build add achievement form"""
        self.title_field = ft.TextField(
            label="Title",
            hint_text="e.g., Healthcare Reform Bill",
            border_radius=8,
            bgcolor="#FAFAFA",
        )
        
        self.description_field = ft.TextField(
            label="Description",
            hint_text="Describe your achievement and its impact...",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=8,
            bgcolor="#FAFAFA",
        )
        
        self.date_field = DatePickerField(
            label="Date",
            width=250,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Add New Achievement", size=14, weight=ft.FontWeight.W_500),
                    ft.Container(height=12),
                    self.title_field,
                    ft.Container(height=12),
                    self.description_field,
                    ft.Container(height=12),
                    self.date_field,
                    ft.Container(height=16),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Submit for Verification",
                                bgcolor=AppTheme.PRIMARY,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e: self._submit_achievement(),
                            ),
                            ft.OutlinedButton(
                                "Cancel",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e: self._toggle_add_form(),
                            ),
                        ],
                        spacing=12,
                    ),
                ],
            ),
            padding=16,
            bgcolor=AppTheme.BG_SECONDARY,
            border_radius=8,
            border=ft.border.all(1, AppTheme.BORDER_COLOR),
        )
    
    def _build_achievement_item(self, ver_id, title, description, status, created_at):
        """Build an achievement item"""
        # Status badge
        if status == "verified":
            status_badge = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color="#4CAF50", size=14),
                        ft.Text("Verified", size=12, color="#4CAF50"),
                    ],
                    spacing=4,
                ),
            )
            status_color = "#4CAF50"
        elif status == "rejected":
            status_badge = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.CANCEL, color="#F44336", size=14),
                        ft.Text("Rejected", size=12, color="#F44336"),
                    ],
                    spacing=4,
                ),
            )
            status_color = "#F44336"
        else:
            status_badge = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.PENDING, color="#FF9800", size=14),
                        ft.Text("Pending", size=12, color="#FF9800"),
                    ],
                    spacing=4,
                ),
            )
            status_color = "#FF9800"
        
        # Format date
        if created_at:
            try:
                date_obj = datetime.strptime(created_at.split(" ")[0], "%Y-%m-%d")
                formatted_date = date_obj.strftime("%m/%d/%Y")
            except:
                formatted_date = created_at
        else:
            formatted_date = "N/A"
        
        # Verified by info
        verified_by_text = "Verified by: COMELEC Official" if status == "verified" else ""
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(title, size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                description if description else "No description provided.",
                                size=12,
                                color=AppTheme.TEXT_SECONDARY,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=12, color=AppTheme.TEXT_SECONDARY),
                                    ft.Text(formatted_date, size=11, color=AppTheme.TEXT_SECONDARY),
                                    ft.Text(verified_by_text, size=11, color=AppTheme.TEXT_SECONDARY) if verified_by_text else ft.Container(),
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    status_badge,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=16,
            bgcolor="#FAFAFA",
            border_radius=8,
            margin=ft.margin.only(bottom=12),
            border=ft.border.only(left=ft.BorderSide(3, status_color)),
        )
    
    def _build_edit_profile_form(self):
        """Build edit profile form"""
        self.edit_full_name = ft.TextField(
            label="Full Name",
            value=self.politician.get("full_name") or "",
            border_radius=8,
            bgcolor="#FAFAFA",
        )
        
        self.edit_username = ft.TextField(
            label="Username",
            value=self.politician.get("username") or "",
            border_radius=8,
            bgcolor="#FAFAFA",
        )
        
        self.edit_password = ft.TextField(
            label="New Password (leave blank to keep current)",
            password=True,
            can_reveal_password=True,
            border_radius=8,
            bgcolor="#FAFAFA",
        )
        
        self.edit_confirm_password = ft.TextField(
            label="Confirm New Password",
            password=True,
            can_reveal_password=True,
            border_radius=8,
            bgcolor="#FAFAFA",
        )
        
        self.edit_position = ft.Dropdown(
            label="Position",
            value=self.politician.get("position") or "",
            options=[
                ft.dropdown.Option("President"),
                ft.dropdown.Option("Vice President"),
                ft.dropdown.Option("Senator"),
                ft.dropdown.Option("Governor"),
                ft.dropdown.Option("Vice Governor"),
                ft.dropdown.Option("Mayor"),
                ft.dropdown.Option("Vice Mayor"),
                ft.dropdown.Option("Congressman"),
                ft.dropdown.Option("Councilor"),
                ft.dropdown.Option("Barangay Captain"),
            ],
            border_radius=8,
            bgcolor="#FAFAFA",
        )
        
        self.edit_party = ft.Dropdown(
            label="Political Party",
            value=self.politician.get("party") or "",
            options=[
                ft.dropdown.Option("PDP-Laban"),
                ft.dropdown.Option("Liberal Party"),
                ft.dropdown.Option("Nacionalista Party"),
                ft.dropdown.Option("NPC (Nationalist People's Coalition)"),
                ft.dropdown.Option("Lakas-CMD"),
                ft.dropdown.Option("NUP (National Unity Party)"),
                ft.dropdown.Option("Aksyon Demokratiko"),
                ft.dropdown.Option("Progressive Alliance"),
                ft.dropdown.Option("United Citizens Party"),
                ft.dropdown.Option("Green Coalition"),
                ft.dropdown.Option("Democratic Reform Party"),
                ft.dropdown.Option("Independent"),
            ],
            border_radius=8,
            bgcolor="#FAFAFA",
        )
        
        self.edit_biography = ft.TextField(
            label="Biography",
            value=self.politician.get("biography") or "",
            multiline=True,
            min_lines=4,
            max_lines=8,
            border_radius=8,
            bgcolor="#FAFAFA",
        )
        
        # Profile image preview
        current_image = self.politician.get("profile_image")
        if current_image:
            image_preview = ft.Container(
                content=ft.Image(
                    src_base64=current_image,
                    fit=ft.ImageFit.COVER,
                    width=100,
                    height=100,
                ),
                width=100,
                height=100,
                border_radius=50,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )
        else:
            image_preview = ft.Container(
                content=ft.Icon(ft.Icons.PERSON, size=40, color="#CCCCCC"),
                width=100,
                height=100,
                bgcolor="#E8EAF6",
                border_radius=50,
                alignment=ft.alignment.center,
            )
        
        return ft.Column(
            [
                # Profile image section
                ft.Row(
                    [
                        image_preview,
                        ft.Column(
                            [
                                ft.Text("Profile Picture", size=14, weight=ft.FontWeight.W_500),
                                ft.Text("Upload a professional photo", size=12, color=AppTheme.TEXT_SECONDARY),
                                ft.ElevatedButton(
                                    "Choose Image",
                                    icon=ft.Icons.UPLOAD,
                                    bgcolor=AppTheme.BG_PRIMARY,
                                    color=AppTheme.PRIMARY,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=lambda e: self.file_picker.pick_files(
                                        allowed_extensions=["png", "jpg", "jpeg"],
                                        allow_multiple=False,
                                    ),
                                ),
                            ],
                            spacing=4,
                        ),
                    ],
                    spacing=16,
                ),
                ft.Container(height=20),
                self.edit_full_name,
                ft.Container(height=12),
                self.edit_username,
                ft.Container(height=12),
                ft.Row(
                    [
                        ft.Container(content=self.edit_password, expand=True),
                        ft.Container(content=self.edit_confirm_password, expand=True),
                    ],
                    spacing=12,
                ),
                ft.Container(height=12),
                ft.Row(
                    [
                        ft.Container(content=self.edit_position, expand=True),
                        ft.Container(content=self.edit_party, expand=True),
                    ],
                    spacing=12,
                ),
                ft.Container(height=12),
                self.edit_biography,
                ft.Container(height=20),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Save Changes",
                            icon=ft.Icons.SAVE,
                            bgcolor="#4CAF50",
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=lambda e: self._save_profile(),
                        ),
                        ft.OutlinedButton(
                            "Cancel",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=lambda e: self._toggle_edit_profile(),
                        ),
                    ],
                    spacing=12,
                ),
            ],
        )
    
    def _toggle_add_form(self):
        """Toggle add achievement form visibility"""
        self.show_add_form = not self.show_add_form
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _toggle_edit_profile(self):
        """Toggle edit profile form visibility"""
        self.show_edit_profile = not self.show_edit_profile
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _submit_achievement(self):
        """Submit achievement for verification"""
        if not self.title_field or not self.title_field.value:
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Please enter a title"),
                    bgcolor="#F44336",
                )
                self.page.snack_bar.open = True
                self.page.update()
            return
        
        title = self.title_field.value
        description = self.description_field.value if self.description_field else ""
        
        # Save to database
        if self.db:
            self.db.create_achievement_verification(
                self.user_id,
                title,
                description,
                None  # evidence_url
            )
        
        # Refresh data and UI
        self.achievements = self._get_achievements()
        self.show_add_form = False
        self._build_ui()
        
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Achievement submitted for verification"),
                bgcolor="#4CAF50",
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _save_profile(self):
        """Save profile changes"""
        if not self.edit_full_name:
            return
        
        full_name = self.edit_full_name.value
        username = self.edit_username.value if self.edit_username else self.politician.get("username")
        password = self.edit_password.value if self.edit_password else ""
        confirm_password = self.edit_confirm_password.value if self.edit_confirm_password else ""
        position = self.edit_position.value if self.edit_position else ""
        party = self.edit_party.value if self.edit_party else ""
        biography = self.edit_biography.value if self.edit_biography else ""
        
        # Validate username
        if not username:
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Username is required"),
                    bgcolor="#F44336",
                )
                self.page.snack_bar.open = True
                self.page.update()
            return
        
        # Validate password match if changing password
        if password:
            if password != confirm_password:
                if self.page:
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text("Passwords do not match"),
                        bgcolor="#F44336",
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                return
            if len(password) < 4:
                if self.page:
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text("Password must be at least 4 characters"),
                        bgcolor="#F44336",
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                return
        
        # Update in database
        if self.db:
            try:
                if password:
                    # Update with new password
                    self.db.update_politician_with_password(
                        self.user_id,
                        full_name,
                        self.politician.get("email"),
                        username,
                        position,
                        party,
                        biography,
                        password,
                        self.edit_image_data
                    )
                elif self.edit_image_data:
                    self.db.update_politician(
                        self.user_id,
                        full_name,
                        self.politician.get("email"),
                        username,
                        position,
                        party,
                        biography,
                        self.edit_image_data
                    )
                else:
                    self.db.update_politician(
                        self.user_id,
                        full_name,
                        self.politician.get("email"),
                        username,
                        position,
                        party,
                        biography
                    )
            except Exception as ex:
                if self.page:
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"Error: Username may already be taken"),
                        bgcolor="#F44336",
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                return
        
        # Refresh data
        self.politician = self._get_politician_data()
        self.show_edit_profile = False
        self.edit_image_data = None
        self._build_ui()
        
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Profile updated successfully"),
                bgcolor="#4CAF50",
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _on_image_selected(self, e: ft.FilePickerResultEvent):
        """Handle image file selection"""
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            try:
                import base64
                with open(file_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()
                self.edit_image_data = image_data
                
                # Show success message
                if self.page:
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text("Image selected. Click 'Save Changes' to apply."),
                        bgcolor="#2196F3",
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
            except Exception as ex:
                if self.page:
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"Error reading image: {str(ex)}"),
                        bgcolor="#F44336",
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
    
    def _build_news_section(self):
        """Build news post creator section for campaign updates"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Campaign Updates",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Share campaign updates and news with voters",
                        size=12,
                        color=AppTheme.TEXT_SECONDARY,
                    ),
                    ft.Container(height=16),
                    NewsPostCreator(
                        db=self.db,
                        author_id=self.user_id,
                        author_role="politician",
                        on_post_created=self._on_news_post_created,
                    ),
                    ft.Container(height=16),
                    MyPostsList(
                        db=self.db,
                        author_id=self.user_id,
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
    
    def _on_news_post_created(self, post_id=None):
        """Handle news post created event"""
        # Rebuild UI to show updated posts
        self._build_ui()
        if self.page:
            self.page.update()
