"""
Test script to verify RunPod API connection and list available endpoints.
"""

import os
import sys
import requests
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings


def test_api_key():
    """Test if the RunPod API key is valid."""
    api_key = os.getenv("RUNPOD_API_KEY", settings.runpod_api_key)
    
    if not api_key:
        print("❌ ERROR: RUNPOD_API_KEY not set")
        print("   Set it in your .env file or environment variable")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    # Test API key by listing pods
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    try:
        # Test with pods endpoint
        url = "https://api.runpod.io/v1/pods"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ API Key is valid!")
            pods = response.json()
            if isinstance(pods, list) and len(pods) > 0:
                print(f"   Found {len(pods)} pod(s)")
                for pod in pods[:3]:  # Show first 3
                    pod_id = pod.get("id", "unknown")
                    pod_name = pod.get("name", "unnamed")
                    print(f"   - Pod: {pod_name} (ID: {pod_id})")
            return True
        elif response.status_code == 401:
            print("❌ ERROR: API Key is invalid or expired")
            return False
        else:
            print(f"⚠️  Warning: Unexpected response: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to connect to RunPod API: {e}")
        return False


def list_serverless_endpoints():
    """List available serverless endpoints."""
    api_key = os.getenv("RUNPOD_API_KEY", settings.runpod_api_key)
    
    if not api_key:
        print("❌ ERROR: RUNPOD_API_KEY not set")
        return []
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    try:
        # List serverless endpoints
        url = "https://api.runpod.io/v2/serverless"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            endpoints = data.get("data", [])
            
            if endpoints:
                print(f"\n✅ Found {len(endpoints)} serverless endpoint(s):")
                for endpoint in endpoints:
                    endpoint_id = endpoint.get("id", "unknown")
                    endpoint_name = endpoint.get("name", "unnamed")
                    gpu_type = endpoint.get("gpuTypeId", "unknown")
                    print(f"   - {endpoint_name}")
                    print(f"     ID: {endpoint_id}")
                    print(f"     GPU: {gpu_type}")
                    print()
                return endpoints
            else:
                print("\n⚠️  No serverless endpoints found")
                print("   You'll need to create one in the RunPod dashboard")
                return []
        else:
            print(f"⚠️  Warning: Could not list endpoints: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to list endpoints: {e}")
        return []


def main():
    """Main test function."""
    print("=" * 60)
    print("RunPod Connection Test")
    print("=" * 60)
    print()
    
    # Test API key
    if not test_api_key():
        print("\n❌ API key test failed. Please check your API key.")
        return
    
    # List endpoints
    endpoints = list_serverless_endpoints()
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    
    if endpoints:
        print("\n✅ You have serverless endpoints available!")
        print("   Use one of the endpoint IDs above in your .env file:")
        print("   RUNPOD_ENDPOINT_ID=your_endpoint_id_here")
    else:
        print("\n⚠️  No serverless endpoints found.")
        print("\n   Option 1: Create a Serverless Endpoint")
        print("   1. Go to: https://www.runpod.io/console/serverless")
        print("   2. Click 'New Endpoint'")
        print("   3. Create endpoint with Boltz-2 handler")
        print("   4. Copy the endpoint ID")
        print("\n   Option 2: Use Your Existing Pod")
        print("   Your pod ID: ei5zbysk7svqp5")
        print("   (Note: This requires SSH-based integration)")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

