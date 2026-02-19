#!/usr/bin/env python3
"""
AI Agriculture Suite - Startup Script
Run this file to start the application.
"""

import os
import sys
import subprocess

def main():
    print("\n" + "="*60)
    print("🌾 AI Agriculture Suite")
    print("="*60)

    # Check dependencies
    try:
        import fastapi
        import uvicorn
        import pandas
        import numpy
    except ImportError:
        print("\n⚠️  Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        print("✅ Dependencies installed!\n")

    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    os.chdir(backend_dir)

    # Add paths
    sys.path.insert(0, backend_dir)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "models"))

    print("\n📍 Open in browser: http://localhost:8002")
    print("📚 API Documentation: http://localhost:8002/docs")
    print("\n🌾 Features:")
    print("  • Crop Yield Prediction")
    print("  • Disease Detection")
    print("  • Pest Risk Prediction")
    print("  • Smart Irrigation Advisor")
    print("  • Market Price Predictor")
    print("  • AI Farming Chatbot (AgriBot)")
    print("\nPress Ctrl+C to stop the server\n")
    print("="*60 + "\n")

    import uvicorn
    from main import app
    uvicorn.run(app, host="0.0.0.0", port=8002)

if __name__ == "__main__":
    main()
