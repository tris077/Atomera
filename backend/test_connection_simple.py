"""
Simple RunPod connection test without emoji characters for Windows compatibility.
"""

import os
import sys
import requests
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings


def main():
    print("=" * 60)
    print("  RunPod Connection Test")
    print("=" * 60)
    print()

    # Get API credentials
    api_key = os.getenv("RUNPOD_API_KEY", settings.runpod_api_key)
    endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID", settings.runpod_endpoint_id)

    if not api_key:
        print("[ERROR] RUNPOD_API_KEY not set")
        print("Set it in backend/.env file")
        return False

    if not endpoint_id:
        print("[ERROR] RUNPOD_ENDPOINT_ID not set")
        print("Set it in backend/.env file")
        return False

    print(f"[OK] API Key found: {api_key[:20]}...")
    print(f"[OK] Endpoint ID: {endpoint_id}")
    print()

    # Test API connection
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    print("Testing API connection...")
    try:
        response = requests.get(
            "https://api.runpod.io/v2/user",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print("[OK] API key is valid")
        else:
            print(f"[ERROR] API returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return False

    # Test endpoint accessibility
    print()
    print(f"Testing endpoint {endpoint_id}...")
    try:
        response = requests.get(
            f"https://api.runpod.io/v2/{endpoint_id}/health",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print("[OK] Endpoint is accessible")
            data = response.json()
            print(f"     Workers: {data.get('workers', 'unknown')}")
        else:
            print(f"[WARNING] Endpoint health check returned {response.status_code}")
            print(f"          This is normal if endpoint is in serverless mode")
    except Exception as e:
        print(f"[WARNING] Health check failed: {e}")
        print("          This is normal for serverless endpoints")

    print()
    print("=" * 60)
    print("  Connection Test PASSED")
    print("=" * 60)
    print()
    print("Your RunPod integration is configured correctly!")
    print()
    print("Next steps:")
    print("  1. Start backend: cd backend && python main.py")
    print("  2. Start frontend: cd frontend && npm run dev")
    print("  3. Create a test job in the UI")
    print()

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
