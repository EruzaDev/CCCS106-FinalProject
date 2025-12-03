import flet as ft


class PostCreator(ft.Container):
    """Post creation component with write, photo, video options"""
    
    def __init__(self, on_write_post=None, on_upload_photo=None, 
                 on_upload_video=None, on_submit=None):
        super().__init__()
        self.on_write_post = on_write_post
        self.on_upload_photo = on_upload_photo
        self.on_upload_video = on_upload_video
        self.on_submit = on_submit
        
        # Text input field
        self.post_input = ft.TextField(
            hint_text="Write something here...",
            border_radius=10,
            border_color=ft.Colors.GREY_200,
            focused_border_color=ft.Colors.BLUE_400,
            multiline=True,
            min_lines=2,
            max_lines=5,
            text_size=14,
            content_padding=ft.padding.all(15),
        )
        
        # Build the UI
        self.content = self._build_ui()
        self.bgcolor = ft.Colors.WHITE
        self.border_radius = 15
        self.padding = 20
        self.margin = ft.margin.only(bottom=20)
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
        )
    
    def _build_ui(self):
        """Build the post creator UI"""
        
        # Action buttons row
        actions_row = ft.Row(
            controls=[
                # Write a post button
                ft.TextButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.EDIT, size=18, color=ft.Colors.AMBER_600),
                            ft.Text("Write a post", size=13, color=ft.Colors.GREY_700),
                        ],
                        spacing=5,
                    ),
                    on_click=self._handle_write_post,
                ),
                # Upload photo button
                ft.TextButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.PHOTO_CAMERA, size=18, color=ft.Colors.GREEN_600),
                            ft.Text("Upload photo", size=13, color=ft.Colors.GREY_700),
                        ],
                        spacing=5,
                    ),
                    on_click=self._handle_upload_photo,
                ),
                # Upload video button
                ft.TextButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.VIDEOCAM, size=18, color=ft.Colors.RED_600),
                            ft.Text("Upload video", size=13, color=ft.Colors.GREY_700),
                        ],
                        spacing=5,
                    ),
                    on_click=self._handle_upload_video,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
        
        # Input area
        input_area = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.EDIT_NOTE, size=18, color=ft.Colors.GREY_400),
                    ft.Container(width=5),
                    ft.Text(
                        "Write something here...",
                        size=13,
                        color=ft.Colors.GREY_400,
                    ),
                ],
            ),
            bgcolor=ft.Colors.GREY_50,
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            border=ft.border.all(1, ft.Colors.GREY_200),
            ink=True,
            on_click=self._show_input_field,
        )
        
        return ft.Column(
            controls=[
                actions_row,
                ft.Container(height=10),
                input_area,
            ],
            spacing=0,
        )
    
    def _handle_write_post(self, e):
        """Handle write post button click"""
        if self.on_write_post:
            self.on_write_post()
    
    def _handle_upload_photo(self, e):
        """Handle upload photo button click"""
        if self.on_upload_photo:
            self.on_upload_photo()
    
    def _handle_upload_video(self, e):
        """Handle upload video button click"""
        if self.on_upload_video:
            self.on_upload_video()
    
    def _show_input_field(self, e):
        """Show the text input field"""
        pass  # Can be expanded to show a dialog or expand the input area
    
    def get_post_content(self):
        """Get the current post content"""
        return self.post_input.value
    
    def clear_post(self):
        """Clear the post input"""
        self.post_input.value = ""
        self.post_input.update()
