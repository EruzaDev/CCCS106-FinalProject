import flet as ft
import base64
import os


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
        
        # Politician image data
        self.politician_image_data = None
        self.politician_image_path = None
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the main UI"""
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
                bgcolor="#F5F5F5",
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
        self.voter_name_field = ft.TextField(
            label="Full Name *",
            hint_text="e.g., Juan dela Cruz",
            border_radius=8,
        )
        self.voter_username_field = ft.TextField(
            label="Username *",
            hint_text="e.g., juandelacruz",
            border_radius=8,
        )
        self.voter_email_field = ft.TextField(
            label="Email *",
            hint_text="e.g., juan@email.com",
            border_radius=8,
        )
        self.voter_password_field = ft.TextField(
            label="Password *",
            hint_text="••••••••",
            password=True,
            can_reveal_password=True,
            border_radius=8,
        )
        
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
                                "Create Account",
                                bgcolor="#4CAF50",
                                color=ft.Colors.WHITE,
                                on_click=lambda e: self._create_voter(),
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
        """Build create/edit politician form with image upload"""
        self.politician_name_field = ft.TextField(
            label="Full Name *",
            hint_text="e.g., Maria Santos",
            border_radius=8,
        )
        self.politician_email_field = ft.TextField(
            label="Email *",
            hint_text="e.g., maria@email.com",
            border_radius=8,
        )
        self.politician_position_field = ft.TextField(
            label="Position *",
            hint_text="e.g., Senator, Governor",
            border_radius=8,
        )
        self.politician_party_field = ft.TextField(
            label="Political Party *",
            hint_text="e.g., Progressive Alliance",
            border_radius=8,
        )
        self.politician_username_field = ft.TextField(
            label="Username *",
            hint_text="e.g., mariasantos",
            border_radius=8,
        )
        self.politician_password_field = ft.TextField(
            label="Password *",
            hint_text="••••••••",
            password=True,
            can_reveal_password=True,
            border_radius=8,
        )
        self.politician_biography_field = ft.TextField(
            label="Biography *",
            hint_text="Brief biography and political background...",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=8,
        )
        
        # Image preview
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
        
        # File picker for image
        self.file_picker = ft.FilePicker(
            on_result=self._on_image_selected,
        )
        
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
                            ft.Container(self.politician_position_field, expand=True),
                            ft.Container(self.politician_party_field, expand=True),
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
                                "Create Account",
                                bgcolor="#4CAF50",
                                color=ft.Colors.WHITE,
                                on_click=lambda e: self._create_politician(),
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
                    self.file_picker,
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
        self._refresh_ui()
    
    def _toggle_politician_form(self):
        """Toggle politician form visibility"""
        self.show_politician_form = not self.show_politician_form
        self.editing_user_id = None
        self.politician_image_data = None
        self.politician_image_path = None
        self._refresh_ui()
    
    def _pick_image(self):
        """Open file picker for image selection"""
        if hasattr(self, 'file_picker') and self.file_picker.page:
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
                
                # Update preview
                self.image_preview.content = ft.Image(
                    src_base64=self.politician_image_data,
                    width=120,
                    height=120,
                    fit=ft.ImageFit.COVER,
                    border_radius=8,
                )
                self._refresh_ui()
            except Exception as ex:
                print(f"Error loading image: {ex}")
    
    def _create_voter(self):
        """Create new voter account"""
        name = self.voter_name_field.value
        username = self.voter_username_field.value
        email = self.voter_email_field.value
        password = self.voter_password_field.value
        
        if not all([name, username, email, password]):
            self._show_error("Please fill all required fields")
            return
        
        success = self.db.create_voter(username, email, password, name)
        if success:
            self.show_voter_form = False
            self._refresh_ui()
        else:
            self._show_error("Username or email already exists")
    
    def _create_politician(self):
        """Create new politician account"""
        name = self.politician_name_field.value
        email = self.politician_email_field.value
        position = self.politician_position_field.value
        party = self.politician_party_field.value
        username = self.politician_username_field.value
        password = self.politician_password_field.value
        biography = self.politician_biography_field.value
        
        if not all([name, email, position, party, username, password, biography]):
            self._show_error("Please fill all required fields")
            return
        
        success = self.db.create_politician(
            username, email, password, name, position, party, biography, self.politician_image_data
        )
        if success:
            self.show_politician_form = False
            self.politician_image_data = None
            self.politician_image_path = None
            self._refresh_ui()
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
    
    def _refresh_ui(self):
        """Refresh the UI"""
        self._build_ui()
        if self.page:
            self.page.update()
