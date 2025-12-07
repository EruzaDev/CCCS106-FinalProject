import flet as ft


class NewsPostCreator(ft.Container):
    """Component for creating news posts (for officials)"""
    
    def __init__(self, db, author_id, author_role, on_post_created=None):
        super().__init__()
        self.db = db
        self.author_id = author_id
        self.author_role = author_role
        self.on_post_created = on_post_created
        
        # Form fields
        self.title_field = None
        self.content_field = None
        self.category_dropdown = None
        self.pinned_checkbox = None
        self.status_text = None
        
        self._build()
    
    def _build(self):
        self.title_field = ft.TextField(
            label="Title",
            hint_text="Enter post title...",
            border_radius=8,
            bgcolor=ft.Colors.WHITE,
        )
        
        self.content_field = ft.TextField(
            label="Content",
            hint_text="Write your announcement or update...",
            multiline=True,
            min_lines=3,
            max_lines=6,
            border_radius=8,
            bgcolor=ft.Colors.WHITE,
        )
        
        # Category options based on role
        category_options = [
            ft.dropdown.Option("general", "General"),
            ft.dropdown.Option("announcement", "Announcement"),
        ]
        
        if self.author_role == "politician":
            category_options.append(ft.dropdown.Option("campaign", "Campaign Update"))
        elif self.author_role == "nbi":
            category_options.append(ft.dropdown.Option("legal", "Legal Notice"))
        elif self.author_role == "comelec":
            category_options.append(ft.dropdown.Option("election", "Election Update"))
        
        self.category_dropdown = ft.Dropdown(
            label="Category",
            options=category_options,
            value="general",
            border_radius=8,
            bgcolor=ft.Colors.WHITE,
            width=200,
        )
        
        self.pinned_checkbox = ft.Checkbox(
            label="Pin this post",
            value=False,
        )
        
        self.status_text = ft.Text("", size=12, visible=False)
        
        # Role-specific styling
        role_colors = {
            "politician": "#2196F3",
            "nbi": "#FF5722",
            "comelec": "#4CAF50",
        }
        accent_color = role_colors.get(self.author_role, "#757575")
        
        self.content = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.EDIT_NOTE, size=24, color=accent_color),
                            ft.Text(
                                "Create New Post",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Text(
                        "Share updates with voters",
                        size=12,
                        color=ft.Colors.GREY_600,
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_300),
                    self.title_field,
                    self.content_field,
                    ft.Row(
                        [
                            self.category_dropdown,
                            self.pinned_checkbox,
                        ],
                        spacing=20,
                    ),
                    self.status_text,
                    ft.Row(
                        [
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                "Post",
                                icon=ft.Icons.SEND,
                                bgcolor=accent_color,
                                color=ft.Colors.WHITE,
                                on_click=self._on_post_click,
                            ),
                        ],
                    ),
                ],
                spacing=12,
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_300),
        )
    
    def _on_post_click(self, e):
        """Handle post button click"""
        title = self.title_field.value.strip() if self.title_field.value else ""
        content = self.content_field.value.strip() if self.content_field.value else ""
        
        if not title:
            self._show_status("Please enter a title", error=True)
            return
        
        if not content:
            self._show_status("Please enter content", error=True)
            return
        
        # Create the post
        category = self.category_dropdown.value or "general"
        is_pinned = self.pinned_checkbox.value
        
        post_id = self.db.create_news_post(
            author_id=self.author_id,
            author_role=self.author_role,
            title=title,
            content=content,
            category=category,
            is_pinned=is_pinned
        )
        
        if post_id:
            self._show_status("Post created successfully!", error=False)
            # Clear form
            self.title_field.value = ""
            self.content_field.value = ""
            self.category_dropdown.value = "general"
            self.pinned_checkbox.value = False
            
            if self.on_post_created:
                self.on_post_created(post_id)
        else:
            self._show_status("Failed to create post", error=True)
        
        if self.page:
            self.page.update()
    
    def _show_status(self, message, error=False):
        """Show status message"""
        self.status_text.value = message
        self.status_text.color = ft.Colors.RED if error else ft.Colors.GREEN
        self.status_text.visible = True
        if self.page:
            self.page.update()


class MyPostsList(ft.Column):
    """Component showing the user's own posts with edit/delete options"""
    
    def __init__(self, db, author_id):
        super().__init__()
        self.db = db
        self.author_id = author_id
        self.spacing = 12
        self._build()
    
    def _build(self):
        posts = self.db.get_news_posts_by_author(self.author_id) if self.db else []
        
        if not posts:
            self.controls = [
                ft.Container(
                    content=ft.Text(
                        "You haven't posted any updates yet.",
                        size=14,
                        color=ft.Colors.GREY_500,
                    ),
                    padding=20,
                ),
            ]
            return
        
        self.controls = [
            ft.Text(
                f"Your Posts ({len(posts)})",
                size=16,
                weight=ft.FontWeight.W_600,
            ),
        ]
        
        for post in posts:
            post_id, title, content, category, is_pinned, created_at, updated_at = post
            
            # Format date
            date_display = created_at[:10] if created_at else "Unknown date"
            
            post_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    title,
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    expand=True,
                                ),
                                ft.Container(
                                    content=ft.Icon(ft.Icons.PUSH_PIN, size=14, color=ft.Colors.ORANGE),
                                    visible=is_pinned,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_size=18,
                                    icon_color=ft.Colors.RED,
                                    tooltip="Delete post",
                                    on_click=lambda e, pid=post_id: self._delete_post(pid),
                                ),
                            ],
                        ),
                        ft.Text(
                            content[:100] + "..." if len(content) > 100 else content,
                            size=12,
                            color=ft.Colors.GREY_700,
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        category.capitalize(),
                                        size=10,
                                        color=ft.Colors.WHITE,
                                    ),
                                    bgcolor=ft.Colors.GREY_600,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                    border_radius=10,
                                ),
                                ft.Text(
                                    date_display,
                                    size=10,
                                    color=ft.Colors.GREY_500,
                                ),
                            ],
                            spacing=8,
                        ),
                    ],
                    spacing=8,
                ),
                padding=12,
                bgcolor=ft.Colors.GREY_50,
                border_radius=8,
            )
            
            self.controls.append(post_card)
    
    def _delete_post(self, post_id):
        """Delete a post"""
        if self.db:
            self.db.delete_news_post(post_id)
            self._build()
            if self.page:
                self.page.update()
    
    def refresh(self):
        """Refresh the posts list"""
        self._build()
        if self.page:
            self.page.update()
