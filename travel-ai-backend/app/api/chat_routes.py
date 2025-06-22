from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from app.conversational_bot import call_gemini_update_state, INITIAL_STATE
from app.utils.session_manager import get_session, update_session

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    extracted_params: Dict[str, Any]
    follow_up_questions: List[str]
    session_id: str
    conversation_complete: bool = False

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to handle chat messages and update session state.
    """
    session_id = request.session_id
    session = get_session(session_id)

    if not session:
        session = {"state": INITIAL_STATE.copy(), "history": []}

    state = session.get("state", INITIAL_STATE.copy())
    history = session.get("history", [])

    try:
        updated_state, missing_fields, next_question = call_gemini_update_state(
            state,
            request.message,
            history
        )

        session["state"] = updated_state
        session["history"].append(request.message)
        
        conversation_complete = not next_question
        if conversation_complete:
            session["conversation_complete"] = True

        new_session_id = update_session(session, session_id)

        return ChatResponse(
            extracted_params=updated_state,
            follow_up_questions=[next_question] if next_question else [],
            session_id=new_session_id,
            conversation_complete=conversation_complete
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))