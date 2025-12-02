"""
Test the RunPod handler locally to verify it works before building Docker image.
"""

import sys
import json
import base64
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the handler
from runpod_handler_template import handler


def test_handler():
    """Test the handler with minimal input."""
    print("=" * 70)
    print("  Testing RunPod Handler Locally")
    print("=" * 70)
    print()

    # Create minimal test YAML
    test_yaml = """version: 1
sequences:
  - protein:
      id: A
      sequence: "MKFLKFSLLTAVLLSVVFAFSSCGDDDDTGYLPPSQAIQDLLKRMKV"
  - ligand:
      id: B
      smiles: "CCO"
properties:
  - affinity:
      binder: B
"""

    # Encode as base64
    yaml_b64 = base64.b64encode(test_yaml.encode("utf-8")).decode("utf-8")

    # Create test event
    event = {
        "input": {
            "job_id": "test-123",
            "input_yaml": yaml_b64,
            "request_data": {
                "protein": {"id": "A", "sequence": "MKFLKFSLLTAVLLSVVFAFSSCGDDDDTGYLPPSQAIQDLLKRMKV"},
                "ligand": {"id": "B", "smiles": "CCO"}
            },
            "config": {
                "devices": 1,
                "accelerator": "cpu",  # Use CPU for local test
                "diffusion_samples": 1,
                "use_msa_server": False  # Disable MSA server for local test
            }
        }
    }

    print("[1] Test Event Created")
    print(f"    Job ID: {event['input']['job_id']}")
    print(f"    Config: {event['input']['config']}")
    print()

    print("[2] Calling Handler...")
    print()

    try:
        result = handler(event)

        print()
        print("[3] Handler Response:")
        print(json.dumps(result, indent=2, default=str)[:500])
        print()

        if "error" in result:
            print("❌ Handler returned error:")
            print(f"   {result['error']}")
            return False
        else:
            print("✅ Handler executed successfully!")
            print(f"   Affinity: {result.get('affinity_pred_value')}")
            print(f"   Confidence: {result.get('confidence_score')}")
            print(f"   Poses: {len(result.get('pose_files', {}))}")
            return True

    except Exception as e:
        print()
        print("❌ Handler threw exception:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print()
    success = test_handler()
    print()
    print("=" * 70)
    if success:
        print("  ✅ Test PASSED - Handler is working!")
    else:
        print("  ❌ Test FAILED - Fix handler before building Docker image")
    print("=" * 70)
    print()
    sys.exit(0 if success else 1)
