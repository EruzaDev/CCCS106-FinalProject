import flet as ft


class LoginPage(ft.Column):
    """Local voting app login page"""
    
    def __init__(self, on_login, on_create_account, on_forgot_password):
        super().__init__()
        self.on_login = on_login
        self.on_create_account = on_create_account
        self.on_forgot_password = on_forgot_password
        
        # Form fields
        self.email_field = ft.TextField(
            label="Email",
            width=300,
            icon=ft.Icons.EMAIL,
        )
        
        self.password_field = ft.TextField(
            label="Password",
            password=True,
            width=300,
            icon=ft.Icons.LOCK,
        )
        
        self.error_text = ft.Text(
            "",
            color=ft.Colors.RED,
            size=12,
        )
        
        # Build UI
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "HonestBallot",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE,
                        ),
                        ft.Text(
                            "Local Voting System",
                            size=16,
                            color=ft.Colors.GREY,
                        ),
                        ft.Divider(height=30),
                        ft.Text("Demo Credentials:", weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "alice@honestballot.local / password123\n"
                            "bob@honestballot.local / password123\n"
                            "charlie@honestballot.local / password123",
                            size=11,
                            color=ft.Colors.GREY_700,
                        ),
                        ft.Divider(height=30),
                        self.email_field,
                        self.password_field,
                        self.error_text,
                        ft.ElevatedButton(
                            text="Login",
                            width=300,
                            icon=ft.Icons.LOGIN,
                            on_click=self._handle_login,
                        ),
                        ft.TextButton(
                            text="Forgot Password?",
                            on_click=lambda e: self.on_forgot_password(),
                        ),
                        ft.Divider(height=20),
                        ft.Text("Don't have an account?", text_align=ft.TextAlign.CENTER),
                        ft.TextButton(
                            text="Create Account",
                            on_click=lambda e: self.on_create_account(),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=50,
            )
        ]
        
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.expand = True
    
    def _handle_login(self, e):
        """Handle login button click"""
        email = self.email_field.value.strip()
        password = self.password_field.value.strip()
        
        if not email or not password:
            self.error_text.value = "Please fill all fields"
            self.update()
            return
        
        self.on_login(email, password)
