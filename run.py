#!/usr/bin/env python3
"""
EduGenius Application Runner
Run this script to start the EduGenius server.
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("=" * 60)
    print("🎓 Starting EduGenius - AI-Powered Educational Assistant")
    print("=" * 60)
    print(f"Server: http://{settings.host}:{settings.port}")
    print(f"Default LLM Provider: {settings.default_llm_provider.upper()}")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
