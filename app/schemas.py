from pydantic import BaseModel, Field
from typing import List, Optional

class ScoreReasoning(BaseModel):
    positive_points: List[str] = Field(
        description="List of specific things done well, referencing photos with quick descriptions (not just number) if applicable"
    )
    improvement_points: List[str] = Field(
        description="List of specific (provide clear examples/ references (i.e., short description of photos, not just number) improvement suggestions, providing actionable and clear examples, referencing photos with quick descriptions (not just number)if applicable"
    )
    score: int = Field(description="Score for this category (0-100)")

    class Config:
        extra = "forbid"

class CategoryScore(BaseModel):
    score: int = Field(description="Current score for the category (0-100)")
    potential_score: int = Field(description="Potential score if improvements are made (0-100)")
    reasoning: ScoreReasoning = Field(description="Detailed reasoning for the score")

    class Config:
        extra = "forbid"

class RedFlag(BaseModel):
    category: str = Field(description="Category the red flag belongs to")
    description: str = Field(description="Detailed description of the red flag, referencing photos with quick descriptions if applicable")
    quick_fix: Optional[str] = Field(description="Specific, actionable quick solution if available")

    class Config:
        extra = "forbid"

class ImprovementAction(BaseModel):
    category: str = Field(description="Category this improvement belongs to")
    action: str = Field(description="Specific, simple, and actionable step to take")
    priority: int = Field(description="Priority level (1-5)")
    reasoning: str = Field(description="Clear explanation of why this improvement matters, including benefits")

    class Config:
        extra = "forbid"


class ProfileAnalysis(BaseModel):
    overall_score: int = Field(description="Current overall profile score (0-100)")
    potential_score: int = Field(description="Potential overall score after improvements (0-100)")
    
    photo_quality: CategoryScore = Field(description="Photo quality analysis")
    no_catfish: CategoryScore = Field(description="No catfish score analysis")
    vibe: CategoryScore = Field(description="Vibe score analysis")
    lifestyle: CategoryScore = Field(description="Lifestyle score analysis")
    social_proof: CategoryScore = Field(description="Social proof score analysis")
    
    red_flags: List[RedFlag] = Field(description="List of detected red flags")
    improvement_actions: List[ImprovementAction] = Field(description="Prioritized improvement actions to improve the overall profile (stand out criteria or profile completeness could be relevant additionally to the improvement actions per category)")

    class Config:
        extra = "forbid"
