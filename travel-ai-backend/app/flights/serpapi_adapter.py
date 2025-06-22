import aiohttp
from typing import Dict, Any, List
from app.models.travel_models import FlightSearchRequest
from app.config import settings
import pandas as pd


class SerpApiAdapter:
    """Minimal SerpAPI adapter for hackathon"""
    
    def __init__(self):
        self.api_key = settings.SERPAPI_KEY
    
    async def search_flights(self, request: FlightSearchRequest) -> List[Dict[str, Any]]:
        """Search flights via SerpAPI (always round trip)"""
        if not self.api_key:
            raise Exception("No SerpAPI key")
        
        params = {
            "api_key": self.api_key,
            "engine": "google_flights",
            "hl": "en",
            "gl": "us",
            "currency": "USD",
            "departure_id": request.origin,
            "arrival_id": request.destination,
            "outbound_date": request.departure_date.strftime("%Y-%m-%d"),
            "return_date": request.return_date.strftime("%Y-%m-%d"),
            "adults": str(request.num_travelers),
            "type": "1"  # Always round trip
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get("https://serpapi.com/search", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._extract_flights(data)
                else:
                    error_text = await response.text()
                    raise Exception(f"SerpAPI error: {response.status} - {error_text}")
    
    def _extract_flights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract flight data from SerpAPI response"""
        flights = []
        
        # SerpAPI returns best_flights and other_flights
        best_flights = data.get("best_flights", [])
        other_flights = data.get("other_flights", [])
        
        # Process best flights first
        for flight_group in best_flights:
            if "flights" in flight_group:
                for flight in flight_group["flights"]:
                    try:
                        flights.append({
                            "id": flight.get("flight_number", ""),
                            "airline": flight.get("airline", "Unknown"),
                            "price": self._extract_price(str(flight_group.get("price", "0"))),
                            "departure": {
                                "at": flight.get("departure_airport", {}).get("time", ""),
                                "iataCode": flight.get("departure_airport", {}).get("id", "")
                            },
                            "arrival": {
                                "at": flight.get("arrival_airport", {}).get("time", ""),
                                "iataCode": flight.get("arrival_airport", {}).get("id", "")
                            },
                            "duration": flight.get("duration", 0),
                            "stops": 0  # best_flights are typically direct
                        })
                    except:
                        continue
        
        # Process other flights
        for flight_group in other_flights:
            if "flights" in flight_group:
                for flight in flight_group["flights"]:
                    try:
                        flights.append({
                            "id": flight.get("flight_number", ""),
                            "airline": flight.get("airline", "Unknown"),
                            "price": self._extract_price(str(flight_group.get("price", "0"))),
                            "departure": {
                                "at": flight.get("departure_airport", {}).get("time", ""),
                                "iataCode": flight.get("departure_airport", {}).get("id", "")
                            },
                            "arrival": {
                                "at": flight.get("arrival_airport", {}).get("time", ""),
                                "iataCode": flight.get("arrival_airport", {}).get("id", "")
                            },
                            "duration": flight.get("duration", 0),
                            "stops": 0  # other_flights are typically direct
                        })
                    except:
                        continue
        
        return flights
    
    def _extract_price(self, price_str: str) -> float:
        """Extract price"""
        try:
            return float(price_str.replace("$", "").replace(",", ""))
        except:
            return 0.0
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse duration to minutes, supports '5h 30m', '2h', '45m', etc."""
        try:
            parts = duration_str.split()
            hours = 0
            minutes = 0
            for part in parts:
                if 'h' in part:
                    hours = int(part.replace('h', ''))
                elif 'm' in part:
                    minutes = int(part.replace('m', ''))
            return hours * 60 + minutes
        except:
            return 0
    
    async def get_airport_code(self, city_name: str) -> str:
        """Get airport code for a city"""
        airports = {
            pd.read_csv('airport_codes.csv')['city'].str.lower(): pd.read_csv('airport_codes.csv')['iata_code'].str.upper()
        }
        
        return airports.get(city_name.lower(), city_name.upper()) 