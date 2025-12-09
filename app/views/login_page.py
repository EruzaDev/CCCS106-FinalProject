import flet as ft
from app.theme import AppTheme


class LoginPage(ft.Container):
    """Voting app login page with blue aesthetic theme"""
    
    def __init__(self, on_login, on_create_account, on_forgot_password):
        super().__init__()
        self.on_login_callback = on_login
        self.on_create_account = on_create_account
        self.on_forgot_password = on_forgot_password
        
        # Form fields with theme styling
        self.username_field = ft.TextField(
            label="Username",
            hint_text="Enter username",
            width=300,
            border_radius=10,
            bgcolor=AppTheme.BG_CARD,
            border_color=AppTheme.BORDER_LIGHT,
            focused_border_color=AppTheme.PRIMARY,
            cursor_color=AppTheme.PRIMARY,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            prefix_icon=ft.Icons.PERSON_OUTLINE,
        )
        
        self.password_field = ft.TextField(
            label="Password",
            hint_text="Enter password",
            password=True,
            can_reveal_password=True,
            width=300,
            border_radius=10,
            bgcolor=AppTheme.BG_CARD,
            border_color=AppTheme.BORDER_LIGHT,
            focused_border_color=AppTheme.PRIMARY,
            cursor_color=AppTheme.PRIMARY,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            prefix_icon=ft.Icons.LOCK_OUTLINE,
        )
        
        self.error_text = ft.Text(
            "",
            color=AppTheme.ERROR,
            size=12,
        )
        
        # Build the login card
        self.content = self._build_page()
        self.expand = True
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[AppTheme.BG_SECONDARY, AppTheme.BG_PRIMARY, "#E8F4FD"],
        )
        self.padding = 20
    
    def _build_page(self):
        """Build the complete login page"""
        return ft.Column(
            [
                # Header with branding
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.HOW_TO_VOTE,
                                    color=AppTheme.PRIMARY,
                                    size=24,
                                ),
                                bgcolor=AppTheme.SURFACE_LIGHT,
                                border_radius=8,
                                padding=8,
                            ),
                            ft.Text(
                                "HonestBallot",
                                size=20,
                                color=AppTheme.PRIMARY,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.only(left=30, top=25),
                    alignment=ft.alignment.top_left,
                ),
                
                # Centered login card
                ft.Container(
                    content=self._build_login_card(),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            expand=True,
        )
    
    def _build_login_card(self):
        """Build the white login card with blue theme"""
        return ft.Container(
            content=ft.Column(
                [
                    # Logo icon with gradient-like effect
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.HOW_TO_VOTE,
                            size=45,
                            color=ft.Colors.WHITE,
                        ),
                        width=80,
                        height=80,
                        bgcolor=AppTheme.PRIMARY,
                        border_radius=20,
                        alignment=ft.alignment.center,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=15,
                            color=ft.Colors.with_opacity(0.3, AppTheme.PRIMARY),
                            offset=ft.Offset(0, 5),
                        ),
                    ),
                    
                    ft.Container(height=15),
                    
                    # App name
                    ft.Text(
                        "HonestBallot",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    
                    # Tagline
                    ft.Text(
                        "Voter Education & Transparency Platform",
                        size=13,
                        color=AppTheme.TEXT_MUTED,
                    ),
                    
                    ft.Container(height=30),
                    
                    # Username field
                    self.username_field,
                    
                    ft.Container(height=10),
                    
                    # Password field
                    self.password_field,
                    
                    # Error text
                    self.error_text,
                    
                    ft.Container(height=15),
                    
                    # Login button
                    ft.ElevatedButton(
                        text="Sign In",
                        width=300,
                        height=50,
                        bgcolor=AppTheme.PRIMARY,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=3,
                        ),
                        on_click=self._handle_login,
                    ),
                    
                    ft.Container(height=15),
                    
                    # Divider with "or"
                    ft.Row(
                        [
                            ft.Container(
                                bgcolor=AppTheme.BORDER_LIGHT,
                                height=1,
                                expand=True,
                            ),
                            ft.Container(
                                content=ft.Text("or", size=12, color=AppTheme.TEXT_MUTED),
                                padding=ft.padding.symmetric(horizontal=15),
                            ),
                            ft.Container(
                                bgcolor=AppTheme.BORDER_LIGHT,
                                height=1,
                                expand=True,
                            ),
                        ],
                        width=300,
                    ),
                    
                    ft.Container(height=15),
                    
                    # Create account link
                    ft.TextButton(
                        content=ft.Text(
                            "Don't have an account? Sign Up",
                            size=13,
                            color=AppTheme.PRIMARY,
                        ),
                        on_click=lambda e: self.on_create_account(),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            width=420,
            padding=45,
            bgcolor=AppTheme.BG_CARD,
            border_radius=20,
            border=ft.border.all(1, AppTheme.BORDER_LIGHT),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.1, AppTheme.PRIMARY),
                offset=ft.Offset(0, 10),
            ),
        )
    
    def _handle_login(self, e):
        """Handle login button click"""
        username = self.username_field.value.strip() if self.username_field.value else ""
        password = self.password_field.value.strip() if self.password_field.value else ""
        
        if not username or not password:
            self.error_text.value = "Please fill all fields"
            self.update()
            return
        
        self.on_login_callback(username, password)

