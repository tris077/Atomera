"""
Simple test script for Atomera API using only built-in libraries.
No external dependencies required - just run this after starting the server.
"""

import urllib.request
import urllib.parse
import json
import time


def test_endpoint(url, method="GET", data=None):
    """Test an API endpoint and return the result."""
    try:
        if method == "GET":
            req = urllib.request.Request(url)
        else:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8") if data else None,
                headers={"Content-Type": "application/json"},
            )
            req.get_method = lambda: method

        with urllib.request.urlopen(req) as response:
            result = response.read().decode("utf-8")
            return response.status, json.loads(result) if result else {}
    except Exception as e:
        return None, str(e)


def main():
    """Test all API endpoints."""
    base_url = "http://localhost:8000"

    print("🧪 Testing Atomera API (Built-in libraries only)")
    print("=" * 50)

    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    status, result = test_endpoint(f"{base_url}/")
    if status == 200:
        print(f"✅ Root endpoint: {result.get('message', 'OK')}")
    else:
        print(f"❌ Root endpoint failed: {status}")

    # Test 2: Health check
    print("\n2. Testing health check...")
    status, result = test_endpoint(f"{base_url}/health")
    if status == 200:
        print(f"✅ Health check: {result.get('status', 'OK')}")
        print(f"   Boltz-2 available: {result.get('boltz_available', 'Unknown')}")
    else:
        print(f"❌ Health check failed: {status}")

    # Test 3: Examples endpoint
    print("\n3. Testing examples endpoint...")
    status, result = test_endpoint(f"{base_url}/examples")
    if status == 200:
        proteins = result.get("proteins", {})
        ligands = result.get("ligands", {})
        print(f"✅ Examples: {len(proteins)} proteins, {len(ligands)} ligands")
    else:
        print(f"❌ Examples failed: {status}")

    # Test 4: Protein validation
    print("\n4. Testing protein validation...")
    protein_data = {
        "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
        "id": "A",
    }
    status, result = test_endpoint(f"{base_url}/validate/protein", "POST", protein_data)
    if status == 200:
        print(f"✅ Protein validation: {result.get('message', 'OK')}")
    else:
        print(f"❌ Protein validation failed: {status}")

    # Test 5: Ligand validation
    print("\n5. Testing ligand validation...")
    ligand_data = {"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O", "id": "B"}
    status, result = test_endpoint(f"{base_url}/validate/ligand", "POST", ligand_data)
    if status == 200:
        print(f"✅ Ligand validation: {result.get('message', 'OK')}")
    else:
        print(f"❌ Ligand validation failed: {status}")

    # Test 6: Create prediction job
    print("\n6. Testing prediction job creation...")
    prediction_data = {"protein": protein_data, "ligand": ligand_data, "use_msa": True}
    status, result = test_endpoint(f"{base_url}/predict", "POST", prediction_data)
    if status == 200:
        job_id = result.get("job_id")
        print(f"✅ Prediction job created: {job_id}")
        print(f"   Status: {result.get('status', 'Unknown')}")

        # Test 7: Check job status
        print("\n7. Testing job status...")
        time.sleep(1)  # Wait a bit
        status, result = test_endpoint(f"{base_url}/jobs/{job_id}")
        if status == 200:
            print(f"✅ Job status: {result.get('status', 'Unknown')}")
            print(f"   Progress: {result.get('progress', 'N/A')}%")
        else:
            print(f"❌ Job status failed: {status}")
    else:
        print(f"❌ Prediction job creation failed: {status}")
        if result:
            print(f"   Error: {result}")

    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("\n💡 Next steps:")
    print("   - Open http://localhost:8000/docs for interactive testing")
    print("   - Use the examples endpoint to get sample molecules")
    print("   - Test real predictions with your own protein/ligand data")


if __name__ == "__main__":
    main()
