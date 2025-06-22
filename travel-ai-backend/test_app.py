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
        "origin": "San Francisco",
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

def test_chat_endpoint(client, monkeypatch):
    """
    Tests the chat endpoint, ensuring it handles session state and returns the correct response format.
    """
    # Mock the call_gemini_update_state function to return a predictable response
    def mock_update_state(state, message, history):
        # Simulate extracting one piece of information and asking the next question
        updated_state = state.copy()
        updated_state["destination"] = "New York"
        return updated_state, ["dates_of_travel"], "When would you like to travel?"

    monkeypatch.setattr("app.api.chat_routes.call_gemini_update_state", mock_update_state)

    # First request (no session_id)
    initial_request = {"message": "I want to go to New York"}
    response = client.post("/api/v1/chat/chat", json=initial_request)

    # Assertions for the first response
    assert response.status_code == 200
    data = response.json()
    assert data["extracted_params"]["destination"] == "New York"
    assert data["follow_up_questions"] == ["When would you like to travel?"]
    assert "session_id" in data
    session_id = data["session_id"]

    # Second request (with session_id)
    second_request = {"message": "Next week", "session_id": session_id}
    response = client.post("/api/v1/chat/chat", json=second_request)

    # Assertions for the second response
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id  # Ensure session is maintained

def test_chat_endpoint_flight_parameter_extraction(client, monkeypatch):
    """
    Tests that the chat endpoint extracts flight parameters when conversation is complete.
    """
    # Mock the call_gemini_update_state function to simulate a complete conversation
    def mock_update_state_complete(state, message, history):
        # Simulate a complete conversation with all required fields filled
        complete_state = {
            "budget": "mid-range",
            "starting_location": "San Francisco",
            "destination": "New York",
            "accessibility_needs": "None",
            "dietary_needs": "No restrictions",
            "age_group_of_travelers": "Adults",
            "interests": ["Museums", "Food"],
            "how_packed_trip": "Moderate",
            "ok_with_walking": True,
            "dates_of_travel": {"start_date": "2024-06-15", "end_date": "2024-06-22"},
            "trip_type": "Leisure",
            "number_of_travelers": 2
        }
        return complete_state, [], ""  # Empty next_question indicates completion

    # Mock the extract_flight_parameters_from_state function
    def mock_extract_flight_params(state):
        return {
            "origin": "San Francisco",
            "destination": "New York",
            "departure_date": "2024-06-15",
            "return_date": "2024-06-22",
            "num_travelers": 2,
            "budget": "medium",
            "accessibility_requirements": False
        }

    monkeypatch.setattr("app.api.chat_routes.call_gemini_update_state", mock_update_state_complete)
    monkeypatch.setattr("app.api.chat_routes.extract_flight_parameters_from_state", mock_extract_flight_params)

    # Send a message that completes the conversation
    request = {"message": "That sounds perfect, I'm ready to book!"}
    response = client.post("/api/v1/chat/chat", json=request)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    # Check that conversation is marked as complete
    assert data["conversation_complete"] is True
    assert data["follow_up_questions"] == []
    
    # Check that flight parameters are extracted and returned
    assert "flight_parameters" in data
    assert data["flight_parameters"] is not None
    
    flight_params = data["flight_parameters"]
    assert flight_params["origin"] == "San Francisco"
    assert flight_params["destination"] == "New York"
    assert flight_params["departure_date"] == "2024-06-15"
    assert flight_params["return_date"] == "2024-06-22"
    assert flight_params["num_travelers"] == 2
    assert flight_params["budget"] == "medium"
    assert flight_params["accessibility_requirements"] is False

def test_chat_endpoint_incomplete_conversation_no_flight_params(client, monkeypatch):
    """
    Tests that flight parameters are NOT extracted when conversation is incomplete.
    """
    # Mock incomplete conversation
    def mock_update_state_incomplete(state, message, history):
        updated_state = state.copy()
        updated_state["destination"] = "Paris"
        return updated_state, ["dates_of_travel", "budget"], "When would you like to travel and what's your budget?"

    monkeypatch.setattr("app.api.chat_routes.call_gemini_update_state", mock_update_state_incomplete)

    request = {"message": "I want to visit Paris"}
    response = client.post("/api/v1/chat/chat", json=request)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    # Check that conversation is NOT complete
    assert data["conversation_complete"] is False
    assert len(data["follow_up_questions"]) > 0
    
    # Check that flight parameters are NOT extracted
    assert data["flight_parameters"] is None

def test_chat_endpoint_flight_parameter_extraction_error_handling(client, monkeypatch):
    """
    Tests error handling when flight parameter extraction fails.
    """
    # Mock complete conversation
    def mock_update_state_complete(state, message, history):
        complete_state = {
            "budget": "luxury",
            "starting_location": "Los Angeles",
            "destination": "Tokyo",
            "accessibility_needs": "Wheelchair accessible",
            "dietary_needs": "Vegetarian",
            "age_group_of_travelers": "Adults",
            "interests": ["Culture", "Technology"],
            "how_packed_trip": "Busy",
            "ok_with_walking": False,
            "dates_of_travel": {"start_date": "2024-08-10", "end_date": "2024-08-20"},
            "trip_type": "Cultural",
            "number_of_travelers": 1
        }
        return complete_state, [], ""  # Empty next_question indicates completion

    # Mock extraction function that returns None (simulating failure)
    def mock_extract_flight_params_failure(state):
        return None

    monkeypatch.setattr("app.api.chat_routes.call_gemini_update_state", mock_update_state_complete)
    monkeypatch.setattr("app.api.chat_routes.extract_flight_parameters_from_state", mock_extract_flight_params_failure)

    request = {"message": "Perfect, let's proceed!"}
    response = client.post("/api/v1/chat/chat", json=request)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    # Check that conversation is complete but flight parameters are None due to extraction failure
    assert data["conversation_complete"] is True
    assert data["flight_parameters"] is None

def test_session_stores_flight_parameters(client, monkeypatch):
    """
    Tests that flight parameters are stored in the session when extracted.
    """
    # Mock complete conversation and extraction
    def mock_update_state_complete(state, message, history):
        complete_state = {
            "budget": "economy",
            "starting_location": "Chicago",
            "destination": "Miami",
            "accessibility_needs": "None",
            "dietary_needs": "No restrictions",
            "age_group_of_travelers": "Young Adults",
            "interests": ["Beach", "Nightlife"],
            "how_packed_trip": "Relaxed",
            "ok_with_walking": True,
            "dates_of_travel": {"start_date": "2024-07-01", "end_date": "2024-07-07"},
            "trip_type": "Leisure",
            "number_of_travelers": 3
        }
        return complete_state, [], ""

    def mock_extract_flight_params(state):
        return {
            "origin": "Chicago",
            "destination": "Miami",
            "departure_date": "2024-07-01",
            "return_date": "2024-07-07",
            "num_travelers": 3,
            "budget": "low",
            "accessibility_requirements": False
        }

    # Mock session management to capture stored data
    stored_sessions = {}
    
    def mock_get_session(session_id):
        return stored_sessions.get(session_id)
    
    def mock_update_session(session, session_id=None):
        if session_id is None:
            session_id = "test_session_123"
        stored_sessions[session_id] = session
        return session_id

    monkeypatch.setattr("app.api.chat_routes.call_gemini_update_state", mock_update_state_complete)
    monkeypatch.setattr("app.api.chat_routes.extract_flight_parameters_from_state", mock_extract_flight_params)
    monkeypatch.setattr("app.api.chat_routes.get_session", mock_get_session)
    monkeypatch.setattr("app.api.chat_routes.update_session", mock_update_session)

    request = {"message": "All set, let's find flights!"}
    response = client.post("/api/v1/chat/chat", json=request)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    # Check response
    assert data["conversation_complete"] is True
    assert data["flight_parameters"] is not None
    
    # Check that session contains flight parameters
    session_id = data["session_id"]
    stored_session = stored_sessions[session_id]
    assert "flight_parameters" in stored_session
    assert stored_session["flight_parameters"]["origin"] == "Chicago"
    assert stored_session["flight_parameters"]["destination"] == "Miami"
    assert stored_session["conversation_complete"] is True