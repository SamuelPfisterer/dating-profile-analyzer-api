from pydantic import BaseModel, Field
from typing import List, Optional

class ScoreReasoning(BaseModel):
    positive_points: List[str] = Field(description="List of things done well")
    improvement_points: List[str] = Field(description="List of things that could be improved")
    score: int = Field(description="Score for this category (0-100)")

class CategoryScore(BaseModel):
    score: int = Field(description="Current score for the category (0-100)")
    potential_score: int = Field(description="Potential score if improvements are made (0-100)")
    reasoning: ScoreReasoning = Field(description="Detailed reasoning for the score")

class RedFlag(BaseModel):
    category: str = Field(description="Category the red flag belongs to")
    description: str = Field(description="Description of the red flag")
    severity: str = Field(description="Severity level: 'low', 'medium', or 'high'")
    quick_fix: Optional[str] = Field(description="Quick solution if available")

class ImprovementAction(BaseModel):
    category: str = Field(description="Category this improvement belongs to")
    action: str = Field(description="Specific action to take")
    expected_impact: int = Field(description="Expected impact score (0-100)")
    priority: int = Field(description="Priority level (1-5)")
    reasoning: str = Field(description="Why this improvement matters")

class ProfileAnalysis(BaseModel):
    overall_score: int = Field(description="Current overall profile score (0-100)")
    potential_score: int = Field(description="Potential overall score after improvements (0-100)")
    
    photo_quality: CategoryScore = Field(description="Photo quality analysis")
    no_catfish: CategoryScore = Field(description="No catfish score analysis")
    vibe: CategoryScore = Field(description="Vibe score analysis")
    lifestyle: CategoryScore = Field(description="Lifestyle score analysis")
    social_proof: CategoryScore = Field(description="Social proof score analysis")
    stand_out: CategoryScore = Field(description="Stand out score analysis")
    
    red_flags: List[RedFlag] = Field(description="List of detected red flags")
    improvement_actions: List[ImprovementAction] = Field(description="Prioritized improvement actions") 