#!/usr/bin/env python3
"""
Test script to verify the backend validation fix.
"""

import requests
import json


def test_prediction_endpoint():
    """Test the /predict endpoint with the data that was failing."""

    url = "http://localhost:8000/predict"

    # Test data that was failing
    test_data = {
        "protein": {
            "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            "id": "insulin",
        },
        "ligand": {"smiles": "CC1=CC=CC=C1C(=O)O", "id": "aspirin"},
        "use_msa": True,
    }

    print("🧪 Testing /predict endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(test_data, indent=2)}")

    try:
        response = requests.post(url, json=test_data, timeout=10)

        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            print("✅ SUCCESS! Job created successfully")
            result = response.json()
            print(f"📋 Job ID: {result.get('job_id')}")
            print(f"📋 Status: {result.get('status')}")
        else:
            print("❌ FAILED!")
            print(f"📋 Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend server not running")
        print("💡 Start the backend with: python start.py")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_prediction_endpoint()

