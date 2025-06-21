#!/usr/bin/env python3
"""Minimal SerpAPI test for hackathon"""

import asyncio
import os
from datetime import date
from app.flights.serpapi_adapter import SerpApiAdapter
from app.models.travel_models import FlightSearchRequest, BudgetLevel


async def test_serpapi():
    """Test SerpAPI"""
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("❌ No SERPAPI_KEY found")
        print("💡 Get free key: https://serpapi.com/")
        return
    
    request = FlightSearchRequest(
        origin="JFK",
        destination="LAX", 
        departure_date=date(2024, 6, 15),
        num_travelers=2,
        budget=BudgetLevel.MEDIUM,
        accessibility_requirements=True
    )
    
    adapter = SerpApiAdapter()
    
    try:
        flights = await adapter.search_flights(request)
        print(f"✅ Found {len(flights)} flights")
        
        for i, flight in enumerate(flights[:3], 1):
            print(f"{i}. {flight['airline']} - ${flight['price']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_serpapi()) 