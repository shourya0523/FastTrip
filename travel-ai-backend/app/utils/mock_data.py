import random
from typing import List
from datetime import datetime, timedelta

from app.models.travel_models import FlightSearchRequest, FlightOffer


def get_mock_flights(request: FlightSearchRequest) -> List[FlightOffer]:
    """Generate test flight data"""
    num_flights = random.randint(5, 12)
    flights = []
    
    # Base departure time
    base_departure = datetime.combine(request.departure_date, datetime.min.time().replace(hour=8))
    
    airlines = ["American Airlines", "Delta", "United", "Southwest", "JetBlue", "Alaska Airlines"]
    aircraft_types = ["B737", "A320", "B787", "A350", "B777"]
    
    for i in range(num_flights):
        # Vary departure time
        departure_time = base_departure + timedelta(hours=random.randint(0, 14))
        
        # Duration based on route (1-8 hours)
        duration_hours = random.randint(1, 8)
        arrival_time = departure_time + timedelta(hours=duration_hours)
        
        # Price based on budget
        price = _get_price_for_budget(request.budget)
        
        # Calculate accessibility score
        accessibility_score, accessibility_features = _calculate_mock_accessibility_score(request)
        
        # Direct vs connecting (30% direct)
        is_direct = random.random() < 0.3
        stops = 0 if is_direct else random.randint(1, 2)
        
        flight = FlightOffer(
            flight_id=f"TEST_FLIGHT_{i+1}",
            airline=random.choice(airlines),
            flight_number=f"{random.randint(100, 9999)}",
            origin=request.origin,
            destination=request.destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration_minutes=duration_hours * 60,
            price=price,
            currency="USD",
            accessibility_score=accessibility_score,
            accessibility_features=accessibility_features,
            is_direct=is_direct,
            stops=stops,
            aircraft_type=random.choice(aircraft_types)
        )
        
        flights.append(flight)
    
    return flights


def _get_price_for_budget(budget: str) -> float:
    """Get price range based on budget level"""
    if budget == "low":
        return random.randint(150, 350)
    elif budget == "medium":
        return random.randint(300, 600)
    else:  # high
        return random.randint(500, 1200)


def _calculate_mock_accessibility_score(request: FlightSearchRequest) -> tuple[float, List[str]]:
    """Calculate mock accessibility score"""
    score = 5.0  # Base score
    features = []
    
    # If accessibility requirements are needed
    if request.accessibility_requirements:
        score += 2.0
        features.extend([
            "Wheelchair assistance available",
            "Special seating options",
            "Medical equipment support",
            "Service animal friendly",
            "Priority boarding"
        ])
        
        # Add some additional accessibility features randomly
        additional_features = [
            "Accessible boarding ramp",
            "Assistance with carry-on luggage",
            "Accessible lavatory",
            "Oxygen support available",
            "Visual assistance available",
            "Hearing assistance available"
        ]
        
        # Add 2-3 random additional features
        num_additional = random.randint(2, 3)
        selected_features = random.sample(additional_features, num_additional)
        features.extend(selected_features)
        score += num_additional * 0.5
    
    # Ensure score is within 0-10 range
    score = max(0.0, min(10.0, score))
    
    return score, features 