import flet as ft


class RightSidebar(ft.Container):
    """Right sidebar with people suggestions and boost post section"""
    
    def __init__(self, on_follow=None, on_boost=None):
        super().__init__()
        self.on_follow = on_follow
        self.on_boost = on_boost
        
        # Sample people suggestions
        self.suggestions = [
            {
                "name": "KADY",
                "bio": "I am a metal man, who Is cutlepie",
                "followers": "6M+ Followers",
                "avatar_color": ft.Colors.PINK_300,
            },
            {
                "name": "elyyyy",
                "bio": "ewian",
                "followers": "3M+ Followers",
                "avatar_color": ft.Colors.PURPLE_300,
            },
            {
                "name": "Arababe",
                "bio": "Tagged you in her 250th post a...",
                "followers": "",
                "avatar_color": ft.Colors.ORANGE_300,
            },
            {
                "name": "Roiroi",
                "bio": "Liked your comment on their po...",
                "followers": "",
                "avatar_color": ft.Colors.TEAL_300,
            },
        ]
        
        # Build the UI
        self.content = self._build_ui()
        self.width = 280
        self.padding = ft.padding.all(15)
    
    def _build_ui(self):
        """Build the right sidebar UI"""
        
        # People you may know section
        people_section = self._build_people_section()
        
        # Boost your post section
        boost_section = self._build_boost_section()
        
        return ft.Column(
            controls=[
                people_section,
                ft.Container(height=20),
                boost_section,
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def _build_people_section(self):
        """Build the people you may know section"""
        
        # Section header
        header = ft.Text(
            "People you may know",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.RED_400,
        )
        
        # People list
        people_list = ft.Column(
            controls=[
                self._build_person_item(person)
                for person in self.suggestions
            ],
            spacing=10,
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    ft.Container(height=15),
                    people_list,
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=15,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            ),
        )
    
    def _build_person_item(self, person):
        """Build a single person suggestion item"""
        return ft.Row(
            controls=[
                # Avatar
                ft.Container(
                    content=ft.Text(
                        person["name"][0],
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    width=40,
                    height=40,
                    bgcolor=person.get("avatar_color", ft.Colors.GREY_400),
                    border_radius=20,
                    alignment=ft.alignment.center,
                ),
                ft.Container(width=10),
                # Info
                ft.Column(
                    controls=[
                        ft.Text(
                            person["name"],
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Text(
                            person["bio"],
                            size=11,
                            color=ft.Colors.GREY_600,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(
                            person["followers"],
                            size=10,
                            color=ft.Colors.BLUE_400,
                            weight=ft.FontWeight.W_500,
                        ) if person["followers"] else ft.Container(),
                    ],
                    spacing=1,
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _build_boost_section(self):
        """Build the boost your post section"""
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Boost your post",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Container(height=15),
                    # Illustration placeholder
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.CAMPAIGN,
                            size=60,
                            color=ft.Colors.BLUE_200,
                        ),
                        width=120,
                        height=80,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=10),
                    # Boost info
                    ft.Row(
                        controls=[
                            ft.Text(
                                "@EUTABLE",
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.BLACK,
                            ),
                            ft.Container(width=10),
                            ft.Text(
                                "Vote wisely guys!",
                                size=11,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                    ),
                    ft.Container(height=5),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.FAVORITE, size=14, color=ft.Colors.RED_400),
                            ft.Text(
                                "& 180 others liked your post & ...",
                                size=11,
                                color=ft.Colors.BLUE_400,
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=15,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            ),
        )
    
    def add_suggestion(self, name, bio, followers="", avatar_color=None):
        """Add a new person suggestion"""
        self.suggestions.append({
            "name": name,
            "bio": bio,
            "followers": followers,
            "avatar_color": avatar_color or ft.Colors.GREY_400,
        })
        self.content = self._build_ui()
        self.update()
