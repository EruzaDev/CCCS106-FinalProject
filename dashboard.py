import flet as ft

def main(page: ft.Page):
    page.title = "EUTABLE"
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_50
    
    # Header
    def create_header():
        return ft.Container(
            content=ft.Row(
                controls=[
                    # Logo
                    ft.Container(
                        content=ft.Icon(ft.Icons.PUBLIC, color=ft.Colors.WHITE, size=30),
                        bgcolor=ft.Colors.BLUE_700,
                        width=50,
                        height=50,
                        border_radius=25,
                        alignment=ft.alignment.center,
                    ),
                    # Search bar
                    ft.Container(
                        content=ft.TextField(
                            hint_text="Search for anything...",
                            border=ft.InputBorder.NONE,
                            text_size=14,
                            prefix_icon=ft.Icons.SEARCH,
                        ),
                        bgcolor=ft.Colors.WHITE,
                        width=400,
                        border_radius=20,
                        padding=5,
                    ),
                    ft.Container(expand=True),
                    # User info
                    ft.Row(
                        controls=[
                            ft.Text("RAYHAN", weight=ft.FontWeight.BOLD),
                            ft.Text("Admin | STAFF", size=12, color=ft.Colors.GREY_600),
                        ],
                        spacing=5,
                    ),
                    ft.IconButton(icon=ft.Icons.SETTINGS, icon_color=ft.Colors.GREY_700),
                    ft.IconButton(icon=ft.Icons.LOCATION_ON, icon_color=ft.Colors.GREY_700),
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=25),
                        bgcolor=ft.Colors.BLUE_400,
                        width=40,
                        height=40,
                        border_radius=20,
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=15,
            bgcolor=ft.Colors.WHITE,
        )
    
    # Sidebar
    def create_sidebar():
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Profile section
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=35),
                                    bgcolor=ft.Colors.GREY_800,
                                    width=70,
                                    height=70,
                                    border_radius=35,
                                    alignment=ft.alignment.center,
                                ),
                                ft.Text("SUITABLE", weight=ft.FontWeight.BOLD, size=16),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        padding=20,
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_300),
                    # Menu items
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Explore panel", color=ft.Colors.ORANGE, size=12, weight=ft.FontWeight.BOLD),
                                create_menu_item(ft.Icons.PERSON, "Profile", False),
                                create_menu_item(ft.Icons.EDIT, "Post manage", False),
                                create_menu_item(ft.Icons.BAR_CHART, "State analytics", False),
                            ],
                            spacing=5,
                        ),
                        padding=ft.padding.only(left=15, right=15, top=20),
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_300),
                    # Settings
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Settings", color=ft.Colors.ORANGE, size=12, weight=ft.FontWeight.BOLD),
                                create_menu_item(ft.Icons.SETTINGS, "Settings", False),
                                create_menu_item(ft.Icons.SECURITY, "Security data", False),
                                create_menu_item(ft.Icons.LOGOUT, "Logout", False),
                            ],
                            spacing=5,
                        ),
                        padding=ft.padding.only(left=15, right=15, top=20),
                    ),
                ],
            ),
            width=250,
            bgcolor=ft.Colors.WHITE,
            padding=10,
        )
    
    def create_menu_item(icon, text, selected):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, size=20, color=ft.Colors.BLUE_700 if selected else ft.Colors.GREY_700),
                    ft.Text(text, size=14, color=ft.Colors.BLUE_700 if selected else ft.Colors.GREY_700),
                ],
                spacing=10,
            ),
            bgcolor=ft.Colors.BLUE_50 if selected else ft.Colors.TRANSPARENT,
            padding=10,
            border_radius=8,
            ink=True,
        )
    
    # Post card
    def create_post_card(name, username, date, content, checkmarks):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=25),
                                bgcolor=ft.Colors.PINK_300,
                                width=50,
                                height=50,
                                border_radius=25,
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(name, weight=ft.FontWeight.BOLD, size=16),
                                    ft.Text(username, size=12, color=ft.Colors.GREY_600),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Text(content, size=14),
                    ft.Column(
                        controls=checkmarks,
                        spacing=3,
                    ),
                ],
                spacing=10,
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.GREY_200),
        )
    
    def create_checkmark_item(text, checked=True):
        return ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE if checked else ft.Icons.CIRCLE_OUTLINED,
                    size=16,
                    color=ft.Colors.GREEN if checked else ft.Colors.GREY_400,
                ),
                ft.Text(text, size=12, color=ft.Colors.GREEN if checked else ft.Colors.GREY_600),
            ],
            spacing=5,
        )
    
    # Notification sidebar
    def create_notifications():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Notifications", weight=ft.FontWeight.BOLD, size=18),
                            ft.Container(expand=True),
                            ft.IconButton(icon=ft.Icons.MORE_HORIZ, icon_size=20),
                        ],
                    ),
                    ft.Divider(height=1),
                    # Notification items
                    create_notification_item("FAIZI", "FAIZI added new post", ft.Colors.PURPLE_300),
                    create_notification_item("Merry", "Merry added new post", ft.Colors.GREEN_300),
                    ft.Divider(height=1),
                    ft.Text("DAILIES", size=12, color=ft.Colors.GREY_600),
                    ft.ElevatedButton("See previous notifications", style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREY_100,
                        color=ft.Colors.GREY_800,
                    )),
                    ft.ElevatedButton("Boost your post!", style=ft.ButtonStyle(
                        bgcolor=ft.Colors.ORANGE_300,
                        color=ft.Colors.WHITE,
                    )),
                    # Illustration
                    ft.Container(
                        content=ft.Image(
                            src="https://via.placeholder.com/200x150?text=Illustration",
                            width=200,
                            height=150,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Text("@SUITABLE", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                    ft.Text("With article, by user", size=10, color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER),
                ],
                spacing=15,
            ),
            width=300,
            bgcolor=ft.Colors.WHITE,
            padding=20,
        )
    
    def create_notification_item(name, message, color):
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=20),
                    bgcolor=color,
                    width=40,
                    height=40,
                    border_radius=20,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    controls=[
                        ft.Text(name, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text(message, size=12, color=ft.Colors.GREY_600),
                    ],
                    spacing=2,
                ),
            ],
            spacing=10,
        )
    
    # Action buttons
    action_buttons = ft.Row(
        controls=[
            ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.EDIT, size=16),
                        ft.Text("Write a post"),
                    ],
                    spacing=5,
                ),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.YELLOW_100,
                    color=ft.Colors.BLACK,
                ),
            ),
            ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.UPLOAD, size=16),
                        ft.Text("Upload photo"),
                    ],
                    spacing=5,
                ),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_100,
                    color=ft.Colors.BLACK,
                ),
            ),
            ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.VIDEOCAM, size=16),
                        ft.Text("Upload Video"),
                    ],
                    spacing=5,
                ),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.YELLOW_100,
                    color=ft.Colors.BLACK,
                ),
            ),
        ],
        spacing=10,
    )
    
    # Main content area
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                action_buttons,
                ft.Text("Write something here", size=12, color=ft.Colors.GREY_400),
                ft.Divider(height=20),
                # Posts
                create_post_card(
                    "CJXY",
                    "@magix_pop10k",
                    "June 2025",
                    "See to know your candidates before voting your voter registration. Read the platform of your choice.",
                    [
                        create_checkmark_item("Participated for Transgender government"),
                        create_checkmark_item("Upholding every citizen equality"),
                        create_checkmark_item("Widespread in mental health"),
                    ]
                ),
                ft.Container(height=20),
                create_post_card(
                    "Geo10",
                    "@maddieXgrey10",
                    "5 Continents released: June 2025",
                    "Geo10 is a geography game with beautiful minimalistic art style where you learn the countries, cities, US States, flags, notable mountains and other things by guessing what is shown in the most recent public forum. Read the official Geo10 Wiki!",
                    [
                        create_checkmark_item("Cute design"),
                        create_checkmark_item("Illustration"),
                    ]
                ),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=20,
        expand=True,
    )
    
    # Layout
    page.add(
        ft.Column(
            controls=[
                create_header(),
                ft.Row(
                    controls=[
                        create_sidebar(),
                        main_content,
                        create_notifications(),
                    ],
                    spacing=0,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )
    )

ft.app(target=main)