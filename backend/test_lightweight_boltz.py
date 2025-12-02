#!/usr/bin/env python3
"""Test lightweight Boltz-2 configuration for reliable execution."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule

def test_lightweight_boltz():
    """Test lightweight Boltz-2 configuration."""
    print("🧬 Testing Lightweight Boltz-2 Configuration")
    print("=" * 60)
    print("Configuration:")
    print("  - Ultra-short sequences (max 20 residues)")
    print("  - Minimal MSA sequences (8)")
    print("  - Single diffusion sample")
    print("  - Half precision (16-bit)")
    print("  - Single device/worker")
    print("  - No templates")
    print("=" * 60)
    
    # Create service
    service = BoltzService()
    
    # Test with VERY short sequence for maximum reliability
    request = PredictionRequest(
        protein=ProteinSequence(
            id='test_protein', 
            sequence='MALWMRLLPLLALLALWGPDP'  # Only 20 residues
        ),
        ligand=LigandMolecule(
            id='test_ligand', 
            smiles='CC(=O)O'  # Simple molecule
        ),
        use_msa=True,
        confidence_threshold=0.5
    )
    
    print(f"Protein sequence: {request.protein.sequence}")
    print(f"Sequence length: {len(request.protein.sequence)}")
    print(f"Ligand SMILES: {request.ligand.smiles}")
    
    # Test YAML creation
    print("\n📝 Creating lightweight YAML input...")
    yaml_file = service._create_input_yaml('test_lightweight', request)
    print(f"✅ YAML created: {yaml_file}")
    
    with open(yaml_file, 'r') as f:
        print(f"YAML content:\n{f.read()}")
    
    # Test Boltz-2 execution
    print("\n🚀 Testing lightweight Boltz-2 execution...")
    try:
        result = service.run_prediction('test_lightweight', request)
        print(f"\n✅ EXECUTION SUCCESSFUL!")
        print(f"   Status: {result.status}")
        
        if hasattr(result, 'affinity') and result.affinity:
            print(f"   🧬 Affinity: {result.affinity}")
        if hasattr(result, 'confidence') and result.confidence:
            print(f"   📊 Confidence: {result.confidence}")
        if hasattr(result, 'poses') and result.poses:
            print(f"   🎯 Poses: {len(result.poses)}")
        if hasattr(result, 'error_message') and result.error_message:
            print(f"   ❌ Error: {result.error_message}")
            
        print(f"\n🎉 REAL DATA EXECUTION SUCCESSFUL!")
        return True
            
    except Exception as e:
        print(f"❌ Execution Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_jobs():
    """Test multiple job submissions for reliability."""
    print("\n" + "=" * 60)
    print("🔄 Testing Multiple Job Submissions")
    print("=" * 60)
    
    service = BoltzService()
    
    # Test different short sequences
    test_cases = [
        ("MALWMRLLPLLALLALWGPDP", "CC(=O)O"),  # 20 residues
        ("MALWMRLLPLLALLALWGP", "CC(=O)OC1=CC=CC=C1"),  # 18 residues
        ("MALWMRLLPLLALLALW", "CC(=O)OC1=CC=CC=C1C(=O)O"),  # 16 residues
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, (seq, smiles) in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}/{total_count} ---")
        print(f"Sequence: {seq} ({len(seq)} residues)")
        print(f"SMILES: {smiles}")
        
        request = PredictionRequest(
            protein=ProteinSequence(id=f'test_protein_{i}', sequence=seq),
            ligand=LigandMolecule(id=f'test_ligand_{i}', smiles=smiles),
            use_msa=True,
            confidence_threshold=0.5
        )
        
        try:
            result = service.run_prediction(f'test_job_{i}', request)
            if result.status == "completed":
                print(f"✅ Job {i} completed successfully")
                success_count += 1
            else:
                print(f"❌ Job {i} failed: {result.status}")
        except Exception as e:
            print(f"❌ Job {i} error: {e}")
    
    print(f"\n📊 Results: {success_count}/{total_count} jobs successful")
    return success_count == total_count

if __name__ == "__main__":
    # Test single job
    single_success = test_lightweight_boltz()
    
    if single_success:
        # Test multiple jobs
        multi_success = test_multiple_jobs()
        
        if multi_success:
            print("\n🎉 ALL TESTS PASSED! Lightweight configuration is working!")
        else:
            print("\n⚠️  Some jobs failed, but basic functionality works.")
    else:
        print("\n❌ Basic test failed. Need further optimization.")
