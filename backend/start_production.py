#!/usr/bin/env python3
"""
Production startup script for Atomera API server.
"""

import sys
import os
import uvicorn
from pathlib import Path


def main():
    """Start the Atomera API server in production mode."""
    print("🚀 Starting Atomera API Server (Production Mode)")
    print("=" * 60)

    # Get the current directory
    current_dir = Path.cwd()
    print(f"Working directory: {current_dir}")

    # Create output directories
    output_dir = current_dir / "output"
    predictions_dir = output_dir / "predictions"
    temp_dir = output_dir / "temp"

    try:
        output_dir.mkdir(exist_ok=True)
        predictions_dir.mkdir(exist_ok=True)
        temp_dir.mkdir(exist_ok=True)
        print("✅ Output directories ready")
    except Exception as e:
        print(f"⚠️ Directory creation warning: {e}")

    # Test imports
    try:
        from main import app

        print("✅ FastAPI app imported successfully")
    except Exception as e:
        print(f"❌ Failed to import app: {e}")
        sys.exit(1)

    # Test Boltz service
    try:
        from services.boltz_service import BoltzService

        service = BoltzService()
        boltz_available = service.check_boltz_availability()
        print(
            f"✅ Boltz service: {'Available' if boltz_available else 'Not available (will use mock mode)'}"
        )
    except Exception as e:
        print(f"⚠️ Boltz service warning: {e}")

    # Start server
    print("\n🌐 Starting API server...")
    print("   URL: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   Health: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)

    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True,
            reload=False,  # Disable reload in production
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
