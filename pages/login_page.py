import flet as ft


class LoginPage(ft.Container):
    """Login page with email/phone and password fields"""
    
    def __init__(self, on_login=None, on_create_account=None, on_forgot_password=None):
        super().__init__()
        self.on_login = on_login
        self.on_create_account = on_create_account
        self.on_forgot_password = on_forgot_password
        
        # Input fields
        self.email_field = ft.TextField(
            hint_text="Email or phone number",
            border_radius=20,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_400,
            height=45,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
        )
        
        self.password_field = ft.TextField(
            hint_text="Password",
            password=True,
            can_reveal_password=True,
            border_radius=20,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_400,
            height=45,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
        )
        
        # Build the UI
        self.content = self._build_ui()
        self.expand = True
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.LIGHT_BLUE_100, ft.Colors.LIGHT_BLUE_50],
        )
    
    def _build_ui(self):
        """Build the login page UI"""
        
        # Login form card
        login_card = ft.Container(
            content=ft.Column(
                controls=[
                    self.email_field,
                    ft.Container(height=10),
                    self.password_field,
                    ft.Container(height=15),
                    # Login button
                    ft.ElevatedButton(
                        text="Log In",
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_400,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=20),
                        ),
                        width=200,
                        height=40,
                        on_click=self._handle_login,
                    ),
                    ft.Container(height=10),
                    # Forgot password link
                    ft.TextButton(
                        text="Forgot Password?",
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_400,
                        ),
                        on_click=self._handle_forgot_password,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=30,
            width=280,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            ),
        )
        
        # Create new account button
        create_account_btn = ft.ElevatedButton(
            text="Create new account",
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=20),
            ),
            width=200,
            height=40,
            on_click=self._handle_create_account,
        )
        
        # Large background logo circle
        background_logo = ft.Container(
            content=ft.Image(
                src="assets/fd875946-c220-48f7-a5db-e8e1d3e0a2a0.jpg",
                width=450,
                height=450,
                fit=ft.ImageFit.COVER,
            ),
            width=450,
            height=450,
            border_radius=225,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )
        
        # Form content centered in the middle
        form_content = ft.Column(
            controls=[
                login_card,
                ft.Container(height=15),
                create_account_btn,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # Clipboard/notepad container (decorative)
        clipboard = ft.Stack(
            controls=[
                # Large logo background - centered
                ft.Container(
                    content=background_logo,
                    alignment=ft.alignment.center,
                    width=450,
                    height=450,
                ),
                # Paper/form container - centered on top
                ft.Container(
                    content=form_content,
                    width=450,
                    height=450,
                    alignment=ft.alignment.center,
                ),
            ],
            width=450,
            height=450,
        )
        
        # Main layout - properly centered
        return ft.Container(
            content=clipboard,
            expand=True,
            alignment=ft.alignment.center,
        )
    
    def _handle_login(self, e):
        """Handle login button click"""
        if self.on_login:
            self.on_login(self.email_field.value, self.password_field.value)
    
    def _handle_create_account(self, e):
        """Handle create account button click"""
        if self.on_create_account:
            self.on_create_account()
    
    def _handle_forgot_password(self, e):
        """Handle forgot password link click"""
        if self.on_forgot_password:
            self.on_forgot_password()
