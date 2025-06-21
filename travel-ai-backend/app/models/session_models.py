"""
Session and user preference models for hackathon
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel


class BudgetLevel(str, Enum):
    """Budget levels for travel planning"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UserPreferences(BaseModel):
    """User preferences for travel planning"""
    budget_level: BudgetLevel = BudgetLevel.MEDIUM
    accessibility_required: bool = False
    preferred_airlines: Optional[list[str]] = None
    max_layovers: int = 2
    preferred_departure_times: Optional[list[str]] = None


class SessionData(BaseModel):
    """Session data for user"""
    session_id: str
    user_preferences: Optional[UserPreferences] = None
    search_history: list[Dict[str, Any]] = []
    current_search: Optional[Dict[str, Any]] = None
