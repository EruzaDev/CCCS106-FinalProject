import flet as ft
import base64
import os
from app.theme import AppTheme


# Dropdown options for positions and parties
POSITION_OPTIONS = [
    "President",
    "Vice President",
    "Senator",
    "Governor",
    "Vice Governor",
    "Mayor",
    "Vice Mayor",
    "Congressman",
    "Councilor",
    "Barangay Captain",
]

PARTY_OPTIONS = [
    "PDP-Laban",
    "Liberal Party",
    "Nacionalista Party",
    "NPC (Nationalist People's Coalition)",
    "Lakas-CMD",
    "NUP (National Unity Party)",
    "Aksyon Demokratiko",
    "Progressive Alliance",
    "United Citizens Party",
    "Green Coalition",
    "Democratic Reform Party",
    "Independent",
]


class UserManagement(ft.Column):
    """User Management page for COMELEC - Create and manage voter and politician accounts"""
    
    def __init__(self, username, db, on_logout, on_back):
        super().__init__()
        self.username = username
        self.db = db
        self.on_logout = on_logout
        self.on_back = on_back
        
        # Current tab (voters or politicians)
        self.current_tab = "voters"
        
        # Form visibility
        self.show_voter_form = False
        self.show_politician_form = False
        
        # Edit mode
        self.editing_user_id = None
        self.editing_user_data = None
        
        # Politician image data
        self.politician_image_data = None
        self.politician_image_path = None
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the main UI"""
        # Create file picker (will be added to page overlay by main.py)
        if not hasattr(self, 'file_picker') or self.file_picker is None:
            self.file_picker = ft.FilePicker(on_result=self._on_image_selected)
        
        self.controls = [
            self._build_header(),
            ft.Container(
                content=ft.Column(
                    [
                        self._build_back_link(),
                        ft.Container(height=16),
                        self._build_main_card(),
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
                padding=24,
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
                                bgcolor=AppTheme.PRIMARY,
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
                                style=ft.ButtonStyle(color="#5C6BC0"),
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
    
    def _build_back_link(self):
        """Build back to dashboard link"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ARROW_BACK, color="#5C6BC0", size=18),
                    ft.TextButton(
                        "Back to Dashboard",
                        on_click=lambda e: self.on_back(),
                        style=ft.ButtonStyle(color="#5C6BC0"),
                    ),
                ],
                spacing=4,
            ),
        )
    
    def _build_main_card(self):
        """Build the main content card"""
        self.main_card_content = ft.Column(
            [
                ft.Text(
                    "User Management",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Create and manage voter and politician accounts",
                    size=14,
                    color="#666666",
                ),
                ft.Container(height=20),
                self._build_tabs(),
                ft.Container(height=20),
                self._build_tab_content(),
            ],
        )
        
        return ft.Container(
            content=self.main_card_content,
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def _build_tabs(self):
        """Build the Voters/Politicians tabs"""
        voters_selected = self.current_tab == "voters"
        politicians_selected = self.current_tab == "politicians"
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.PEOPLE,
                                    color="#5C6BC0" if voters_selected else "#666666",
                                    size=18,
                                ),
                                ft.Text(
                                    "Voters",
                                    color="#5C6BC0" if voters_selected else "#666666",
                                    weight=ft.FontWeight.W_500 if voters_selected else None,
                                ),
                            ],
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=40, vertical=12),
                        border=ft.border.only(
                            bottom=ft.BorderSide(3, "#5C6BC0") if voters_selected else None
                        ),
                        bgcolor="#E8EAF6" if voters_selected else None,
                        on_click=lambda e: self._switch_tab("voters"),
                        ink=True,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.PERSON_PIN,
                                    color="#5C6BC0" if politicians_selected else "#666666",
                                    size=18,
                                ),
                                ft.Text(
                                    "Politicians",
                                    color="#5C6BC0" if politicians_selected else "#666666",
                                    weight=ft.FontWeight.W_500 if politicians_selected else None,
                                ),
                            ],
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=40, vertical=12),
                        border=ft.border.only(
                            bottom=ft.BorderSide(3, "#5C6BC0") if politicians_selected else None
                        ),
                        bgcolor="#E8EAF6" if politicians_selected else None,
                        on_click=lambda e: self._switch_tab("politicians"),
                        ink=True,
                        expand=True,
                    ),
                ],
                spacing=0,
            ),
            border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        )
    
    def _build_tab_content(self):
        """Build content for current tab"""
        if self.current_tab == "voters":
            return self._build_voters_content()
        else:
            return self._build_politicians_content()
    
    def _build_voters_content(self):
        """Build voters tab content"""
        # Get voters from database
        voters = self.db.get_users_by_role("voter")
        
        content_items = [
            ft.Row(
                [
                    ft.Text("Voter Accounts", size=16, weight=ft.FontWeight.W_500),
                    ft.ElevatedButton(
                        "+ Create Voter",
                        bgcolor="#5C6BC0",
                        color=ft.Colors.WHITE,
                        on_click=lambda e: self._toggle_voter_form(),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ]
        
        # Show voter form if active
        if self.show_voter_form:
            content_items.append(ft.Container(height=16))
            content_items.append(self._build_voter_form())
        
        content_items.append(ft.Container(height=16))
        content_items.append(self._build_voters_table(voters))
        
        return ft.Column(content_items)
    
    def _build_voter_form(self):
        """Build create/edit voter form"""
        # Pre-fill values if editing
        name_value = ""
        username_value = ""
        email_value = ""
        
        if self.editing_user_id and self.editing_user_data:
            name_value = self.editing_user_data.get("full_name", "")
            username_value = self.editing_user_data.get("username", "")
            email_value = self.editing_user_data.get("email", "")
        
        self.voter_name_field = ft.TextField(
            label="Full Name *",
            hint_text="e.g., Juan dela Cruz",
            value=name_value,
            border_radius=8,
        )
        self.voter_username_field = ft.TextField(
            label="Username *",
            hint_text="e.g., juandelacruz",
            value=username_value,
            border_radius=8,
        )
        self.voter_email_field = ft.TextField(
            label="Email *",
            hint_text="e.g., juan@email.com",
            value=email_value,
            border_radius=8,
        )
        self.voter_password_field = ft.TextField(
            label="Password *" if not self.editing_user_id else "Password (leave blank to keep current)",
            hint_text="••••••••",
            password=True,
            can_reveal_password=True,
            border_radius=8,
        )
        
        button_text = "Update Account" if self.editing_user_id else "Create Account"
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Create New Voter Account" if not self.editing_user_id else "Edit Voter Account",
                        size=14,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Container(height=12),
                    ft.Row(
                        [
                            ft.Container(self.voter_name_field, expand=True),
                            ft.Container(self.voter_email_field, expand=True),
                        ],
                        spacing=16,
                    ),
                    ft.Row(
                        [
                            ft.Container(self.voter_username_field, expand=True),
                            ft.Container(self.voter_password_field, expand=True),
                        ],
                        spacing=16,
                    ),
                    ft.Container(height=12),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                button_text,
                                bgcolor="#4CAF50",
                                color=ft.Colors.WHITE,
                                on_click=lambda e: self._save_voter(),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                            ft.OutlinedButton(
                                "Cancel",
                                on_click=lambda e: self._toggle_voter_form(),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                        ],
                        spacing=12,
                    ),
                ],
            ),
            padding=20,
            bgcolor="#FAFAFA",
            border_radius=8,
            border=ft.border.all(1, "#E0E0E0"),
        )
    
    def _build_voters_table(self, voters):
        """Build voters data table"""
        rows = []
        for voter in voters:
            user_id, username, email, role, created_at, full_name, status, *_ = voter
            display_name = full_name if full_name else username
            display_status = status if status else "active"
            
            # Create closure to capture user_id
            def make_edit_handler(uid, uname, uemail, ufull_name):
                return lambda e: self._edit_voter(uid, uname, uemail, ufull_name)
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(display_name)),
                        ft.DataCell(ft.Text(username)),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    display_status.capitalize(),
                                    color="#4CAF50" if display_status == "active" else "#F44336",
                                    size=12,
                                ),
                                bgcolor="#E8F5E9" if display_status == "active" else "#FFEBEE",
                                padding=ft.padding.symmetric(horizontal=12, vertical=4),
                                border_radius=12,
                            )
                        ),
                        ft.DataCell(
                            ft.TextButton(
                                "Edit",
                                on_click=make_edit_handler(user_id, username, email, full_name),
                                style=ft.ButtonStyle(color="#5C6BC0"),
                            )
                        ),
                    ],
                )
            )
        
        if not rows:
            return ft.Container(
                content=ft.Text("No voter accounts found", color="#666666"),
                padding=20,
                alignment=ft.alignment.center,
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Username", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD)),
            ],
            rows=rows,
            border=ft.border.all(1, "#E0E0E0"),
            border_radius=8,
            heading_row_color="#F5F5F5",
        )
    
    def _build_politicians_content(self):
        """Build politicians tab content"""
        # Get politicians from database
        politicians = self.db.get_users_by_role("politician")
        
        content_items = [
            ft.Row(
                [
                    ft.Text("Politician Accounts", size=16, weight=ft.FontWeight.W_500),
                    ft.ElevatedButton(
                        "+ Create Politician",
                        bgcolor="#5C6BC0",
                        color=ft.Colors.WHITE,
                        on_click=lambda e: self._toggle_politician_form(),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ]
        
        # Show politician form if active
        if self.show_politician_form:
            content_items.append(ft.Container(height=16))
            content_items.append(self._build_politician_form())
        
        content_items.append(ft.Container(height=16))
        content_items.append(self._build_politicians_table(politicians))
        
        return ft.Column(content_items)
    
    def _build_politician_form(self):
        """Build create/edit politician form with image upload and dropdowns"""
        # Pre-fill values if editing
        name_value = ""
        email_value = ""
        position_value = None
        party_value = None
        username_value = ""
        biography_value = ""
        
        if self.editing_user_id and self.editing_user_data:
            name_value = self.editing_user_data.get("full_name", "")
            email_value = self.editing_user_data.get("email", "")
            position_value = self.editing_user_data.get("position", "")
            party_value = self.editing_user_data.get("party", "")
            username_value = self.editing_user_data.get("username", "")
            biography_value = self.editing_user_data.get("biography", "")
            # Only load existing image if no new image has been selected (indicated by politician_image_path)
            if not self.politician_image_path and self.editing_user_data.get("profile_image"):
                self.politician_image_data = self.editing_user_data.get("profile_image")
        
        self.politician_name_field = ft.TextField(
            label="Full Name *",
            hint_text="e.g., Maria Santos",
            value=name_value,
            border_radius=8,
        )
        self.politician_email_field = ft.TextField(
            label="Email *",
            hint_text="e.g., maria@email.com",
            value=email_value,
            border_radius=8,
        )
        
        # Position dropdown
        self.politician_position_dropdown = ft.Dropdown(
            label="Position *",
            hint_text="Select position",
            options=[ft.dropdown.Option(pos) for pos in POSITION_OPTIONS],
            value=position_value if position_value in POSITION_OPTIONS else None,
            border_radius=8,
        )
        
        # Party dropdown
        self.politician_party_dropdown = ft.Dropdown(
            label="Political Party *",
            hint_text="Select party",
            options=[ft.dropdown.Option(party) for party in PARTY_OPTIONS],
            value=party_value if party_value in PARTY_OPTIONS else None,
            border_radius=8,
        )
        
        self.politician_username_field = ft.TextField(
            label="Username *",
            hint_text="e.g., mariasantos",
            value=username_value,
            border_radius=8,
        )
        self.politician_password_field = ft.TextField(
            label="Password *" if not self.editing_user_id else "Password (leave blank to keep current)",
            hint_text="••••••••",
            password=True,
            can_reveal_password=True,
            border_radius=8,
        )
        self.politician_biography_field = ft.TextField(
            label="Biography *",
            hint_text="Brief biography and political background...",
            value=biography_value,
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=8,
        )
        
        # Image preview - show current image if exists
        if self.politician_image_data:
            self.image_preview = ft.Container(
                content=ft.Image(
                    src_base64=self.politician_image_data,
                    width=120,
                    height=120,
                    fit=ft.ImageFit.COVER,
                    border_radius=8,
                ),
                width=120,
                height=120,
                border_radius=8,
                border=ft.border.all(1, "#E0E0E0"),
            )
        else:
            self.image_preview = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.PERSON, size=48, color="#BDBDBD"),
                        ft.Text("No image selected", size=12, color="#666666"),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=120,
                height=120,
                bgcolor="#F5F5F5",
                border_radius=8,
                border=ft.border.all(1, "#E0E0E0"),
                alignment=ft.alignment.center,
            )
        
        button_text = "Update Account" if self.editing_user_id else "Create Account"
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Create New Politician Account" if not self.editing_user_id else "Edit Politician Account",
                        size=14,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Container(height=12),
                    ft.Row(
                        [
                            ft.Container(self.politician_name_field, expand=True),
                            ft.Container(self.politician_email_field, expand=True),
                        ],
                        spacing=16,
                    ),
                    ft.Row(
                        [
                            ft.Container(self.politician_position_dropdown, expand=True),
                            ft.Container(self.politician_party_dropdown, expand=True),
                        ],
                        spacing=16,
                    ),
                    ft.Row(
                        [
                            ft.Container(self.politician_username_field, expand=True),
                            ft.Container(self.politician_password_field, expand=True),
                        ],
                        spacing=16,
                    ),
                    ft.Container(height=8),
                    ft.Text("Profile Image", size=12, weight=ft.FontWeight.W_500),
                    ft.Container(height=4),
                    ft.Row(
                        [
                            self.image_preview,
                            ft.Column(
                                [
                                    ft.ElevatedButton(
                                        "Choose Image",
                                        icon=ft.Icons.UPLOAD_FILE,
                                        on_click=lambda e: self._pick_image(),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                    ),
                                    ft.Text(
                                        "Supported formats: JPG, PNG, GIF",
                                        size=11,
                                        color="#666666",
                                    ),
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=16,
                    ),
                    ft.Container(height=8),
                    self.politician_biography_field,
                    ft.Container(height=12),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                button_text,
                                bgcolor="#4CAF50",
                                color=ft.Colors.WHITE,
                                on_click=lambda e: self._save_politician(),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                            ft.OutlinedButton(
                                "Cancel",
                                on_click=lambda e: self._toggle_politician_form(),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                        ],
                        spacing=12,
                    ),
                ],
            ),
            padding=20,
            bgcolor="#FAFAFA",
            border_radius=8,
            border=ft.border.all(1, "#E0E0E0"),
        )
    
    def _build_politicians_table(self, politicians):
        """Build politicians data table"""
        rows = []
        for politician in politicians:
            user_id, username, email, role, created_at, full_name, status, position, party, biography, profile_image = politician
            display_name = full_name if full_name else username
            display_status = status if status else "active"
            display_position = position if position else "-"
            display_party = party if party else "-"
            
            # Create closure to capture all user data
            def make_edit_handler(uid, uname, uemail, ufull_name, uposition, uparty, ubio, uimg):
                return lambda e: self._edit_politician(uid, uname, uemail, ufull_name, uposition, uparty, ubio, uimg)
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(display_name)),
                        ft.DataCell(ft.Text(display_position)),
                        ft.DataCell(ft.Text(display_party)),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    display_status.capitalize(),
                                    color="#4CAF50" if display_status == "active" else "#F44336",
                                    size=12,
                                ),
                                bgcolor="#E8F5E9" if display_status == "active" else "#FFEBEE",
                                padding=ft.padding.symmetric(horizontal=12, vertical=4),
                                border_radius=12,
                            )
                        ),
                        ft.DataCell(
                            ft.TextButton(
                                "Edit",
                                on_click=make_edit_handler(user_id, username, email, full_name, position, party, biography, profile_image),
                                style=ft.ButtonStyle(color="#5C6BC0"),
                            )
                        ),
                    ],
                )
            )
        
        if not rows:
            return ft.Container(
                content=ft.Text("No politician accounts found", color="#666666"),
                padding=20,
                alignment=ft.alignment.center,
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Position", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Party", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD)),
            ],
            rows=rows,
            border=ft.border.all(1, "#E0E0E0"),
            border_radius=8,
            heading_row_color="#F5F5F5",
        )
    
    def _switch_tab(self, tab):
        """Switch between voters and politicians tabs"""
        self.current_tab = tab
        self.show_voter_form = False
        self.show_politician_form = False
        self.editing_user_id = None
        self._refresh_ui()
    
    def _toggle_voter_form(self):
        """Toggle voter form visibility"""
        self.show_voter_form = not self.show_voter_form
        self.editing_user_id = None
        self.editing_user_data = None
        self._refresh_ui()
    
    def _toggle_politician_form(self):
        """Toggle politician form visibility"""
        self.show_politician_form = not self.show_politician_form
        self.editing_user_id = None
        self.editing_user_data = None
        self.politician_image_data = None
        self.politician_image_path = None
        self._refresh_ui()
    
    def _edit_voter(self, user_id, username, email, full_name):
        """Open edit form for voter"""
        self.editing_user_id = user_id
        self.editing_user_data = {
            "username": username,
            "email": email,
            "full_name": full_name,
        }
        self.show_voter_form = True
        self._refresh_ui()
    
    def _edit_politician(self, user_id, username, email, full_name, position, party, biography, profile_image):
        """Open edit form for politician"""
        self.editing_user_id = user_id
        self.editing_user_data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "position": position,
            "party": party,
            "biography": biography,
            "profile_image": profile_image,
        }
        self.politician_image_data = profile_image
        self.show_politician_form = True
        self._refresh_ui()
    
    def _pick_image(self):
        """Open file picker for image selection"""
        if self.file_picker:
            self.file_picker.pick_files(
                allowed_extensions=["jpg", "jpeg", "png", "gif"],
                allow_multiple=False,
            )
    
    def _on_image_selected(self, e: ft.FilePickerResultEvent):
        """Handle image file selection"""
        if e.files and len(e.files) > 0:
            file = e.files[0]
            self.politician_image_path = file.path
            
            # Read and encode image for preview and storage
            try:
                with open(file.path, "rb") as f:
                    image_bytes = f.read()
                    self.politician_image_data = base64.b64encode(image_bytes).decode('utf-8')
                
                # Rebuild UI to show the image
                self._refresh_ui()
            except Exception as ex:
                print(f"Error loading image: {ex}")
                self._show_error(f"Error loading image: {ex}")
    
    def _save_voter(self):
        """Create or update voter account"""
        name = self.voter_name_field.value
        username = self.voter_username_field.value
        email = self.voter_email_field.value
        password = self.voter_password_field.value
        
        if not all([name, username, email]):
            self._show_error("Please fill all required fields")
            return
        
        if self.editing_user_id:
            # Update existing voter
            if password:
                # Update with new password
                success = self.db.update_voter_with_password(self.editing_user_id, name, email, username, password)
            else:
                # Update without changing password
                success = self.db.update_voter(self.editing_user_id, name, email, username)
            
            if success:
                self.show_voter_form = False
                self.editing_user_id = None
                self.editing_user_data = None
                self._refresh_ui()
                self._show_success("Voter account updated successfully")
            else:
                self._show_error("Username or email already exists")
        else:
            # Create new voter
            if not password:
                self._show_error("Password is required for new accounts")
                return
            
            success = self.db.create_voter(username, email, password, name)
            if success:
                self.show_voter_form = False
                self._refresh_ui()
                self._show_success("Voter account created successfully")
            else:
                self._show_error("Username or email already exists")
    
    def _save_politician(self):
        """Create or update politician account"""
        name = self.politician_name_field.value
        email = self.politician_email_field.value
        position = self.politician_position_dropdown.value
        party = self.politician_party_dropdown.value
        username = self.politician_username_field.value
        password = self.politician_password_field.value
        biography = self.politician_biography_field.value
        
        if not all([name, email, position, party, username, biography]):
            self._show_error("Please fill all required fields")
            return
        
        if self.editing_user_id:
            # Update existing politician
            if password:
                success = self.db.update_politician_with_password(
                    self.editing_user_id, name, email, username, position, party, biography, password, self.politician_image_data
                )
            else:
                success = self.db.update_politician(
                    self.editing_user_id, name, email, username, position, party, biography, self.politician_image_data
                )
            
            if success:
                self.show_politician_form = False
                self.editing_user_id = None
                self.editing_user_data = None
                self.politician_image_data = None
                self.politician_image_path = None
                self._refresh_ui()
                self._show_success("Politician account updated successfully")
            else:
                self._show_error("Username or email already exists")
        else:
            # Create new politician
            if not password:
                self._show_error("Password is required for new accounts")
                return
            
            success = self.db.create_politician(
                username, email, password, name, position, party, biography, self.politician_image_data
            )
            if success:
                self.show_politician_form = False
                self.politician_image_data = None
                self.politician_image_path = None
                self._refresh_ui()
                self._show_success("Politician account created successfully")
            else:
                self._show_error("Username or email already exists")
    
    def _show_error(self, message):
        """Show error snackbar"""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED_400,
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _show_success(self, message):
        """Show success snackbar"""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.GREEN_400,
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _refresh_ui(self):
        """Refresh the UI"""
        self._build_ui()
        if self.page:
            self.page.update()
