#!/usr/bin/env python3
"""Integration test for SerpAPI with FastAPI"""

import os
import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta

from app.main import app

client = TestClient(app)


def test_flight_search_with_serpapi():
    """Test flight search endpoint with real SerpAPI"""
    
    # Check if SerpAPI key is available
    if not os.getenv("SERPAPI_KEY"):
        pytest.skip("No SERPAPI_KEY found - skipping real API test")
    
    # Test request
    request_data = {
        "origin": "JFK",
        "destination": "LAX",
        "departure_date": "2024-06-15",
        "return_date": "2024-06-22",
        "num_travelers": 2,
        "budget": "medium",
        "accessibility_requirements": True
    }
    
    response = client.post("/api/v1/flights/search", json=request_data)
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure
    assert "search_id" in data
    assert "offers" in data
    assert "total_results" in data
    assert "search_summary" in data
    
    # Verify offers
    offers = data["offers"]
    assert len(offers) > 0
    
    # Check first offer structure
    first_offer = offers[0]
    assert "flight_id" in first_offer
    assert "airline" in first_offer
    assert "price" in first_offer
    assert "accessibility_score" in first_offer
    
    print(f"✅ Found {len(offers)} flights from SerpAPI")
    print(f"📊 First flight: {first_offer['airline']} - ${first_offer['price']}")


def test_airport_search():
    """Test airport search endpoint"""
    response = client.get("/api/v1/flights/airports/JFK")
    assert response.status_code == 200
    
    data = response.json()
    assert "airports" in data
    assert len(data["airports"]) > 0


if __name__ == "__main__":
    # Run integration test
    if os.getenv("SERPAPI_KEY"):
        print("🔑 Testing with real SerpAPI...")
        test_flight_search_with_serpapi()
    else:
        print("❌ No SERPAPI_KEY found")
        print("💡 Set with: export SERPAPI_KEY='your_key_here'") 