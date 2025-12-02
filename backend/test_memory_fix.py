#!/usr/bin/env python3
"""Test memory-optimized Boltz-2 execution."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule

def test_memory_optimized_boltz():
    """Test memory-optimized Boltz-2 execution."""
    print("🧬 Testing Memory-Optimized Boltz-2 Execution")
    print("=" * 60)
    
    # Create service
    service = BoltzService()
    
    # Create request with SHORT sequence to minimize memory usage
    request = PredictionRequest(
        protein=ProteinSequence(
            id='test_protein', 
            sequence='MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT'  # 54 residues
        ),
        ligand=LigandMolecule(
            id='test_ligand', 
            smiles='CC(=O)OC1=CC=CC=C1C(=O)O'  # Simple aspirin-like molecule
        ),
        use_msa=True,
        confidence_threshold=0.5
    )
    
    print(f"Protein sequence: {request.protein.sequence}")
    print(f"Sequence length: {len(request.protein.sequence)}")
    print(f"Ligand SMILES: {request.ligand.smiles}")
    
    # Test YAML creation
    print("\n📝 Creating memory-optimized YAML input...")
    yaml_file = service._create_input_yaml('test_memory_job', request)
    print(f"✅ YAML created: {yaml_file}")
    
    with open(yaml_file, 'r') as f:
        print(f"YAML content:\n{f.read()}")
    
    # Test Boltz-2 execution with memory optimizations
    print("\n🚀 Testing memory-optimized Boltz-2 execution...")
    print("   - Using minimal diffusion samples (1)")
    print("   - Limited MSA sequences (32)")
    print("   - Single device")
    print("   - Truncated sequence if needed")
    print("   - Memory-optimized environment variables")
    
    try:
        result = service.run_prediction('test_memory_job', request)
        print(f"\n✅ Result Status: {result.status}")
        
        if hasattr(result, 'affinity') and result.affinity:
            print(f"   🧬 Affinity: {result.affinity}")
        if hasattr(result, 'confidence') and result.confidence:
            print(f"   📊 Confidence: {result.confidence}")
        if hasattr(result, 'poses') and result.poses:
            print(f"   🎯 Poses: {len(result.poses)}")
        if hasattr(result, 'error_message') and result.error_message:
            print(f"   ❌ Error: {result.error_message}")
            
    except Exception as e:
        print(f"❌ Execution Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_memory_optimized_boltz()
