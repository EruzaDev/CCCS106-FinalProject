import flet as ft
from datetime import datetime, date


class DatePickerField(ft.Container):
    """
    A date input field that opens a calendar picker when clicked.
    
    Usage:
        date_field = DatePickerField(
            label="Date",
            on_change=lambda date_str: print(f"Selected: {date_str}"),
        )
    
    To get the value:
        date_string = date_field.value  # Returns "MM/DD/YYYY" format
    """
    
    def __init__(
        self,
        label="Date",
        value="",
        width=220,
        on_change=None,
        border_radius=8,
        bgcolor="#FAFAFA",
    ):
        # Store properties first
        self.label_text = label
        self._value = value
        self.field_width = width
        self.on_change_callback = on_change
        self._border_radius = border_radius
        self._bgcolor = bgcolor
        self._date_picker = None
        
        # Text to display the selected date
        self.display_text = ft.Text(
            value=value if value else "",
            size=14,
            color=ft.Colors.BLACK87,
        )
        
        # Build the content
        content = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            label,
                            size=12,
                            color=ft.Colors.GREY_700,
                        ),
                        self.display_text,
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Icon(
                    ft.Icons.CALENDAR_MONTH,
                    size=22,
                    color=ft.Colors.BLUE_GREY_700,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Initialize the Container
        super().__init__(
            content=content,
            width=width,
            height=50,
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=border_radius,
            bgcolor=bgcolor,
            border=ft.border.all(1, ft.Colors.GREY_400),
            on_click=self._open_picker,
            ink=True,
        )
    
    @property
    def value(self):
        """Get the current date value as string (MM/DD/YYYY)"""
        return self._value or ""
    
    @value.setter
    def value(self, new_value):
        """Set the date value"""
        self._value = new_value
        self.display_text.value = new_value
        if self.page:
            self.display_text.update()
    
    def _open_picker(self, e):
        """Open the date picker"""
        if not self.page:
            return
        
        # Parse existing value for initial date
        initial_date = datetime.now()
        if self._value:
            try:
                initial_date = datetime.strptime(self._value, "%m/%d/%Y")
            except:
                pass
        
        # Create date picker
        self._date_picker = ft.DatePicker(
            value=initial_date,
            first_date=datetime(1900, 1, 1),
            last_date=datetime(2100, 12, 31),
            on_change=self._on_date_change,
            on_dismiss=self._on_dismiss,
        )
        
        self.page.overlay.append(self._date_picker)
        self._date_picker.open = True
        self.page.update()
    
    def _on_date_change(self, e):
        """Handle date selection"""
        if e.control.value:
            formatted = e.control.value.strftime("%m/%d/%Y")
            self._value = formatted
            self.display_text.value = formatted
        
        self._close_picker()
        
        if self.on_change_callback and self._value:
            self.on_change_callback(self._value)
    
    def _on_dismiss(self, e):
        """Handle picker dismiss"""
        self._close_picker()
    
    def _close_picker(self):
        """Close and cleanup the picker"""
        if self.page and self._date_picker:
            self._date_picker.open = False
            if self._date_picker in self.page.overlay:
                self.page.overlay.remove(self._date_picker)
            self._date_picker = None
            self.page.update()
    
    def clear(self):
        """Clear the date field"""
        self._value = ""
        self.display_text.value = ""
        if self.page:
            self.display_text.update()
    
    def set_error(self, error_text):
        """Set an error state on the field"""
        self.border = ft.border.all(1, ft.Colors.RED_400)
        if self.page:
            self.update()
    
    def clear_error(self):
        """Clear the error state"""
        self.border = ft.border.all(1, ft.Colors.GREY_400)
        if self.page:
            self.update()
