import aiohttp
from typing import Dict, Any, List
from app.models.travel_models import FlightSearchRequest
from app.config import settings
import pandas as pd


class SerpApiAdapter:
    """Minimal SerpAPI adapter for hackathon"""
    
    def __init__(self):
        self.api_key = settings.SERPAPI_KEY
        self._airport_mapping = None
    
    def _load_airport_mapping(self):
        """Load airport code mapping from CSV"""
        if self._airport_mapping is None:
            import os
            csv_path = os.path.join(os.path.dirname(__file__), 'airport_codes.csv')
            try:
                df = pd.read_csv(csv_path, names=['iata_code', 'city'])
                
                # Create mapping, but prioritize 3-letter IATA codes over others
                mapping = {}
                for _, row in df.iterrows():
                    city = row['city'].lower()
                    code = row['iata_code'].upper()
                    
                    # If city not in mapping, or current code is 3 letters and existing isn't
                    if (city not in mapping or 
                        (len(code) == 3 and len(mapping[city]) != 3)):
                        mapping[city] = code
                
                self._airport_mapping = mapping
            except Exception as e:
                print(f"Warning: Could not load airport mapping: {e}")
                self._airport_mapping = {}
        return self._airport_mapping

    def get_airport_code(self, city_name: str) -> str:
        """Get airport code for a city"""
        mapping = self._load_airport_mapping()
        
        # Try exact match first
        city_lower = city_name.lower().strip()
        if city_lower in mapping:
            return mapping[city_lower]
        
        # Try partial matches for cities with multiple airports
        for city, code in mapping.items():
            if city_lower in city or city in city_lower:
                return code
        
        # If no match found, return the original (might already be an airport code)
        return city_name.upper()
    
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