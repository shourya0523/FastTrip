import uuid
from typing import Dict, Any, Optional

# In-memory session storage for simplicity in a hackathon context
_sessions: Dict[str, Dict[str, Any]] = {}

def get_session(session_id: Optional[str]) -> Optional[Dict[str, Any]]:
    """Retrieves a session from the in-memory store."""
    if session_id and session_id in _sessions:
        return _sessions[session_id]
    return None

def update_session(session_data: Dict[str, Any], session_id: Optional[str] = None) -> str:
    """Updates or creates a session in the in-memory store."""
    if not session_id or session_id not in _sessions:
        session_id = str(uuid.uuid4())
    _sessions[session_id] = session_data
    return session_id