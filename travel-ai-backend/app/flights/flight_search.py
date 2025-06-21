import uuid
from typing import List
from datetime import datetime

from app.models.travel_models import FlightSearchRequest, FlightSearchResponse, FlightOffer
from app.flights.serpapi_adapter import SerpApiAdapter
from app.utils.mock_data import get_mock_flights
from app.config import settings


class FlightSearchService:
    """Minimal flight search for hackathon"""
    
    def __init__(self):
        self.serpapi = SerpApiAdapter()
    
    async def search_flights(self, request: FlightSearchRequest) -> FlightSearchResponse:
        """Search flights with fallback to mock"""
        search_id = str(uuid.uuid4())
        
        # Use mock data if no API key or configured
        if settings.USE_MOCK_DATA or not settings.SERPAPI_KEY:
            offers = get_mock_flights(request)
        else:
            try:
                raw_flights = await self.serpapi.search_flights(request)
                if not raw_flights:
                    # If SerpAPI returns no flights, use mock data as a fallback for the demo
                    offers = get_mock_flights(request)
                else:
                    offers = self._process_flights(raw_flights, request)
            except Exception as e:
                print(f"Error processing flights, falling back to mock data. Error: {e}")
                import traceback
                traceback.print_exc()
                offers = get_mock_flights(request)
        
        # Sort by accessibility then price
        offers = sorted(offers, key=lambda x: (-x.accessibility_score, x.price))
        
        # Take the top 3 best offers
        top_offers = offers[:3]

        return FlightSearchResponse(
            search_id=search_id,
            offers=top_offers,
            total_results=len(offers), # Report total flights found before slicing
            search_summary={
                "origin": request.origin,
                "destination": request.destination,
                "departure_date": request.departure_date.isoformat(),
                "num_travelers": request.num_travelers,
                "budget": request.budget.value,
                "accessibility_requirements": request.accessibility_requirements
            }
        )
    
    def _process_flights(self, raw_data: List[dict], request: FlightSearchRequest) -> List[FlightOffer]:
        """Process API data to FlightOffer objects"""
        offers = []
        
        for flight in raw_data:
            try:
                # Ensure date/time strings are valid before parsing
                dep_at = flight.get("departure", {}).get("at")
                arr_at = flight.get("arrival", {}).get("at")
                if not dep_at or not arr_at:
                    continue # Skip flight if essential time info is missing

                departure_time = datetime.strptime(dep_at, "%Y-%m-%d %H:%M")
                arrival_time = datetime.strptime(arr_at, "%Y-%m-%d %H:%M")
                
                # Simple accessibility score
                score = 7.0 if flight.get("stops", 0) == 0 else 5.0
                if request.accessibility_requirements:
                    score += 2.0
                
                offers.append(FlightOffer(
                    flight_id=flight.get("id", ""),
                    airline=flight.get("airline", "Unknown"),
                    flight_number=flight.get("id", ""), # Use the flight ID as the number
                    origin=flight["departure"]["iataCode"],
                    destination=flight["arrival"]["iataCode"],
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                    duration_minutes=flight.get("duration", 0),
                    price=flight.get("price", 0),
                    currency="USD",
                    accessibility_score=min(10.0, score),
                    accessibility_features=["Direct flight"] if flight.get("stops", 0) == 0 else [],
                    is_direct=flight.get("stops", 0) == 0,
                    stops=flight.get("stops", 0),
                    aircraft_type=None
                ))
            except (KeyError, ValueError, TypeError) as e:
                print(f"Skipping a flight due to parsing error: {e}")
                continue
        
        return offers 