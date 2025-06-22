from app.services.travel_service import travel_service

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # ... existing code ...
    
    if not next_question:
        conversation_complete = True
        # Process completed conversation
        flight_parameters = await travel_service.process_completed_conversation(
            request.session_id, updated_state
        )
    
    return ChatResponse(
        message=response_message,
        next_question=next_question,
        conversation_complete=conversation_complete,
        flight_parameters=flight_parameters
    )