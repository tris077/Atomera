#!/usr/bin/env python3
"""
Test the frontend fix by simulating the exact request the frontend makes
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"


def test_frontend_request():
    """Test the exact request format the frontend sends"""
    print("🧪 Testing frontend request format...")

    # Simulate the exact data the frontend sends
    payload = {
        "protein": {
            "sequence": "MGPGGLPGRRVQGHFRYRLKETVTGKWRPLLEKHKLYYDKTVDCPRLPGLVEYLKQYLLDKKVLKYTVDCPCLKQLSPEEKDLLLQKYRKELTQNYQLKELENLARLFVQ",
            "id": "A",
        },
        "ligand": {"smiles": "Cc1ccc2c(c1)C(=O)NC(C3CCNCC3)C2=O", "id": "B"},
        "use_msa": True,
        "confidence_threshold": 0.5,
    }

    print("📤 Sending request with cleaned protein sequence...")
    print(f"Protein sequence length: {len(payload['protein']['sequence'])}")
    print(f"Ligand SMILES: {payload['ligand']['smiles']}")

    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS! Job created: {data['job_id']}")
            return True
        else:
            print(f"❌ FAILED: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error text: {response.text}")
            return False

    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False


if __name__ == "__main__":
    print("🔧 Testing Frontend Fix")
    print("=" * 40)

    success = test_frontend_request()

    if success:
        print(
            "\n✅ Frontend fix successful! Jobs should now work in the web interface."
        )
    else:
        print("\n❌ Frontend fix needs more work.")
