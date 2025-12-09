"""
Analytics Page - Election analytics with AI insights and data visualization
"""

import flet as ft
from app.components.charts import (
    BarChart, DonutChart, StatCard, CompatibilityMeter, InsightCard, ChartColors
)
from app.services.ai_service import AIService, RecommendationEngine
from app.theme import AppTheme


class AnalyticsPage(ft.Column):
    """Analytics dashboard with AI-powered insights and visualizations"""
    
    def __init__(self, username, db, user_role, on_back, on_logout, current_user_id=None):
        super().__init__()
        self.username = username
        self.db = db
        self.user_role = user_role
        self.on_back = on_back
        self.on_logout = on_logout
        self.current_user_id = current_user_id
        
        # Initialize AI services
        self.ai_service = AIService(db)
        self.recommendation_engine = RecommendationEngine(db, self.ai_service)
        
        # User preferences for recommendations
        self.user_preferences = []
        self.preference_chips = []
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the main UI"""
        self.controls = [
            self._build_header(),
            ft.Container(
                content=ft.Column(
                    [
                        self._build_content(),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[AppTheme.BG_SECONDARY, AppTheme.BG_PRIMARY],
                ),
                padding=20,
            ),
        ]
        
        self.expand = True
        self.spacing = 0
    
    def _build_header(self):
        """Build the header"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color=AppTheme.PRIMARY,
                                on_click=lambda e: self.on_back(),
                            ),
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.ANALYTICS,
                                    color=ft.Colors.WHITE,
                                    size=24,
                                ),
                                bgcolor=AppTheme.PRIMARY,
                                border_radius=8,
                                padding=8,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Election Analytics",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color="#333333",
                                    ),
                                    ft.Text(
                                        "AI-Powered Insights & Recommendations",
                                        size=12,
                                        color="#666666",
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.AUTO_AWESOME, color="#FF9800", size=16),
                                ft.Text("AI Enhanced", size=12, color="#FF9800"),
                            ],
                            spacing=4,
                        ),
                        bgcolor=ft.Colors.with_opacity(0.1, "#FF9800"),
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=16,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        )
    
    def _build_content(self):
        """Build main content area"""
        return ft.Column(
            [
                # Statistics Overview
                self._build_stats_section(),
                ft.Container(height=24),
                
                # AI Recommendation Section
                self._build_recommendation_section(),
                ft.Container(height=24),
                
                # Top Candidates by AI Score
                self._build_top_candidates_section(),
                ft.Container(height=24),
                
                # Voting Analytics Charts
                self._build_charts_section(),
                ft.Container(height=24),
                
                # Candidate Insights
                self._build_insights_section(),
            ],
        )
    
    def _build_stats_section(self):
        """Build statistics overview cards"""
        stats = self._get_stats()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Overview", size=18, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Container(height=12),
                    ft.Row(
                        [
                            StatCard(
                                title="Total Candidates",
                                value=str(stats["candidates"]),
                                icon=ft.Icons.PEOPLE,
                                color="#5C6BC0",
                                subtitle="Running for office",
                            ),
                            StatCard(
                                title="Verified Achievements",
                                value=str(stats["verified"]),
                                icon=ft.Icons.VERIFIED,
                                color="#4CAF50",
                                trend=15.3,
                                subtitle="Confirmed records",
                            ),
                            StatCard(
                                title="Votes Cast",
                                value=str(stats["votes"]),
                                icon=ft.Icons.HOW_TO_VOTE,
                                color="#FF9800",
                                subtitle="This election",
                            ),
                            StatCard(
                                title="Positions",
                                value=str(stats["positions"]),
                                icon=ft.Icons.CATEGORY,
                                color="#9C27B0",
                                subtitle="Available offices",
                            ),
                        ],
                        spacing=16,
                        wrap=True,
                    ),
                ],
            ),
        )
    
    def _build_recommendation_section(self):
        """Build AI recommendation section with preference selection"""
        available_preferences = [
            "Education", "Healthcare", "Economy", "Environment", 
            "Security", "Infrastructure", "Social Welfare", "Governance"
        ]
        
        preference_chips = []
        for pref in available_preferences:
            is_selected = pref.lower().replace(" ", "_") in self.user_preferences
            preference_chips.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CHECK if is_selected else ft.Icons.ADD,
                                size=14,
                                color=ft.Colors.WHITE if is_selected else "#666666",
                            ),
                            ft.Text(
                                pref,
                                size=12,
                                color=ft.Colors.WHITE if is_selected else "#333333",
                            ),
                        ],
                        spacing=4,
                    ),
                    bgcolor="#5C6BC0" if is_selected else "#E0E0E0",
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    border_radius=20,
                    on_click=lambda e, p=pref: self._toggle_preference(p),
                    ink=True,
                )
            )
        
        # Get recommendations
        recommendations = []
        if self.user_preferences:
            recommendations = self.recommendation_engine.get_recommendations(
                self.user_preferences, limit=3
            )
        
        recommendation_cards = []
        for rec in recommendations:
            pol = rec["politician"]
            recommendation_cards.append(
                self._build_recommendation_card(
                    name=pol.get("full_name") or pol.get("username"),
                    position=pol.get("position", "Unknown"),
                    party=pol.get("party", "Independent"),
                    score=rec["compatibility_score"],
                    reason=rec["reason"],
                    matching=rec["matching_areas"],
                )
            )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.AUTO_AWESOME, color="#FF9800", size=20),
                            ft.Text("AI Candidate Recommendations", size=18, weight=ft.FontWeight.BOLD, color="#333333"),
                        ],
                        spacing=8,
                    ),
                    ft.Text(
                        "Select your priorities to get personalized candidate recommendations",
                        size=12,
                        color="#666666",
                    ),
                    ft.Container(height=12),
                    
                    # Preference chips
                    ft.Row(preference_chips, spacing=8, wrap=True),
                    
                    ft.Container(height=16),
                    
                    # Recommendations
                    ft.Column(recommendation_cards, spacing=12) if recommendation_cards else ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.TOUCH_APP, size=48, color="#CCCCCC"),
                                ft.Text("Select your priorities above to get recommendations", size=14, color="#666666"),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=24,
                        alignment=ft.alignment.center,
                    ),
                ],
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=20,
        )
    
    def _build_recommendation_card(self, name, position, party, score, reason, matching):
        """Build a recommendation card"""
        match_chips = []
        for area in matching[:3]:
            match_chips.append(
                ft.Container(
                    content=ft.Text(area, size=10, color="#5C6BC0"),
                    bgcolor=ft.Colors.with_opacity(0.1, "#5C6BC0"),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=10,
                )
            )
        
        return ft.Container(
            content=ft.Row(
                [
                    # Compatibility score
                    CompatibilityMeter(score=score, size=80, label="Match"),
                    ft.Container(width=16),
                    
                    # Candidate info
                    ft.Column(
                        [
                            ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color="#333333"),
                            ft.Text(f"{position} • {party}", size=12, color="#666666"),
                            ft.Container(height=4),
                            ft.Row(match_chips, spacing=4),
                            ft.Container(height=4),
                            ft.Text(reason, size=11, color="#888888", italic=True),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
            ),
            bgcolor="#FAFAFA",
            border=ft.border.all(1, "#E0E0E0"),
            border_radius=12,
            padding=16,
        )
    
    def _build_top_candidates_section(self):
        """Build top candidates section with AI scores"""
        if not self.db:
            return ft.Container()
        
        politicians = self.db.get_users_by_role("politician")
        
        # Calculate AI scores for all candidates
        scored_candidates = []
        for pol in politicians:
            pol_dict = {
                "id": pol[0],
                "username": pol[1],
                "full_name": pol[4],
                "position": pol[7] if len(pol) > 7 else None,
                "party": pol[8] if len(pol) > 8 else None,
                "biography": pol[9] if len(pol) > 9 else "",
                "profile_image": pol[6] if len(pol) > 6 else None,
            }
            
            insights = self.ai_service.get_candidate_insights(pol_dict)
            score = self.ai_service._calculate_overall_score(insights)
            summary = self.ai_service.generate_candidate_summary(pol_dict)
            
            scored_candidates.append({
                "politician": pol_dict,
                "insights": insights,
                "score": score,
                "summary": summary,
            })
        
        # Sort by score
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        top_5 = scored_candidates[:5]
        
        if not top_5:
            return ft.Container()
        
        # Build candidate cards
        candidate_cards = []
        for i, cand in enumerate(top_5):
            pol = cand["politician"]
            insights = cand["insights"]
            
            # Determine rank medal
            if i == 0:
                rank_icon = "🥇"
                rank_color = "#FFD700"
            elif i == 1:
                rank_icon = "🥈"
                rank_color = "#C0C0C0"
            elif i == 2:
                rank_icon = "🥉"
                rank_color = "#CD7F32"
            else:
                rank_icon = f"#{i+1}"
                rank_color = "#666666"
            
            # Experience badge
            exp_level = insights.get("experience_level", "unknown")
            exp_badge = {
                "high": ("Veteran", "#4CAF50"),
                "medium": ("Experienced", "#2196F3"),
                "emerging": ("Fresh Face", "#FF9800"),
            }.get(exp_level, ("New", "#9E9E9E"))
            
            # Strengths chips
            strength_chips = []
            for strength in insights.get("key_strengths", [])[:3]:
                strength_chips.append(
                    ft.Container(
                        content=ft.Text(strength, size=9, color="#5C6BC0"),
                        bgcolor=ft.Colors.with_opacity(0.1, "#5C6BC0"),
                        padding=ft.padding.symmetric(horizontal=6, vertical=2),
                        border_radius=8,
                    )
                )
            
            candidate_cards.append(
                ft.Container(
                    content=ft.Row(
                        [
                            # Rank
                            ft.Container(
                                content=ft.Text(rank_icon, size=20),
                                width=40,
                                alignment=ft.alignment.center,
                            ),
                            
                            # Score circle
                            ft.Container(
                                content=ft.Container(
                                    content=ft.Text(
                                        str(cand["score"]),
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE,
                                    ),
                                    width=44,
                                    height=44,
                                    border_radius=22,
                                    bgcolor="#5C6BC0" if cand["score"] >= 70 else "#FF9800" if cand["score"] >= 50 else "#F44336",
                                    alignment=ft.alignment.center,
                                ),
                            ),
                            ft.Container(width=12),
                            
                            # Candidate info
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                pol.get("full_name") or pol.get("username", "Unknown"),
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color="#333333",
                                            ),
                                            ft.Container(
                                                content=ft.Text(exp_badge[0], size=9, color=ft.Colors.WHITE),
                                                bgcolor=exp_badge[1],
                                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                                border_radius=8,
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Text(
                                        f"{pol.get('position', 'Unknown')} • {pol.get('party', 'Independent')}",
                                        size=11,
                                        color="#666666",
                                    ),
                                    ft.Row(strength_chips, spacing=4) if strength_chips else ft.Container(),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            
                            # Verified count
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.VERIFIED, size=14, color="#4CAF50"),
                                        ft.Text(str(insights.get("verified_achievements", 0)), size=12, color="#4CAF50"),
                                    ],
                                    spacing=2,
                                ),
                                tooltip=f"{insights.get('verified_achievements', 0)} verified achievements",
                            ),
                        ],
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, "#E0E0E0"),
                    border_radius=10,
                    padding=12,
                )
            )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LEADERBOARD, color="#5C6BC0", size=20),
                            ft.Text("Top Candidates by AI Score", size=18, weight=ft.FontWeight.BOLD, color="#333333"),
                            ft.Container(expand=True),
                            ft.Container(
                                content=ft.Text("Based on verified achievements & profile analysis", size=10, color="#999999"),
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=12),
                    ft.Column(candidate_cards, spacing=8),
                ],
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=20,
        )
    
    def _build_charts_section(self):
        """Build data visualization charts"""
        # Get data for charts
        chart_data = self._get_chart_data()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Election Analytics", size=18, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Container(height=12),
                    ft.Row(
                        [
                            # Votes by position chart
                            ft.Container(
                                content=BarChart(
                                    data=chart_data["votes_by_position"],
                                    title="Votes by Position",
                                    show_values=True,
                                ),
                                expand=True,
                            ),
                            
                            # Party distribution chart
                            ft.Container(
                                content=DonutChart(
                                    data=chart_data["party_distribution"],
                                    title="Candidates by Party",
                                    show_legend=True,
                                ),
                                expand=True,
                            ),
                        ],
                        spacing=16,
                    ),
                    ft.Container(height=16),
                    ft.Row(
                        [
                            # Verification status chart
                            ft.Container(
                                content=BarChart(
                                    data=chart_data["verification_status"],
                                    title="Achievement Verifications",
                                ),
                                expand=True,
                            ),
                            
                            # Legal records chart
                            ft.Container(
                                content=BarChart(
                                    data=chart_data["legal_records"],
                                    title="Legal Records Status",
                                ),
                                expand=True,
                            ),
                        ],
                        spacing=16,
                    ),
                ],
            ),
        )
    
    def _build_insights_section(self):
        """Build AI insights section with enhanced layout"""
        insights = self._generate_insights()
        
        if not insights:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.PSYCHOLOGY, size=48, color="#CCCCCC"),
                        ft.Text("No insights available yet", size=14, color="#666666"),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=40,
                alignment=ft.alignment.center,
            )
        
        # Create rows of insight cards (2 per row for better readability)
        insight_rows = []
        for i in range(0, len(insights), 2):
            row_cards = []
            for j in range(2):
                if i + j < len(insights):
                    insight = insights[i + j]
                    row_cards.append(
                        ft.Container(
                            content=InsightCard(
                                title=insight["title"],
                                insights=insight["points"],
                                icon=insight.get("icon", ft.Icons.LIGHTBULB),
                                color=insight.get("color", "#5C6BC0"),
                            ),
                            expand=True,
                        )
                    )
            insight_rows.append(ft.Row(row_cards, spacing=16))
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PSYCHOLOGY, color="#9C27B0", size=20),
                            ft.Text("AI-Generated Insights", size=18, weight=ft.FontWeight.BOLD, color="#333333"),
                            ft.Container(expand=True),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.AUTO_AWESOME, size=14, color="#FF9800"),
                                        ft.Text("Powered by AI Analysis", size=11, color="#666666"),
                                    ],
                                    spacing=4,
                                ),
                                bgcolor=ft.Colors.with_opacity(0.1, "#FF9800"),
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=12,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=16),
                    ft.Column(insight_rows, spacing=16),
                ],
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=20,
        )
    
    def _toggle_preference(self, preference):
        """Toggle a preference selection"""
        pref_key = preference.lower().replace(" ", "_")
        if pref_key in self.user_preferences:
            self.user_preferences.remove(pref_key)
        else:
            self.user_preferences.append(pref_key)
        
        # Rebuild UI
        self._build_ui()
        if self.page:
            self.page.update()
    
    def _get_stats(self):
        """Get statistics from database"""
        stats = {
            "candidates": 0,
            "verified": 0,
            "votes": 0,
            "positions": 0,
        }
        
        if not self.db:
            return stats
        
        # Get candidates
        politicians = self.db.get_users_by_role("politician")
        stats["candidates"] = len(politicians)
        
        # Get unique positions
        positions = set(p[7] for p in politicians if p[7])
        stats["positions"] = len(positions)
        
        # Get verified achievements
        for pol in politicians:
            verifications = self.db.get_verifications_by_politician(pol[0])
            stats["verified"] += len([v for v in verifications if v[4] == 'verified'])
        
        # Get votes - result[6] is vote_count from get_election_results
        results = self.db.get_election_results()
        stats["votes"] = sum(r[6] for r in results)
        
        return stats
    
    def _get_chart_data(self):
        """Get data for charts"""
        data = {
            "votes_by_position": [],
            "party_distribution": [],
            "verification_status": [],
            "legal_records": [],
        }
        
        if not self.db:
            return data
        
        # Votes by position - result[3] is position, result[6] is vote_count
        results = self.db.get_election_results()
        position_votes = {}
        for result in results:
            pos = result[3] if len(result) > 3 else "Unknown"
            position_votes[pos] = position_votes.get(pos, 0) + result[6]
        
        colors = ChartColors.MIXED
        for i, (pos, votes) in enumerate(position_votes.items()):
            data["votes_by_position"].append({
                "label": pos,
                "value": votes,
                "color": colors[i % len(colors)],
            })
        
        # Party distribution
        politicians = self.db.get_users_by_role("politician")
        party_counts = {}
        for pol in politicians:
            party = pol[8] if pol[8] else "Independent"
            party_counts[party] = party_counts.get(party, 0) + 1
        
        for i, (party, count) in enumerate(party_counts.items()):
            data["party_distribution"].append({
                "label": party,
                "value": count,
                "color": colors[i % len(colors)],
            })
        
        # Verification status
        verified = pending = rejected = 0
        for pol in politicians:
            verifications = self.db.get_verifications_by_politician(pol[0])
            for v in verifications:
                if v[4] == 'verified':
                    verified += 1
                elif v[4] == 'pending':
                    pending += 1
                else:
                    rejected += 1
        
        data["verification_status"] = [
            {"label": "Verified", "value": verified, "color": "#4CAF50"},
            {"label": "Pending", "value": pending, "color": "#FF9800"},
            {"label": "Rejected", "value": rejected, "color": "#F44336"},
        ]
        
        # Legal records
        legal_stats = self.db.get_legal_records_stats()
        data["legal_records"] = [
            {"label": "Total Records", "value": legal_stats.get("total", 0), "color": "#5C6BC0"},
            {"label": "Verified", "value": legal_stats.get("verified", 0), "color": "#4CAF50"},
            {"label": "Pending", "value": legal_stats.get("pending", 0), "color": "#FF9800"},
        ]
        
        return data
    
    def _generate_insights(self):
        """Generate AI insights with comprehensive analysis"""
        insights = []
        
        if not self.db:
            return insights
        
        politicians = self.db.get_users_by_role("politician")
        results = self.db.get_election_results()
        
        # === 1. Campaign Focus Analysis ===
        all_themes = []
        experience_levels = {"high": 0, "medium": 0, "emerging": 0, "unknown": 0}
        
        for pol in politicians:
            bio = pol[9] if len(pol) > 9 and pol[9] else ""
            themes = self.ai_service._extract_themes(bio)
            all_themes.extend(themes)
            exp = self.ai_service._assess_experience(bio)
            experience_levels[exp] = experience_levels.get(exp, 0) + 1
        
        # Count theme frequency
        from collections import Counter
        theme_counts = Counter(all_themes)
        top_themes = theme_counts.most_common(5)
        
        if top_themes:
            theme_points = []
            if len(top_themes) >= 1:
                theme_points.append(f"🔥 Top focus: {top_themes[0][0]} ({top_themes[0][1]} candidates)")
            if len(top_themes) >= 2:
                theme_points.append(f"📊 2nd focus: {top_themes[1][0]} ({top_themes[1][1]} candidates)")
            if len(top_themes) >= 3:
                theme_points.append(f"📈 Also popular: {', '.join(t[0] for t in top_themes[2:4])}")
            
            insights.append({
                "title": "Campaign Focus Analysis",
                "points": theme_points,
                "icon": ft.Icons.CAMPAIGN,
                "color": "#5C6BC0",
            })
        
        # === 2. Experience Distribution ===
        exp_points = []
        total = sum(experience_levels.values())
        if experience_levels["high"] > 0:
            pct = int(experience_levels["high"] / total * 100)
            exp_points.append(f"👨‍💼 {experience_levels['high']} veteran candidates ({pct}%)")
        if experience_levels["emerging"] > 0:
            pct = int(experience_levels["emerging"] / total * 100)
            exp_points.append(f"🌟 {experience_levels['emerging']} fresh/new candidates ({pct}%)")
        exp_points.append(f"📋 {len(set(p[7] for p in politicians if len(p) > 7 and p[7]))} different positions contested")
        
        insights.append({
            "title": "Candidate Experience",
            "points": exp_points,
            "icon": ft.Icons.WORKSPACE_PREMIUM,
            "color": "#9C27B0",
        })
        
        # === 3. Verification & Trust Score ===
        total_verified = 0
        total_pending = 0
        candidates_with_verifications = 0
        
        for p in politicians:
            verifs = self.db.get_verifications_by_politician(p[0])
            verified_count = len([v for v in verifs if v[4] == 'verified'])
            pending_count = len([v for v in verifs if v[4] == 'pending'])
            total_verified += verified_count
            total_pending += pending_count
            if verified_count > 0:
                candidates_with_verifications += 1
        
        trust_pct = int(candidates_with_verifications / len(politicians) * 100) if politicians else 0
        
        trust_points = [
            f"✅ {total_verified} total verified achievements",
            f"⏳ {total_pending} verifications pending",
            f"🏆 {trust_pct}% of candidates have verified records",
        ]
        
        insights.append({
            "title": "Transparency Score",
            "points": trust_points,
            "icon": ft.Icons.VERIFIED_USER,
            "color": "#4CAF50",
        })
        
        # === 4. Voting Trends ===
        if results:
            total_votes = sum(r[6] for r in results)
            candidates_with_votes = len([r for r in results if r[6] > 0])
            
            # Find leader by position
            position_leaders = {}
            for r in results:
                pos = r[3] if len(r) > 3 else "Unknown"
                if pos not in position_leaders or r[6] > position_leaders[pos][1]:
                    position_leaders[pos] = (r[1], r[6])  # name, votes
            
            trend_points = [
                f"📊 {total_votes} total votes cast",
                f"🗳️ {candidates_with_votes}/{len(politicians)} candidates received votes",
            ]
            
            if position_leaders:
                top_pos = list(position_leaders.items())[0]
                trend_points.append(f"🏅 Leading in {top_pos[0]}: {top_pos[1][0]}")
            
            insights.append({
                "title": "Voting Trends",
                "points": trend_points,
                "icon": ft.Icons.TRENDING_UP,
                "color": "#FF9800",
            })
        
        # === 5. AI Recommendation ===
        insights.append({
            "title": "Smart Voting Tips",
            "points": [
                "🎯 Select your priorities above for personalized matches",
                "🔍 Compare candidates running for the same position",
                "📋 Review verified achievements before deciding",
            ],
            "icon": ft.Icons.TIPS_AND_UPDATES,
            "color": "#00BCD4",
        })
        
        return insights
