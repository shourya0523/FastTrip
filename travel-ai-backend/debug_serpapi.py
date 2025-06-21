#!/usr/bin/env python3
"""
Debug script to test SerpAPI integration
"""

import asyncio
from datetime import date
from app.flights.serpapi_adapter import SerpApiAdapter
from app.models.travel_models import FlightSearchRequest
from app.config import settings

async def test_serpapi():
    """Test SerpAPI integration"""
    print(f"SerpAPI Key: {settings.SERPAPI_KEY[:10]}...")
    print(f"Use Mock Data: {settings.USE_MOCK_DATA}")
    
    adapter = SerpApiAdapter()
    req = FlightSearchRequest(
        origin='JFK',
        destination='LAX', 
        departure_date=date(2025, 7, 15),
        return_date=date(2025, 7, 22),
        budget='medium'
    )
    
    try:
        print("Calling SerpAPI...")
        flights = await adapter.search_flights(req)
        print(f"✅ SerpAPI returned {len(flights)} flights")
        if flights:
            print(f"First flight: {flights[0]}")
    except Exception as e:
        print(f"❌ SerpAPI error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_serpapi()) 