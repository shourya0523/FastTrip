from typing import Optional
from app.models.travel_models import FlightSearchRequest
from app.conversational_bot import extract_flight_parameters_from_state

class TravelService:
    def __init__(self):
        self.flight_parameters_cache = {}
    
    async def process_completed_conversation(self, session_id: str, conversation_state: dict) -> Optional[FlightSearchRequest]:
        """Extract and cache flight parameters when conversation completes"""
        try:
            flight_params = await extract_flight_parameters_from_state(conversation_state)
            self.flight_parameters_cache[session_id] = {
                "parameters": flight_params,
                "status": "ready",
                "created_at": datetime.utcnow()
            }
            return flight_params
        except Exception as e:
            logger.error(f"Failed to extract flight parameters: {e}")
            return None
    
    def get_flight_parameters(self, session_id: str) -> Optional[FlightSearchRequest]:
        """Get cached flight parameters for a session"""
        cached = self.flight_parameters_cache.get(session_id)
        return cached["parameters"] if cached else None

# Global instance
travel_service = TravelService()