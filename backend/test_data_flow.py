#!/usr/bin/env python3
"""
Test data flow from backend to frontend to ensure all data is properly parsed and displayed.
"""

import requests
import json
import time
from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule

def test_data_flow():
    """Test complete data flow from backend to frontend."""
    print("🔄 Testing Data Flow: Backend → Frontend")
    print("=" * 60)
    
    # 1. Create a job
    print("1. Creating prediction job...")
    service = BoltzService()
    
    protein = ProteinSequence(
        sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
        id="test_protein"
    )
    ligand = LigandMolecule(
        smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
        id="test_ligand"
    )
    request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)
    
    job_id = service.create_prediction_job(request)
    print(f"   ✅ Job created: {job_id}")
    
    # 2. Run prediction
    print("2. Running prediction...")
    result = service.run_prediction(job_id, request)
    print(f"   ✅ Prediction completed: {result.status}")
    
    # 3. Check what data is available
    print("3. Backend data available:")
    print(f"   - affinity_pred_value: {result.affinity_pred_value}")
    print(f"   - affinity_probability_binary: {result.affinity_probability_binary}")
    print(f"   - confidence_score: {result.confidence_score}")
    print(f"   - processing_time_seconds: {result.processing_time_seconds}")
    print(f"   - error_message: {result.error_message}")
    
    # 4. Test API endpoints
    print("4. Testing API endpoints...")
    
    # Test job status endpoint
    try:
        response = requests.get(f"http://localhost:8000/jobs/{job_id}")
        if response.status_code == 200:
            status_data = response.json()
            print(f"   ✅ Job status endpoint: {status_data['status']}")
        else:
            print(f"   ❌ Job status endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Job status endpoint error: {e}")
    
    # Test job result endpoint
    try:
        response = requests.get(f"http://localhost:8000/jobs/{job_id}/result")
        if response.status_code == 200:
            result_data = response.json()
            print(f"   ✅ Job result endpoint:")
            print(f"      - affinity_pred_value: {result_data.get('affinity_pred_value')}")
            print(f"      - affinity_probability_binary: {result_data.get('affinity_probability_binary')}")
            print(f"      - confidence_score: {result_data.get('confidence_score')}")
            print(f"      - processing_time_seconds: {result_data.get('processing_time_seconds')}")
        else:
            print(f"   ❌ Job result endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Job result endpoint error: {e}")
    
    # 5. Check file structure
    print("5. Checking output files...")
    from pathlib import Path
    job_dir = Path("output/predictions") / job_id
    
    if job_dir.exists():
        print(f"   ✅ Job directory exists: {job_dir}")
        
        # Check affinity_prediction.json
        result_file = job_dir / "affinity_prediction.json"
        if result_file.exists():
            with open(result_file) as f:
                file_data = json.load(f)
            print(f"   ✅ Result file contains:")
            print(f"      - affinity_pred_value: {file_data.get('affinity_pred_value')}")
            print(f"      - affinity_probability_binary: {file_data.get('affinity_probability_binary')}")
            print(f"      - confidence_score: {file_data.get('confidence_score')}")
        else:
            print(f"   ❌ Result file not found: {result_file}")
        
        # Check metadata.json
        metadata_file = job_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)
            print(f"   ✅ Metadata file contains:")
            print(f"      - status: {metadata.get('status')}")
            print(f"      - progress: {metadata.get('progress')}")
            print(f"      - created_at: {metadata.get('created_at')}")
            print(f"      - updated_at: {metadata.get('updated_at')}")
        else:
            print(f"   ❌ Metadata file not found: {metadata_file}")
    else:
        print(f"   ❌ Job directory not found: {job_dir}")
    
    print("\n" + "=" * 60)
    print("✅ Data flow test completed!")
    print("\nFrontend should display:")
    print(f"- Binding Affinity: {result.affinity_pred_value} log(IC50)")
    print(f"- Binding Probability: {result.affinity_probability_binary * 100:.1f}%")
    print(f"- Confidence Score: {result.confidence_score * 100:.1f}%")
    print(f"- Processing Time: {result.processing_time_seconds:.1f}s")

if __name__ == "__main__":
    test_data_flow()
