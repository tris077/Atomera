#!/usr/bin/env python3
"""
Demo script to show Atomera job lifecycle and data output
"""
import requests
import json
import time

def demo_job_lifecycle():
    base_url = "http://localhost:8000"
    
    print("🚀 ATOmera Job Lifecycle Demo")
    print("=" * 50)
    
    # 1. Check system health
    print("\n1. 🔍 Checking system health...")
    try:
        response = requests.get(f"{base_url}/health")
        health_data = response.json()
        print(f"✅ Backend Status: {health_data['status']}")
        print(f"✅ Boltz-2 Available: {health_data['boltz_available']}")
        print(f"✅ Version: {health_data['version']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # 2. Submit a prediction job
    print("\n2. 📝 Submitting prediction job...")
    prediction_request = {
        "protein": {
            "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            "id": "A"
        },
        "ligand": {
            "smiles": "CC1=CC=C(C=C1)C2=NC3=C(C=CC=C3)N2C4=CC=CC=C4",
            "id": "B"
        },
        "use_msa": True,
        "confidence_threshold": 0.5
    }
    
    try:
        response = requests.post(f"{base_url}/predict", json=prediction_request)
        if response.status_code == 200:
            result = response.json()
            job_id = result.get("job_id")
            print(f"✅ Job submitted successfully!")
            print(f"   Job ID: {job_id}")
            print(f"   Status: {result.get('status')}")
            print(f"   Processing Time: {result.get('processing_time_seconds', 0)}s")
        else:
            print(f"❌ Job submission failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Job submission error: {e}")
        return
    
    # 3. Monitor job progress
    print(f"\n3. 👀 Monitoring job progress...")
    print(f"   Job ID: {job_id}")
    
    for i in range(15):  # Monitor for up to 45 seconds
        time.sleep(3)
        try:
            status_response = requests.get(f"{base_url}/jobs/{job_id}")
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"   Status check {i+1}: {status_data['status']} (progress: {status_data.get('progress', 'N/A')}%)")
                
                if status_data['status'] == 'completed':
                    print("✅ Job completed successfully!")
                    break
                elif status_data['status'] == 'failed':
                    print(f"❌ Job failed: {status_data}")
                    return
            else:
                print(f"   Status check {i+1} failed: {status_response.status_code}")
        except Exception as e:
            print(f"   Status check {i+1} error: {e}")
    
    # 4. Retrieve and display results
    print(f"\n4. 📊 Retrieving job results...")
    try:
        result_response = requests.get(f"{base_url}/jobs/{job_id}/result")
        if result_response.status_code == 200:
            result_data = result_response.json()
            print("✅ Results retrieved successfully!")
            print("\n" + "="*50)
            print("🎯 PREDICTION RESULTS")
            print("="*50)
            
            # Core prediction data
            print(f"\n📈 Core Predictions:")
            print(f"   • Affinity (log IC50): {result_data.get('affinity_pred_value', 'N/A')}")
            print(f"   • Binding Probability: {result_data.get('affinity_probability_binary', 'N/A')}")
            print(f"   • Confidence Score: {result_data.get('confidence_score', 'N/A')}")
            print(f"   • ΔG (kcal/mol): {result_data.get('delta_g', 'N/A')}")
            print(f"   • Kd (nM): {result_data.get('kd_nm', 'N/A')}")
            print(f"   • IC50 (nM): {result_data.get('ic50_nm', 'N/A')}")
            
            # Pose information
            print(f"\n🧬 Pose Information:")
            print(f"   • Poses Generated: {result_data.get('poses_generated', 'N/A')}")
            print(f"   • Pose Files: {len(result_data.get('pose_files', []))} files")
            
            # Boltz-2 metrics
            print(f"\n🔬 Boltz-2 Quality Metrics:")
            print(f"   • pTM: {result_data.get('ptm', 'N/A')}")
            print(f"   • Interface pTM: {result_data.get('iptm', 'N/A')}")
            print(f"   • Complex pLDDT: {result_data.get('complex_plddt', 'N/A')}")
            print(f"   • Ligand Interface pTM: {result_data.get('ligand_iptm', 'N/A')}")
            print(f"   • Protein Interface pTM: {result_data.get('protein_iptm', 'N/A')}")
            
            # Pose quality metrics
            print(f"\n🎯 Pose Quality Metrics:")
            print(f"   • RMSD (Å): {result_data.get('rmsd', 'N/A')}")
            print(f"   • H-bond Count: {result_data.get('hbond_count', 'N/A')}")
            print(f"   • Hydrophobic Contacts: {result_data.get('hydrophobic_contacts', 'N/A')}")
            print(f"   • Salt Bridges: {result_data.get('salt_bridges', 'N/A')}")
            print(f"   • π-stacking: {result_data.get('pi_stacking', 'N/A')}")
            print(f"   • SASA Change (Å²): {result_data.get('sasa_change', 'N/A')}")
            print(f"   • Clash Score: {result_data.get('clash_score', 'N/A')}")
            print(f"   • Pocket Volume (Å³): {result_data.get('pocket_volume', 'N/A')}")
            
            # Ligand properties
            print(f"\n💊 Ligand Properties:")
            print(f"   • SMILES: {result_data.get('ligand_smiles', 'N/A')}")
            print(f"   • Name: {result_data.get('ligand_name', 'N/A')}")
            print(f"   • Molecular Weight: {result_data.get('ligand_mw', 'N/A')} g/mol")
            print(f"   • cLogP: {result_data.get('ligand_clogp', 'N/A')}")
            print(f"   • TPSA: {result_data.get('ligand_tpsa', 'N/A')} Å²")
            print(f"   • HBD: {result_data.get('ligand_hbd', 'N/A')}")
            print(f"   • HBA: {result_data.get('ligand_hba', 'N/A')}")
            
            # Target information
            print(f"\n🎯 Target Information:")
            print(f"   • PDB ID: {result_data.get('target_pdb', 'N/A')}")
            print(f"   • UniProt ID: {result_data.get('target_uniprot', 'N/A')}")
            print(f"   • Chain: {result_data.get('target_chain', 'N/A')}")
            print(f"   • Pocket: {result_data.get('target_pocket', 'N/A')}")
            
            # Run information
            print(f"\n⚙️ Run Information:")
            print(f"   • Model Version: {result_data.get('model_version', 'N/A')}")
            print(f"   • Run ID: {result_data.get('run_id', 'N/A')}")
            print(f"   • Device: {result_data.get('device', 'N/A')}")
            print(f"   • Processing Time: {result_data.get('processing_time_seconds', 'N/A')}s")
            print(f"   • Data Completeness: {result_data.get('data_completeness', 'N/A')}%")
            
            # Data quality warnings
            warnings = result_data.get('data_quality_warnings', [])
            if warnings:
                print(f"\n⚠️ Data Quality Warnings:")
                for warning in warnings:
                    print(f"   • {warning}")
            
            print("\n" + "="*50)
            print("🎉 Demo completed successfully!")
            print("="*50)
            
        else:
            print(f"❌ Result retrieval failed: {result_response.status_code}")
    except Exception as e:
        print(f"❌ Result retrieval error: {e}")

if __name__ == "__main__":
    demo_job_lifecycle()
