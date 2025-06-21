import os
import json
from dotenv import load_dotenv
from datetime import date

# Gemini setup
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

REQUIRED_FIELDS = [
    "budget", "start_location", "destination", "start_date", "end_date",
    "accessibility_needs", "dietary_needs", "age", "interest", "how_packed_trip",
    "okay_with_walking", "trip_type", "number_of_travellers"
]

INITIAL_STATE = {field: None for field in REQUIRED_FIELDS}

# Gemini wrapper

def call_gemini_update_state(state, user_message, conversation_history=[]):
    """
    Calls Gemini to update the state JSON, return missing fields, and suggest the next question to ask.
    If Gemini is not available, uses a mock function.
    """
    prompt = f"""
    You are a helpful and very friendly travel assistant for sometimes confused users who may have accessibility requirements. You are collecting information to plan an accessible travel itinerary.

    # Current User Information
    {json.dumps(state, indent=2)}

    # Expected Schema Fields (Priority Order)
    - user.mobility_aids: ["walker", "wheelchair", "cane", null] - How the user moves around
    - user.age_range: ["55-64", "65-74", "75+", null] - User's age range
    - user.accommodation_requirements: ["ground_floor", "elevator", "roll_in_shower", "grab_bars", "wider_doorways", null] - Special room needs
    - user.energy_constraints: ["minimal_fatigue", "moderate_fatigue", "significant_fatigue", null] - How much activity they can handle daily
    - trip.destinations: ["New York", "Miami", "San Francisco", null] - Where they want to go
    - trip.dates.start_date: YYYY-MM-DD - When they want to begin traveling
    - trip.dates.end_date: YYYY-MM-DD - When they want to return
    - trip.transportation_preferences: ["plane", "train", "car", "bus", null] - How they prefer to travel
    - trip.activity_interests: ["museums", "dining", "parks", "shows", null] - What they enjoy doing

    # Conversation History
    {' '.join([f"USER: {msg}" for msg in conversation_history[-3:] if conversation_history])}

    # Latest User Message
    USER: "{user_message}"

    # Instructions
    1. Update the JSON state with new information from the user's message
    2. When updating:
       - Only update fields you're confident about (80%+ certainty)
       - Resolve contradictions by using the most recent information
       - Convert approximate dates (e.g., "next week") to specific dates
       - Never remove previously filled values unless explicitly contradicted
       - Infer values when reasonable (e.g., if user mentions "my wheelchair", set mobility_aids)
       
    3. After updating:
       - Identify missing high-priority fields (focus on accessibility needs first)
       - Generate a warm, friendly follow-up question about THE SINGLE most important missing field
       - If asking about dates, remind user the current date is {date.today().strftime("%B %d, %Y")}
       - If all critical fields are filled, ask about activity preferences or offer to generate an itinerary

    4. If the user seems confused or gives irrelevant information, gently redirect to the most important missing information

    # Response Format (JSON only)
    {{
      "updated_json": {{complete updated state object}},
      "missing_fields": ["list", "of", "missing", "fields", "in", "priority", "order"],
      "next_question": "A single, conversational question focusing on the highest priority missing field. Be warm and understanding. Mention one relevant accessibility consideration if appropriate."
    }}
    """
    if GEMINI_AVAILABLE and GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
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


def main():
    print("Welcome to the AccessibleTravel AI Chatbot!\n")
    state = INITIAL_STATE.copy()
    missing_fields = [k for k, v in state.items() if v is None]
    user_message = ""
    next_question = None
    while missing_fields:
        # Let the model generate the next question
        state, missing_fields, next_question = call_gemini_update_state(state, user_message)
        print(f"Bot: {next_question}")
        if not missing_fields:
            break
        user_message = input("You: ")
        print(f"[Current state]: {json.dumps(state, indent=2)}\n")
    print("\nAll information collected! Here is your travel profile:")
    print(json.dumps(state, indent=2))

if __name__ == "__main__":
    main()
