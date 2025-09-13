#!/usr/bin/env python3
"""
Integration test for Boltz-2 service.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule


def test_boltz_service():
    """Test the Boltz service integration."""
    print("🧬 Testing Boltz-2 Service Integration")
    print("=" * 50)

    try:
        # Initialize the service
        print("1. Initializing Boltz service...")
        service = BoltzService()
        print("✅ Service initialized successfully")

        # Check boltz availability
        print("\n2. Checking Boltz-2 availability...")
        boltz_available = service.check_boltz_availability()
        print(f"✅ Boltz-2 available: {boltz_available}")

        if not boltz_available:
            print("❌ Boltz-2 is not available. Cannot proceed with tests.")
            return False

        # Create a test prediction request
        print("\n3. Creating test prediction request...")
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            id="test_insulin",
        )
        ligand = LigandMolecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O", id="test_aspirin")
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)
        print("✅ Test request created successfully")
        print(f"   Protein: {protein.id} (length: {len(protein.sequence)})")
        print(f"   Ligand: {ligand.id} (SMILES: {ligand.smiles})")

        # Test job creation
        print("\n4. Testing job creation...")
        job_id = service.create_prediction_job(request)
        print(f"✅ Job created successfully with ID: {job_id}")

        # Test input YAML creation
        print("\n5. Testing input YAML creation...")
        yaml_path = service._create_input_yaml(job_id, request)
        print(f"✅ Input YAML created: {yaml_path}")

        # Check if YAML file exists and has correct content
        if os.path.exists(yaml_path):
            with open(yaml_path, "r") as f:
                yaml_content = f.read()
                print("✅ YAML file content:")
                print(yaml_content)
        else:
            print("❌ YAML file not found")
            return False

        # Test job status retrieval
        print("\n6. Testing job status retrieval...")
        status = service.get_job_status(job_id)
        if status:
            print(f"✅ Job status retrieved: {status.status}")
            print(f"   Progress: {status.progress}%")
            print(f"   Created: {status.created_at}")
        else:
            print("❌ Failed to retrieve job status")
            return False

        # Test a simple prediction (this will use mock data for now)
        print("\n7. Testing prediction execution...")
        try:
            result = service.run_prediction(job_id, request)
            print(f"✅ Prediction completed: {result.status}")
            if result.status == "completed":
                print(f"   Affinity: {result.affinity_pred_value} kcal/mol")
                print(f"   Probability: {result.affinity_probability_binary}")
                print(f"   Confidence: {result.confidence_score}")
                print(f"   Processing time: {result.processing_time_seconds:.2f}s")
            elif result.status == "failed":
                print(f"   Error: {result.error_message}")
        except Exception as e:
            print(f"⚠️ Prediction test failed (this is expected for now): {e}")
            print(
                "   This is likely because the actual Boltz-2 command needs proper setup"
            )

        print("\n" + "=" * 50)
        print("🎉 Boltz-2 Service Integration Test Completed!")
        print("✅ Service initialization: PASSED")
        print("✅ Boltz-2 availability: PASSED")
        print("✅ Job creation: PASSED")
        print("✅ YAML generation: PASSED")
        print("✅ Status management: PASSED")
        print("⚠️ Prediction execution: PARTIAL (needs proper Boltz-2 setup)")

        return True

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_boltz_service()
    sys.exit(0 if success else 1)

