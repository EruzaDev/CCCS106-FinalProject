import flet as ft


class LoginPage(ft.Container):
    """Voting app login page matching the design"""
    
    def __init__(self, on_login, on_create_account, on_forgot_password):
        super().__init__()
        self.on_login_callback = on_login
        self.on_create_account = on_create_account
        self.on_forgot_password = on_forgot_password
        
        # Form fields
        self.username_field = ft.TextField(
            label="Username",
            hint_text="Enter username",
            width=280,
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12),
        )
        
        self.password_field = ft.TextField(
            label="Password",
            hint_text="Enter password",
            password=True,
            can_reveal_password=True,
            width=280,
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12),
        )
        
        self.error_text = ft.Text(
            "",
            color=ft.Colors.RED,
            size=12,
        )
        
        # Build the login card
        self.content = self._build_page()
        self.expand = True
        self.bgcolor = "#E8EAF6"  # Light purple/blue background
        self.padding = 20
    
    def _build_page(self):
        """Build the complete login page"""
        return ft.Column(
            [
                # Header text
                ft.Container(
                    content=ft.Text(
                        "Voting Web and Mobile App",
                        size=18,
                        color="#5C6BC0",
                        weight=ft.FontWeight.W_400,
                    ),
                    padding=ft.padding.only(left=20, top=20),
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
        """Build the white login card"""
        return ft.Container(
            content=ft.Column(
                [
                    # Logo icon
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.HOW_TO_VOTE,
                            size=40,
                            color=ft.Colors.WHITE,
                        ),
                        width=70,
                        height=70,
                        bgcolor="#5C6BC0",
                        border_radius=15,
                        alignment=ft.alignment.center,
                    ),
                    
                    # App name
                    ft.Text(
                        "HonestBallot",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#5C6BC0",
                    ),
                    
                    # Tagline
                    ft.Text(
                        "Voter Education & Transparency Platform",
                        size=12,
                        color=ft.Colors.GREY_600,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Username field
                    self.username_field,
                    
                    ft.Container(height=5),
                    
                    # Password field
                    self.password_field,
                    
                    # Error text
                    self.error_text,
                    
                    ft.Container(height=10),
                    
                    # Login button
                    ft.ElevatedButton(
                        text="Login",
                        width=280,
                        height=45,
                        bgcolor="#5C6BC0",
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=self._handle_login,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            width=380,
            padding=40,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
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

