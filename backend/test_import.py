#!/usr/bin/env python3
"""Test script to check if backend can be imported."""
import sys
import traceback

try:
    print("Testing imports...")
    from main import app
    print("✅ SUCCESS: App imported successfully!")
    print(f"App type: {type(app)}")
    print(f"App title: {app.title}")
    sys.exit(0)
except Exception as e:
    print(f"❌ ERROR: {e}")
    print(f"Error type: {type(e).__name__}")
    traceback.print_exc()
    sys.exit(1)











