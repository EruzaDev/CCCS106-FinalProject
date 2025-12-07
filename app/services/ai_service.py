"""
AI Service - Rule-based AI features for candidate analysis and recommendations
Uses lightweight rule-based inference without external API dependencies
"""

import re
from typing import Dict, List, Optional, Tuple
from collections import Counter


class AIService:
    """AI-powered analysis and recommendation service"""
    
    # Keywords for different policy areas
    POLICY_KEYWORDS = {
        "education": ["education", "school", "student", "learning", "teacher", "scholarship", "university", "curriculum"],
        "healthcare": ["health", "medical", "hospital", "doctor", "medicine", "wellness", "care", "insurance"],
        "economy": ["economy", "business", "job", "employment", "trade", "industry", "growth", "investment"],
        "environment": ["environment", "climate", "green", "sustainable", "pollution", "conservation", "renewable"],
        "security": ["security", "police", "crime", "safety", "military", "defense", "law", "order"],
        "infrastructure": ["infrastructure", "road", "bridge", "transport", "construction", "development", "urban"],
        "social_welfare": ["welfare", "poverty", "housing", "community", "support", "assistance", "social"],
        "governance": ["governance", "transparency", "corruption", "reform", "accountability", "democracy"],
    }
    
    # Sentiment indicators
    POSITIVE_WORDS = ["success", "achieved", "improved", "led", "champion", "advocate", "reform", "innovative", 
                      "dedicated", "experienced", "accomplished", "passionate", "committed"]
    NEGATIVE_WORDS = ["alleged", "accused", "failed", "scandal", "controversy", "dismissed", "rejected"]
    
    def __init__(self, db=None):
        self.db = db
    
    def generate_candidate_summary(self, politician: Dict) -> str:
        """Generate an AI-powered summary of a candidate"""
        name = politician.get("full_name") or politician.get("username", "Unknown")
        position = politician.get("position", "Unknown Position")
        party = politician.get("party", "Independent")
        biography = politician.get("biography", "")
        
        # Analyze biography for key themes
        themes = self._extract_themes(biography)
        
        # Build summary
        summary_parts = [f"{name} is running for {position}"]
        
        if party and party != "Independent":
            summary_parts[0] += f" representing {party}"
        
        if themes:
            theme_str = ", ".join(themes[:3])  # Top 3 themes
            summary_parts.append(f"Key focus areas: {theme_str}")
        
        # Add sentiment analysis
        sentiment = self._analyze_sentiment(biography)
        if sentiment > 0.3:
            summary_parts.append("Profile indicates strong positive track record.")
        elif sentiment < -0.2:
            summary_parts.append("Profile contains some concerning elements worth reviewing.")
        
        return ". ".join(summary_parts) + "."
    
    def calculate_compatibility_score(self, voter_preferences: List[str], politician: Dict) -> Tuple[int, List[str]]:
        """
        Calculate compatibility score between voter preferences and politician
        Returns score (0-100) and list of matching areas
        """
        biography = politician.get("biography", "").lower()
        position = politician.get("position", "").lower()
        party = politician.get("party", "").lower()
        
        combined_text = f"{biography} {position} {party}"
        
        matches = []
        score = 50  # Base score
        
        for pref in voter_preferences:
            pref_lower = pref.lower()
            if pref_lower in self.POLICY_KEYWORDS:
                keywords = self.POLICY_KEYWORDS[pref_lower]
                keyword_matches = sum(1 for kw in keywords if kw in combined_text)
                if keyword_matches > 0:
                    matches.append(pref)
                    score += min(15, keyword_matches * 5)  # Max 15 points per category
            elif pref_lower in combined_text:
                matches.append(pref)
                score += 10
        
        # Get verification bonus
        if self.db:
            verifications = self.db.get_verifications_by_politician(politician.get("id", 0))
            verified_count = len([v for v in verifications if v[4] == 'verified'])
            score += min(20, verified_count * 5)  # Bonus for verified achievements
        
        return min(100, max(0, score)), matches
    
    def get_candidate_insights(self, politician: Dict) -> Dict:
        """Generate comprehensive insights about a candidate"""
        biography = politician.get("biography", "")
        
        insights = {
            "themes": self._extract_themes(biography),
            "sentiment_score": self._analyze_sentiment(biography),
            "experience_level": self._assess_experience(biography),
            "key_strengths": self._identify_strengths(biography),
            "focus_areas": self._get_focus_areas(biography),
        }
        
        # Add verification status if db available
        if self.db:
            verifications = self.db.get_verifications_by_politician(politician.get("id", 0))
            insights["verified_achievements"] = len([v for v in verifications if v[4] == 'verified'])
            insights["pending_verifications"] = len([v for v in verifications if v[4] == 'pending'])
            
            # Get legal records
            records = self.db.get_legal_records_by_politician(politician.get("id", 0))
            insights["legal_records"] = len(records)
            insights["verified_records"] = len([r for r in records if r[6] == 'verified'])
        
        return insights
    
    def compare_candidates(self, candidate1: Dict, candidate2: Dict) -> Dict:
        """AI-powered comparison between two candidates"""
        insights1 = self.get_candidate_insights(candidate1)
        insights2 = self.get_candidate_insights(candidate2)
        
        comparison = {
            "candidate1": {
                "name": candidate1.get("full_name") or candidate1.get("username"),
                "insights": insights1,
                "overall_score": self._calculate_overall_score(insights1),
            },
            "candidate2": {
                "name": candidate2.get("full_name") or candidate2.get("username"),
                "insights": insights2,
                "overall_score": self._calculate_overall_score(insights2),
            },
            "comparison_summary": self._generate_comparison_summary(candidate1, candidate2, insights1, insights2),
        }
        
        return comparison
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extract key themes from text"""
        text_lower = text.lower()
        themes = []
        
        for theme, keywords in self.POLICY_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > 0:
                themes.append((theme.replace("_", " ").title(), matches))
        
        # Sort by frequency and return theme names
        themes.sort(key=lambda x: x[1], reverse=True)
        return [t[0] for t in themes]
    
    def _analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis (-1 to 1)"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.POSITIVE_WORDS if word in text_lower)
        negative_count = sum(1 for word in self.NEGATIVE_WORDS if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        return (positive_count - negative_count) / total
    
    def _assess_experience(self, text: str) -> str:
        """Assess experience level from biography"""
        text_lower = text.lower()
        
        experience_indicators = {
            "high": ["decades", "extensive", "veteran", "senior", "long-standing", "20 years", "15 years"],
            "medium": ["years", "experience", "served", "worked", "former", "previous"],
            "emerging": ["new", "fresh", "young", "aspiring", "first-time"],
        }
        
        for level, indicators in experience_indicators.items():
            if any(ind in text_lower for ind in indicators):
                return level
        
        return "unknown"
    
    def _identify_strengths(self, text: str) -> List[str]:
        """Identify key strengths mentioned"""
        text_lower = text.lower()
        strengths = []
        
        strength_keywords = {
            "Leadership": ["led", "leader", "leadership", "spearheaded", "headed"],
            "Reform-oriented": ["reform", "change", "innovative", "modernize"],
            "Community Focus": ["community", "grassroots", "local", "constituents"],
            "Policy Expert": ["policy", "legislation", "law", "regulatory"],
            "Economic Knowledge": ["economic", "business", "finance", "fiscal"],
        }
        
        for strength, keywords in strength_keywords.items():
            if any(kw in text_lower for kw in keywords):
                strengths.append(strength)
        
        return strengths[:4]  # Return top 4
    
    def _get_focus_areas(self, text: str) -> List[Dict]:
        """Get focus areas with relevance scores"""
        text_lower = text.lower()
        areas = []
        
        for area, keywords in self.POLICY_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > 0:
                areas.append({
                    "area": area.replace("_", " ").title(),
                    "relevance": min(100, matches * 25),
                })
        
        areas.sort(key=lambda x: x["relevance"], reverse=True)
        return areas[:5]
    
    def _calculate_overall_score(self, insights: Dict) -> int:
        """Calculate overall candidate score"""
        score = 50  # Base
        
        # Sentiment bonus
        sentiment = insights.get("sentiment_score", 0)
        score += int(sentiment * 20)
        
        # Verified achievements bonus
        verified = insights.get("verified_achievements", 0)
        score += min(20, verified * 5)
        
        # Experience bonus
        exp = insights.get("experience_level", "unknown")
        if exp == "high":
            score += 15
        elif exp == "medium":
            score += 10
        
        # Penalty for legal records
        records = insights.get("legal_records", 0)
        score -= min(15, records * 5)
        
        return min(100, max(0, score))
    
    def _generate_comparison_summary(self, c1: Dict, c2: Dict, i1: Dict, i2: Dict) -> str:
        """Generate a text summary comparing two candidates"""
        name1 = c1.get("full_name") or c1.get("username", "Candidate 1")
        name2 = c2.get("full_name") or c2.get("username", "Candidate 2")
        
        score1 = self._calculate_overall_score(i1)
        score2 = self._calculate_overall_score(i2)
        
        summary_parts = []
        
        # Overall comparison
        if abs(score1 - score2) < 10:
            summary_parts.append(f"Both candidates have similar overall profiles.")
        elif score1 > score2:
            summary_parts.append(f"{name1} has a stronger verified profile overall.")
        else:
            summary_parts.append(f"{name2} has a stronger verified profile overall.")
        
        # Theme comparison
        themes1 = set(i1.get("themes", []))
        themes2 = set(i2.get("themes", []))
        common = themes1 & themes2
        
        if common:
            summary_parts.append(f"Both focus on: {', '.join(list(common)[:2])}.")
        
        unique1 = themes1 - themes2
        unique2 = themes2 - themes1
        
        if unique1:
            summary_parts.append(f"{name1} uniquely emphasizes {list(unique1)[0]}.")
        if unique2:
            summary_parts.append(f"{name2} uniquely emphasizes {list(unique2)[0]}.")
        
        return " ".join(summary_parts)


class RecommendationEngine:
    """Smart candidate recommendation engine"""
    
    def __init__(self, db, ai_service: AIService = None):
        self.db = db
        self.ai = ai_service or AIService(db)
    
    def get_recommendations(self, voter_preferences: List[str], position: str = None, limit: int = 5) -> List[Dict]:
        """Get recommended candidates based on voter preferences"""
        politicians = self.db.get_users_by_role("politician") if self.db else []
        
        recommendations = []
        
        for pol in politicians:
            politician_dict = {
                "id": pol[0],
                "username": pol[1],
                "email": pol[2],
                "full_name": pol[5],
                "position": pol[7],
                "party": pol[8],
                "biography": pol[9],
                "profile_image": pol[10],
            }
            
            # Filter by position if specified
            if position and politician_dict["position"] != position:
                continue
            
            # Calculate compatibility
            score, matches = self.ai.calculate_compatibility_score(voter_preferences, politician_dict)
            
            # Get insights
            insights = self.ai.get_candidate_insights(politician_dict)
            
            recommendations.append({
                "politician": politician_dict,
                "compatibility_score": score,
                "matching_areas": matches,
                "insights": insights,
                "reason": self._generate_recommendation_reason(politician_dict, matches, insights),
            })
        
        # Sort by compatibility score
        recommendations.sort(key=lambda x: x["compatibility_score"], reverse=True)
        
        return recommendations[:limit]
    
    def get_similar_candidates(self, politician_id: int, limit: int = 3) -> List[Dict]:
        """Find candidates similar to a given politician"""
        # Get the reference politician
        politicians = self.db.get_users_by_role("politician") if self.db else []
        reference = None
        others = []
        
        for pol in politicians:
            pol_dict = {
                "id": pol[0],
                "username": pol[1],
                "full_name": pol[5],
                "position": pol[7],
                "party": pol[8],
                "biography": pol[9],
                "profile_image": pol[10],
            }
            
            if pol[0] == politician_id:
                reference = pol_dict
            else:
                others.append(pol_dict)
        
        if not reference:
            return []
        
        # Get reference themes
        ref_themes = self.ai._extract_themes(reference.get("biography", ""))
        
        # Score similarity
        similar = []
        for other in others:
            other_themes = self.ai._extract_themes(other.get("biography", ""))
            
            # Calculate theme overlap
            common_themes = set(ref_themes) & set(other_themes)
            similarity = len(common_themes) / max(len(ref_themes), 1) * 100
            
            # Bonus for same position
            if other.get("position") == reference.get("position"):
                similarity += 20
            
            similar.append({
                "politician": other,
                "similarity_score": min(100, int(similarity)),
                "common_themes": list(common_themes),
            })
        
        similar.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similar[:limit]
    
    def _generate_recommendation_reason(self, politician: Dict, matches: List[str], insights: Dict) -> str:
        """Generate a human-readable recommendation reason"""
        name = politician.get("full_name") or politician.get("username")
        reasons = []
        
        if matches:
            reasons.append(f"Aligns with your interest in {', '.join(matches[:2])}")
        
        if insights.get("verified_achievements", 0) > 0:
            reasons.append(f"{insights['verified_achievements']} verified achievements")
        
        strengths = insights.get("key_strengths", [])
        if strengths:
            reasons.append(f"Known for {strengths[0]}")
        
        if not reasons:
            reasons.append("Candidate profile matches your criteria")
        
        return ". ".join(reasons) + "."
