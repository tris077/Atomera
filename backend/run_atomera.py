#!/usr/bin/env python3
"""
Atomera Backend - Production Runner
Comprehensive startup script with health checks and monitoring.
"""

import sys
import os
import time
import signal
import subprocess
from pathlib import Path
from typing import Optional


def check_dependencies():
    """Check if all required dependencies are available."""
    print("🔍 Checking dependencies...")

    try:
        import fastapi

        print("✅ FastAPI available")
    except ImportError:
        print("❌ FastAPI not found. Install with: pip install fastapi")
        return False

    try:
        import uvicorn

        print("✅ Uvicorn available")
    except ImportError:
        print("❌ Uvicorn not found. Install with: pip install uvicorn")
        return False

    try:
        import pydantic

        print("✅ Pydantic available")
    except ImportError:
        print("❌ Pydantic not found. Install with: pip install pydantic")
        return False

    try:
        import boltz

        print("✅ Boltz available")
    except ImportError:
        print("⚠️ Boltz not found. Will use mock mode.")

    return True


def setup_directories():
    """Set up required directories."""
    print("📁 Setting up directories...")

    current_dir = Path.cwd()
    output_dir = current_dir / "output"
    predictions_dir = output_dir / "predictions"
    temp_dir = output_dir / "temp"

    try:
        output_dir.mkdir(exist_ok=True)
        predictions_dir.mkdir(exist_ok=True)
        temp_dir.mkdir(exist_ok=True)
        print("✅ Directories ready")
        return True
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return False


def test_backend_service():
    """Test backend service functionality."""
    print("🧬 Testing backend service...")

    try:
        from services.boltz_service import BoltzService
        from models import PredictionRequest, ProteinSequence, LigandMolecule

        service = BoltzService()
        boltz_available = service.check_boltz_availability()
        print(
            f"✅ Backend service ready (Boltz: {'Yes' if boltz_available else 'Mock mode'})"
        )

        # Quick test
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT", id="test"
        )
        ligand = LigandMolecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O", id="test")
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)

        job_id = service.create_prediction_job(request)
        print(f"✅ Job creation test passed (ID: {job_id})")

        return True
    except Exception as e:
        print(f"❌ Backend service test failed: {e}")
        return False


def start_server(host="0.0.0.0", port=8000, reload=False):
    """Start the FastAPI server."""
    print(f"🚀 Starting Atomera API server...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Reload: {reload}")
    print("=" * 60)

    try:
        import uvicorn
        from main import app

        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            log_level="info",
            access_log=True,
            reload=reload,
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        return False

    return True


def run_health_check(host="localhost", port=8000, timeout=30):
    """Run health check on the server."""
    print("🏥 Running health check...")

    import requests

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"http://{host}:{port}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['status']}")
                print(f"   Boltz available: {data['boltz_available']}")
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Health check error: {e}")
            time.sleep(1)

    print("❌ Health check failed - server not responding")
    return False


def main():
    """Main entry point."""
    print("🧬 Atomera Backend - Production Runner")
    print("=" * 60)

    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="Atomera Backend Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--skip-tests", action="store_true", help="Skip startup tests")
    parser.add_argument(
        "--health-check", action="store_true", help="Run health check after startup"
    )

    args = parser.parse_args()

    # Run startup checks
    if not args.skip_tests:
        if not check_dependencies():
            print("❌ Dependency check failed")
            sys.exit(1)

        if not setup_directories():
            print("❌ Directory setup failed")
            sys.exit(1)

        if not test_backend_service():
            print("❌ Backend service test failed")
            sys.exit(1)

        print("✅ All startup checks passed")

    # Start server
    print(f"\n🌐 Starting server on {args.host}:{args.port}")
    print("   Press Ctrl+C to stop")
    print("=" * 60)

    # Start server in background if health check is requested
    if args.health_check:
        import threading
        import time

        def start_server_thread():
            start_server(args.host, args.port, args.reload)

        server_thread = threading.Thread(target=start_server_thread)
        server_thread.daemon = True
        server_thread.start()

        # Wait for server to start
        time.sleep(5)

        # Run health check
        if run_health_check(args.host, args.port):
            print("🎉 Server started successfully!")
            print(f"   API: http://{args.host}:{args.port}")
            print(f"   Docs: http://{args.host}:{args.port}/docs")
            print(f"   Health: http://{args.host}:{args.port}/health")

            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
        else:
            print("❌ Server failed to start properly")
            sys.exit(1)
    else:
        start_server(args.host, args.port, args.reload)


if __name__ == "__main__":
    main()
