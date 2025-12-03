import flet as ft


class NotificationDropdown(ft.Container):
    """Notification dropdown panel with unread and earlier sections"""
    
    def __init__(self, on_close=None, on_see_previous=None):
        super().__init__()
        self.on_close = on_close
        self.on_see_previous = on_see_previous
        
        # Sample notifications data
        self.unread_notifications = [
            {"user": "KADY", "action": "added new post...", "avatar": "K"},
            {"user": "elyyyy", "action": "added new post...", "avatar": "E"},
        ]
        
        self.earlier_notifications = []
        
        # Build the UI
        self.content = self._build_ui()
        self.bgcolor = ft.Colors.WHITE
        self.border_radius = 15
        self.width = 280
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
        )
        self.visible = False
    
    def _build_ui(self):
        """Build the notification dropdown UI"""
        
        # Header
        header = ft.Row(
            controls=[
                ft.Text(
                    "Notifications",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_size=18,
                    icon_color=ft.Colors.GREY_600,
                    on_click=self._handle_close,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Unread section
        unread_section = ft.Column(
            controls=[
                ft.Text(
                    "Unread",
                    size=12,
                    color=ft.Colors.GREY_600,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Container(height=5),
                *[self._build_notification_item(n, is_unread=True) 
                  for n in self.unread_notifications],
            ],
            spacing=5,
        )
        
        # Earlier section
        earlier_section = ft.Column(
            controls=[
                ft.Container(height=10),
                ft.Text(
                    "EARLIER",
                    size=12,
                    color=ft.Colors.GREY_600,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Container(height=5),
                *[self._build_notification_item(n, is_unread=False) 
                  for n in self.earlier_notifications],
            ],
            spacing=5,
        )
        
        # See previous button
        see_previous_btn = ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ARROW_BACK, size=16, color=ft.Colors.BLUE_400),
                    ft.Text("See previous notifications", size=12, color=ft.Colors.BLUE_400),
                ],
                spacing=5,
            ),
            on_click=self._handle_see_previous,
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    ft.Divider(height=1, color=ft.Colors.GREY_200),
                    ft.Container(height=10),
                    unread_section,
                    earlier_section,
                    ft.Container(height=10),
                    see_previous_btn,
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=15,
        )
    
    def _build_notification_item(self, notification, is_unread=False):
        """Build a single notification item"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    # Avatar
                    ft.Container(
                        content=ft.Text(
                            notification["avatar"],
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        width=35,
                        height=35,
                        bgcolor=ft.Colors.PINK_200 if is_unread else ft.Colors.GREY_400,
                        border_radius=17.5,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=10),
                    # Notification text
                    ft.Column(
                        controls=[
                            ft.Text(
                                notification["user"],
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.BLACK,
                            ),
                            ft.Text(
                                notification["action"],
                                size=11,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        spacing=2,
                    ),
                    ft.Container(expand=True),
                    # Unread indicator
                    ft.Container(
                        width=8,
                        height=8,
                        bgcolor=ft.Colors.BLUE_400 if is_unread else ft.Colors.TRANSPARENT,
                        border_radius=4,
                    ) if is_unread else ft.Container(),
                ],
            ),
            padding=ft.padding.symmetric(vertical=8, horizontal=5),
            border_radius=8,
            ink=True,
            on_click=lambda e: print(f"Clicked notification: {notification['user']}"),
        )
    
    def _handle_close(self, e):
        """Handle close button click"""
        self.visible = False
        if self.on_close:
            self.on_close()
        self.update()
    
    def _handle_see_previous(self, e):
        """Handle see previous notifications click"""
        if self.on_see_previous:
            self.on_see_previous()
    
    def show(self):
        """Show the notification dropdown"""
        self.visible = True
        self.update()
    
    def hide(self):
        """Hide the notification dropdown"""
        self.visible = False
        self.update()
    
    def toggle(self):
        """Toggle the notification dropdown visibility"""
        self.visible = not self.visible
        self.update()
