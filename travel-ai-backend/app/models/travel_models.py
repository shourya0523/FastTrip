from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from enum import Enum
from app.models.session_models import BudgetLevel

class BudgetLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    departure_date: date
    return_date: date
    num_travelers: int = 1
    budget: BudgetLevel = BudgetLevel.MEDIUM
    accessibility_requirements: bool = False

class FlightOffer(BaseModel):
    flight_id: str
    airline: str
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    price: float
    currency: str = "USD"
    accessibility_score: float  # 0-10 scale
    accessibility_features: List[str]
    is_direct: bool
    stops: int
    aircraft_type: Optional[str] = None

class FlightSearchResponse(BaseModel):
    search_id: str
    offers: List[FlightOffer]
    total_results: int
    search_summary: dict