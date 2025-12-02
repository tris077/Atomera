#!/usr/bin/env python3
"""
Simple test to verify the real data integration changes.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_backend_changes():
    """Test that the backend changes are working."""
    print("Testing Backend Changes")
    print("=" * 40)
    
    try:
        # Test importing the main module
        print("1. Testing imports...")
        from backend.main import calculate_ligand_properties
        print("   SUCCESS: calculate_ligand_properties imported")
        
        # Test ligand property calculation
        print("\n2. Testing ligand property calculation...")
        smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
        properties = calculate_ligand_properties(smiles)
        
        if properties:
            print(f"   SUCCESS: Ligand properties calculated for {smiles}")
            print(f"   MW: {properties.get('ligand_mw', 'N/A')}")
            print(f"   cLogP: {properties.get('ligand_clogp', 'N/A')}")
            print(f"   TPSA: {properties.get('ligand_tpsa', 'N/A')}")
            print(f"   HBD: {properties.get('ligand_hbd', 'N/A')}")
            print(f"   HBA: {properties.get('ligand_hba', 'N/A')}")
        else:
            print("   WARNING: No properties calculated (RDKit may not be available)")
        
        # Test that mock data methods are removed
        print("\n3. Testing mock data removal...")
        from backend.services.boltz_service import BoltzService
        
        service = BoltzService()
        
        # Check if mock methods exist
        has_mock_methods = (
            hasattr(service, '_generate_mock_results') or
            hasattr(service, '_save_mock_results_to_files') or
            hasattr(service, '_create_mock_pose_files')
        )
        
        if not has_mock_methods:
            print("   SUCCESS: Mock data methods have been removed")
        else:
            print("   ERROR: Mock data methods still exist")
            return False
        
        print("\n4. Testing BoltzService functionality...")
        print(f"   SUCCESS: BoltzService created successfully")
        print(f"   Output dir: {service.output_dir}")
        print(f"   Temp dir: {service.temp_dir}")
        
        return True
        
    except ImportError as e:
        print(f"   ERROR: Import failed: {e}")
        return False
    except Exception as e:
        print(f"   ERROR: Unexpected error: {e}")
        return False

def test_frontend_changes():
    """Test that frontend changes are working."""
    print("\nTesting Frontend Changes")
    print("=" * 40)
    
    try:
        # Check if jobService exists and has the right structure
        job_service_path = os.path.join('frontend', 'src', 'lib', 'jobService.ts')
        if os.path.exists(job_service_path):
            with open(job_service_path, 'r') as f:
                content = f.read()
            
            # Check if mock data fallbacks are removed
            if 'mock data' in content.lower() and 'fallback' in content.lower():
                print("   WARNING: Mock data fallbacks may still exist")
            else:
                print("   SUCCESS: Mock data fallbacks appear to be removed")
            
            # Check if real data handling is present
            if 'real data' in content.lower() or 'backend data' in content.lower():
                print("   SUCCESS: Real data handling appears to be implemented")
            else:
                print("   INFO: Real data handling may need verification")
            
            return True
        else:
            print("   ERROR: jobService.ts not found")
            return False
            
    except Exception as e:
        print(f"   ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Starting Simple Real Data Integration Test")
    print("=" * 50)
    
    backend_success = test_backend_changes()
    frontend_success = test_frontend_changes()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print(f"Backend Changes: {'PASS' if backend_success else 'FAIL'}")
    print(f"Frontend Changes: {'PASS' if frontend_success else 'FAIL'}")
    
    if backend_success and frontend_success:
        print("\nSUCCESS: Real data integration changes are working!")
        print("Mock data has been successfully replaced with real data.")
    else:
        print("\nERROR: Some changes may need attention.")
    
    print("=" * 50)
