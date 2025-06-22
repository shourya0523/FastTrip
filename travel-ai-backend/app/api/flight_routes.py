from fastapi import APIRouter, HTTPException
from typing import List
from app.models.travel_models import FlightSearchRequest, FlightSearchResponse
from app.flights.flight_search import FlightSearchService
from app.utils.session_manager import get_session
from app.conversational_bot import extract_flight_parameters_from_state
from datetime import datetime, date

router = APIRouter()


@router.post("/search", response_model=FlightSearchResponse)
async def search_flights(request: FlightSearchRequest):
    """
    Search for flights with accessibility considerations
    """
    try:
        service = FlightSearchService()
        response = await service.search_flights(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flight search failed: {str(e)}")


@router.get("/airports/{query}")
async def search_airports(query: str):
    """
    Search for airports by name or code
    """
    airports = [
        {"code": "JFK", "name": "John F. Kennedy International Airport", "city": "New York"},
        {"code": "LAX", "name": "Los Angeles International Airport", "city": "Los Angeles"},
        {"code": "ORD", "name": "O'Hare International Airport", "city": "Chicago"},
        {"code": "ATL", "name": "Hartsfield-Jackson Atlanta International Airport", "city": "Atlanta"},
        {"code": "DFW", "name": "Dallas/Fort Worth International Airport", "city": "Dallas"},
        {"code": "DEN", "name": "Denver International Airport", "city": "Denver"},
        {"code": "SFO", "name": "San Francisco International Airport", "city": "San Francisco"},
        {"code": "LAS", "name": "McCarran International Airport", "city": "Las Vegas"},
        {"code": "MCO", "name": "Orlando International Airport", "city": "Orlando"},
        {"code": "CLT", "name": "Charlotte Douglas International Airport", "city": "Charlotte"},
    ]
    
    # Filter by query
    filtered = [airport for airport in airports 
                if query.upper() in airport["code"] or query.lower() in airport["name"].lower()]
    
    return {"airports": filtered}


@router.get("/auto-search/{session_id}", response_model=FlightSearchResponse)
async def auto_search_flights(session_id: str):
    """
    Automatically search for the best flights based on completed conversation
    """
    print(f"[DEBUG] Auto-search called for session: {session_id}")
    
    # Get session data
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    print(f"[DEBUG] Session data: {json.dumps(session, indent=2, default=str)}")
    
    # Check if conversation is complete
    if not session.get("conversation_complete", False):
        raise HTTPException(status_code=400, detail="Conversation not yet complete. Please finish the chat first.")
    
    # Get or extract flight parameters
    flight_params = session.get("flight_parameters")
    print(f"[DEBUG] Cached flight_parameters: {flight_params}")
    
    if not flight_params:
        # Try to extract from current state
        state = session.get("state", {})
        print(f"[DEBUG] Extracting from state: {json.dumps(state, indent=2)}")
        flight_params = extract_flight_parameters_from_state(state)
        print(f"[DEBUG] Extracted flight_parameters: {flight_params}")
        
        if not flight_params or "error" in flight_params:
            raise HTTPException(status_code=400, detail=f"Unable to extract flight parameters from conversation. Got: {flight_params}")
    
    try:
        # Convert conversation data to FlightSearchRequest
        search_request = FlightSearchRequest(
            origin=flight_params.get("origin", flight_params.get("starting_location", "")),
            destination=flight_params.get("destination", ""),
            departure_date=datetime.strptime(flight_params.get("departure_date", ""), "%Y-%m-%d").date() if flight_params.get("departure_date") else date.today(),
            return_date=datetime.strptime(flight_params.get("return_date", ""), "%Y-%m-%d").date() if flight_params.get("return_date") else date.today(),
            num_travelers=flight_params.get("num_travelers", 1),
            budget=flight_params.get("budget", "medium"),
            accessibility_requirements=flight_params.get("accessibility_requirements", False)
        )
        
        print(f"[DEBUG] FlightSearchRequest: {search_request.dict()}")
        
        # Use existing flight search service
        service = FlightSearchService()
        response = await service.search_flights(search_request)
        
        print(f"[DEBUG] Flight search response: Found {len(response.offers)} flights")
        
        # Store search results in session for future reference
        session["last_flight_search"] = {
            "search_request": search_request.dict(),
            "search_results": response.dict(),
            "search_timestamp": datetime.now().isoformat()
        }
        
        return response
        
    except Exception as e:
        print(f"[DEBUG] Auto flight search error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Auto flight search failed: {str(e)}")