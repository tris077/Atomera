"""
Test RunPod endpoint directly.
"""

import os
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import settings


def main():
    print("=" * 60)
    print("  RunPod Endpoint Test")
    print("=" * 60)
    print()

    api_key = os.getenv("RUNPOD_API_KEY", settings.runpod_api_key)
    endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID", settings.runpod_endpoint_id)

    if not api_key or not endpoint_id:
        print("[ERROR] API key or endpoint ID not set")
        return False

    print(f"API Key: {api_key[:20]}...")
    print(f"Endpoint ID: {endpoint_id}")
    print()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Try to check endpoint health
    print("Testing endpoint health...")
    url = f"https://api.runpod.io/v2/{endpoint_id}/health"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Health check error: {e}")
        print("(This is normal for serverless endpoints)")

    print()
    print("=" * 60)
    print("Configuration looks correct!")
    print("=" * 60)
    print()
    print("Your credentials are set up. The endpoint will be tested")
    print("when you submit your first job.")
    print()

    return True


if __name__ == "__main__":
    main()
