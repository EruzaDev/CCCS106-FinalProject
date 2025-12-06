import flet as ft
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.top_taskbar import TopTaskbar
from components.sidebar import Sidebar

"""
=============================================================================
SETTINGS PAGE - USER PREFERENCES & APPEARANCE
=============================================================================

Features:
- Dark/Light mode toggle
- Language selection
- Brand color customization
- Dashboard chart styles
- Cookie banner options

=============================================================================
"""


class SettingsPage(ft.Container):
    """Settings page with sidebar, top taskbar, and appearance settings"""
    
    def __init__(self, username="EUTABLE", user_handle="@CUTIE_EUTABLE",
                 on_save=None, on_cancel=None, on_back=None,
                 on_logout=None, on_profile=None, on_home=None,
                 on_theme_change=None, current_theme="light", page=None):
        super().__init__()
        self.username = username
        self.user_handle = user_handle
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.on_back = on_back
        self.on_logout = on_logout
        self.on_profile = on_profile
        self.on_home = on_home
        self.on_theme_change = on_theme_change
        self._page = page  # Store page reference for theme changes
        
        # =================================================================
        # THEME/APPEARANCE SETTINGS
        # =================================================================
        self.current_theme = current_theme  # "light" or "dark"
        self.brand_color = "#444CE7"
        self.chart_style = "Default"
        self.language = "English (UK)"
        self.cookie_banner = "Default"
        # =================================================================
        
        # Create top taskbar
        self.top_taskbar = TopTaskbar(
            username=username,
            user_handle=user_handle,
            on_settings=None,  # Already on settings
            on_search=self._handle_search,
        )
        
        # Create sidebar with settings active
        self.sidebar = Sidebar(
            username=username,
            on_profile=on_profile,
            on_settings=None,  # Already on settings
            on_logout=on_logout,
        )
        # Set settings as active in sidebar
        self.sidebar.active_item = "settings"
        
        # Build the UI
        self.content = self._build_ui()
        self.expand = True
        self.bgcolor = "#E1F5FE"  # Very light blue background
    
    def _build_ui(self):
        """Build the settings page with sidebar and taskbar"""
        
        # Settings content area
        settings_content = self._build_settings_content()
        
        # Main content area (sidebar + settings)
        main_content = ft.Row(
            controls=[
                # Left sidebar
                self.sidebar,
                # Vertical divider
                ft.VerticalDivider(width=1, color=ft.Colors.GREY_300),
                # Settings content
                ft.Container(
                    content=settings_content,
                    expand=True,
                    padding=20,
                ),
            ],
            expand=True,
            spacing=0,
        )
        
        # Full layout with taskbar at top spanning full width
        return ft.Column(
            controls=[
                self.top_taskbar,
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                main_content,
            ],
            spacing=0,
            expand=True,
        )
    
    def _build_settings_content(self):
        """Build the main settings content area"""
        
        # Header
        header = ft.Text(
            "SETTINGS",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
        )
        
        # Only Appearance tab
        tabs = ft.Row(
            controls=[
                self._build_tab("Appearance", enabled=True, active=True),
            ],
            spacing=10,
        )
        
        # Appearance content
        appearance_content = self._build_appearance_content()
        
        # Footer buttons
        footer = ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.OutlinedButton(
                    text="Cancel",
                    style=ft.ButtonStyle(
                        color=ft.Colors.GREY_700,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=self._handle_cancel,
                ),
                ft.ElevatedButton(
                    text="Save changes",
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=self._handle_save,
                ),
            ],
            spacing=10,
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    ft.Container(height=20),
                    tabs,
                    ft.Divider(height=1, color=ft.Colors.GREY_200),
                    ft.Container(height=20),
                    ft.Container(
                        content=appearance_content,
                        expand=True,
                    ),
                    ft.Container(height=20),
                    footer,
                ],
                spacing=0,
                expand=True,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=30,
            expand=True,
        )
    
    def _build_tab(self, name, enabled=True, active=False):
        """Build a single tab button"""
        text_color = ft.Colors.BLACK if active else (ft.Colors.GREY_600 if enabled else ft.Colors.GREY_400)
        
        return ft.Container(
            content=ft.Text(
                name,
                size=14,
                weight=ft.FontWeight.W_500 if active else ft.FontWeight.NORMAL,
                color=text_color,
            ),
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            border=ft.border.only(bottom=ft.BorderSide(2, ft.Colors.BLUE_600)) if active else None,
        )
    
    def _build_appearance_content(self):
        """Build the appearance settings content"""
        
        # Section header helper
        def section_header(title, subtitle):
            return ft.Column(
                controls=[
                    ft.Text(title, size=14, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                    ft.Text(subtitle, size=12, color=ft.Colors.GREY_600),
                ],
                spacing=2,
            )
        
        # Appearance header
        appearance_header = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Appearance", size=16, weight=ft.FontWeight.W_600),
                        ft.Text("Change how your public dashboard looks and feels.", 
                               size=12, color=ft.Colors.GREY_600),
                    ],
                    spacing=2,
                ),
                ft.Container(expand=True),
                ft.Text("dashboard.untitledui.com", size=12, color=ft.Colors.GREY_500),
                ft.Icon(ft.Icons.OPEN_IN_NEW, size=14, color=ft.Colors.GREY_500),
            ],
        )
        
        # Theme mode section (Dark/Light)
        self.theme_switch = ft.Switch(
            value=self.current_theme == "dark",
            on_change=self._toggle_theme,
            active_color=ft.Colors.BLUE_600,
        )
        
        theme_section = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Dark Mode", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                            ft.Text("Switch between light and dark theme", size=12, color=ft.Colors.GREY_600),
                        ],
                        spacing=2,
                    ),
                    ft.Container(expand=True),
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.LIGHT_MODE,
                                size=20,
                                color=ft.Colors.AMBER_500 if self.current_theme == "light" else ft.Colors.GREY_400,
                            ),
                            self.theme_switch,
                            ft.Icon(
                                ft.Icons.DARK_MODE,
                                size=20,
                                color=ft.Colors.BLUE_800 if self.current_theme == "dark" else ft.Colors.GREY_400,
                            ),
                        ],
                        spacing=10,
                    ),
                ],
            ),
            padding=ft.padding.all(15),
            bgcolor=ft.Colors.GREY_50,
            border_radius=10,
        )
        
        # Brand color section
        brand_color_section = ft.Row(
            controls=[
                section_header("Brand color", "Select or customize your brand color."),
                ft.Container(expand=True),
                ft.Switch(value=True),
                ft.Container(
                    content=ft.Text(f"# {self.brand_color[1:]}", size=12),
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                ),
            ],
        )
        
        # Dashboard charts section
        def chart_option(title, subtitle, selected):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text("</> Edit CSS" if title == "Custom CSS" else "", 
                                          size=10, color=ft.Colors.GREY_600),
                            width=120,
                            height=70,
                            bgcolor=ft.Colors.GREY_100,
                            border_radius=8,
                            border=ft.border.all(2, ft.Colors.BLUE_400) if selected else ft.border.all(1, ft.Colors.GREY_300),
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(title, size=12, weight=ft.FontWeight.W_500),
                        ft.Text(subtitle, size=10, color=ft.Colors.GREY_600),
                    ],
                    spacing=5,
                ),
                ink=True,
                on_click=lambda e, t=title: self._select_chart_style(t),
            )
        
        charts_section = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        section_header("Dashboard charts", "How charts are displayed."),
                        ft.Container(expand=True),
                        ft.TextButton("View examples", style=ft.ButtonStyle(color=ft.Colors.BLUE_600)),
                    ],
                ),
                ft.Container(height=10),
                ft.Row(
                    controls=[
                        chart_option("Default", "Default company branding.", self.chart_style == "Default"),
                        chart_option("Simplified", "Minimal and modern.", self.chart_style == "Simplified"),
                        chart_option("Custom CSS", "Manage styling with CSS.", self.chart_style == "Custom CSS"),
                    ],
                    spacing=20,
                ),
            ],
            spacing=0,
        )
        
        # Language section
        language_section = ft.Row(
            controls=[
                section_header("Language", "Default language for public dashboard."),
                ft.Container(expand=True),
                ft.Dropdown(
                    value=self.language,
                    options=[
                        ft.dropdown.Option("English (UK)"),
                        ft.dropdown.Option("English (US)"),
                        ft.dropdown.Option("Filipino"),
                        ft.dropdown.Option("Spanish"),
                    ],
                    width=200,
                    border_radius=8,
                ),
            ],
        )
        
        # Cookie banner section
        def cookie_option(title, subtitle, selected):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            width=120,
                            height=70,
                            bgcolor=ft.Colors.GREY_100,
                            border_radius=8,
                            border=ft.border.all(2, ft.Colors.BLUE_400) if selected else ft.border.all(1, ft.Colors.GREY_300),
                        ),
                        ft.Text(title, size=12, weight=ft.FontWeight.W_500),
                        ft.Text(subtitle, size=10, color=ft.Colors.GREY_600, max_lines=1),
                    ],
                    spacing=5,
                ),
                ink=True,
                on_click=lambda e, t=title: self._select_cookie_banner(t),
            )
        
        cookie_section = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        section_header("Cookie banner", "Display cookie banners to visitors."),
                        ft.Container(expand=True),
                        ft.TextButton("View examples", style=ft.ButtonStyle(color=ft.Colors.BLUE_600)),
                    ],
                ),
                ft.Container(height=10),
                ft.Row(
                    controls=[
                        cookie_option("Default", "Cookie controls for visitors.", self.cookie_banner == "Default"),
                        cookie_option("Simplified", "Show a simplified banner.", self.cookie_banner == "Simplified"),
                        cookie_option("None", "Don't show any banners.", self.cookie_banner == "None"),
                    ],
                    spacing=20,
                ),
            ],
            spacing=0,
        )
        
        return ft.Column(
            controls=[
                appearance_header,
                ft.Divider(height=20, color=ft.Colors.GREY_200),
                theme_section,
                ft.Divider(height=20, color=ft.Colors.GREY_200),
                charts_section,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
    
    def _toggle_theme(self, e):
        """Handle theme toggle"""
        self.current_theme = "dark" if e.control.value else "light"
        
        # Update page theme directly for immediate effect
        if self._page:
            if self.current_theme == "dark":
                self._page.theme_mode = ft.ThemeMode.DARK
                self._page.bgcolor = "#1a1a2e"
            else:
                self._page.theme_mode = ft.ThemeMode.LIGHT
                self._page.bgcolor = ft.Colors.GREY_100
            self._page.update()
        
        # Also call the callback for app-level state
        if self.on_theme_change:
            self.on_theme_change(self.current_theme)
    
    def _select_chart_style(self, style):
        """Handle chart style selection"""
        self.chart_style = style
        self.content = self._build_ui()
        self.update()
    
    def _select_cookie_banner(self, option):
        """Handle cookie banner selection"""
        self.cookie_banner = option
        self.content = self._build_ui()
        self.update()
    
    def _handle_search(self, query):
        """Handle search"""
        print(f"Search: {query}")
    
    def _handle_save(self, e):
        """Handle save button click"""
        if self.on_save:
            self.on_save({
                "theme": self.current_theme,
                "brand_color": self.brand_color,
                "chart_style": self.chart_style,
                "language": self.language,
                "cookie_banner": self.cookie_banner,
            })
    
    def _handle_cancel(self, e):
        """Handle cancel button click"""
        if self.on_cancel:
            self.on_cancel()
