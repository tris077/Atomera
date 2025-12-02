#!/usr/bin/env python3
"""
Debug script to check what's wrong with the backend.
"""

import sys
import os

# Set UTF-8 encoding for Windows compatibility
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("=== BACKEND DEBUGGING ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Check if we can import the backend
try:
    print("\n1. Testing imports...")
    sys.path.append('backend')
    
    print("   - Testing basic imports...")
    import fastapi
    print(f"   SUCCESS: FastAPI version: {fastapi.__version__}")
    
    import uvicorn
    print("   SUCCESS: Uvicorn imported")
    
    print("   - Testing backend imports...")
    from backend.config import settings
    print(f"   SUCCESS: Settings imported: {settings.app_name}")
    
    from backend.models import PredictionRequest
    print("   SUCCESS: Models imported")
    
    from backend.services.boltz_service import BoltzService
    print("   SUCCESS: BoltzService imported")
    
    print("   - Testing main module...")
    from backend import main
    print("   SUCCESS: Main module imported")
    
    print("\n2. Testing app creation...")
    app = main.app
    print(f"   SUCCESS: App created: {app.title}")
    
    print("\n3. Testing server startup...")
    print("   Starting server on http://localhost:8000")
    print("   Press Ctrl+C to stop")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    
except ImportError as e:
    print(f"   ERROR: Import error: {e}")
    print("   TIP: Try: pip install fastapi uvicorn python-multipart")
    
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()
