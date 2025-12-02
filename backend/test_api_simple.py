#!/usr/bin/env python3
"""
Simple API test to verify server is running and responding.
"""

import requests
import time


def test_api():
    """Test API endpoints."""
    base_url = "http://localhost:8000"

    print("🌐 Testing Atomera API Server")
    print("=" * 50)

    try:
        # Test health endpoint
        print("Testing /health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"   Boltz available: {data['boltz_available']}")
            print(f"   Version: {data['version']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False

        # Test examples endpoint
        print("\nTesting /examples endpoint...")
        response = requests.get(f"{base_url}/examples", timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            proteins = data.get("proteins", {})
            ligands = data.get("ligands", {})
            print(f"✅ Examples: {len(proteins)} proteins, {len(ligands)} ligands")
        else:
            print(f"❌ Examples failed: {response.status_code}")
            return False

        # Test prediction endpoint
        print("\nTesting /predict endpoint...")
        prediction_data = {
            "protein": {
                "id": "test_protein",
                "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            },
            "ligand": {"id": "test_ligand", "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"},
            "use_msa": True,
        }

        response = requests.post(
            f"{base_url}/predict", json=prediction_data, timeout=15
        )
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            job_id = data.get("job_id")
            print(f"✅ Prediction job created: {job_id}")
            print(f"   Status: {data.get('status')}")

            # Test job status
            print("\nTesting job status...")
            time.sleep(2)
            response = requests.get(f"{base_url}/jobs/{job_id}", timeout=10)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                status_data = response.json()
                print(f"✅ Job status: {status_data['status']}")
                print(f"   Progress: {status_data.get('progress', 'N/A')}%")
            else:
                print(f"❌ Job status failed: {response.status_code}")
                return False
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

        print("\n🎉 All API tests passed!")
        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server.")
        print("   Make sure the server is running with:")
        print(
            "   python -c \"import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8000)\""
        )
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_api()
    if success:
        print("\n✅ Atomera API is fully functional!")
    else:
        print("\n❌ API tests failed.")
    exit(0 if success else 1)
