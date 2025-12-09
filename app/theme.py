"""
Theme Configuration for HonestBallot
Light Blue Aesthetic Theme
"""

import flet as ft


class AppTheme:
    """Centralized theme colors and styles for the application"""
    
    # Primary Blue Palette
    PRIMARY = "#2196F3"           # Main blue
    PRIMARY_LIGHT = "#64B5F6"     # Light blue
    PRIMARY_DARK = "#1976D2"      # Dark blue
    PRIMARY_ACCENT = "#03A9F4"    # Accent blue
    
    # Secondary Colors
    SECONDARY = "#1976D2"         # Deeper blue
    SECONDARY_LIGHT = "#4DD0E1"   # Light cyan
    
    # Accent Color (for highlights)
    ACCENT = "#03A9F4"            # Sky blue accent
    
    # Background Colors
    BG_PRIMARY = "#E3F2FD"        # Light blue background
    BG_SECONDARY = "#F5F9FF"      # Very light blue background
    BG_CARD = "#FFFFFF"           # White cards
    BG_HEADER = "#FFFFFF"         # White header
    
    # Surface Colors
    SURFACE_LIGHT = "#E1F5FE"     # Light blue surface
    SURFACE_HOVER = "#BBDEFB"     # Hover state
    
    # Text Colors
    TEXT_PRIMARY = "#333333"      # Dark text for readability
    TEXT_SECONDARY = "#666666"    # Secondary text
    TEXT_MUTED = "#78909C"        # Muted gray-blue
    TEXT_ON_PRIMARY = "#FFFFFF"   # White text on primary
    
    # Border Colors
    BORDER_COLOR = "#B3E5FC"      # Light blue border (main)
    BORDER_LIGHT = "#B3E5FC"      # Light blue border
    BORDER_DEFAULT = "#90CAF9"    # Default border
    BORDER_FOCUS = "#2196F3"      # Focus border
    
    # Status Colors
    SUCCESS = "#4CAF50"           # Green
    SUCCESS_LIGHT = "#C8E6C9"     # Light green
    WARNING = "#FF9800"           # Orange
    WARNING_LIGHT = "#FFE0B2"     # Light orange
    ERROR = "#F44336"             # Red
    ERROR_LIGHT = "#FFCDD2"       # Light red
    INFO = "#2196F3"              # Blue (same as primary)
    
    # Shadow
    SHADOW_COLOR = "rgba(33, 150, 243, 0.15)"
    
    # Gradients (for special elements)
    GRADIENT_START = "#2196F3"
    GRADIENT_END = "#03A9F4"
    
    @classmethod
    def get_card_shadow(cls):
        """Get standard card shadow"""
        return ft.BoxShadow(
            spread_radius=0,
            blur_radius=12,
            color=ft.Colors.with_opacity(0.08, cls.PRIMARY),
            offset=ft.Offset(0, 4),
        )
    
    @classmethod
    def get_elevated_shadow(cls):
        """Get elevated shadow for hover states"""
        return ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.15, cls.PRIMARY),
            offset=ft.Offset(0, 8),
        )
    
    @classmethod
    def get_button_style(cls, variant="primary"):
        """Get button style based on variant"""
        if variant == "primary":
            return ft.ButtonStyle(
                bgcolor=cls.PRIMARY,
                color=cls.TEXT_ON_PRIMARY,
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=2,
            )
        elif variant == "secondary":
            return ft.ButtonStyle(
                bgcolor=cls.BG_SECONDARY,
                color=cls.PRIMARY,
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        elif variant == "outline":
            return ft.ButtonStyle(
                bgcolor=ft.Colors.TRANSPARENT,
                color=cls.PRIMARY,
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(1, cls.PRIMARY),
            )
    
    @classmethod
    def get_text_field_style(cls):
        """Get consistent text field styling"""
        return {
            "border_radius": 10,
            "bgcolor": cls.BG_CARD,
            "border_color": cls.BORDER_LIGHT,
            "focused_border_color": cls.PRIMARY,
            "cursor_color": cls.PRIMARY,
            "selection_color": ft.Colors.with_opacity(0.3, cls.PRIMARY),
        }


# Create a global theme instance
theme = AppTheme()
