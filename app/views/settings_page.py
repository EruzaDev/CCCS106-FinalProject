import flet as ft


class SettingsPage(ft.Column):
    """Settings page for user preferences"""
    
    def __init__(self, username, user_handle, on_save, on_cancel, on_back, on_logout, on_profile):
        super().__init__()
        self.username = username
        self.user_handle = user_handle
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.on_back = on_back
        self.on_logout = on_logout
        self.on_profile = on_profile
        
        # Theme settings
        self.theme_dropdown = ft.Dropdown(
            label="Theme",
            options=[
                ft.dropdown.Option("light", "Light Mode"),
                ft.dropdown.Option("dark", "Dark Mode"),
                ft.dropdown.Option("auto", "Auto"),
            ],
            value="light",
            width=200,
        )
        
        # Notification settings
        self.notifications_switch = ft.Switch(
            label="Enable Notifications",
            value=True,
        )
        
        # Build UI
        self.controls = [
            self._build_top_bar(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Settings",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Divider(height=20),
                        ft.Text(
                            "Appearance",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        self.theme_dropdown,
                        ft.Divider(height=20),
                        ft.Text(
                            "Notifications",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        self.notifications_switch,
                        ft.Divider(height=30),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text="Save",
                                    on_click=self._handle_save,
                                ),
                                ft.TextButton(
                                    text="Cancel",
                                    on_click=lambda e: self.on_cancel(),
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=10,
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
                        on_click=lambda e: self.on_back(),
                        tooltip="Back",
                    ),
                    ft.Text(
                        "Settings",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(expand=True),
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
    
    def _handle_save(self, e):
        """Handle save settings"""
        settings_data = {
            "theme": self.theme_dropdown.value,
            "notifications": self.notifications_switch.value,
        }
        self.on_save(settings_data)
