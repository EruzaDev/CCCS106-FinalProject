# Emerging Technology Explanation

## Overview

HonestBallot integrates **AI-Assisted Decision Making** as its emerging technology component. This document explains the technology choice, implementation approach, integration details, and known limitations.

## Why AI-Assisted Decision Making?

### Problem Context
Voters face information overload when evaluating candidates:
- Multiple candidates with varying platforms
- Complex policy positions across many issues
- Limited time to research each candidate thoroughly
- Difficulty matching personal priorities to candidate positions

### Solution Approach
We implemented a **Rule-Based AI System** that provides:
1. **Automated candidate analysis** - Extract themes and assess sentiment from biographies
2. **Personalized matching** - Calculate compatibility between voter preferences and candidates
3. **Smart recommendations** - Suggest candidates aligned with voter priorities
4. **Insight generation** - Provide quick summaries of candidate strengths

## Technology Choice: Rule-Based AI vs Machine Learning

### Why Rule-Based AI?

| Aspect | Rule-Based AI (Chosen) | Machine Learning |
|--------|------------------------|------------------|
| **Transparency** | ✅ Decisions are explainable | ❌ Often "black box" |
| **Data Requirements** | ✅ No training data needed | ❌ Requires large datasets |
| **Implementation Time** | ✅ Fast to develop | ❌ Longer development cycle |
| **Accuracy Control** | ✅ Deterministic, predictable | ❌ Probabilistic outputs |
| **Maintenance** | ✅ Easy to update rules | ❌ Requires retraining |
| **Electoral Context** | ✅ Auditable decisions | ❌ Harder to verify |

For an electoral application where **transparency and auditability** are paramount, rule-based AI provides the best balance of functionality and trust.

## Implementation Details

### 1. Theme Extraction

**Purpose**: Identify policy focus areas from candidate biographies

**Approach**: Keyword matching against predefined policy dictionaries

```python
POLICY_KEYWORDS = {
    "education": ["education", "school", "university", "student", ...],
    "healthcare": ["health", "hospital", "medicine", "medical", ...],
    "economy": ["economy", "jobs", "business", "employment", ...],
    "environment": ["environment", "climate", "pollution", "green", ...],
    ...
}
```

**How It Works**:
1. Convert biography text to lowercase
2. Scan for keywords from each policy category
3. Return list of identified themes

**Example**:
```
Input: "Dedicated to education reform and student scholarships"
Output: ["education"]
```

### 2. Sentiment Analysis

**Purpose**: Assess overall positivity/negativity of candidate profile

**Approach**: Lexicon-based sentiment scoring

```python
POSITIVE_WORDS = ["success", "achieved", "improved", "dedicated", ...]
NEGATIVE_WORDS = ["scandal", "failed", "corrupt", "allegations", ...]
```

**How It Works**:
1. Count positive and negative word occurrences
2. Calculate net sentiment score (-1.0 to +1.0)
3. Normalize by total sentiment words found

**Example**:
```
Input: "Achieved major reforms but faced allegations"
Positive: 2 ("Achieved", "reforms")
Negative: 1 ("allegations")
Score: (2-1)/(2+1) = 0.33 (slightly positive)
```

### 3. Compatibility Scoring

**Purpose**: Match voter preferences to candidate positions

**Approach**: Theme overlap calculation

**How It Works**:
1. Extract themes from candidate biography
2. Compare with voter's selected preferences
3. Calculate percentage match
4. Return score (0-100) and matching areas

**Example**:
```
Voter Preferences: ["education", "healthcare"]
Candidate Themes: ["education", "economy", "infrastructure"]
Matching Areas: ["education"]
Score: 1/2 * 100 = 50%
```

### 4. Experience Assessment

**Purpose**: Categorize candidate experience level

**Approach**: Keyword-based classification

| Category | Trigger Keywords |
|----------|-----------------|
| High | "decade", "years of experience", "veteran", "senior" |
| Medium | "experience", "served", "worked" |
| Emerging | "fresh", "new", "young" |
| Unknown | (default) |

### 5. Strength Identification

**Purpose**: Identify candidate's key strengths

**Approach**: Pattern matching for strength indicators

| Strength | Trigger Keywords |
|----------|-----------------|
| Leadership | "led", "leader", "headed", "managed" |
| Reform | "reform", "change", "transform", "improve" |
| Community Focus | "community", "grassroots", "local" |
| Technical | "expert", "specialist", "technical" |

## Integration Points

### Analytics Dashboard
The AI service powers the Analytics page:
- **Top Candidates** section with AI-generated summaries
- **Compatibility scores** displayed for each candidate
- **Theme visualization** showing policy focus areas

### Candidate Cards
AI insights appear on candidate profile cards:
- Identified policy themes
- Sentiment indicator
- Experience level badge

### Recommendation Engine
Voters can get personalized recommendations:
1. Select policy areas of interest
2. AI calculates compatibility for all candidates
3. Results sorted by match percentage
4. Top recommendations displayed with explanations

## Limitations

### Current Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **English Only** | Filipino text not analyzed | Future: Add Filipino keyword dictionary |
| **Keyword Dependent** | Misses context/nuance | Use comprehensive keyword lists |
| **No Learning** | Can't improve from data | Manually update rules based on feedback |
| **Biography Dependent** | Requires text content | Encourage complete profiles |
| **No Fact-Checking** | Assumes text is accurate | Pair with NBI verification |

### What It Cannot Do

1. **Verify claims** - AI doesn't check if statements are true
2. **Predict behavior** - Past analysis ≠ future actions
3. **Understand sarcasm** - Literal interpretation only
4. **Read images/videos** - Text-based analysis only
5. **Replace human judgment** - Aids, not replaces, voter decisions

## Future Enhancements

### Phase 2 Improvements
- Filipino language support
- Expanded keyword dictionaries
- Synonym recognition

### Phase 3: Machine Learning Integration
- Train models on voter feedback
- Collaborative filtering recommendations
- Natural Language Processing (NLP) with transformers

## Ethical Considerations

### Bias Mitigation
- Keyword dictionaries reviewed for political neutrality
- No party-based scoring adjustments
- Equal treatment of all candidates

### Transparency
- All scoring algorithms are explainable
- Users can see why recommendations were made
- Open-source codebase for audit

### User Autonomy
- Recommendations are suggestions, not directives
- Users can browse all candidates freely
- Final voting decision always with the user

---

*Document Version: 1.0*  
*Last Updated: December 2025*
