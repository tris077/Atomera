"""
Test script to diagnose job submission issues.
Submits a minimal test job and shows detailed diagnostics.
"""

import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from models import PredictionRequest, ProteinSequence, LigandMolecule
from services.boltz_service import BoltzService


def test_job_submission():
    """Test submitting a minimal job and check results."""
    print("=" * 70)
    print("  Job Submission Diagnostic Test")
    print("=" * 70)
    print()

    # Create a minimal test request
    print("[1] Creating minimal test request...")
    request = PredictionRequest(
        protein=ProteinSequence(
            id="A",
            sequence="MKFLKFSLLTAVLLSVVFAFSSCGDDDDTGYLPPSQAIQDLLKRMKV"
        ),
        ligand=LigandMolecule(
            id="B",
            smiles="CCO"
        ),
        use_msa=True,
        confidence_threshold=0.5
    )
    print(f"    Protein: {request.protein.sequence[:30]}... ({len(request.protein.sequence)} residues)")
    print(f"    Ligand: {request.ligand.smiles}")
    print()

    # Initialize service
    print("[2] Initializing Boltz service...")
    try:
        service = BoltzService()
        print(f"    ✅ Service initialized")
        print(f"    RunPod enabled: {service.use_runpod}")
        print(f"    RunPod service: {service.runpod_service is not None}")
    except Exception as e:
        print(f"    ❌ Failed to initialize service: {e}")
        import traceback
        traceback.print_exc()
        return
    print()

    # Create job
    print("[3] Creating prediction job...")
    try:
        job_id = service.create_prediction_job(request)
        print(f"    ✅ Job created: {job_id}")
    except Exception as e:
        print(f"    ❌ Failed to create job: {e}")
        import traceback
        traceback.print_exc()
        return
    print()

    # Run prediction
    print("[4] Running prediction...")
    print("    (This will take a few minutes if using RunPod...)")
    print()

    try:
        result = service.run_prediction(job_id, request)
        print(f"    ✅ Prediction completed!")
        print(f"    Status: {result.status}")

        if result.status == "completed":
            print(f"    Affinity: {result.affinity_pred_value}")
            print(f"    Confidence: {result.confidence_score}")
            print(f"    Processing time: {result.processing_time_seconds:.2f}s")
            print(f"    Poses generated: {result.poses_generated}")
        elif result.status == "failed":
            print(f"    ❌ Job failed!")
            print(f"    Error: {result.error_message}")

    except Exception as e:
        print(f"    ❌ Prediction failed with exception: {e}")
        import traceback
        traceback.print_exc()

        # Check job status
        print()
        print("[5] Checking job status...")
        try:
            status = service.get_job_status(job_id)
            if status:
                print(f"    Job status: {status.status}")
                print(f"    Progress: {status.progress}%")

                # Read metadata for more details
                job_dir = service.output_dir / job_id
                metadata_file = job_dir / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                    print(f"    Metadata: {json.dumps(metadata, indent=2)}")
            else:
                print(f"    ❌ Job not found")
        except Exception as status_error:
            print(f"    ❌ Error checking status: {status_error}")

    print()
    print("=" * 70)
    print("  Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_job_submission()
