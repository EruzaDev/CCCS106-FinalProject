import flet as ft

def main(page: ft.Page):
    page.title = "Login"
    page.window_width = 500
    page.window_height = 500
    page.padding = 0
    page.bgcolor = "#87CEEB"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Username field
    username_field = ft.TextField(
        hint_text="Email id or phone number",
        hint_style=ft.TextStyle(size=12, color="#999999"),
        border_radius=20,
        height=40,
        bgcolor="#F5F5F5",
        filled=True,
        border_color="transparent",
        content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
        text_size=12,
    )
    
    # Password field
    password_field = ft.TextField(
        hint_text="Password",
        hint_style=ft.TextStyle(size=12, color="#999999"),
        password=True,
        can_reveal_password=True,
        border_radius=20,
        height=40,
        bgcolor="#F5F5F5",
        filled=True,
        border_color="transparent",
        content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
        text_size=12,
    )
    
    # Login button
    login_button = ft.ElevatedButton(
        text="Log in",
        width=250,
        height=40,
        style=ft.ButtonStyle(
            bgcolor="#6B9BD5",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=20),
            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
        ),
    )
    
    # Forgot password link
    forgot_password = ft.TextButton(
        text="Forgot password?",
        style=ft.ButtonStyle(
            color="#6B9BD5",
            text_style=ft.TextStyle(size=12),
        ),
    )
    
    # Create new account button
    create_account_button = ft.ElevatedButton(
        text="Create new account",
        width=250,
        height=40,
        style=ft.ButtonStyle(
            bgcolor="#6B9BD5",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=20),
            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
        ),
    )
    
    # Login card container
    login_card = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=25),
                username_field,
                ft.Container(height=8),
                password_field,
                ft.Container(height=12),
                login_button,
                ft.Container(height=5),
                forgot_password,
                ft.Container(height=5),
                create_account_button,
                ft.Container(height=25),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        width=280,
        bgcolor="white",
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=15, vertical=0),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
    )
    
    # Stack with logo BEHIND and MUCH BIGGER than login card
    main_design = ft.Stack(
        [
            # HUGE LOGO in the background - centered
            ft.Container(
                content=ft.Image(
                    src="976e0e1b-3a89-40e0-8116-486d3f48ae40.jpg",
                    width=480,
                    height=480,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=450
                ),
                left=25,
                top=25,
            ),
            # Login card on top - centered and smaller than logo
            ft.Container(
                content=login_card,
                left=110,
                top=125,
            ),
        ],
        width=500,
        height=500,
    )
    
    # Center everything on the page
    main_container = ft.Container(
        content=main_design,
        alignment=ft.alignment.center,
        expand=True,
    )
    
    page.add(main_container)

ft.app(target=main)