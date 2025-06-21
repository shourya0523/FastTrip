import pytest
from fastapi.testclient import TestClient
from datetime import datetime, date
import re # Import the regular expression module

# Set the environment variable for testing before importing the app
import os
# os.environ['USE_MOCK_DATA'] = 'True'  # Commented out to ensure no backend mock data is used

from app.main import app
from app.models.travel_models import FlightSearchResponse

@pytest.fixture(scope="module")
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as c:
        yield c             

@pytest.fixture
def mock_serpapi_response():
    """Provides a realistic mock of the SerpAPI adapter's output."""
    return [
        {'id': 'UA-123', 'airline': 'United', 'price': 350.0, 'departure': {'at': '2025-09-15 09:00', 'iataCode': 'SFO'}, 'arrival': {'at': '2025-09-15 17:00', 'iataCode': 'JFK'}, 'duration': 480, 'stops': 0},
        {'id': 'AA-456', 'airline': 'American', 'price': 320.0, 'departure': {'at': '2025-09-15 10:00', 'iataCode': 'SFO'}, 'arrival': {'at': '2025-09-15 18:00', 'iataCode': 'JFK'}, 'duration': 480, 'stops': 0},
        {'id': 'DL-789', 'airline': 'Delta', 'price': 400.0, 'departure': {'at': '2025-09-15 11:00', 'iataCode': 'SFO'}, 'arrival': {'at': '2025-09-15 19:00', 'iataCode': 'JFK'}, 'duration': 480, 'stops': 1},
        {'id': 'JB-101', 'airline': 'JetBlue', 'price': 280.0, 'departure': {'at': '2025-09-15 08:00', 'iataCode': 'SFO'}, 'arrival': {'at': '2025-09-15 16:00', 'iataCode': 'JFK'}, 'duration': 480, 'stops': 0},
    ]

def test_successful_flight_search(client, monkeypatch, mock_serpapi_response):
    """
    Tests a valid flight search, ensuring data is processed, sorted, and truncated correctly.
    """
    # Mock the SerpApiAdapter to avoid real API calls
    async def mock_search(*args, **kwargs):
        return mock_serpapi_response
        
    monkeypatch.setattr("app.flights.serpapi_adapter.SerpApiAdapter.search_flights", mock_search)
    
    # Define a valid request payload
    valid_request = {
        "origin": "SFO",
        "destination": "JFK",
        "departure_date": "2025-09-15",
        "return_date": "2025-09-22",
        "num_travelers": 1,
        "accessibility_requirements": True,
        "budget": "medium"
    }

    # Make the request
    response = client.post("/api/v1/flights/search", json=valid_request)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    # Validate the response model
    assert FlightSearchResponse.model_validate(data)
    
    # Check that we got the top 3 results
    assert len(data["offers"]) == 3
    
    # Check that the total results reflects the count before truncating
    assert data["total_results"] == 4
    
    # Check sorting: higher accessibility score (direct flights) and then lower price
    # Expected order: JB-101 (9.0, $280), AA-456 (9.0, $320), UA-123 (9.0, $350)
    offer_ids = [offer['flight_id'] for offer in data['offers']]
    assert offer_ids == ["JB-101", "AA-456", "UA-123"]
    assert data['offers'][0]['price'] == 280.0
    
@pytest.mark.parametrize("invalid_payload, expected_detail_part", [
    # Missing origin: Pydantic's 'missing' type error
    ({"destination": "JFK", "departure_date": "2025-09-15", "return_date": "2025-09-22"}, 
     "'type': 'missing'.*'loc':.*'origin'"),
    # Invalid date format: Pydantic's 'date_from_datetime_parsing' error
    ({"origin": "SFO", "destination": "JFK", "departure_date": "not-a-date", "return_date": "2025-09-22"}, 
     "'type': 'date_from_datetime_parsing'.*'loc':.*'departure_date'"),
    # Invalid budget enum: Pydantic's 'enum' error
    ({"origin": "SFO", "destination": "JFK", "departure_date": "2025-09-15", "return_date": "2025-09-22", "budget": "invalid-budget"}, 
     "'type': 'enum'.*'loc':.*'budget'"),
    # Invalid num_travelers: Pydantic's 'int_parsing' error
    ({"origin": "SFO", "destination": "JFK", "departure_date": "2025-09-15", "return_date": "2025-09-22", "num_travelers": "one"}, 
     "'type': 'int_parsing'.*'loc':.*'num_travelers'"),
])
def test_flight_search_validation(client, invalid_payload, expected_detail_part):
    """
    Tests various invalid request payloads to ensure Pydantic validation is working.
    """
    response = client.post("/api/v1/flights/search", json=invalid_payload)
    
    assert response.status_code == 422
    # Use re.search to correctly handle the regex patterns for Pydantic's structured errors
    assert re.search(expected_detail_part, str(response.json()["detail"]), re.IGNORECASE) 