import flet as ft


class PostCard(ft.Container):
    """Individual post card component with image support"""
    
    def __init__(self, username, handle, content, checkmarks=None, 
                 avatar_color=None, is_verified=False, post_tag=None,
                 image_url=None, timestamp=None,
                 on_like=None, on_comment=None, on_share=None, on_report=None):
        super().__init__()
        self.username = username
        self.handle = handle
        self.post_content = content
        self.checkmarks = checkmarks or []
        self.avatar_color = avatar_color or ft.Colors.ORANGE_300
        self.is_verified = is_verified
        self.post_tag = post_tag
        self.image_url = image_url
        self.timestamp = timestamp
        self.on_like = on_like
        self.on_comment = on_comment
        self.on_share = on_share
        self.on_report = on_report
        
        # Track interaction states
        self.is_liked = False
        self.like_count = 0
        self.comment_count = 0
        self.share_count = 0
        
        # Build the UI
        self.content = self._build_ui()
        self.bgcolor = ft.Colors.WHITE
        self.border_radius = 15
        self.padding = 15
        self.margin = ft.margin.only(bottom=15)
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
        )
    
    def _build_ui(self):
        """Build the post card UI"""
        
        # User avatar
        avatar = ft.Container(
            content=ft.Text(
                self.username[0] if self.username else "?",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            width=50,
            height=50,
            bgcolor=self.avatar_color,
            border_radius=25,
            alignment=ft.alignment.center,
        )
        
        # User info row with timestamp
        user_info = ft.Row(
            controls=[
                ft.Text(
                    self.username,
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                ft.Text(
                    self.handle,
                    size=13,
                    color=ft.Colors.GREY_500,
                ),
                ft.Text(
                    f"· {self.timestamp}" if self.timestamp else "",
                    size=12,
                    color=ft.Colors.GREY_400,
                ),
            ],
            spacing=8,
        )
        
        # Post tag (if any)
        tag_widget = None
        if self.post_tag:
            tag_widget = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CIRCLE, size=8, color=ft.Colors.GREEN_400),
                        ft.Text(
                            self.post_tag,
                            size=12,
                            color=ft.Colors.GREY_700,
                        ),
                    ],
                    spacing=5,
                ),
                margin=ft.margin.only(top=5),
            )
        
        # Post content
        content_column = ft.Column(
            controls=[
                ft.Text(
                    self.post_content,
                    size=13,
                    color=ft.Colors.BLACK87,
                ) if self.post_content else ft.Container(),
            ],
            spacing=5,
        )
        
        # Add checkmarks if any
        if self.checkmarks:
            for check in self.checkmarks:
                content_column.controls.append(
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.CHECK,
                                size=16,
                                color=ft.Colors.BLUE_400,
                            ),
                            ft.Text(
                                check,
                                size=12,
                                color=ft.Colors.BLUE_400,
                            ),
                        ],
                        spacing=5,
                    )
                )
        
        # Image display (if any)
        image_widget = None
        if self.image_url:
            image_widget = ft.Container(
                content=ft.Image(
                    src=self.image_url,
                    fit=ft.ImageFit.COVER,
                    border_radius=10,
                ),
                border_radius=10,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                margin=ft.margin.only(top=10),
                height=250,
            )
        
        # Header row with avatar and user info
        header = ft.Row(
            controls=[
                avatar,
                ft.Container(width=10),
                ft.Column(
                    controls=[
                        user_info,
                        tag_widget if tag_widget else ft.Container(),
                    ],
                    spacing=0,
                ),
                ft.Container(expand=True),
                # More options menu
                ft.PopupMenuButton(
                    icon=ft.Icons.MORE_HORIZ,
                    icon_color=ft.Colors.GREY_500,
                    items=[
                        ft.PopupMenuItem(text="Report post", icon=ft.Icons.FLAG_OUTLINED, on_click=self._handle_report),
                    ],
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        # Interaction buttons (Like only)
        self.like_button = ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.FAVORITE if self.is_liked else ft.Icons.FAVORITE_BORDER,
                        size=18,
                        color=ft.Colors.RED_400 if self.is_liked else ft.Colors.GREY_500,
                    ),
                    ft.Text(
                        f"{self.like_count}" if self.like_count > 0 else "Like",
                        size=12,
                        color=ft.Colors.RED_400 if self.is_liked else ft.Colors.GREY_600,
                    ),
                ],
                spacing=5,
            ),
            on_click=self._handle_like,
        )
        
        interactions_row = ft.Row(
            controls=[
                self.like_button,
            ],
            spacing=10,
        )
        
        # Build main content
        main_controls = [header, ft.Container(height=10), content_column]
        
        if image_widget:
            main_controls.append(image_widget)
        
        main_controls.extend([
            ft.Container(height=10),
            ft.Divider(height=1, color=ft.Colors.GREY_200),
            interactions_row,
        ])
        
        return ft.Column(
            controls=main_controls,
            spacing=0,
        )
    
    def _handle_like(self, e):
        """Handle like button click"""
        self.is_liked = not self.is_liked
        if self.is_liked:
            self.like_count += 1
        else:
            self.like_count = max(0, self.like_count - 1)
        
        # Update button appearance
        self.like_button.content.controls[0].name = ft.Icons.FAVORITE if self.is_liked else ft.Icons.FAVORITE_BORDER
        self.like_button.content.controls[0].color = ft.Colors.RED_400 if self.is_liked else ft.Colors.GREY_500
        self.like_button.content.controls[1].value = f"{self.like_count}" if self.like_count > 0 else "Like"
        self.like_button.content.controls[1].color = ft.Colors.RED_400 if self.is_liked else ft.Colors.GREY_600
        self.like_button.update()
        
        if self.on_like:
            self.on_like(self.is_liked)
    
    def _handle_comment(self, e):
        """Handle comment button click"""
        if self.on_comment:
            self.on_comment()
    
    def _handle_share(self, e):
        """Handle share button click"""
        if self.on_share:
            self.on_share()
    
    def _handle_report(self, e):
        """Handle report button click"""
        if self.on_report:
            self.on_report()
