"""
Pydantic models for product review analysis
"""
from pydantic import BaseModel, Field, validator
from typing import List


class ReviewAnalysis(BaseModel):
    """
    Pydantic model for structured product review analysis
    
    Attributes:
        sentiment: Overall sentiment of the review (positive, negative, neutral)
        rating: Numeric rating from 1-5
        key_features: List of key product features mentioned
        improvement_suggestions: List of suggested improvements
    """
    sentiment: str = Field(
        ..., 
        description="Overall sentiment of the review: positive, negative, or neutral"
    )
    rating: int = Field(
        ..., 
        ge=1, 
        le=5,
        description="Numeric rating from 1 to 5"
    )
    key_features: List[str] = Field(
        default_factory=list,
        description="List of key product features mentioned in the review"
    )
    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="List of suggested improvements for the product"
    )
    
    @validator('sentiment')
    def validate_sentiment(cls, v):
        """Validate that sentiment is one of the allowed values"""
        valid_sentiments = ['positive', 'negative', 'neutral']
        if v.lower() not in valid_sentiments:
            raise ValueError(f'Sentiment must be one of {valid_sentiments}')
        return v.lower()
    
    @validator('key_features', 'improvement_suggestions', pre=True, always=True)
    def ensure_list(cls, v):
        """Ensure fields are lists"""
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        if isinstance(v, list):
            return v
        return [str(v)]
    
    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "sentiment": "positive",
                "rating": 4,
                "key_features": ["excellent quality", "fast delivery"],
                "improvement_suggestions": ["better packaging"]
            }
        }
