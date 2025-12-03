import flet as ft
from .post_creator import PostCreator
from .post_card import PostCard


class PostContainer(ft.Container):
    """Main post container with post creator and feed"""
    
    def __init__(self, on_post_submit=None):
        super().__init__()
        self.on_post_submit = on_post_submit
        
        # Create post creator
        self.post_creator = PostCreator(
            on_submit=self._handle_post_submit,
        )
        
        # Sample posts data
        self.posts = [
            {
                "username": "CJAY",
                "handle": "@slege_paprint",
                "content": "Get to know your candidates before casting your vote!\nToday's featured candidate: Atty. Maria Santos",
                "checkmarks": [
                    "Advocates for transparent governance",
                    "Plans to improve healthcare access",
                    "Focused on youth employment programs",
                ],
                "avatar_color": ft.Colors.ORANGE_300,
            },
            {
                "username": "dexie",
                "handle": "@dexielangto",
                "content": "Engr. Luis Ramirez emphasizes sustainable infrastructure and rural development in his latest public forum.\nRead his full plan inside the app!\n#Elections2025 #CandidateWatch",
                "checkmarks": [],
                "avatar_color": ft.Colors.TEAL_300,
                "post_tag": "Candidate Update: Governor Race 2025",
            },
        ]
        
        # Build the UI
        self.content = self._build_ui()
        self.expand = True
        self.padding = ft.padding.symmetric(horizontal=20, vertical=15)
    
    def _build_ui(self):
        """Build the post container UI"""
        
        # Post cards list
        post_cards = [
            PostCard(
                username=post["username"],
                handle=post["handle"],
                content=post["content"],
                checkmarks=post.get("checkmarks", []),
                avatar_color=post.get("avatar_color", ft.Colors.GREY_400),
                post_tag=post.get("post_tag"),
            )
            for post in self.posts
        ]
        
        return ft.Column(
            controls=[
                self.post_creator,
                ft.Container(height=10),
                *post_cards,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
    
    def _handle_post_submit(self):
        """Handle post submission"""
        if self.on_post_submit:
            self.on_post_submit(self.post_creator.get_post_content())
        self.post_creator.clear_post()
    
    def add_post(self, username, handle, content, checkmarks=None, 
                 avatar_color=None, post_tag=None):
        """Add a new post to the feed"""
        new_post = {
            "username": username,
            "handle": handle,
            "content": content,
            "checkmarks": checkmarks or [],
            "avatar_color": avatar_color or ft.Colors.GREY_400,
            "post_tag": post_tag,
        }
        self.posts.insert(0, new_post)
        self.content = self._build_ui()
        self.update()
    
    def refresh_posts(self):
        """Refresh the posts display"""
        self.content = self._build_ui()
        self.update()
