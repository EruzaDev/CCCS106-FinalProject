import flet as ft


class PostCreator(ft.Container):
    """Post creation component with write, photo options and image preview"""
    
    def __init__(self, page=None, on_write_post=None, on_upload_photo=None, 
                 on_submit=None):
        super().__init__()
        self.page = page
        self.on_write_post = on_write_post
        self.on_upload_photo = on_upload_photo
        self.on_submit = on_submit
        
        # Track selected image
        self.selected_image_path = None
        self.is_expanded = False
        
        # File picker for image selection
        self.file_picker = ft.FilePicker(
            on_result=self._handle_file_picked,
        )
        
        # Text input field
        self.post_input = ft.TextField(
            hint_text="What's on your mind?",
            border_radius=10,
            border_color=ft.Colors.GREY_200,
            focused_border_color=ft.Colors.BLUE_400,
            multiline=True,
            min_lines=3,
            max_lines=8,
            text_size=14,
            content_padding=ft.padding.all(15),
            on_change=self._on_input_change,
        )
        
        # Image preview container (initially hidden)
        self.image_preview = ft.Container(
            visible=False,
            margin=ft.margin.only(top=10),
        )
        
        # Submit button (initially disabled)
        self.submit_button = ft.ElevatedButton(
            text="Post",
            icon=ft.Icons.SEND,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.Colors.BLUE_600,
                    ft.ControlState.DISABLED: ft.Colors.GREY_300,
                },
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.DISABLED: ft.Colors.GREY_500,
                },
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=self._handle_submit,
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
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
        
        # Collapsed input area (shown when not expanded)
        self.collapsed_input = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.EDIT_NOTE, size=18, color=ft.Colors.GREY_400),
                    ft.Container(width=5),
                    ft.Text(
                        "What's on your mind?",
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
            on_click=self._expand_input,
            visible=not self.is_expanded,
        )
        
        # Expanded input area (shown when creating a post)
        self.expanded_input = ft.Container(
            content=ft.Column(
                controls=[
                    self.post_input,
                    self.image_preview,
                    ft.Container(height=10),
                    # Bottom action bar
                    ft.Row(
                        controls=[
                            # Add image button
                            ft.IconButton(
                                icon=ft.Icons.IMAGE_OUTLINED,
                                icon_color=ft.Colors.GREEN_600,
                                tooltip="Add image",
                                on_click=self._handle_upload_photo,
                            ),
                            ft.Container(expand=True),
                            # Cancel button
                            ft.TextButton(
                                text="Cancel",
                                style=ft.ButtonStyle(color=ft.Colors.GREY_600),
                                on_click=self._collapse_input,
                            ),
                            self.submit_button,
                        ],
                    ),
                ],
            ),
            visible=self.is_expanded,
        )
        
        return ft.Column(
            controls=[
                actions_row,
                ft.Container(height=10),
                self.collapsed_input,
                self.expanded_input,
                self.file_picker,
            ],
            spacing=0,
        )
    
    def _expand_input(self, e=None):
        """Expand to show the full input area"""
        self.is_expanded = True
        self.collapsed_input.visible = False
        self.expanded_input.visible = True
        self.update()
        # Focus the text input
        self.post_input.focus()
    
    def _collapse_input(self, e=None):
        """Collapse back to the simple input area"""
        self.is_expanded = False
        self.collapsed_input.visible = True
        self.expanded_input.visible = False
        self.post_input.value = ""
        self.selected_image_path = None
        self.image_preview.visible = False
        self.image_preview.content = None
        self.submit_button.disabled = True
        self.update()
    
    def _on_input_change(self, e):
        """Handle text input changes"""
        has_content = bool(self.post_input.value and self.post_input.value.strip())
        has_image = self.selected_image_path is not None
        self.submit_button.disabled = not (has_content or has_image)
        self.submit_button.update()
    
    def _handle_file_picked(self, e: ft.FilePickerResultEvent):
        """Handle file picker result"""
        if e.files and len(e.files) > 0:
            self.selected_image_path = e.files[0].path
            self._show_image_preview()
    
    def _show_image_preview(self):
        """Show the selected image preview"""
        if self.selected_image_path:
            self.image_preview.content = ft.Stack(
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src=self.selected_image_path,
                            fit=ft.ImageFit.COVER,
                            border_radius=10,
                        ),
                        width=200,
                        height=150,
                        border_radius=10,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    ),
                    # Remove button
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_size=16,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                            on_click=self._remove_image,
                        ),
                        right=5,
                        top=5,
                    ),
                ],
            )
            self.image_preview.visible = True
            self.submit_button.disabled = False
            self.update()
    
    def _remove_image(self, e):
        """Remove the selected image"""
        self.selected_image_path = None
        self.image_preview.visible = False
        self.image_preview.content = None
        self._on_input_change(None)
        self.update()
    
    def _handle_write_post(self, e):
        """Handle write post button click"""
        self._expand_input()
        if self.on_write_post:
            self.on_write_post()
    
    def _handle_upload_photo(self, e):
        """Handle upload photo button click"""
        if not self.is_expanded:
            self._expand_input()
        # Open file picker for images
        self.file_picker.pick_files(
            allowed_extensions=["png", "jpg", "jpeg", "gif", "webp"],
            allow_multiple=False,
            dialog_title="Select an image",
        )
        if self.on_upload_photo:
            self.on_upload_photo()
    
    def _handle_submit(self, e):
        """Handle post submission"""
        if self.on_submit:
            self.on_submit()
    
    def get_post_content(self):
        """Get the current post content"""
        return self.post_input.value
    
    def get_selected_image(self):
        """Get the selected image path"""
        return self.selected_image_path
    
    def clear_post(self):
        """Clear the post input and collapse"""
        self._collapse_input()
