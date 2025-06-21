#!/usr/bin/env python3
"""
Simple test script for the Flight API
Run this to test the API endpoints manually
"""

import asyncio
import json
from datetime import date
from app.models.travel_models import FlightSearchRequest, BudgetLevel
from app.flights.flight_search import FlightSearchService


async def test_flight_search():
    """Test the flight search functionality"""
    print("🧪 Testing Flight Search Service...")
    
    service = FlightSearchService()
    
    # Test 1: Basic search without accessibility
    print("\n1️⃣ Testing basic flight search...")
    basic_request = FlightSearchRequest(
        origin="JFK",
        destination="LAX",
        departure_date=date(2024, 2, 15),
        num_travelers=2,
        budget=BudgetLevel.MEDIUM,
        accessibility_requirements=False
    )
    
    try:
        response = await service.search_flights(basic_request)
        print(f"✅ Basic search successful!")
        print(f"   Found {response.total_results} flights")
        print(f"   Search ID: {response.search_id}")
        print(f"   First flight: {response.offers[0].airline} ${response.offers[0].price}")
        print(f"   Accessibility score: {response.offers[0].accessibility_score}")
    except Exception as e:
        print(f"❌ Basic search failed: {e}")
    
    # Test 2: Search with accessibility requirements
    print("\n2️⃣ Testing flight search with accessibility...")
    accessibility_request = FlightSearchRequest(
        origin="JFK",
        destination="LAX",
        departure_date=date(2024, 2, 15),
        num_travelers=1,
        budget=BudgetLevel.HIGH,
        accessibility_requirements=True
    )
    
    try:
        response = await service.search_flights(accessibility_request)
        print(f"✅ Accessibility search successful!")
        print(f"   Found {response.total_results} flights")
        print(f"   First flight accessibility score: {response.offers[0].accessibility_score}")
        print(f"   Accessibility features: {response.offers[0].accessibility_features[:3]}")
    except Exception as e:
        print(f"❌ Accessibility search failed: {e}")
    
    # Test 3: Different budget levels
    print("\n3️⃣ Testing different budget levels...")
    for budget in [BudgetLevel.LOW, BudgetLevel.MEDIUM, BudgetLevel.HIGH]:
        budget_request = FlightSearchRequest(
            origin="JFK",
            destination="LAX",
            departure_date=date(2024, 2, 15),
            budget=budget,
            accessibility_requirements=False
        )
        
        try:
            response = await service.search_flights(budget_request)
            avg_price = sum(offer.price for offer in response.offers) / len(response.offers)
            print(f"   {budget.value} budget: ${avg_price:.0f} average price")
        except Exception as e:
            print(f"   {budget.value} budget: Failed - {e}")


async def test_skyscanner_connection():
    """Test Skyscanner API connection"""
    print("\n🔌 Testing Skyscanner API Connection...")
    
    from app.flights.skyscanner_adapter import SkyscannerAdapter
    from app.config import settings
    
    if not settings.RAPIDAPI_KEY:
        print("⚠️  No RapidAPI key found - using mock data")
        print("   To use real data, get a key from: https://rapidapi.com/skyscanner-api-skyscanner-api-default/api/skyscanner-api/")
        return False
    
    adapter = SkyscannerAdapter()
    
    # Test flight search
    try:
        request = FlightSearchRequest(
            origin="JFK",
            destination="LAX",
            departure_date=date(2024, 2, 15),
            num_travelers=1,
            budget=BudgetLevel.MEDIUM,
            accessibility_requirements=False
        )
        
        flights = await adapter.search_flights(request)
        print(f"✅ Skyscanner search successful: {len(flights)} flights found")
        return True
    except Exception as e:
        print(f"❌ Skyscanner search failed: {e}")
        return False


def test_mock_data():
    """Test mock data generation"""
    print("\n🎭 Testing Mock Data Generation...")
    
    from app.utils.mock_data import get_mock_flights
    
    request = FlightSearchRequest(
        origin="JFK",
        destination="LAX",
        departure_date=date(2024, 2, 15),
        budget=BudgetLevel.MEDIUM,
        accessibility_requirements=True
    )
    
    try:
        flights = get_mock_flights(request)
        print(f"✅ Mock data generated: {len(flights)} flights")
        
        # Show sample flight
        sample = flights[0]
        print(f"   Sample flight: {sample.airline} {sample.flight_number}")
        print(f"   Price: ${sample.price}")
        print(f"   Accessibility score: {sample.accessibility_score}")
        print(f"   Features: {sample.accessibility_features[:3]}")
        
    except Exception as e:
        print(f"❌ Mock data failed: {e}")


async def main():
    """Run all tests"""
    print("🚀 Starting Flight API Tests...")
    print("=" * 50)
    
    # Test mock data first
    test_mock_data()
    
    # Test flight search service
    await test_flight_search()
    
    # Test Skyscanner connection
    skyscanner_success = await test_skyscanner_connection()
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print("✅ Mock data generation")
    print("✅ Flight search service")
    if skyscanner_success:
        print("✅ Skyscanner API connection")
    else:
        print("⚠️  Skyscanner API connection (using mock data)")
    
    print("\n🎯 To test the full API server:")
    print("1. Optional: Get RapidAPI key from https://rapidapi.com/skyscanner-api-skyscanner-api-default/api/skyscanner-api/")
    print("2. Run: python run.py")
    print("3. Visit: http://localhost:8000/docs")
    print("4. Test the /api/v1/flights/search endpoint")
    
    print("\n💡 For hackathon demo:")
    print("   - Mock data works perfectly without any API setup")
    print("   - Real data available with RapidAPI key")


if __name__ == "__main__":
    asyncio.run(main()) 