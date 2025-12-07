import flet as ft
from datetime import datetime


class AuditLogPage(ft.Column):
    """Audit Log Page - View system activity logs based on role permissions"""
    
    def __init__(self, username, db, user_role, on_back, current_user_id=None):
        super().__init__()
        self.username = username
        self.db = db
        self.user_role = user_role
        self.on_back = on_back
        self.current_user_id = current_user_id
        
        # Search and filter state
        self.search_query = ""
        self.selected_filter = "all"
        
        # UI references
        self.logs_container = None
        self.search_field = None
        self.stats_row = None
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the main UI"""
        self.controls = [
            self._build_header(),
            ft.Container(
                content=ft.Column(
                    [
                        self._build_stats_section(),
                        ft.Container(height=20),
                        self._build_filters_section(),
                        ft.Container(height=20),
                        self._build_logs_section(),
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
        """Build the header"""
        role_colors = {
            'comelec': '#4CAF50',
            'nbi': '#FF5722',
            'politician': '#5C6BC0',
        }
        header_color = role_colors.get(self.user_role, '#5C6BC0')
        
        role_labels = {
            'comelec': 'COMELEC',
            'nbi': 'NBI',
            'politician': 'Politician',
        }
        role_label = role_labels.get(self.user_role, self.user_role.title())
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color="#333333",
                                on_click=lambda e: self.on_back(),
                            ),
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.HISTORY,
                                    color=ft.Colors.WHITE,
                                    size=24,
                                ),
                                bgcolor=header_color,
                                border_radius=8,
                                padding=8,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Audit Logs",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color="#333333",
                                    ),
                                    ft.Text(
                                        f"Viewing as {role_label}",
                                        size=12,
                                        color="#666666",
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Container(
                        content=ft.Text(
                            f"Role: {role_label}",
                            size=12,
                            color=ft.Colors.WHITE,
                        ),
                        bgcolor=header_color,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=16,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        )
    
    def _build_stats_section(self):
        """Build statistics cards"""
        stats = self.db.get_audit_log_stats() if self.db else {'total': 0, 'today': 0, 'by_type': []}
        
        # Count by type for display
        type_counts = dict(stats.get('by_type', []))
        
        stats_cards = [
            self._create_stat_card("Total Logs", str(stats.get('total', 0)), ft.Icons.LIST_ALT, "#5C6BC0"),
            self._create_stat_card("Today", str(stats.get('today', 0)), ft.Icons.TODAY, "#4CAF50"),
        ]
        
        # Add type-specific stats based on role
        if self.user_role == 'comelec':
            stats_cards.append(
                self._create_stat_card("Voting Actions", str(type_counts.get('voting', 0)), ft.Icons.HOW_TO_VOTE, "#FF9800")
            )
            stats_cards.append(
                self._create_stat_card("User Actions", str(type_counts.get('user', 0)), ft.Icons.PEOPLE, "#E91E63")
            )
        elif self.user_role == 'nbi':
            stats_cards.append(
                self._create_stat_card("Legal Records", str(type_counts.get('legal_record', 0)), ft.Icons.GAVEL, "#FF5722")
            )
        elif self.user_role == 'politician':
            stats_cards.append(
                self._create_stat_card("Verifications", str(type_counts.get('verification', 0)), ft.Icons.VERIFIED, "#4CAF50")
            )
        
        self.stats_row = ft.Row(
            stats_cards,
            spacing=16,
            wrap=True,
        )
        
        return self.stats_row
    
    def _create_stat_card(self, title, value, icon, color):
        """Create a statistics card"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icon, color=ft.Colors.WHITE, size=20),
                        bgcolor=color,
                        border_radius=8,
                        padding=10,
                    ),
                    ft.Column(
                        [
                            ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color="#333333"),
                            ft.Text(title, size=12, color="#666666"),
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
                spacing=12,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=16,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            width=200,
        )
    
    def _build_filters_section(self):
        """Build search and filter controls"""
        self.search_field = ft.TextField(
            hint_text="Search logs by action, description, or user...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=8,
            height=45,
            bgcolor=ft.Colors.WHITE,
            border_color="#E0E0E0",
            focused_border_color="#5C6BC0",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            on_change=self._on_search_change,
            expand=True,
        )
        
        # Filter buttons based on role
        filter_options = self._get_filter_options()
        
        filter_buttons = ft.Row(
            [
                ft.ElevatedButton(
                    text=label,
                    bgcolor="#5C6BC0" if self.selected_filter == value else ft.Colors.WHITE,
                    color=ft.Colors.WHITE if self.selected_filter == value else "#333333",
                    on_click=lambda e, v=value: self._apply_filter(v),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                )
                for value, label in filter_options
            ],
            spacing=8,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([self.search_field], expand=True),
                    ft.Container(height=12),
                    filter_buttons,
                ],
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=16,
        )
    
    def _get_filter_options(self):
        """Get filter options based on role"""
        base_options = [("all", "All")]
        
        if self.user_role == 'comelec':
            return base_options + [
                ("login", "Login/Logout"),
                ("voting", "Voting"),
                ("user", "User Management"),
                ("verification", "Verifications"),
                ("legal_record", "Legal Records"),
            ]
        elif self.user_role == 'nbi':
            return base_options + [
                ("login", "Login/Logout"),
                ("legal_record", "Legal Records"),
            ]
        elif self.user_role == 'politician':
            return base_options + [
                ("verification", "Verifications"),
                ("legal_record", "Legal Records"),
            ]
        
        return base_options
    
    def _build_logs_section(self):
        """Build the logs list section"""
        logs = self._get_filtered_logs()
        
        self.logs_container = ft.Container(
            content=self._build_logs_list(logs),
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Activity Log", size=16, weight=ft.FontWeight.BOLD, color="#333333"),
                            ft.Text(f"{len(logs)} entries", size=12, color="#666666"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=12),
                    self.logs_container,
                ],
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=16,
        )
    
    def _get_filtered_logs(self):
        """Get logs based on current filters"""
        if not self.db:
            return []
        
        if self.search_query:
            logs = self.db.search_audit_logs(self.search_query, self.user_role)
        elif self.selected_filter == "all":
            logs = self.db.get_audit_logs_for_role(self.user_role)
        else:
            logs = self.db.get_audit_logs(action_type=self.selected_filter)
        
        return logs
    
    def _build_logs_list(self, logs):
        """Build the list of log entries"""
        if not logs:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.HISTORY, size=48, color="#CCCCCC"),
                        ft.Text("No audit logs found", size=14, color="#666666"),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=40,
                alignment=ft.alignment.center,
            )
        
        log_items = []
        for log in logs:
            log_id, action, action_type, description, user_id, user_role, \
            target_type, target_id, details, ip_address, created_at, username, full_name = log
            
            log_items.append(self._build_log_item(
                action=action,
                action_type=action_type,
                description=description,
                user_name=full_name or username or "System",
                user_role=user_role,
                created_at=created_at,
                target_type=target_type,
            ))
        
        return ft.Column(log_items, spacing=8)
    
    def _build_log_item(self, action, action_type, description, user_name, user_role, created_at, target_type):
        """Build a single log item"""
        # Icon and color based on action type
        type_config = {
            'login': (ft.Icons.LOGIN, '#4CAF50'),
            'logout': (ft.Icons.LOGOUT, '#FF9800'),
            'voting': (ft.Icons.HOW_TO_VOTE, '#5C6BC0'),
            'user': (ft.Icons.PERSON, '#2196F3'),
            'verification': (ft.Icons.VERIFIED, '#4CAF50'),
            'legal_record': (ft.Icons.GAVEL, '#FF5722'),
            'election': (ft.Icons.BALLOT, '#9C27B0'),
        }
        
        icon, color = type_config.get(action_type, (ft.Icons.INFO, '#666666'))
        
        # Format timestamp
        try:
            if created_at:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                time_str = dt.strftime("%b %d, %Y %I:%M %p")
            else:
                time_str = "Unknown"
        except:
            time_str = str(created_at) if created_at else "Unknown"
        
        # Role badge
        role_colors = {
            'comelec': '#4CAF50',
            'nbi': '#FF5722',
            'politician': '#5C6BC0',
            'voter': '#2196F3',
        }
        role_color = role_colors.get(user_role, '#666666')
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icon, color=ft.Colors.WHITE, size=16),
                        bgcolor=color,
                        border_radius=8,
                        padding=8,
                    ),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(action, size=14, weight=ft.FontWeight.W_500, color="#333333"),
                                    ft.Container(
                                        content=ft.Text(action_type.replace('_', ' ').title(), size=10, color=ft.Colors.WHITE),
                                        bgcolor=color,
                                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                        border_radius=10,
                                    ),
                                ],
                                spacing=8,
                            ),
                            ft.Text(description or "No description", size=12, color="#666666"),
                            ft.Row(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.PERSON, size=12, color="#999999"),
                                            ft.Text(user_name, size=11, color="#999999"),
                                        ],
                                        spacing=4,
                                    ),
                                    ft.Container(
                                        content=ft.Text(user_role or "system", size=10, color=ft.Colors.WHITE),
                                        bgcolor=role_color,
                                        padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                        border_radius=8,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.ACCESS_TIME, size=12, color="#999999"),
                                            ft.Text(time_str, size=11, color="#999999"),
                                        ],
                                        spacing=4,
                                    ),
                                ],
                                spacing=16,
                            ),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                ],
                spacing=12,
            ),
            bgcolor="#FAFAFA",
            border_radius=8,
            padding=12,
            border=ft.border.all(1, "#E0E0E0"),
        )
    
    def _on_search_change(self, e):
        """Handle search input change"""
        self.search_query = e.control.value
        self._update_logs()
    
    def _apply_filter(self, filter_value):
        """Apply a filter"""
        self.selected_filter = filter_value
        self._rebuild_filters()
        self._update_logs()
    
    def _rebuild_filters(self):
        """Rebuild filter buttons to show selected state"""
        # This will be called when filter changes
        if self.page:
            self._build_ui()
            self.page.update()
    
    def _update_logs(self):
        """Update the logs list"""
        if self.logs_container:
            logs = self._get_filtered_logs()
            self.logs_container.content = self._build_logs_list(logs)
            if self.page:
                self.page.update()
