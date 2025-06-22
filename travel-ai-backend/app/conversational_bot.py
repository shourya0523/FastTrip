import os
import json
from dotenv import load_dotenv
from datetime import date
from app.models.travel_models import FlightSearchRequest, BudgetLevel

# Gemini setup
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

REQUIRED_FIELDS = [
    "budget", "starting_location", "destination", "accessibility_needs", "dietary_needs", 
    "age_group_of_travelers", "interests", "how_packed_trip", "ok_with_walking", 
    "dates_of_travel", "trip_type", "number_of_travelers"
]

INITIAL_STATE = {
    "budget": None,
    "starting_location": None,
    "destination": None,
    "accessibility_needs": None,
    "dietary_needs": None,
    "age_group_of_travelers": None,
    "interests": [],
    "how_packed_trip": None,
    "ok_with_walking": None,
    "dates_of_travel": {"start_date": None, "end_date": None},
    "trip_type": None,
    "number_of_travelers": None
}

# Gemini wrapper

def call_gemini_update_state(state, user_message, conversation_history=[]):
    """
    Calls Gemini to update the state JSON, return missing fields, and suggest the next question to ask.
    If Gemini is not available, uses a mock function.
    """
    # Define the schema outside the f-string to avoid formatting issues
    schema = '''
{
  "starting_location": {"type": "string", "required": true},
  "destination": {"type": "string", "required": true, ONLY VALID CITIES, ASK IF NOT VALID},
  "dates_of_travel": {
    "type": "object",
    "properties": {
      "start_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$", "required": true},
      "end_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$", "required": true}
    },
    "required": true
  },
  "number_of_travelers": {"type": "integer", "minimum": 1, "required": true, ONLY VALID CITY NAMES},
  "trip_type": {"type": "string", "enum": ["Leisure", "Business", "Adventure", "Cultural", "Family", "Romantic"], "required": true},
  "budget": {"type": "string", "required": true, "enum": [economy, mid-range, luxury"},
  "interests": {"type": "array", "items": {"type": "string"}, "required": true, "minItems": 1},
  "how_packed_trip": {"type": "string", "enum": ["Relaxed", "Moderate", "Busy"], "required": true},
  "ok_with_walking": {"type": "boolean", "required": true},
  "age_group_of_travelers": {"type": "string", "required": true},
  "accessibility_needs": {"type": "string", "required": true},
  "dietary_needs": {"type": "string", "required": true}
}
'''
    
    prompt = f"""
    You are a friendly travel planner having a casual conversation with a user. Your goal is to help them plan their perfect trip while keeping the chat comfortable and natural.
    
    IMPORTANT: Only mark the conversation as complete when ALL required fields are filled with valid values.
    
    The user's trip info is stored in a JSON object. Here is the schema:
    {schema}

    CURRENT INFO: {json.dumps(state)}
    CHAT HISTORY: {' '.join([f"USER: {msg}" for msg in conversation_history[-2:] if conversation_history])}
    USER SAID: "{user_message}"
    TODAY'S DATE: {date.today().strftime("%Y-%m-%d")}

    YOUR JOB:
    1. Update the trip info with what you learn from the user
    2. Focus on the core trip details first (where, when, who, what)
    3. Ask ONE natural follow-up question about missing details
    4. Be conversational - sound like a helpful friend, not a form
    5. Only set next_question to empty string "" when ALL fields are completely filled
    6. Only have valid cities for the destination

    REQUIRED FIELDS THAT MUST BE FILLED:
    - starting_location (must be a valid city/airport)
    - destination (must be a valid city/airport)
    - dates_of_travel.start_date (YYYY-MM-DD format)
    - dates_of_travel.end_date (YYYY-MM-DD format)
    - number_of_travelers (positive integer)
    - trip_type (one of: Leisure, Business, Adventure, Cultural, Family, Romantic)
    - budget (one of: economy, mid-range, luxury)
    - interests (array with at least one item)
    - how_packed_trip (one of: Relaxed, Moderate, Busy)
    - ok_with_walking (true or false)
    - age_group_of_travelers (descriptive string)
    - accessibility_needs (string, can be "none" if no needs)
    - dietary_needs (string, can be "none" if no needs)

    RESPONSE (JSON ONLY):
    {{
      "updated_json": {{UPDATED_STATE}},
      "missing_fields": ["MOST_IMPORTANT_MISSING_FIELDS_FIRST"],
      "next_question": "ONE_NATURAL_CONVERSATIONAL_QUESTION_OR_EMPTY_STRING_IF_ALL_COMPLETE"
    }}
    """
    if GEMINI_AVAILABLE and GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")  # Updated to latest model
        response = model.generate_content(prompt)
        try:
            import re
            match = re.search(r'\{[\s\S]*\}', response.text)
            if match:
                result = json.loads(match.group(0))
                return result["updated_json"], result["missing_fields"], result["next_question"]
        except Exception as e:
            print("[Gemini parsing error]", e)
            missing = [k for k, v in state.items() if v is None]
            return state, missing, "Sorry, I had trouble understanding. Could you tell me more?"
    else:
        # Mock: just fill the first missing field with a dummy value and ask about the next
        missing = [k for k, v in state.items() if v is None]
        if not missing:
            return state, [], "Thank you! All information is collected."
        state = state.copy()
        state[missing[0]] = f"mock_{missing[0]}"
        next_question = f"Could you please tell me your {missing[1].replace('_', ' ')}?" if len(missing) > 1 else "Thank you! All information is collected."
        return state, missing[1:], next_question


def extract_flight_parameters_from_state(state):
    """
    Extract flight search parameters from the conversation state using Gemini.
    Maps the collected travel information to FlightSearchRequest format.
    """
    from app.flights.serpapi_adapter import SerpApiAdapter
    
    print(f"[DEBUG] Extracting from state: {json.dumps(state, indent=2)}")
    
    # Initialize airport code mapper
    serpapi_adapter = SerpApiAdapter()
    
    # Extract and convert city names to airport codes
    origin_city = state.get("starting_location")
    destination_city = state.get("destination")
    
    origin_code = serpapi_adapter.get_airport_code(origin_city) if origin_city else None
    destination_code = serpapi_adapter.get_airport_code(destination_city) if destination_city else None
    
    # Budget mapping function
    def normalize_budget(budget_value):
        """Convert various budget terms to accepted enum values"""
        if not budget_value:
            return "medium"
        
        budget_str = str(budget_value).lower().strip()
        
        # Map common budget terms to enum values
        budget_mapping = {
            # Low budget terms
            "low": "low",
            "cheap": "low", 
            "budget": "low",
            "economy": "low",
            "basic": "low",
            "minimal": "low",
            
            # Medium budget terms
            "medium": "medium",
            "moderate": "medium",
            "standard": "medium",
            "regular": "medium",
            "average": "medium",
            
            # High budget terms
            "high": "high",
            "expensive": "high",
            "premium": "high",
            "luxury": "high",
            "first-class": "high",
            "business": "high"
        }
        
        return budget_mapping.get(budget_str, "medium")
    
    manual_params = {
        "origin": origin_code,
        "destination": destination_code,
        "departure_date": state.get("dates_of_travel", {}).get("start_date"),
        "return_date": state.get("dates_of_travel", {}).get("end_date"),
        "num_travelers": state.get("number_of_travelers", 1),
        "budget": normalize_budget(state.get("budget")),
        "accessibility_requirements": bool(state.get("accessibility_needs"))
    }
    
    print(f"[DEBUG] Manual extraction result: {json.dumps(manual_params, indent=2)}")
    print(f"[DEBUG] Converted {origin_city} -> {origin_code}, {destination_city} -> {destination_code}")
    print(f"[DEBUG] Budget normalized: {state.get('budget')} -> {manual_params['budget']}")
    
    if manual_params.get("origin") and manual_params.get("destination"):
        return manual_params

    # Otherwise try Gemini extraction
    prompt = f"""
    You are a travel data processor. Extract flight search parameters from the collected travel information.
    
    COLLECTED TRAVEL DATA: {json.dumps(state)}
    
    Map this data to flight search parameters:
    - origin: starting_location (airport code or city name)
    - destination: destination (airport code or city name) 
    - departure_date: start_date from dates_of_travel (YYYY-MM-DD format)
    - return_date: end_date from dates_of_travel (YYYY-MM-DD format)
    - num_travelers: number_of_travelers (integer)
    - budget: map budget to EXACTLY "low", "medium", or "high" (convert economy->low, premium->high, etc.)
    - accessibility_requirements: true if accessibility_needs mentions any requirements, false otherwise
    
    IMPORTANT: Budget must be exactly "low", "medium", or "high" - no other values allowed!
    
    RESPONSE (JSON ONLY):
    {{
      "origin": "EXTRACTED_ORIGIN",
      "destination": "EXTRACTED_DESTINATION", 
      "departure_date": "YYYY-MM-DD",
      "return_date": "YYYY-MM-DD",
      "num_travelers": INTEGER,
      "budget": "low|medium|high",
      "accessibility_requirements": BOOLEAN
    }}
    """
    
    if GEMINI_AVAILABLE and GEMINI_API_KEY:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            print(f"[DEBUG] Gemini response: {response.text}")
            
            import re
            match = re.search(r'\{[\s\S]*\}', response.text)
            if match:
                flight_params = json.loads(match.group(0))
                # Ensure budget is normalized even from Gemini response
                if 'budget' in flight_params:
                    flight_params['budget'] = normalize_budget(flight_params['budget'])
                print(f"[DEBUG] Gemini extraction result: {json.dumps(flight_params, indent=2)}")
                return flight_params
        except Exception as e:
            print(f"[Flight extraction error]: {e}")
            # Fall back to manual extraction
            return manual_params if manual_params.get("origin") and manual_params.get("destination") else None
    
    # If Gemini not available, return manual extraction or error
    if manual_params.get("origin") and manual_params.get("destination"):
        return manual_params
    else:
        return {
            "error": "Flight extraction not available. Please try again later."
        }


def is_conversation_complete(state):
    """
    Check if all required fields are properly filled in the conversation state.
    """
    for field in REQUIRED_FIELDS:
        if field == "dates_of_travel":
            # Special handling for nested dates object
            dates = state.get(field, {})
            if not dates or not dates.get("start_date") or not dates.get("end_date"):
                return False
        elif field == "interests":
            # Special handling for interests array
            interests = state.get(field, [])
            if not interests or len(interests) == 0:
                return False
        else:
            # Regular field validation
            value = state.get(field)
            if value is None or value == "" or (isinstance(value, str) and value.strip() == ""):
                return False
    return True
