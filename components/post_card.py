import flet as ft


class PostCard(ft.Container):
    """Individual post card component"""
    
    def __init__(self, username, handle, content, checkmarks=None, 
                 avatar_color=None, is_verified=False, post_tag=None,
                 on_like=None, on_comment=None, on_share=None):
        super().__init__()
        self.username = username
        self.handle = handle
        self.post_content = content
        self.checkmarks = checkmarks or []
        self.avatar_color = avatar_color or ft.Colors.ORANGE_300
        self.is_verified = is_verified
        self.post_tag = post_tag
        self.on_like = on_like
        self.on_comment = on_comment
        self.on_share = on_share
        
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
        
        # User info row
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
            ],
            spacing=10,
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
                ),
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
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        # Main content layout
        return ft.Column(
            controls=[
                header,
                ft.Container(height=10),
                content_column,
            ],
            spacing=0,
        )
