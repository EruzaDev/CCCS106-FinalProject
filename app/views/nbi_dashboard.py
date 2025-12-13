import flet as ft
from datetime import datetime
from app.components.news_post_creator import NewsPostCreator, MyPostsList
from app.theme import AppTheme
from components.date_picker_field import DatePickerField


class NBIDashboard(ft.Column):
    """NBI Dashboard - Main dashboard for NBI officers to manage legal records"""
    
    def __init__(self, username, db, on_logout, current_user_id=None, on_audit_log=None):
        super().__init__()
        self.username = username
        self.db = db
        self.on_logout = on_logout
        self.current_user_id = current_user_id
        self.on_audit_log = on_audit_log
        
        # Dialog references
        self.add_record_dialog = None
        self.edit_dialog = None
        
        # Search state
        self.search_query = ""
        self.records_container = None
        
        # Form state for adding records
        self.selected_politician_id = None
        self.selected_record_type = None
        self.record_title_field = None
        self.record_description_field = None
        self.record_date_field = None
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the main UI"""
        self.controls = [
            self._build_header(),
            ft.Container(
                content=ft.Column(
                    [
                        self._build_statistics_row(),
                        ft.Container(height=20),
                        self._build_record_management(),
                        ft.Container(height=20),
                        self._build_politician_records_simple(),
                        ft.Container(height=20),
                        self._build_news_section(),
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
    
    def _build_politician_records_simple(self):
        """Build a simplified politician records section with verify/dismiss actions"""
        # Get all legal records
        records = self.db.get_all_legal_records() if self.db else []
        
        # Store records container reference for refreshing
        self.records_list_column = ft.Column(spacing=8)
        self._populate_records_list(records)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Legal Records", size=18, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.IconButton(
                        icon=ft.Icons.REFRESH,
                        icon_color=AppTheme.PRIMARY,
                        tooltip="Refresh Records",
                        on_click=lambda e: self._refresh_legal_records(),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=12),
                self.records_list_column,
            ]),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def _populate_records_list(self, records):
        """Populate the records list with record cards"""
        self.records_list_column.controls.clear()
        
        if not records:
            self.records_list_column.controls.append(
                ft.Container(
                    content=ft.Text("No legal records found", color="#666666"),
                    padding=20,
                )
            )
            return
        
        for record in records:
            record_id = record[0]
            status = record[6]
            
            # Build action buttons based on status
            action_buttons = []
            if status == "pending":
                action_buttons = [
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CHECK, size=14),
                            ft.Text("Verify", size=11),
                        ], spacing=4),
                        bgcolor="#4CAF50",
                        color=ft.Colors.WHITE,
                        on_click=lambda e, rid=record_id: self._verify_legal_record(rid),
                    ),
                    ft.OutlinedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CLOSE, size=14),
                            ft.Text("Dismiss", size=11),
                        ], spacing=4),
                        style=ft.ButtonStyle(
                            side=ft.BorderSide(1, "#F44336"),
                            color="#F44336",
                        ),
                        on_click=lambda e, rid=record_id: self._dismiss_legal_record(rid),
                    ),
                ]
            elif status == "verified":
                action_buttons = [
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.VERIFIED, size=14, color="#4CAF50"),
                            ft.Text("Verified", size=11, color="#4CAF50"),
                        ], spacing=4),
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    ),
                ]
            elif status == "dismissed" or status == "rejected":
                action_buttons = [
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CANCEL, size=14, color="#F44336"),
                            ft.Text("Dismissed", size=11, color="#F44336"),
                        ], spacing=4),
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    ),
                ]
            
            self.records_list_column.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(record[3], weight=ft.FontWeight.BOLD, size=14),  # title
                            ft.Container(
                                content=ft.Text(status.capitalize(), size=10, color=ft.Colors.WHITE),
                                bgcolor=self._get_status_color(status),
                                border_radius=10,
                                padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(f"Type: {record[2]}", size=12, color="#666666"),
                        ft.Text(f"Politician: {record[8] or record[9]}", size=12, color="#666666"),
                        ft.Text(f"Description: {(record[4] or 'N/A')[:100]}{'...' if record[4] and len(record[4]) > 100 else ''}", size=12, color="#666666"),
                        ft.Text(f"Date: {record[5] or 'N/A'}", size=11, color="#999999"),
                        ft.Container(height=8),
                        ft.Row(action_buttons, spacing=8),
                    ], spacing=4),
                    bgcolor="#F8F9FA",
                    border_radius=8,
                    padding=12,
                )
            )
    
    def _refresh_legal_records(self):
        """Refresh the legal records list"""
        records = self.db.get_all_legal_records() if self.db else []
        self._populate_records_list(records)
        if self.page:
            self.page.update()
    
    def _verify_legal_record(self, record_id):
        """Verify a legal record"""
        try:
            self.db.update_legal_record_status(record_id, "verified", self.current_user_id)
            self.db.log_action(
                action="Legal Record Verified",
                action_type="legal_record",
                description=f"Record ID {record_id} verified",
                user_id=self.current_user_id,
                user_role="nbi",
            )
            self._show_success("Record verified successfully")
            self._refresh_legal_records()
            self._update_stats()
        except Exception as ex:
            print(f"Error verifying record: {ex}")
            self._show_error("Failed to verify record")
    
    def _dismiss_legal_record(self, record_id):
        """Dismiss a legal record"""
        try:
            self.db.update_legal_record_status(record_id, "dismissed", self.current_user_id)
            self.db.log_action(
                action="Legal Record Dismissed",
                action_type="legal_record",
                description=f"Record ID {record_id} dismissed",
                user_id=self.current_user_id,
                user_role="nbi",
            )
            self._show_success("Record dismissed successfully")
            self._refresh_legal_records()
            self._update_stats()
        except Exception as ex:
            print(f"Error dismissing record: {ex}")
            self._show_error("Failed to dismiss record")
    
    def _update_stats(self):
        """Update the statistics display"""
        # Rebuild UI to update stats
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _build_header(self):
        """Build the header with NBI branding"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.SECURITY,
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
                                        "NBI Officer Dashboard",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        f"Welcome, Officer {self.username}",
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
        return ft.Column(
            [
                # Statistics Row
                self._build_statistics_row(),
                ft.Container(height=20),
                # Record Management Section
                self._build_record_management(),
                ft.Container(height=20),
                # Politician Records List
                self._build_politician_records(),
                ft.Container(height=20),
                # News Post Creator
                self._build_news_section(),
            ],
        )
    
    def _build_statistics_row(self):
        """Build statistics cards row"""
        stats = self.db.get_legal_records_stats() if self.db else {"total": 0, "verified": 0, "pending": 0}
        
        return ft.Row(
            [
                self._build_stat_card(
                    "Total Records",
                    str(stats.get("total", 0)),
                    ft.Icons.FOLDER_OUTLINED,
                    "#FF5722",
                ),
                self._build_stat_card(
                    "Verified Records",
                    str(stats.get("verified", 0)),
                    ft.Icons.VERIFIED_OUTLINED,
                    "#4CAF50",
                ),
                self._build_stat_card(
                    "Pending Review",
                    str(stats.get("pending", 0)),
                    ft.Icons.PENDING_OUTLINED,
                    "#FFC107",
                ),
            ],
            spacing=20,
        )
    
    def _build_stat_card(self, title, value, icon, color):
        """Build a statistics card"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(title, size=12, color="#666666"),
                            ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color="#333333"),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Icon(icon, color=color, size=24),
                        bgcolor=f"{color}20",
                        border_radius=20,
                        padding=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=20,
            expand=True,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def _build_record_management(self):
        """Build record management section"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Record Management",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#333333",
                            ),
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.ADD, size=16),
                                        ft.Text("Add Record"),
                                    ],
                                    spacing=4,
                                ),
                                bgcolor="#FF5722",
                                color=ft.Colors.WHITE,
                                on_click=self._show_add_record_form,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=16),
                    # Add Record Form (initially hidden)
                    self._build_add_record_form(),
                ],
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
    
    def _build_add_record_form(self):
        """Build the add record form"""
        # Get politicians for dropdown
        politicians = self.db.get_users_by_role("politician") if self.db else []
        politician_options = [
            ft.dropdown.Option(key=str(p[0]), text=f"{p[5] or p[1]} - {p[7] or 'Position N/A'}")
            for p in politicians
        ]
        
        record_types = [
            ft.dropdown.Option("Graft and Corruption Case"),
            ft.dropdown.Option("Conflict of Interest Allegation"),
            ft.dropdown.Option("Tax Compliance Issue"),
            ft.dropdown.Option("Libel Case"),
            ft.dropdown.Option("Criminal Case"),
            ft.dropdown.Option("Administrative Case"),
            ft.dropdown.Option("Civil Case"),
            ft.dropdown.Option("Other"),
        ]
        
        self.politician_dropdown = ft.Dropdown(
            label="Politician",
            options=politician_options,
            width=300,
            on_change=self._on_politician_selected,
        )
        
        self.record_type_dropdown = ft.Dropdown(
            label="Record Type",
            options=record_types,
            width=300,
            on_change=self._on_record_type_selected,
        )
        
        self.record_title_field = ft.TextField(
            label="Title",
            hint_text="e.g., Graft and Corruption Case",
            width=400,
        )
        
        self.record_description_field = ft.TextField(
            label="Description",
            hint_text="Provide detailed information about the record...",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=400,
        )
        
        self.record_date_field = DatePickerField(
            label="Date",
            width=250,
        )
        
        self.add_record_form_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Add New Record", size=14, weight=ft.FontWeight.W_600, color="#666666"),
                    ft.Container(height=8),
                    self.politician_dropdown,
                    ft.Container(height=12),
                    self.record_type_dropdown,
                    ft.Container(height=12),
                    self.record_title_field,
                    ft.Container(height=12),
                    self.record_description_field,
                    ft.Container(height=12),
                    self.record_date_field,
                    ft.Container(height=16),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Submit Record",
                                bgcolor="#FF5722",
                                color=ft.Colors.WHITE,
                                on_click=self._submit_record,
                            ),
                            ft.OutlinedButton(
                                "Cancel",
                                on_click=self._hide_add_record_form,
                            ),
                        ],
                        spacing=12,
                    ),
                ],
            ),
            visible=False,
            padding=ft.padding.only(top=16),
            border=ft.border.only(top=ft.BorderSide(1, "#E0E0E0")),
        )
        
        return self.add_record_form_container
    
    def _show_add_record_form(self, e):
        """Show the add record form"""
        try:
            self.add_record_form_container.visible = True
            if self.page:
                self.page.update()
        except Exception as ex:
            print(f"Error showing form: {ex}")
    
    def _hide_add_record_form(self, e):
        """Hide the add record form and clear fields"""
        try:
            self.add_record_form_container.visible = False
            self.politician_dropdown.value = None
            self.record_type_dropdown.value = None
            self.record_title_field.value = ""
            self.record_description_field.value = ""
            self.record_date_field.value = ""
            if self.page:
                self.page.update()
        except Exception as ex:
            print(f"Error hiding form: {ex}")
    
    def _on_politician_selected(self, e):
        """Handle politician selection"""
        self.selected_politician_id = e.control.value
    
    def _on_record_type_selected(self, e):
        """Handle record type selection"""
        self.selected_record_type = e.control.value
        if self.record_title_field and not self.record_title_field.value:
            self.record_title_field.value = e.control.value
            if self.page:
                self.page.update()
    
    def _submit_record(self, e):
        """Submit a new legal record"""
        if not self.politician_dropdown.value:
            self._show_error("Please select a politician")
            return
        
        if not self.record_type_dropdown.value:
            self._show_error("Please select a record type")
            return
        
        if not self.record_title_field.value:
            self._show_error("Please enter a title")
            return
        
        # Create the record
        record_id = self.db.create_legal_record(
            politician_id=int(self.politician_dropdown.value),
            record_type=self.record_type_dropdown.value,
            title=self.record_title_field.value,
            description=self.record_description_field.value or "",
            date=self.record_date_field.value or datetime.now().strftime("%m/%d/%Y"),
            added_by=self.current_user_id,
        )
        
        if record_id:
            # Log the action
            self.db.log_action(
                action="Legal Record Added",
                action_type="legal_record",
                description=f"Added record: {self.record_title_field.value}",
                user_id=self.current_user_id,
                user_role="nbi",
                target_type="politician",
                target_id=int(self.politician_dropdown.value),
            )
            self._hide_add_record_form(None)
            self._refresh_records()
            self._show_success("Record added successfully")
        else:
            self._show_error("Failed to add record")
    
    def _build_politician_records(self):
        """Build the politician records list section"""
        try:
            self.records_container = ft.Column(
                [self._build_records_list()],
            )
            
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "Politician Records",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color="#333333",
                                ),
                            ],
                        ),
                        ft.Container(height=12),
                        # Search bar
                        ft.TextField(
                            hint_text="Search politicians...",
                            prefix_icon=ft.Icons.SEARCH,
                            width=300,
                            height=40,
                            border_radius=20,
                            on_change=self._on_search_change,
                        ),
                        ft.Container(height=16),
                        self.records_container,
                    ],
                ),
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                padding=20,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                ),
            )
        except Exception as e:
            print(f"ERROR in _build_politician_records: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return ft.Container(
                content=ft.Text(f"Error loading records: {e}", color="red"),
                padding=20,
            )
    
    def _on_search_change(self, e):
        """Handle search input change"""
        self.search_query = e.control.value
        self._refresh_records()
    
    def _build_records_list(self):
        """Build the list of politician records"""
        if self.search_query:
            records = self.db.search_legal_records(self.search_query) if self.db else []
        else:
            records = self.db.get_all_legal_records() if self.db else []
        
        # Group records by politician
        politicians_records = {}
        for record in records:
            pol_id = record[1]
            if pol_id not in politicians_records:
                politicians_records[pol_id] = {
                    "id": pol_id,
                    "name": record[8] or record[9],  # full_name or username
                    "position": record[10] or "N/A",
                    "party": record[11] or "N/A",
                    "profile_image": record[12],
                    "records": [],
                }
            politicians_records[pol_id]["records"].append({
                "id": record[0],
                "type": record[2],
                "title": record[3],
                "description": record[4],
                "date": record[5],
                "status": record[6],
                "created_at": record[7],
            })
        
        # Get all politicians to show those without records too
        all_politicians = self.db.get_users_by_role("politician") if self.db else []
        
        politician_cards = []
        
        # First show politicians with records
        for pol_id, pol_data in politicians_records.items():
            politician_cards.append(self._build_politician_card(pol_data))
        
        # Then show politicians without records (if not searching)
        if not self.search_query:
            for pol in all_politicians:
                pol_id = pol[0]
                if pol_id not in politicians_records:
                    pol_data = {
                        "id": pol_id,
                        "name": pol[5] or pol[1],
                        "position": pol[7] or "N/A",
                        "party": pol[8] or "N/A",
                        "profile_image": pol[10],
                        "records": [],
                    }
                    politician_cards.append(self._build_politician_card(pol_data))
        
        if not politician_cards:
            return ft.Container(
                content=ft.Text("No politicians found", color="#666666"),
                padding=20,
            )
        
        return ft.Column(politician_cards, spacing=12)
    
    def _build_politician_card(self, pol_data):
        """Build a card for a politician with their records"""
        has_records = len(pol_data["records"]) > 0
        
        # Build profile image or placeholder
        if pol_data.get("profile_image"):
            profile_widget = ft.Image(
                src=pol_data["profile_image"],
                width=50,
                height=50,
                fit=ft.ImageFit.COVER,
                border_radius=25,
            )
        else:
            profile_widget = ft.Container(
                content=ft.Text(
                    pol_data["name"][0].upper() if pol_data["name"] else "?",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                width=50,
                height=50,
                border_radius=25,
                bgcolor="#FF5722",
                alignment=ft.alignment.center,
            )
        
        # Build records list
        records_widgets = []
        for record in pol_data["records"]:
            status_color = self._get_status_color(record["status"])
            records_widgets.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        record["title"],
                                        size=13,
                                        weight=ft.FontWeight.W_600,
                                        color="#333333",
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            record["status"].capitalize(),
                                            size=10,
                                            color=ft.Colors.WHITE,
                                        ),
                                        bgcolor=status_color,
                                        border_radius=10,
                                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(
                                record["description"][:100] + "..." if len(record["description"]) > 100 else record["description"],
                                size=12,
                                color="#666666",
                            ) if record["description"] else ft.Container(),
                            ft.Row(
                                [
                                    ft.Text(
                                        record["date"] or "N/A",
                                        size=11,
                                        color="#999999",
                                    ),
                                    ft.Row(
                                        [
                                            self._build_record_action_button(record, "edit"),
                                            self._build_record_action_button(record, "verify") if record["status"] == "pending" else ft.Container(),
                                        ],
                                        spacing=4,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        spacing=4,
                    ),
                    bgcolor="#F8F9FA",
                    border_radius=8,
                    padding=12,
                    margin=ft.margin.only(top=8),
                )
            )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            profile_widget,
                            ft.Column(
                                [
                                    ft.Text(
                                        pol_data["name"],
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color="#333333",
                                    ),
                                    ft.Text(
                                        f"{pol_data['position']} - {pol_data['party']}",
                                        size=12,
                                        color="#666666",
                                    ),
                                    ft.Text(
                                        f"{'Records on file' if has_records else 'No records on file'}",
                                        size=11,
                                        color="#FF5722" if has_records else "#4CAF50",
                                        italic=True,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                        ],
                        spacing=12,
                    ),
                    *records_widgets,
                ],
            ),
            border=ft.border.all(1, "#E0E0E0"),
            border_radius=12,
            padding=16,
        )
    
    def _build_record_action_button(self, record, action):
        """Build action button for a record"""
        if action == "verify":
            return ft.OutlinedButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.CHECK, size=14, color="#4CAF50"),
                        ft.Text("Verify", size=11),
                    ],
                    spacing=4,
                ),
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, "#4CAF50"),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                ),
                on_click=lambda e, r=record: self._verify_record(r),
            )
        elif action == "edit":
            return ft.OutlinedButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.EDIT, size=14, color="#2196F3"),
                        ft.Text("Edit", size=11),
                    ],
                    spacing=4,
                ),
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, "#2196F3"),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                ),
                on_click=lambda e, r=record: self._show_edit_dialog(r),
            )
        return ft.Container()
    
    def _verify_record(self, record):
        """Verify a legal record"""
        self.db.update_legal_record_status(record["id"], "verified", self.current_user_id)
        
        # Log the action
        self.db.log_action(
            action="Legal Record Verified",
            action_type="legal_record_status",
            description=f"Verified record: {record['title']}",
            user_id=self.current_user_id,
            user_role="nbi",
            target_type="legal_record",
            target_id=record["id"],
        )
        
        self._refresh_records()
        self._show_success("Record verified successfully")
    
    def _show_edit_dialog(self, record):
        """Show dialog to edit a record"""
        record_types = [
            ft.dropdown.Option("Graft and Corruption Case"),
            ft.dropdown.Option("Conflict of Interest Allegation"),
            ft.dropdown.Option("Tax Compliance Issue"),
            ft.dropdown.Option("Libel Case"),
            ft.dropdown.Option("Criminal Case"),
            ft.dropdown.Option("Administrative Case"),
            ft.dropdown.Option("Civil Case"),
            ft.dropdown.Option("Other"),
        ]
        
        edit_type_dropdown = ft.Dropdown(
            label="Record Type",
            options=record_types,
            value=record["type"],
            width=350,
        )
        
        edit_title_field = ft.TextField(
            label="Title",
            value=record["title"],
            width=350,
        )
        
        edit_description_field = ft.TextField(
            label="Description",
            value=record["description"] or "",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=350,
        )
        
        edit_date_field = DatePickerField(
            label="Date",
            value=record["date"] or "",
            width=250,
        )
        
        status_options = [
            ft.dropdown.Option("pending", "Pending"),
            ft.dropdown.Option("verified", "Verified"),
            ft.dropdown.Option("dismissed", "Dismissed"),
            ft.dropdown.Option("rejected", "Rejected"),
        ]
        
        edit_status_dropdown = ft.Dropdown(
            label="Status",
            options=status_options,
            value=record["status"],
            width=200,
        )
        
        def save_changes(e):
            if not edit_title_field.value:
                self._show_error("Title is required")
                return
            
            # Update record details
            success = self.db.update_legal_record(
                record["id"],
                edit_type_dropdown.value,
                edit_title_field.value,
                edit_description_field.value,
                edit_date_field.value,
            )
            
            # Update status if changed
            status_changed = False
            if edit_status_dropdown.value != record["status"]:
                self.db.update_legal_record_status(
                    record["id"],
                    edit_status_dropdown.value,
                    self.current_user_id,
                )
                status_changed = True
            
            if success:
                # Log the action
                description = f"Updated record: {edit_title_field.value}"
                if status_changed:
                    description += f" (status changed to {edit_status_dropdown.value})"
                
                self.db.log_action(
                    action="Legal Record Updated",
                    action_type="legal_record_edit",
                    description=description,
                    user_id=self.current_user_id,
                    user_role="nbi",
                    target_type="legal_record",
                    target_id=record["id"],
                )
                
                close_dialog(e)
                self._refresh_records()
                self._show_success("Record updated successfully")
            else:
                self._show_error("Failed to update record")
        
        def close_dialog(e):
            self.edit_dialog.open = False
            self.page.update()
        
        self.edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Edit Record", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    [
                        edit_type_dropdown,
                        ft.Container(height=8),
                        edit_title_field,
                        ft.Container(height=8),
                        edit_description_field,
                        ft.Container(height=8),
                        ft.Row(
                            [
                                edit_date_field,
                                edit_status_dropdown,
                            ],
                            spacing=12,
                        ),
                    ],
                    tight=True,
                ),
                width=400,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.ElevatedButton(
                    "Save Changes",
                    bgcolor="#FF5722",
                    color=ft.Colors.WHITE,
                    on_click=save_changes,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.overlay.append(self.edit_dialog)
        self.edit_dialog.open = True
        self.page.update()
    
    def _get_status_color(self, status):
        """Get color for status badge"""
        status_colors = {
            "pending": "#FFC107",
            "verified": "#4CAF50",
            "dismissed": "#9E9E9E",
            "rejected": "#F44336",
        }
        return status_colors.get(status.lower(), "#9E9E9E")
    
    def _build_news_section(self):
        """Build news post creator section for NBI announcements"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "News & Legal Updates",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Create legal updates and announcements for voters",
                        size=12,
                        color="#666666",
                    ),
                    ft.Container(height=16),
                    NewsPostCreator(
                        db=self.db,
                        author_id=self.current_user_id,
                        author_role="nbi",
                        on_post_created=self._on_news_post_created,
                    ),
                    ft.Container(height=16),
                    MyPostsList(
                        db=self.db,
                        author_id=self.current_user_id,
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
    
    def _refresh_records(self):
        """Refresh the records list"""
        if self.records_container:
            self.records_container.controls = [self._build_records_list()]
            self._refresh_stats()
            if self.page:
                self.page.update()
    
    def _refresh_stats(self):
        """Refresh the statistics - rebuild the UI"""
        # For simplicity, just update the page
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _show_error(self, message):
        """Show error snackbar"""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message, color=ft.Colors.WHITE),
                bgcolor="#F44336",
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _show_success(self, message):
        """Show success snackbar"""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message, color=ft.Colors.WHITE),
                bgcolor="#4CAF50",
            )
            self.page.snack_bar.open = True
            self.page.update()
