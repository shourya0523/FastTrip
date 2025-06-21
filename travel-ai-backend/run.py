#!/usr/bin/env python3
"""
Simple run script for hackathon
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Travel AI Backend...")
    print("📡 API will be available at: http://localhost:8000")
    print("📖 Docs will be available at: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 