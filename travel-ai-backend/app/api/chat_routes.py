from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime, date

from app.conversational_bot import call_gemini_update_state, INITIAL_STATE, extract_flight_parameters_from_state, is_conversation_complete
from app.utils.session_manager import get_session, update_session
from app.flights.flight_search import FlightSearchService
from app.models.travel_models import FlightSearchRequest, BudgetLevel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    extracted_params: Dict[str, Any]
    follow_up_questions: List[str]
    session_id: str
    conversation_complete: bool = False
    flight_parameters: Optional[Dict[str, Any]] = None
    flight_results: Optional[Dict[str, Any]] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to handle chat messages and update session state.
    When conversation is complete, extracts flight parameters and runs search.
    """
    session_id = request.session_id
    session = get_session(session_id)

    if not session:
        session = {"state": INITIAL_STATE.copy(), "history": []}

    state = session.get("state", INITIAL_STATE.copy())
    history = session.get("history", [])

    try:
        updated_state, missing_fields, next_question = call_gemini_update_state(
            state,
            request.message,
            history
        )

        session["state"] = updated_state
        session["history"].append(request.message)
        
        # Improved conversation completion logic
        conversation_complete = is_conversation_complete(updated_state)
        flight_parameters = None
        flight_results = None
        
        # Override next_question if conversation is complete
        if conversation_complete:
            next_question = "Perfect! I have all the information I need. Let me search for the best flights for you..."
            session["conversation_complete"] = True
            
            # Extract flight parameters when conversation is complete
            flight_parameters = extract_flight_parameters_from_state(updated_state)
            if flight_parameters and "error" not in flight_parameters:
                session["flight_parameters"] = flight_parameters
                
                # Automatically run flight search and save results
                try:
                    search_request = FlightSearchRequest(
                        origin=flight_parameters.get("origin", ""),
                        destination=flight_parameters.get("destination", ""),
                        departure_date=datetime.strptime(flight_parameters.get("departure_date", ""), "%Y-%m-%d").date() if flight_parameters.get("departure_date") else date.today(),
                        return_date=datetime.strptime(flight_parameters.get("return_date", ""), "%Y-%m-%d").date() if flight_parameters.get("return_date") else date.today(),
                        num_travelers=flight_parameters.get("num_travelers", 1),
                        budget=BudgetLevel(flight_parameters.get("budget", "medium")),
                        accessibility_requirements=flight_parameters.get("accessibility_requirements", False)
                    )
                    
                    service = FlightSearchService()
                    search_response = await service.search_flights(search_request)
                    
                    # Save flight results in session
                    flight_results = {
                        "search_id": search_response.search_id,
                        "offers": [offer.model_dump() for offer in search_response.offers],
                        "total_results": search_response.total_results,
                        "search_summary": search_response.search_summary,
                        "searched_at": datetime.now().isoformat()
                    }
                    session["flight_results"] = flight_results
                    
                    # Update the response message
                    next_question = f"Great! I found {len(search_response.offers)} excellent flight options for you. The search results have been saved and you can view them anytime."
                    
                except Exception as search_error:
                    print(f"[ERROR] Flight search failed: {search_error}")
                    next_question = "I have all your travel details, but there was an issue searching for flights. You can try the search again later."
                    
        elif not missing_fields:
            # If Gemini says no missing fields but our validation says incomplete
            # Force a question to get remaining info
            next_question = next_question or "Could you provide any additional details about your trip preferences?"

        new_session_id = update_session(session, session_id)

        return ChatResponse(
            extracted_params=updated_state,
            follow_up_questions=[next_question] if next_question else [],
            session_id=new_session_id,
            conversation_complete=conversation_complete,
            flight_parameters=flight_parameters,
            flight_results=flight_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))