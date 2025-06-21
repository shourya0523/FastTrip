from fastapi import APIRouter, HTTPException
from typing import List

from app.models.travel_models import FlightSearchRequest, FlightSearchResponse
from app.flights.flight_search import FlightSearchService

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