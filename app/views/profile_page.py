import flet as ft


class ProfilePage(ft.Column):
    """User profile page"""
    
    def __init__(self, username, user_handle, on_logout, on_settings, on_home):
        super().__init__()
        self.username = username
        self.user_handle = user_handle
        self.on_logout = on_logout
        self.on_settings = on_settings
        self.on_home = on_home
        
        # Build UI
        self.controls = [
            self._build_top_bar(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=80, color=ft.Colors.BLUE),
                        ft.Text(
                            self.username,
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            self.user_handle,
                            size=14,
                            color=ft.Colors.GREY_700,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Divider(height=30),
                        ft.Text(
                            "Profile Information",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text("Role:", weight=ft.FontWeight.BOLD, width=100),
                                            ft.Text("Voter"),
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text("Status:", weight=ft.FontWeight.BOLD, width=100),
                                            ft.Text("Active", color=ft.Colors.GREEN),
                                        ]
                                    ),
                                ]
                            ),
                            padding=15,
                            bgcolor=ft.Colors.GREY_100,
                            border_radius=10,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=30,
            ),
        ]
        
        self.expand = True
        self.spacing = 0
    
    def _build_top_bar(self):
        """Build top navigation bar"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.on_home(),
                        tooltip="Back",
                    ),
                    ft.Text(
                        "Profile",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        on_click=lambda e: self.on_settings(),
                        tooltip="Settings",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.LOGOUT,
                        on_click=lambda e: self.on_logout(),
                        tooltip="Logout",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            bgcolor=ft.Colors.WHITE,
            border_bottom=ft.Border(
                bottom=ft.BorderSide(1, ft.Colors.GREY_300)
            ),
        )
