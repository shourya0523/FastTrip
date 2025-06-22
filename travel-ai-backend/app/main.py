"""
Simple FastAPI app for hackathon
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import flight_routes, chat_routes

# Create app
app = FastAPI(title="Travel AI Backend", version="1.0.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(flight_routes.router, prefix="/api/v1/flights", tags=["Flights"])
app.include_router(chat_routes.router, prefix="/api/v1/chat", tags=["Chat"]) 


@app.get("/")
async def root():
    return {"message": "Travel AI Backend - Flight Module"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
