import flet as ft
from datetime import datetime


class NewsFeedCard(ft.Container):
    """Individual news post card component"""
    
    def __init__(self, post: dict):
        super().__init__()
        self.post = post
        self._build()
    
    def _build(self):
        # Role badge colors
        role_colors = {
            "politician": ("#2196F3", "Politician"),
            "nbi": ("#FF5722", "NBI"),
            "comelec": ("#9C27B0", "COMELEC"),
        }
        
        role_color, role_label = role_colors.get(
            self.post.get("author_role", ""), 
            ("#757575", "Official")
        )
        
        # Category badge
        category_colors = {
            "announcement": "#4CAF50",
            "campaign": "#2196F3",
            "legal": "#FF5722",
            "election": "#9C27B0",
            "general": "#757575",
        }
        category = self.post.get("category", "general")
        category_color = category_colors.get(category, "#757575")
        
        # Format date
        created_at = self.post.get("created_at", "")
        if created_at:
            try:
                dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                formatted_date = dt.strftime("%b %d, %Y at %I:%M %p")
            except:
                formatted_date = created_at
        else:
            formatted_date = "Just now"
        
        # Author info
        author_name = self.post.get("author_name", "Unknown")
        author_position = self.post.get("author_position", "")
        author_party = self.post.get("author_party", "")
        
        # Build subtitle
        subtitle_parts = []
        if author_position:
            subtitle_parts.append(author_position)
        if author_party:
            subtitle_parts.append(author_party)
        author_subtitle = " • ".join(subtitle_parts) if subtitle_parts else role_label
        
        # Pinned indicator
        pinned_badge = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.PUSH_PIN, size=12, color=ft.Colors.WHITE),
                    ft.Text("Pinned", size=10, color=ft.Colors.WHITE),
                ],
                spacing=4,
            ),
            bgcolor="#FF9800",
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=12,
            visible=self.post.get("is_pinned", False),
        )
        
        self.content = ft.Container(
            content=ft.Column(
                [
                    # Header row
                    ft.Row(
                        [
                            # Author avatar
                            ft.Container(
                                content=ft.Text(
                                    author_name[0].upper() if author_name else "?",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                width=40,
                                height=40,
                                bgcolor=role_color,
                                border_radius=20,
                                alignment=ft.alignment.center,
                            ),
                            # Author info
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                author_name,
                                                size=14,
                                                weight=ft.FontWeight.W_600,
                                            ),
                                            ft.Container(
                                                content=ft.Text(
                                                    role_label,
                                                    size=10,
                                                    color=ft.Colors.WHITE,
                                                ),
                                                bgcolor=role_color,
                                                padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                                border_radius=10,
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Text(
                                        author_subtitle,
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            pinned_badge,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    
                    # Title
                    ft.Text(
                        self.post.get("title", "Untitled"),
                        size=16,
                        weight=ft.FontWeight.W_600,
                    ),
                    
                    # Content
                    ft.Text(
                        self.post.get("content", ""),
                        size=14,
                        color=ft.Colors.GREY_800,
                    ),
                    
                    # Footer with category and date
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(
                                    category.capitalize(),
                                    size=11,
                                    color=ft.Colors.WHITE,
                                ),
                                bgcolor=category_color,
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=12,
                            ),
                            ft.Container(expand=True),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.ACCESS_TIME, size=12, color=ft.Colors.GREY_500),
                                    ft.Text(
                                        formatted_date,
                                        size=11,
                                        color=ft.Colors.GREY_500,
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                    ),
                ],
                spacing=12,
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )


class NewsFeed(ft.Column):
    """News feed component for displaying updates from officials"""
    
    def __init__(self, db, filter_role=None):
        super().__init__()
        self.db = db
        self.filter_role = filter_role
        self.filter_category = None
        self.posts = []
        
        self.expand = True
        self.spacing = 0
        self._build_ui()
    
    def _build_ui(self):
        self.posts = self._load_posts()
        
        # Filter buttons
        filter_row = ft.Row(
            [
                ft.Text("Filter by:", size=12, color=ft.Colors.GREY_600),
                self._create_filter_chip("All", None),
                self._create_filter_chip("Politicians", "politician"),
                self._create_filter_chip("NBI", "nbi"),
                self._create_filter_chip("COMELEC", "comelec"),
            ],
            spacing=8,
            wrap=True,
        )
        
        category_row = ft.Row(
            [
                ft.Text("Category:", size=12, color=ft.Colors.GREY_600),
                self._create_category_chip("All", None),
                self._create_category_chip("Announcements", "announcement"),
                self._create_category_chip("Campaign", "campaign"),
                self._create_category_chip("Legal", "legal"),
                self._create_category_chip("Election", "election"),
            ],
            spacing=8,
            wrap=True,
        )
        
        # Posts list
        if self.posts:
            posts_content = ft.Column(
                [NewsFeedCard(post) for post in self.posts],
                spacing=16,
            )
        else:
            posts_content = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ARTICLE_OUTLINED, size=48, color=ft.Colors.GREY_400),
                        ft.Text(
                            "No updates yet",
                            size=16,
                            color=ft.Colors.GREY_500,
                        ),
                        ft.Text(
                            "Check back later for announcements from officials",
                            size=12,
                            color=ft.Colors.GREY_400,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=40,
                alignment=ft.alignment.center,
            )
        
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        # Header
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.NEWSPAPER, size=24, color="#1976D2"),
                                ft.Text(
                                    "News Feed",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Text(
                            "Latest updates from politicians, NBI, and COMELEC",
                            size=12,
                            color=ft.Colors.GREY_600,
                        ),
                        ft.Divider(height=1, color=ft.Colors.GREY_300),
                        filter_row,
                        category_row,
                        ft.Divider(height=1, color=ft.Colors.GREY_300),
                        posts_content,
                    ],
                    spacing=12,
                ),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                    offset=ft.Offset(0, 2),
                ),
            ),
        ]
    
    def _create_filter_chip(self, label, role_value):
        is_selected = self.filter_role == role_value
        
        return ft.Container(
            content=ft.Text(
                label,
                size=12,
                color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_700,
            ),
            bgcolor="#1976D2" if is_selected else ft.Colors.GREY_200,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=16,
            on_click=lambda e, r=role_value: self._on_role_filter(r),
            ink=True,
        )
    
    def _create_category_chip(self, label, category_value):
        is_selected = self.filter_category == category_value
        
        return ft.Container(
            content=ft.Text(
                label,
                size=12,
                color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_700,
            ),
            bgcolor="#4CAF50" if is_selected else ft.Colors.GREY_200,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=16,
            on_click=lambda e, c=category_value: self._on_category_filter(c),
            ink=True,
        )
    
    def _on_role_filter(self, role):
        self.filter_role = role
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _on_category_filter(self, category):
        self.filter_category = category
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _load_posts(self):
        if self.db:
            return self.db.get_news_posts(
                limit=50,
                category=self.filter_category,
                author_role=self.filter_role
            )
        return []
    
    def refresh(self):
        """Refresh the news feed"""
        self._build_ui()
        if self.page:
            self.page.update()
