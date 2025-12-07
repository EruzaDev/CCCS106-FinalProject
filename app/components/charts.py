"""
Data Visualization Components - Interactive charts for election analytics
Compatible with Flet 0.21+ (using ft.Container instead of deprecated UserControl)
"""

import flet as ft
from typing import List, Dict


class ChartColors:
    """Color palette for charts"""
    PRIMARY = ["#5C6BC0", "#7986CB", "#9FA8DA", "#C5CAE9"]
    SUCCESS = ["#4CAF50", "#66BB6A", "#81C784", "#A5D6A7"]
    WARNING = ["#FF9800", "#FFA726", "#FFB74D", "#FFCC80"]
    DANGER = ["#F44336", "#EF5350", "#E57373", "#EF9A9A"]
    MIXED = ["#5C6BC0", "#4CAF50", "#FF9800", "#F44336", "#9C27B0", "#00BCD4", "#795548", "#607D8B"]


def create_bar_chart(
    data: List[Dict],  # [{"label": str, "value": float, "color": str (optional)}]
    title: str = "",
    max_value: float = None,
    show_values: bool = True,
    bar_height: int = 30,
) -> ft.Container:
    """Create a horizontal bar chart"""
    calc_max = max_value or max((d.get("value", 0) for d in data), default=100)
    
    bars = []
    for i, item in enumerate(data):
        label = item.get("label", f"Item {i+1}")
        value = item.get("value", 0)
        color = item.get("color", ChartColors.MIXED[i % len(ChartColors.MIXED)])
        
        # Calculate bar width percentage
        percentage = (value / calc_max * 100) if calc_max > 0 else 0
        
        bar_row = ft.Row(
            [
                ft.Container(
                    content=ft.Text(label, size=12, color="#333333", weight=ft.FontWeight.W_500),
                    width=120,
                ),
                ft.Container(
                    content=ft.Container(
                        bgcolor=color,
                        border_radius=4,
                        height=bar_height - 8,
                        width=max(4, percentage * 2),  # Scale for visual, min 4px
                    ),
                    expand=True,
                    alignment=ft.alignment.center_left,
                ),
                ft.Container(
                    content=ft.Text(
                        f"{value:.0f}" if isinstance(value, float) else str(value),
                        size=12,
                        color="#666666",
                        weight=ft.FontWeight.BOLD,
                    ),
                    width=50,
                    alignment=ft.alignment.center_right,
                ) if show_values else ft.Container(),
            ],
            spacing=8,
        )
        
        bars.append(ft.Container(content=bar_row, height=bar_height))
    
    content_controls = []
    if title:
        content_controls.append(ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color="#333333"))
        content_controls.append(ft.Container(height=12))
    content_controls.append(ft.Column(bars, spacing=4))
    
    return ft.Container(
        content=ft.Column(content_controls),
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        padding=16,
    )


def create_donut_chart(
    data: List[Dict],  # [{"label": str, "value": float, "color": str (optional)}]
    title: str = "",
    show_legend: bool = True,
) -> ft.Container:
    """Create a stacked bar chart (simpler alternative to donut)"""
    total = sum(d.get("value", 0) for d in data)
    
    segments = []
    for i, item in enumerate(data):
        value = item.get("value", 0)
        color = item.get("color", ChartColors.MIXED[i % len(ChartColors.MIXED)])
        percentage = (value / total * 100) if total > 0 else 0
        
        segments.append({
            "label": item.get("label", f"Item {i+1}"),
            "value": value,
            "percentage": percentage,
            "color": color,
        })
    
    # Create stacked bar segments
    chart_stack = []
    for seg in segments:
        if seg["percentage"] > 0:
            chart_stack.append(
                ft.Container(
                    bgcolor=seg["color"],
                    expand=int(max(1, seg["percentage"])),
                    height=24,
                    border_radius=4,
                )
            )
    
    chart_visual = ft.Container(
        content=ft.Row(chart_stack, spacing=2),
        border_radius=8,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )
    
    # Legend items
    legend_items = []
    if show_legend:
        for seg in segments:
            legend_items.append(
                ft.Row(
                    [
                        ft.Container(
                            bgcolor=seg["color"],
                            width=12,
                            height=12,
                            border_radius=2,
                        ),
                        ft.Text(
                            f"{seg['label']}: {seg['value']:.0f} ({seg['percentage']:.1f}%)",
                            size=11,
                            color="#666666",
                        ),
                    ],
                    spacing=8,
                )
            )
    
    content_controls = []
    if title:
        content_controls.append(ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color="#333333"))
        content_controls.append(ft.Container(height=12))
    content_controls.append(chart_visual)
    if show_legend:
        content_controls.append(ft.Container(height=12))
        content_controls.append(ft.Column(legend_items, spacing=4))
    
    return ft.Container(
        content=ft.Column(content_controls),
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        padding=16,
    )


def create_stat_card(
    title: str,
    value: str,
    icon: str = None,
    color: str = "#5C6BC0",
    trend: float = None,
    subtitle: str = "",
    width: int = None,
) -> ft.Container:
    """Create an animated statistic card with trend indicator"""
    # Trend indicator
    trend_widget = ft.Container()
    if trend is not None:
        trend_color = "#4CAF50" if trend >= 0 else "#F44336"
        trend_icon = ft.Icons.TRENDING_UP if trend >= 0 else ft.Icons.TRENDING_DOWN
        trend_widget = ft.Row(
            [
                ft.Icon(trend_icon, size=14, color=trend_color),
                ft.Text(f"{abs(trend):.1f}%", size=11, color=trend_color),
            ],
            spacing=2,
        )
    
    icon_container = ft.Container()
    if icon:
        icon_container = ft.Container(
            content=ft.Icon(icon, color=ft.Colors.WHITE, size=24),
            bgcolor=color,
            border_radius=10,
            padding=12,
        )
    
    value_row_controls = [
        ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color="#333333"),
    ]
    if trend is not None:
        value_row_controls.append(trend_widget)
    
    column_controls = [
        ft.Text(title, size=12, color="#666666"),
        ft.Row(
            value_row_controls,
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.END,
        ),
    ]
    if subtitle:
        column_controls.append(ft.Text(subtitle, size=10, color="#999999"))
    
    row_controls = []
    if icon:
        row_controls.append(icon_container)
    row_controls.append(ft.Column(column_controls, spacing=2))
    
    return ft.Container(
        content=ft.Row(row_controls, spacing=16),
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        padding=16,
        width=width,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
    )


def create_compatibility_meter(
    score: int,
    label: str = "Compatibility",
    size: int = 120,
    show_percentage: bool = True,
) -> ft.Container:
    """Create a visual compatibility score meter"""
    score = min(100, max(0, score))
    
    # Color based on score
    if score >= 80:
        color = "#4CAF50"
    elif score >= 60:
        color = "#8BC34A"
    elif score >= 40:
        color = "#FF9800"
    else:
        color = "#F44336"
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Stack(
                    [
                        # Background circle
                        ft.Container(
                            width=size,
                            height=size,
                            border_radius=size // 2,
                            bgcolor="#E0E0E0",
                        ),
                        # Foreground with score
                        ft.Container(
                            content=ft.Container(
                                content=ft.Text(
                                    f"{score}%" if show_percentage else str(score),
                                    size=size // 4,
                                    weight=ft.FontWeight.BOLD,
                                    color=color,
                                ),
                                width=size - 16,
                                height=size - 16,
                                border_radius=(size - 16) // 2,
                                bgcolor=ft.Colors.WHITE,
                                alignment=ft.alignment.center,
                            ),
                            width=size,
                            height=size,
                            border_radius=size // 2,
                            border=ft.border.all(8, color),
                            alignment=ft.alignment.center,
                        ),
                    ],
                ),
                ft.Text(label, size=12, color="#666666"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
    )


def create_insight_card(
    title: str,
    insights: List[str],
    icon: str = ft.Icons.LIGHTBULB,
    color: str = "#5C6BC0",
) -> ft.Container:
    """Create an AI insight display card"""
    insight_items = []
    for insight in insights:
        insight_items.append(
            ft.Row(
                [
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=14, color=color),
                    ft.Text(insight, size=12, color="#333333", expand=True),
                ],
                spacing=8,
            )
        )
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(icon, color=ft.Colors.WHITE, size=16),
                            bgcolor=color,
                            border_radius=6,
                            padding=6,
                        ),
                        ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color="#333333"),
                    ],
                    spacing=8,
                ),
                ft.Container(height=8),
                ft.Column(insight_items, spacing=6),
            ],
        ),
        bgcolor=ft.Colors.with_opacity(0.05, color),
        border=ft.border.all(1, ft.Colors.with_opacity(0.2, color)),
        border_radius=12,
        padding=16,
    )


def create_progress_bar(
    value: float,
    max_value: float = 100,
    color: str = "#5C6BC0",
    height: int = 8,
    show_label: bool = False,
    label: str = "",
) -> ft.Container:
    """Create a simple progress bar"""
    percentage = min(100, max(0, (value / max_value * 100) if max_value > 0 else 0))
    
    progress_bar = ft.Stack(
        [
            ft.Container(
                bgcolor="#E0E0E0",
                height=height,
                border_radius=height // 2,
            ),
            ft.Container(
                bgcolor=color,
                height=height,
                width=percentage * 2,  # Scale for visual
                border_radius=height // 2,
            ),
        ],
    )
    
    if show_label:
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(label, size=11, color="#666666"),
                        ft.Text(f"{value:.0f}/{max_value:.0f}", size=11, color="#999999"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                progress_bar,
            ],
            spacing=4,
        )
    
    return progress_bar


# Legacy class-based exports for backward compatibility
class BarChart(ft.Container):
    """Horizontal bar chart - wrapper around create_bar_chart"""
    def __init__(self, data, title="", max_value=None, show_values=True, **kwargs):
        chart = create_bar_chart(data, title, max_value, show_values)
        super().__init__(content=chart.content, bgcolor=chart.bgcolor, 
                         border_radius=chart.border_radius, padding=chart.padding, **kwargs)


class DonutChart(ft.Container):
    """Donut chart - wrapper around create_donut_chart"""
    def __init__(self, data, title="", show_legend=True, **kwargs):
        chart = create_donut_chart(data, title, show_legend)
        super().__init__(content=chart.content, bgcolor=chart.bgcolor,
                         border_radius=chart.border_radius, padding=chart.padding, **kwargs)


class StatCard(ft.Container):
    """Stat card - wrapper around create_stat_card"""
    def __init__(self, title, value, icon=None, color="#5C6BC0", trend=None, subtitle="", width=None, **kwargs):
        card = create_stat_card(title, value, icon, color, trend, subtitle, width)
        super().__init__(content=card.content, bgcolor=card.bgcolor,
                         border_radius=card.border_radius, padding=card.padding,
                         width=card.width, shadow=card.shadow, **kwargs)


class InsightCard(ft.Container):
    """Insight card - wrapper around create_insight_card"""
    def __init__(self, title, insights, icon=ft.Icons.LIGHTBULB, color="#5C6BC0", **kwargs):
        card = create_insight_card(title, insights, icon, color)
        super().__init__(content=card.content, bgcolor=card.bgcolor,
                         border_radius=card.border_radius, padding=card.padding,
                         border=card.border, **kwargs)


class CompatibilityMeter(ft.Container):
    """Compatibility meter - wrapper around create_compatibility_meter"""
    def __init__(self, score, label="Compatibility", size=120, show_percentage=True, **kwargs):
        meter = create_compatibility_meter(score, label, size, show_percentage)
        super().__init__(content=meter.content, **kwargs)


class TrendIndicator(ft.Container):
    """Simple trend indicator showing up/down arrow with percentage"""
    def __init__(self, value: float, label: str = "", **kwargs):
        color = "#4CAF50" if value >= 0 else "#F44336"
        icon = ft.Icons.TRENDING_UP if value >= 0 else ft.Icons.TRENDING_DOWN
        
        content = ft.Row(
            [
                ft.Icon(icon, size=16, color=color),
                ft.Text(f"{abs(value):.1f}%", size=12, color=color, weight=ft.FontWeight.BOLD),
                ft.Text(label, size=11, color="#666666") if label else ft.Container(),
            ],
            spacing=4,
        )
        super().__init__(content=content, **kwargs)


class ProgressRing(ft.Container):
    """Circular progress indicator"""
    def __init__(self, value: float, max_value: float = 100, color: str = "#5C6BC0", 
                 size: int = 60, **kwargs):
        percentage = min(100, max(0, (value / max_value * 100) if max_value > 0 else 0))
        
        content = ft.Stack(
            [
                ft.Container(
                    width=size,
                    height=size,
                    border_radius=size // 2,
                    border=ft.border.all(4, "#E0E0E0"),
                ),
                ft.Container(
                    content=ft.Text(f"{percentage:.0f}%", size=size // 5, 
                                   weight=ft.FontWeight.BOLD, color=color),
                    width=size,
                    height=size,
                    border_radius=size // 2,
                    border=ft.border.all(4, color),
                    alignment=ft.alignment.center,
                ),
            ],
        )
        super().__init__(content=content, **kwargs)
