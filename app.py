import flet as ft

def main(page: ft.Page):
    page.title = "Research Decide Act"
    page.bgcolor = ft.Colors.LIGHT_BLUE_100
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 50
    
    # Left side - Title and Logo
    left_side = ft.Container(
        content=ft.Column(
            [
                # Title
                ft.Column(
                    [
                        ft.Text(
                            "Research",
                            size=50,
                            weight=ft.FontWeight.BOLD,
                            color="#2d3e6f"
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Decide",
                                size=50,
                                weight=ft.FontWeight.BOLD,
                                color="#2d3e6f"
                            ),
                            margin=ft.margin.only(left=80)
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Act",
                                size=50,
                                weight=ft.FontWeight.BOLD,
                                color="#2d3e6f"
                            ),
                            margin=ft.margin.only(left=160)
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    spacing=0
                ),
                
                # Logo Image
                ft.Image(
                    src="976e0e1b-3a89-40e0-8116-486d3f48ae40.jpg",
                    width=400,
                    height=400,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=500
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30
        ),
        expand=1
    )
    
    # Right side - Sign up/Login form
    right_side = ft.Container(
        content=ft.Column(
            [
                # JOIN US title
                ft.Text(
                    "JOIN US",
                    size=35,
                    weight=ft.FontWeight.BOLD,
                    color="#2d3e6f",
                    text_align=ft.TextAlign.RIGHT
                ),
                
                # Form container
                ft.Container(
                    content=ft.Column(
                        [
                            # Sign in with Google
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.MAIL, color=ft.Colors.RED_500, size=20),
                                        ft.Text("Sign in with Google", size=14, weight=ft.FontWeight.W_500)
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10
                                ),
                                width=400,
                                height=50,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.WHITE,
                                    color=ft.Colors.GREY_800,
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                )
                            ),
                            
                            # Sign in with Apple
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.APPLE, color=ft.Colors.BLACK, size=20),
                                        ft.Text("Sign in with Apple", size=14, weight=ft.FontWeight.W_500)
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10
                                ),
                                width=400,
                                height=50,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.WHITE,
                                    color=ft.Colors.GREY_800,
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                )
                            ),
                            
                            # OR divider
                            ft.Row(
                                [
                                    ft.Container(height=1, bgcolor=ft.Colors.GREY_400, expand=1),
                                    ft.Text("OR", size=12, color=ft.Colors.GREY_600),
                                    ft.Container(height=1, bgcolor=ft.Colors.GREY_400, expand=1),
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            
                            # Create an account
                            ft.ElevatedButton(
                                "Create an account",
                                width=400,
                                height=50,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.LIGHT_BLUE_200,
                                    color=ft.Colors.GREY_800,
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                )
                            ),
                            
                            # Terms text
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text("By signing up, you agree to the ", size=11, color=ft.Colors.GREY_700),
                                        ft.Text("Terms of Service", size=11, color=ft.Colors.BLUE_600),
                                        ft.Text(" and ", size=11, color=ft.Colors.GREY_700),
                                        ft.Text("Privacy Policy", size=11, color=ft.Colors.BLUE_600),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    wrap=True
                                ),
                                width=400,
                            ),
                            
                            # Divider
                            ft.Container(
                                height=1,
                                bgcolor=ft.Colors.GREY_300,
                                margin=ft.margin.only(top=20, bottom=20)
                            ),
                            
                            # Already have account text
                            ft.Text(
                                "Do you have already an account?",
                                size=14,
                                color=ft.Colors.GREY_700,
                                weight=ft.FontWeight.W_500,
                                text_align=ft.TextAlign.CENTER
                            ),
                            
                            # Sign in button
                            ft.ElevatedButton(
                                "Sign in",
                                width=400,
                                height=50,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.LIGHT_BLUE_200,
                                    color=ft.Colors.GREY_800,
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                )
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15
                    ),
                    bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
                    border_radius=25,
                    padding=30,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.BLACK12,
                    ),
                    margin=ft.margin.only(top=30)
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
        ),
        expand=1
    )
    
    # Main layout
    main_row = ft.Row(
        [left_side, right_side],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=100
    )
    
    page.add(main_row)

ft.app(target=main)