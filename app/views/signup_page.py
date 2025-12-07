import flet as ft


class SignupPage(ft.Column):
    """Local voting app signup page"""
    
    def __init__(self, on_google_signin, on_apple_signin, on_create_account, on_signin):
        super().__init__()
        self.on_google_signin = on_google_signin
        self.on_apple_signin = on_apple_signin
        self.on_create_account = on_create_account
        self.on_signin = on_signin
        
        # Form fields
        self.username_field = ft.TextField(
            label="Username",
            width=300,
            icon=ft.Icons.PERSON,
        )
        
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
        
        self.confirm_password_field = ft.TextField(
            label="Confirm Password",
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
                            "Create Your Account",
                            size=16,
                            color=ft.Colors.GREY,
                        ),
                        ft.Divider(height=20),
                        self.username_field,
                        self.email_field,
                        self.password_field,
                        self.confirm_password_field,
                        self.error_text,
                        ft.ElevatedButton(
                            text="Create Account",
                            width=300,
                            icon=ft.Icons.PERSON_ADD,
                            on_click=self._handle_signup,
                        ),
                        ft.Divider(height=10),
                        ft.Text("Already have an account?", text_align=ft.TextAlign.CENTER),
                        ft.TextButton(
                            text="Sign In",
                            on_click=lambda e: self.on_signin(),
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
    
    def _handle_signup(self, e):
        """Handle signup button click"""
        username = self.username_field.value.strip()
        email = self.email_field.value.strip()
        password = self.password_field.value.strip()
        confirm_password = self.confirm_password_field.value.strip()
        
        if not username or not email or not password or not confirm_password:
            self.error_text.value = "Please fill all fields"
            self.update()
            return
        
        if password != confirm_password:
            self.error_text.value = "Passwords do not match"
            self.update()
            return
        
        if len(password) < 6:
            self.error_text.value = "Password must be at least 6 characters"
            self.update()
            return
        
        self.on_create_account(username, email, password)
