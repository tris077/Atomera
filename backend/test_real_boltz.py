#!/usr/bin/env python3
"""Test real Boltz-2 execution with fixed YAML."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule

def test_real_boltz():
    """Test real Boltz-2 execution."""
    print("🧬 Testing Real Boltz-2 Execution")
    print("=" * 50)
    
    # Create service
    service = BoltzService()
    
    # Create request with short sequence to reduce memory usage
    request = PredictionRequest(
        protein=ProteinSequence(
            id='test_protein', 
            sequence='MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT'
        ),
        ligand=LigandMolecule(
            id='test_ligand', 
            smiles='CC(=O)OC1=CC=CC=C1C(=O)O'
        ),
        use_msa=True,
        confidence_threshold=0.5
    )
    
    print(f"Protein sequence: {request.protein.sequence}")
    print(f"Ligand SMILES: {request.ligand.smiles}")
    
    # Test YAML creation
    print("\n📝 Creating YAML input...")
    yaml_file = service._create_input_yaml('test_real_job', request)
    print(f"✅ YAML created: {yaml_file}")
    
    with open(yaml_file, 'r') as f:
        print(f"YAML content:\n{f.read()}")
    
    # Test Boltz-2 execution
    print("\n🚀 Testing Boltz-2 execution...")
    try:
        result = service.run_prediction('test_real_job', request)
        print(f"✅ Result: {result.status}")
        if hasattr(result, 'affinity'):
            print(f"   Affinity: {result.affinity}")
        if hasattr(result, 'error_message'):
            print(f"   Error: {result.error_message}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_boltz()
