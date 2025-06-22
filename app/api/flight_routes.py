from app.services.travel_service import travel_service

@router.get("/search_from_session/{session_id}")
async def search_flights_from_session(session_id: str):
    """Search flights using parameters from completed conversation"""
    flight_params = travel_service.get_flight_parameters(session_id)
    
    if not flight_params:
        raise HTTPException(status_code=404, detail="No flight parameters found for session")
    
    # Use existing search logic
    return await search_flights(flight_params)