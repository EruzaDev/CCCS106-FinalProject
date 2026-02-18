"""
Loading Overlay Component for HonestBallot
Provides reusable loading spinners and progress indicators
"""

import flet as ft
from app.theme import AppTheme


class LoadingOverlay(ft.Stack):
    """
    Full-page translucent overlay with a centered spinner.
    Usage:
        overlay = LoadingOverlay()
        page.overlay.append(overlay)
        overlay.show("Submitting vote…")
        page.update()
        # … do work …
        overlay.hide()
        page.update()
    """

    def __init__(self, message: str = "Loading…"):
        self._message_ref = ft.Ref[ft.Text]()
        super().__init__(
            controls=[
                # Dark scrim
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.45, "#000000"),
                    expand=True,
                ),
                # Centered card
                ft.Container(
                    content=ft.Column(
                        [
                            ft.ProgressRing(
                                width=48,
                                height=48,
                                stroke_width=4,
                                color=AppTheme.PRIMARY,
                            ),
                            ft.Container(height=16),
                            ft.Text(
                                message,
                                ref=self._message_ref,
                                size=14,
                                color=AppTheme.TEXT_PRIMARY,
                                text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=16,
                    padding=ft.padding.symmetric(horizontal=40, vertical=32),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=24,
                        color=ft.Colors.with_opacity(0.18, "#000000"),
                        offset=ft.Offset(0, 8),
                    ),
                    alignment=ft.alignment.center,
                    # Center on screen
                    expand=True,
                ),
            ],
            expand=True,
            visible=False,
        )

    # ── public API ──────────────────────────────────────────────────────────

    def show(self, message: str = "Loading…"):
        """Display the overlay with the given message."""
        if self._message_ref.current:
            self._message_ref.current.value = message
        self.visible = True

    def hide(self):
        """Hide the overlay."""
        self.visible = False


class InlineSpinner(ft.Row):
    """
    Small inline spinner + label, shown inside a card or button area.
    Usage:
        spinner = InlineSpinner("Saving…")
        container.content = spinner
    """

    def __init__(self, message: str = "Loading…", size: int = 20):
        super().__init__(
            controls=[
                ft.ProgressRing(
                    width=size,
                    height=size,
                    stroke_width=3,
                    color=AppTheme.PRIMARY,
                ),
                ft.Text(message, size=13, color=AppTheme.TEXT_SECONDARY),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )


class ButtonLoadingState:
    """
    Helper that swaps a button between normal and loading states.

    Example:
        btn = ft.ElevatedButton("Sign In", on_click=self._handle_login)
        btn_state = ButtonLoadingState(btn, "Sign In", "Signing in…")

        def _handle_login(self, e):
            btn_state.set_loading(True)
            self.page.update()
            # … do work …
            btn_state.set_loading(False)
            self.page.update()
    """

    def __init__(self, button: ft.ElevatedButton, normal_text: str, loading_text: str = "Please wait…"):
        self.button = button
        self.normal_text = normal_text
        self.loading_text = loading_text

    def set_loading(self, loading: bool):
        if loading:
            self.button.text = self.loading_text
            self.button.disabled = True
            self.button.icon = None
            # Add inline spinner in content if supported
            self.button.content = ft.Row(
                [
                    ft.ProgressRing(width=16, height=16, stroke_width=2, color=ft.Colors.WHITE),
                    ft.Text(self.loading_text, color=ft.Colors.WHITE, size=14),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        else:
            self.button.text = self.normal_text
            self.button.disabled = False
            self.button.content = None
