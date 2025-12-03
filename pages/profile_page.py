import flet as ft
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.top_taskbar import TopTaskbar
from components.sidebar import Sidebar


class ProfilePage(ft.Container):
    """
    Profile page displaying user information, stats, posts, and media.
    
    This page is designed to be easily extendable:
    - Profile picture and cover photo can be changed via update methods
    - Posts are stored in a list and can be dynamically added/removed
    - About Me section is editable
    - Photos/Videos gallery supports adding new media
    """
    
    def __init__(
        self,
        username="EUTABLE",
        user_handle="@CUTIE_EUTABLE",
        # User stats
        following_count="11K",
        followers_count="5K",
        likes_count="1M",
        # Profile content
        about_me="fojahbfboasnpfjmasmflcmaxclam,cl",
        # Callbacks
        on_logout=None,
        on_settings=None,
        on_home=None,
    ):
        super().__init__()
        
        # Store user data (can be updated later)
        self.username = username
        self.user_handle = user_handle
        self.following_count = following_count
        self.followers_count = followers_count
        self.likes_count = likes_count
        self.about_me = about_me
        
        # Store callbacks
        self.on_logout = on_logout
        self.on_settings = on_settings
        self.on_home = on_home
        
        # Image paths (can be updated via methods)
        self.profile_picture_path = "assets/fd875946-c220-48f7-a5db-e8e1d3e0a2a0.jpg"
        self.cover_photo_path = None  # None means use gradient placeholder
        
        # Store posts list (for future dynamic updates)
        self.posts_list = []
        
        # Store photos/videos list (for future gallery updates)
        self.media_list = []
        
        # Store location items
        self.location_items = [
            "fojahbfboasnpfjm",
            "fojahbfboasnpfjm",
            "fojahbfboasnpfjm",
            "fojahbfboasnpfjm",
            "fojahbfboasnpfjm",
        ]
        
        # Create components
        self.top_taskbar = TopTaskbar(
            username=username,
            user_handle=user_handle,
            on_settings=self._handle_settings,
        )
        
        self.sidebar = Sidebar(
            username=username,
            on_profile=None,  # Already on profile
            on_settings=self._handle_settings,
            on_logout=self._handle_logout,
        )
        self.sidebar.active_item = "profile"
        
        # Build UI references (for updates)
        self.profile_avatar_ref = None
        self.cover_photo_ref = None
        self.posts_column_ref = None
        self.media_row_ref = None
        
        # Build the UI
        self.content = self._build_ui()
        self.expand = True
        self.bgcolor = "#E1F5FE"  # Light blue background
    
    # ==================== UI BUILDING METHODS ====================
    
    def _build_ui(self):
        """Build the complete profile page layout"""
        
        # Left column: About Me + Location + Photos/Videos
        left_column = self._build_left_column()
        
        # Center column: Cover photo, profile info, stats, and posts
        center_column = self._build_center_column()
        
        # Main content area (sidebar + profile content)
        main_content = ft.Row(
            controls=[
                # Sidebar
                self.sidebar,
                # Vertical divider
                ft.VerticalDivider(width=1, color=ft.Colors.GREY_300),
                # Left info column
                ft.Container(
                    content=left_column,
                    width=220,
                    padding=ft.padding.only(left=15, top=10, right=10),
                ),
                # Center content (profile + posts)
                ft.Container(
                    content=center_column,
                    expand=True,
                    padding=ft.padding.only(top=10, right=20),
                ),
            ],
            expand=True,
            spacing=0,
        )
        
        # Full layout with taskbar at top
        return ft.Column(
            controls=[
                self.top_taskbar,
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                main_content,
            ],
            spacing=0,
            expand=True,
        )
    
    def _build_left_column(self):
        """Build the left column with About Me, Location, and Photos/Videos"""
        
        return ft.Column(
            controls=[
                # About Me section
                self._build_about_me_section(),
                ft.Container(height=15),
                # Location section
                self._build_location_section(),
                ft.Container(height=15),
                # Photos and Videos section
                self._build_photos_videos_section(),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
    
    def _build_about_me_section(self):
        """Build the About Me card"""
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Header
                    ft.Text(
                        "ABOUT ME",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Container(height=8),
                    # About text (can be updated)
                    ft.Text(
                        self.about_me,
                        size=12,
                        color=ft.Colors.GREY_700,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
        )
    
    def _build_location_section(self):
        """Build the location/info items section"""
        
        # Create location rows
        location_rows = []
        icons = [
            ft.Icons.LOCATION_ON_OUTLINED,
            ft.Icons.BUSINESS_OUTLINED,
            ft.Icons.CHAT_BUBBLE_OUTLINE,
            ft.Icons.FACEBOOK_OUTLINED,
            ft.Icons.ALTERNATE_EMAIL,
        ]
        
        for i, item in enumerate(self.location_items):
            icon = icons[i] if i < len(icons) else ft.Icons.INFO_OUTLINE
            location_rows.append(
                ft.Row(
                    controls=[
                        ft.Icon(icon, size=16, color=ft.Colors.GREY_600),
                        ft.Text(item, size=11, color=ft.Colors.GREY_700),
                    ],
                    spacing=8,
                )
            )
        
        return ft.Container(
            content=ft.Column(
                controls=location_rows,
                spacing=8,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
        )
    
    def _build_photos_videos_section(self):
        """Build the Photos and Videos gallery section"""
        
        # Media row reference for future updates
        self.media_row_ref = ft.Row(
            controls=self._build_media_thumbnails(),
            spacing=5,
            wrap=True,
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Header row
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Photos and Videos",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                            ),
                            ft.TextButton(
                                "SEE ALL",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.BLUE_400,
                                ),
                                on_click=self._handle_see_all_media,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    # Media thumbnails
                    self.media_row_ref,
                ],
                spacing=10,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
        )
    
    def _build_media_thumbnails(self):
        """Build placeholder media thumbnails (can be replaced with actual images)"""
        
        # Placeholder colors for demo
        colors = [
            ft.Colors.PINK_100,
            ft.Colors.PURPLE_100,
            ft.Colors.BLUE_100,
            ft.Colors.ORANGE_100,
        ]
        
        thumbnails = []
        for i, color in enumerate(colors):
            thumbnails.append(
                ft.Container(
                    width=45,
                    height=45,
                    bgcolor=color,
                    border_radius=8,
                    # Placeholder - can add actual images here
                    content=ft.Icon(
                        ft.Icons.IMAGE,
                        size=20,
                        color=ft.Colors.GREY_400,
                    ),
                    alignment=ft.alignment.center,
                    on_click=lambda e, idx=i: self._handle_media_click(idx),
                )
            )
        
        return thumbnails
    
    def _build_center_column(self):
        """Build the center column with cover photo, profile info, and posts"""
        
        return ft.Column(
            controls=[
                # Cover photo with profile overlay
                self._build_cover_section(),
                ft.Container(height=15),
                # Post Something section
                self._build_post_creator(),
                ft.Container(height=15),
                # Posts feed
                self._build_posts_feed(),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
    
    def _build_cover_section(self):
        """Build the cover photo with profile picture and stats overlay"""
        
        # Cover photo container (gradient placeholder or actual image)
        if self.cover_photo_path:
            cover_content = ft.Image(
                src=self.cover_photo_path,
                fit=ft.ImageFit.COVER,
                expand=True,
            )
        else:
            # Gradient placeholder with floral design hint
            cover_content = ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.center_left,
                    end=ft.alignment.center_right,
                    colors=["#87CEEB", "#DDA0DD", "#FFB6C1"],
                ),
                expand=True,
            )
        
        # Profile avatar (positioned at bottom-left of cover)
        self.profile_avatar_ref = ft.Container(
            content=ft.CircleAvatar(
                foreground_image_src=self.profile_picture_path,
                radius=45,
            ),
            border=ft.border.all(3, ft.Colors.WHITE),
            border_radius=50,
        )
        
        # Username and handle
        profile_info = ft.Column(
            controls=[
                ft.Text(
                    self.username,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    self.user_handle,
                    size=12,
                    color=ft.Colors.WHITE70,
                ),
            ],
            spacing=2,
        )
        
        # Stats section
        stats_row = ft.Row(
            controls=[
                self._build_stat_item("FOLLOWING", self.following_count),
                self._build_stat_item("FOLLOWERS", self.followers_count),
                self._build_stat_item("LIKES", self.likes_count),
            ],
            spacing=30,
        )
        
        # Profile info row (avatar + name + stats)
        profile_row = ft.Row(
            controls=[
                self.profile_avatar_ref,
                ft.Container(width=10),
                profile_info,
                ft.Container(expand=True),
                stats_row,
                ft.Container(width=20),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Stack cover with profile overlay
        return ft.Container(
            content=ft.Stack(
                controls=[
                    # Cover photo background
                    ft.Container(
                        content=cover_content,
                        height=150,
                        border_radius=ft.border_radius.only(
                            top_left=15,
                            top_right=15,
                        ),
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    ),
                    # Profile info overlay at bottom
                    ft.Container(
                        content=profile_row,
                        bottom=10,
                        left=15,
                        right=15,
                    ),
                ],
            ),
            height=150,
            border_radius=ft.border_radius.only(top_left=15, top_right=15),
            bgcolor=ft.Colors.GREY_200,
        )
    
    def _build_stat_item(self, label, value):
        """Build a single stat item (FOLLOWING, FOLLOWERS, LIKES)"""
        
        return ft.Column(
            controls=[
                ft.Text(
                    label,
                    size=10,
                    color=ft.Colors.WHITE70,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    value,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _build_post_creator(self):
        """Build the 'Post Something' input section"""
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Header
                    ft.Text(
                        "Post Something",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Container(height=10),
                    # Input row
                    ft.Row(
                        controls=[
                            ft.CircleAvatar(
                                foreground_image_src=self.profile_picture_path,
                                radius=20,
                            ),
                            ft.Container(width=10),
                            ft.Container(
                                content=ft.TextField(
                                    hint_text="What's on your mind?",
                                    border=ft.InputBorder.NONE,
                                    text_size=13,
                                    expand=True,
                                ),
                                expand=True,
                                bgcolor=ft.Colors.GREY_100,
                                border_radius=20,
                                padding=ft.padding.symmetric(horizontal=15),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
        )
    
    def _build_posts_feed(self):
        """Build the posts feed section"""
        
        # Reference for dynamic updates
        self.posts_column_ref = ft.Column(
            controls=self._build_sample_posts(),
            spacing=15,
        )
        
        return self.posts_column_ref
    
    def _build_sample_posts(self):
        """Build sample posts (can be replaced with real data)"""
        
        posts = [
            {
                "username": "EUTABLE",
                "time": "20 sep at 10:00 PM",
                "content": "I'm so cute talaga anyways votewisely!!!",
                "comments": 7,
                "likes": 12,
                "shares": 0,
            },
            {
                "username": "EUTABLE",
                "time": "5 aug at 12:00 PM",
                "content": "",
                "comments": 0,
                "likes": 0,
                "shares": 0,
            },
        ]
        
        post_widgets = []
        for post in posts:
            post_widgets.append(self._build_post_card(post))
        
        return post_widgets
    
    def _build_post_card(self, post_data):
        """
        Build a single post card.
        
        post_data dict structure:
        - username: str
        - time: str
        - content: str
        - comments: int
        - likes: int
        - shares: int
        - image: str (optional path to post image)
        """
        
        # Post header (avatar + username + time)
        post_header = ft.Row(
            controls=[
                ft.CircleAvatar(
                    foreground_image_src=self.profile_picture_path,
                    radius=20,
                ),
                ft.Container(width=10),
                ft.Column(
                    controls=[
                        ft.Text(
                            post_data.get("username", "User"),
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Text(
                            post_data.get("time", ""),
                            size=11,
                            color=ft.Colors.GREY_500,
                        ),
                    ],
                    spacing=2,
                ),
            ],
        )
        
        # Post content
        content_controls = [post_header]
        
        if post_data.get("content"):
            content_controls.append(ft.Container(height=10))
            content_controls.append(
                ft.Text(
                    post_data["content"],
                    size=13,
                    color=ft.Colors.BLACK87,
                )
            )
        
        # Post actions (comments, likes, share)
        content_controls.append(ft.Container(height=15))
        content_controls.append(
            ft.Row(
                controls=[
                    # Comments
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=16, color=ft.Colors.GREY_500),
                            ft.Text(
                                f"{post_data.get('comments', 0)} Comments",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Container(width=20),
                    # Likes
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.FAVORITE_BORDER, size=16, color=ft.Colors.GREY_500),
                            ft.Text(
                                f"{post_data.get('likes', 0)} Likes",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Container(width=20),
                    # Share
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SHARE_OUTLINED, size=16, color=ft.Colors.GREY_500),
                            ft.Text(
                                f"{post_data.get('shares', 0)} Share",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        spacing=5,
                    ),
                ],
            )
        )
        
        # Comment input
        content_controls.append(ft.Container(height=10))
        content_controls.append(
            ft.Row(
                controls=[
                    ft.CircleAvatar(
                        foreground_image_src=self.profile_picture_path,
                        radius=15,
                    ),
                    ft.Container(width=8),
                    ft.Container(
                        content=ft.TextField(
                            hint_text="Write you comment...",
                            border=ft.InputBorder.NONE,
                            text_size=12,
                            content_padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        ),
                        expand=True,
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=15,
                    ),
                ],
            )
        )
        
        return ft.Container(
            content=ft.Column(
                controls=content_controls,
                spacing=0,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
        )
    
    # ==================== UPDATE METHODS (For Future Use) ====================
    
    def update_profile_picture(self, image_path):
        """
        Update the profile picture.
        Call this method when user uploads a new profile picture.
        
        Args:
            image_path: Path to the new profile image
        """
        self.profile_picture_path = image_path
        
        # Update avatar in cover section
        if self.profile_avatar_ref:
            self.profile_avatar_ref.content = ft.CircleAvatar(
                foreground_image_src=image_path,
                radius=45,
            )
            self.profile_avatar_ref.update()
        
        # Rebuild sidebar avatar too
        self.sidebar.update_avatar(image_path)
        
        # Update top taskbar avatar
        self.top_taskbar.update_avatar(image_path)
    
    def update_cover_photo(self, image_path):
        """
        Update the cover photo.
        Call this method when user uploads a new cover photo.
        
        Args:
            image_path: Path to the new cover image
        """
        self.cover_photo_path = image_path
        # Rebuild cover section
        if self.cover_photo_ref:
            self.cover_photo_ref.content = ft.Image(
                src=image_path,
                fit=ft.ImageFit.COVER,
                expand=True,
            )
            self.cover_photo_ref.update()
    
    def update_stats(self, following=None, followers=None, likes=None):
        """
        Update user stats.
        
        Args:
            following: New following count (str)
            followers: New followers count (str)
            likes: New likes count (str)
        """
        if following:
            self.following_count = following
        if followers:
            self.followers_count = followers
        if likes:
            self.likes_count = likes
        # Would need to rebuild or update stats UI
    
    def add_post(self, post_data):
        """
        Add a new post to the feed.
        
        Args:
            post_data: Dict with keys: username, time, content, comments, likes, shares
        """
        self.posts_list.insert(0, post_data)
        if self.posts_column_ref:
            self.posts_column_ref.controls.insert(0, self._build_post_card(post_data))
            self.posts_column_ref.update()
    
    def add_media(self, media_path):
        """
        Add a new media item to the gallery.
        
        Args:
            media_path: Path to the image/video
        """
        self.media_list.append(media_path)
        if self.media_row_ref:
            self.media_row_ref.controls.append(
                ft.Container(
                    width=45,
                    height=45,
                    border_radius=8,
                    content=ft.Image(
                        src=media_path,
                        fit=ft.ImageFit.COVER,
                    ),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                )
            )
            self.media_row_ref.update()
    
    # ==================== EVENT HANDLERS ====================
    
    def _handle_settings(self):
        """Handle settings button click"""
        if self.on_settings:
            self.on_settings()
    
    def _handle_logout(self):
        """Handle logout button click"""
        if self.on_logout:
            self.on_logout()
    
    def _handle_see_all_media(self, e):
        """Handle 'SEE ALL' click for photos/videos"""
        print("See all media clicked")
        # Future: Open media gallery view
    
    def _handle_media_click(self, index):
        """Handle click on a media thumbnail"""
        print(f"Media {index} clicked")
        # Future: Open media viewer
