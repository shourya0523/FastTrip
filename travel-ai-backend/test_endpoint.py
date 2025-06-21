#!/usr/bin/env python3
"""
Simple test script for the FastAPI flight search endpoint
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_flight_endpoint():
    """Test the flight search endpoint"""
    
    # Test data
    test_data = {
        "origin": "JFK",
        "destination": "LAX", 
        "departure_date": "2025-07-15",
        "return_date": "2025-07-22",
        "num_travelers": 1,
        "accessibility_required": False,
        "budget_level": "medium"
    }
    
    url = "http://localhost:8000/api/flights/search"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=test_data) as response:
                print(f"Status Code: {response.status}")
                print(f"Response Headers: {dict(response.headers)}")
                
                if response.status == 200:
                    data = await response.json()
                    print("\n✅ SUCCESS! Real API Response:")
                    print(json.dumps(data, indent=2))
                else:
                    error_text = await response.text()
                    print(f"\n❌ ERROR {response.status}:")
                    print(error_text)
                    
    except aiohttp.ClientConnectorError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing FastAPI Flight Search Endpoint")
    print("=" * 50)
    asyncio.run(test_flight_endpoint()) 