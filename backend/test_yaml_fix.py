#!/usr/bin/env python3
"""Test the fixed YAML generation."""

from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule

def test_yaml_generation():
    """Test YAML generation with fixed chain IDs."""
    # Create a test service
    service = BoltzService()
    
    # Create a test request
    request = PredictionRequest(
        protein=ProteinSequence(id='test_protein', sequence='MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT'),
        ligand=LigandMolecule(id='test_ligand', smiles='CC(=O)OC1=CC=CC=C1C(=O)O'),
        use_msa=True,
        confidence_threshold=0.5
    )
    
    # Test YAML creation
    yaml_file = service._create_input_yaml('test_job', request)
    print(f'Created YAML: {yaml_file}')
    
    with open(yaml_file, 'r') as f:
        print(f'YAML content:\n{f.read()}')
    
    return yaml_file

if __name__ == "__main__":
    test_yaml_generation()
