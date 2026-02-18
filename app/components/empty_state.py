"""
Empty State Component for HonestBallot
Provides polished "no data" illustrations with action buttons
"""

import flet as ft
from app.theme import AppTheme


class EmptyState(ft.Container):
    """
    A polished empty-state card with an icon illustration, title,
    subtitle and an optional "Get Started" / CTA button.

    Parameters
    ----------
    icon        : ft.Icons constant  – the large illustration icon
    title       : str                – primary headline
    subtitle    : str                – supporting description
    btn_label   : str | None         – button label (hidden when None)
    on_btn_click: callable | None    – callback for the CTA button
    icon_color  : str                – icon colour (defaults to primary blue)
    compact     : bool               – use a smaller, less padded variant
    """

    def __init__(
        self,
        icon=ft.Icons.INBOX,
        title: str = "Nothing here yet",
        subtitle: str = "Data will appear here once it's available.",
        btn_label: str | None = None,
        on_btn_click=None,
        icon_color: str | None = None,
        compact: bool = False,
    ):
        self._icon = icon
        self._title = title
        self._subtitle = subtitle
        self._btn_label = btn_label
        self._on_btn_click = on_btn_click
        self._icon_color = icon_color or AppTheme.PRIMARY
        self._compact = compact

        super().__init__(
            content=self._build(),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(
                horizontal=32 if not compact else 16,
                vertical=40 if not compact else 24,
            ),
        )

    # ─────────────────────────────────────────────────────────────────────────

    def _build(self):
        icon_size = 56 if not self._compact else 36
        title_size = 18 if not self._compact else 15
        sub_size = 13 if not self._compact else 12

        controls = [
            # Circular icon background
            ft.Container(
                content=ft.Icon(
                    self._icon,
                    size=icon_size,
                    color=self._icon_color,
                ),
                width=icon_size + 32,
                height=icon_size + 32,
                border_radius=(icon_size + 32) / 2,
                bgcolor=ft.Colors.with_opacity(0.10, self._icon_color),
                alignment=ft.alignment.center,
            ),
            ft.Container(height=16 if not self._compact else 10),
            ft.Text(
                self._title,
                size=title_size,
                weight=ft.FontWeight.BOLD,
                color=AppTheme.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=6),
            ft.Text(
                self._subtitle,
                size=sub_size,
                color=AppTheme.TEXT_MUTED,
                text_align=ft.TextAlign.CENTER,
            ),
        ]

        if self._btn_label:
            controls += [
                ft.Container(height=20 if not self._compact else 14),
                ft.ElevatedButton(
                    text=self._btn_label,
                    icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                    bgcolor=AppTheme.PRIMARY,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=2,
                    ),
                    on_click=lambda e: self._on_btn_click() if self._on_btn_click else None,
                ),
            ]

        return ft.Column(
            controls,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
