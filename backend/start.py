#!/usr/bin/env python3
"""
Simple startup script for Atomera API server.
"""
import sys
import os
from pathlib import Path


def main():
    """Start the Atomera API server."""
    print("🧬 Atomera API - Starting...")

    # Get the current directory and create absolute paths
    current_dir = Path.cwd()
    output_dir = current_dir / "output"
    predictions_dir = output_dir / "predictions"
    temp_dir = output_dir / "temp"

    # Create directories with proper error handling
    try:
        # Check if output is a file and remove it if so
        if output_dir.is_file():
            output_dir.unlink()
            print("✅ Removed existing output file")

        output_dir.mkdir(exist_ok=True)
        predictions_dir.mkdir(exist_ok=True)
        temp_dir.mkdir(exist_ok=True)
        print("✅ Directories ready")
    except Exception as e:
        print(f"⚠️ Directory creation warning: {e}")
        print("Continuing anyway...")

    try:
        import uvicorn
        from main import app

        print("✅ Server starting at http://localhost:8000")
        print("📖 API Documentation: http://localhost:8000/docs")
        print("🔍 Health Check: http://localhost:8000/health")
        print("📚 Examples: http://localhost:8000/examples")
        print("\nPress Ctrl+C to stop the server")

        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
