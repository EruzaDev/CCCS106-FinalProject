import flet as ft


class SignupPage(ft.Container):
    """Signup/Join page with social login and create account options"""
    
    def __init__(self, on_google_signin=None, on_apple_signin=None, 
                 on_create_account=None, on_signin=None):
        super().__init__()
        self.on_google_signin = on_google_signin
        self.on_apple_signin = on_apple_signin
        self.on_create_account = on_create_account
        self.on_signin = on_signin
        
        # Build the UI
        self.content = self._build_ui()
        self.expand = True
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.LIGHT_BLUE_100, ft.Colors.LIGHT_BLUE_50],
        )
    
    def _build_ui(self):
        """Build the signup page UI"""
        
        # Left side - Logo and slogan
        logo_section = ft.Column(
            controls=[
                ft.Text(
                    "Research",
                    size=42,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
                ft.Text(
                    "Decide",
                    size=42,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
                ft.Text(
                    "Act",
                    size=42,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
                ft.Container(height=30),
                # Large Logo from assets
                ft.Container(
                    content=ft.Image(
                        src="assets/fd875946-c220-48f7-a5db-e8e1d3e0a2a0.jpg",
                        width=280,
                        height=280,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    width=280,
                    height=280,
                    border_radius=140,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Right side - Join us form
        join_form = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "JOIN US",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                    ft.Container(height=20),
                    # Google sign in button
                    ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Image(
                                    src="https://www.google.com/favicon.ico",
                                    width=20,
                                    height=20,
                                ),
                                ft.Text("Sign In with Google", color=ft.Colors.BLACK),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=25),
                            side=ft.BorderSide(1, ft.Colors.GREY_300),
                        ),
                        width=250,
                        height=45,
                        on_click=self._handle_google_signin,
                    ),
                    ft.Container(height=10),
                    # Apple sign in button
                    ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.APPLE, color=ft.Colors.BLACK, size=20),
                                ft.Text("Sign In with Apple", color=ft.Colors.BLACK),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=25),
                            side=ft.BorderSide(1, ft.Colors.GREY_300),
                        ),
                        width=250,
                        height=45,
                        on_click=self._handle_apple_signin,
                    ),
                    ft.Container(height=15),
                    ft.Text("OR", size=12, color=ft.Colors.GREY_600),
                    ft.Container(height=15),
                    # Create an account button
                    ft.ElevatedButton(
                        text="Create an account",
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.WHITE,
                            color=ft.Colors.BLUE_400,
                            shape=ft.RoundedRectangleBorder(radius=25),
                            side=ft.BorderSide(1, ft.Colors.BLUE_400),
                        ),
                        width=250,
                        height=45,
                        on_click=self._handle_create_account,
                    ),
                    ft.Container(height=15),
                    # Terms text
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "By signing up, you agree to the Terms of Service and Privacy",
                                    size=10,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    "Policy, including Cookie Use.",
                                    size=10,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=2,
                        ),
                        width=250,
                    ),
                    ft.Container(height=30),
                    ft.Divider(height=1, color=ft.Colors.GREY_300),
                    ft.Container(height=20),
                    ft.Text(
                        "Do you have already an account?",
                        size=14,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Container(height=10),
                    # Sign in button
                    ft.OutlinedButton(
                        text="Sign In",
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_400,
                            shape=ft.RoundedRectangleBorder(radius=25),
                            side=ft.BorderSide(1, ft.Colors.BLUE_400),
                        ),
                        width=250,
                        height=45,
                        on_click=self._handle_signin,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=40,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )
        
        # Main layout with left and right sections
        return ft.Row(
            controls=[
                # Left section
                ft.Container(
                    content=logo_section,
                    expand=1,
                    alignment=ft.alignment.center,
                ),
                # Right section
                ft.Container(
                    content=join_form,
                    expand=1,
                    alignment=ft.alignment.center,
                ),
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _handle_google_signin(self, e):
        """Handle Google sign in button click"""
        if self.on_google_signin:
            self.on_google_signin()
    
    def _handle_apple_signin(self, e):
        """Handle Apple sign in button click"""
        if self.on_apple_signin:
            self.on_apple_signin()
    
    def _handle_create_account(self, e):
        """Handle create account button click"""
        if self.on_create_account:
            self.on_create_account()
    
    def _handle_signin(self, e):
        """Handle sign in button click"""
        if self.on_signin:
            self.on_signin()
