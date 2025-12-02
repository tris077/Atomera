"""
Test RunPod endpoint connectivity and API format.
"""

import os
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import settings


def test_endpoint():
    """Test various RunPod API endpoints to find the right format."""
    api_key = os.getenv("RUNPOD_API_KEY", settings.runpod_api_key)
    endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID", settings.runpod_endpoint_id)

    print("=" * 70)
    print("  RunPod Endpoint API Test")
    print("=" * 70)
    print()
    print(f"API Key: {api_key[:20]}...")
    print(f"Endpoint ID: {endpoint_id}")
    print()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    base_url = "https://api.runpod.io/v2"

    # Test different endpoint patterns
    test_urls = [
        (f"{base_url}/{endpoint_id}/health", "GET", "Health check"),
        (f"{base_url}/{endpoint_id}/run", "POST", "Async run (current)"),
        (f"{base_url}/{endpoint_id}/runsync", "POST", "Sync run"),
        (f"https://api.runpod.ai/v2/{endpoint_id}/run", "POST", "Async run (.ai domain)"),
    ]

    print("Testing different API endpoints...")
    print()

    for url, method, description in test_urls:
        print(f"[{method}] {description}")
        print(f"    URL: {url}")

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            else:
                # Minimal test payload
                test_payload = {
                    "input": {
                        "test": "ping"
                    }
                }
                response = requests.post(url, headers=headers, json=test_payload, timeout=10)

            print(f"    Status: {response.status_code}")
            print(f"    Response: {response.text[:200]}")

            if response.status_code < 400:
                print(f"    ✅ SUCCESS!")
            else:
                print(f"    ❌ Failed")

        except Exception as e:
            print(f"    ❌ Error: {e}")

        print()

    print("=" * 70)
    print("  Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_endpoint()
