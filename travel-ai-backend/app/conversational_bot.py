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
  "number_of_travelers": {"type": "integer", "minimum": 1, "required": true},
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
    Once all details are filled, you MUST end the chat.
    The user's trip info is stored in a JSON object. Here is the schema:
    {schema}

    CURRENT INFO: {json.dumps(state)}
    CHAT HISTORY: {' '.join([f"USER: {msg}" for msg in conversation_history[-2:] if conversation_history])}
    USER SAID: "{user_message}"
    TODAY'S DATE: {date.today().strftime("%Y-%m-%d")}

    YOUR JOB:
    1. Update the trip info with what you learn from the user
    2. Focus on the core trip details first (where, when, who, what)
    3. Ask ONE natural follow-up question about the one or two important missing details, unless all details are filled.
    4. Be conversational - sound like a helpful friend, not a form
    5. Do not add your own fields, unless a very significant note exists. Then add additional notes.
    8. Only have valid cities for the destination. If the user says a city that is not valid, ask them to rephrase.

    PRIORITY FOR QUESTIONS:
    1. Destination and dates (where and when)
    2. Trip type and number of travelers (what kind of trip and who's going)
    3. Interests and budget (what they want to do and spend)
    4. Other preferences (pace, accommodations, special needs)

    RESPONSE (JSON ONLY):
    {{
      
      "updated_json": {{UPDATED_STATE}},
      
      "missing_fields": ["MOST_IMPORTANT_MISSING_FIELDS_FIRST"],
      
      "next_question": "ONE_NATURAL_CONVERSATIONAL_QUESTION"
    
    }}
    """
    if GEMINI_AVAILABLE and GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
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
    prompt = f"""
    You are a travel data processor. Extract flight search parameters from the collected travel information.
    
    COLLECTED TRAVEL DATA: {json.dumps(state)}
    
    Map this data to flight search parameters:
    - origin: starting_location (airport code or city name)
    - destination: destination (airport code or city name) 
    - departure_date: start_date from dates_of_travel (YYYY-MM-DD format)
    - return_date: end_date from dates_of_travel (YYYY-MM-DD format)
    - num_travelers: number_of_travelers (integer)
    - budget: map budget to "low", "medium", or "high"
    - accessibility_requirements: true if accessibility_needs mentions any requirements, false otherwise
    
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
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        try:
            import re
            match = re.search(r'\{[\s\S]*\}', response.text)
            if match:
                flight_params = json.loads(match.group(0))
                return flight_params
        except Exception as e:
            print(f"[Flight extraction error]: {e}")
            return None
    else:
        # Mock extraction for testing
        return {
            "origin": state.get("starting_location", "Unknown"),
            "destination": state.get("destination", "Unknown"),
            "departure_date": state.get("dates_of_travel", {}).get("start_date", "2024-01-01"),
            "return_date": state.get("dates_of_travel", {}).get("end_date", "2024-01-07"),
            "num_travelers": state.get("number_of_travelers", 1),
            "budget": "medium",
            "accessibility_requirements": bool(state.get("accessibility_needs"))
        }
    
    return None
