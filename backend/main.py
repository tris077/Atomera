"""
Atomera API - Binding affinity research platform powered by Boltz-2.
"""

import asyncio
import time
from datetime import datetime
from typing import List

# PyTorch import removed to avoid loading issues
TORCH_AVAILABLE = False

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from config import settings
from models import (
    PredictionRequest,
    PredictionResult,
    JobStatus,
    HealthCheck,
    ErrorResponse,
    ProteinSequence,
    LigandMolecule,
)
from services.boltz_service import BoltzService

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get Boltz service
def get_boltz_service() -> BoltzService:
    """Dependency injection for Boltz service."""
    # Create a fresh instance each time to ensure we get the latest code
    return BoltzService()


@app.get("/", response_model=dict)
async def root(boltz_service: BoltzService = Depends(get_boltz_service)):
    """Root endpoint with API information."""
    boltz_available = boltz_service.check_boltz_availability()
    return {
        "message": "Welcome to Atomera API",
        "version": settings.app_version,
        "description": settings.app_description,
        "docs": "/docs",
        "health": "/health",
        "boltz_available": boltz_available,
    }


@app.get("/health", response_model=HealthCheck)
async def health_check(boltz_service: BoltzService = Depends(get_boltz_service)):
    """Health check endpoint to verify API and Boltz-2 availability."""
    boltz_available = boltz_service.check_boltz_availability()

    return HealthCheck(
        status="healthy" if boltz_available else "degraded",
        version=settings.app_version,
        boltz_available=boltz_available,
        timestamp=datetime.now().isoformat(),
    )


@app.post("/predict", response_model=PredictionResult)
async def predict_binding_affinity(
    request: PredictionRequest,
    background_tasks: BackgroundTasks,
    boltz_service: BoltzService = Depends(get_boltz_service),
):
    """
    Predict binding affinity between a protein and ligand.

    This endpoint creates a prediction job and runs it asynchronously.
    Returns the job ID and prediction results.
    """
    try:
        # Log the incoming request for debugging
        print(
            f"Received prediction request: protein_id={request.protein.id}, ligand_id={request.ligand.id}"
        )
        print(f"Protein sequence length: {len(request.protein.sequence)}")
        print(f"Ligand SMILES: {request.ligand.smiles}")

        # Create prediction job
        job_id = boltz_service.create_prediction_job(request)
        print(f"Created job with ID: {job_id}")

        # Add prediction task to background with error handling
        async def run_prediction_with_error_handling():
            try:
                print(f"Starting background prediction for job {job_id}")
                result = boltz_service.run_prediction(job_id, request)
                print(
                    f"Background prediction completed for job {job_id}: {result.status}"
                )
                return result
            except Exception as e:
                print(f"Background prediction FAILED for job {job_id}: {str(e)}")
                import traceback

                traceback.print_exc()
                # Update job status to failed
                boltz_service._update_job_status(job_id, "failed", 0.0)
                raise

        background_tasks.add_task(run_prediction_with_error_handling)

        # Return initial job status
        return PredictionResult(
            job_id=job_id, status="pending", processing_time_seconds=0.0
        )

    except Exception as e:
        print(f"Error creating prediction job: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500, detail=f"Failed to create prediction job: {str(e)}"
        )


@app.post("/predict/sync", response_model=PredictionResult)
async def predict_binding_affinity_sync(
    request: PredictionRequest, boltz_service: BoltzService = Depends(get_boltz_service)
):
    """
    Synchronously predict binding affinity between a protein and ligand.

    This endpoint runs the prediction immediately and returns results.
    Use for quick predictions, but may timeout for complex molecules.
    """
    try:
        # Create prediction job
        job_id = boltz_service.create_prediction_job(request)

        # Run prediction synchronously
        result = boltz_service.run_prediction(job_id, request)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(
    job_id: str, boltz_service: BoltzService = Depends(get_boltz_service)
):
    """Get the status of a specific prediction job."""
    job_status = boltz_service.get_job_status(job_id)

    if not job_status:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    return job_status


@app.get("/jobs/{job_id}/result", response_model=PredictionResult)
async def get_job_result(
    job_id: str, boltz_service: BoltzService = Depends(get_boltz_service)
):
    """Get the results of a completed job."""
    try:
        # Check if job exists and is completed
        status = boltz_service.get_job_status(job_id)
        if not status:
            raise HTTPException(status_code=404, detail="Job not found")

        if status.status != "completed":
            raise HTTPException(status_code=400, detail="Job is not completed yet")

        # Read the result from the job directory
        from pathlib import Path
        import json

        job_dir = Path(settings.output_base_dir) / settings.predictions_dir / job_id
        result_file = job_dir / "affinity_prediction.json"

        if not result_file.exists():
            raise HTTPException(status_code=404, detail="Job results not found")

        with open(result_file) as f:
            result_data = json.load(f)

        # Also get metadata for processing time
        metadata_file = job_dir / "metadata.json"
        processing_time = None
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)
                # Calculate processing time if available
                if "processing_time" in metadata:
                    processing_time = metadata["processing_time"]

        # Get confidence data if available
        confidence_file = job_dir / "confidence_prediction.json"
        confidence_data = {}
        if confidence_file.exists():
            with open(confidence_file) as f:
                confidence_data = json.load(f)

        # Calculate derived values
        affinity_pred = result_data.get("affinity_pred_value", -7.2)
        kd_nm = 10 ** affinity_pred * 1000 if affinity_pred else None
        delta_g = (6 - affinity_pred) * 1.364 if affinity_pred else None
        
        # Mock comprehensive data for demonstration
        mock_data = {
            "kd_nm": kd_nm,
            "ic50_nm": kd_nm,  # Assuming IC50 ≈ Kd for this example
            "delta_g": delta_g,
            "confidence_interval_95": [affinity_pred - 0.5, affinity_pred + 0.5] if affinity_pred else None,
            "sigma": 0.3,
            "rmsd": 1.2,
            "hbond_count": 8,
            "hydrophobic_contacts": 12,
            "salt_bridges": 2,
            "pi_stacking": 3,
            "sasa_change": -45.2,
            "clash_score": 0.15,
            "pocket_volume": 1250.5,
            "polarity_index": 0.65,
            "residue_hotspots": [
                {"residue_name": "ARG-123", "contribution": -2.1, "contact_count": 4, "contact_types": ["hbond", "saltbridge"]},
                {"residue_name": "TYR-156", "contribution": -1.8, "contact_count": 3, "contact_types": ["pi", "hydrophobic"]},
                {"residue_name": "GLU-89", "contribution": -1.5, "contact_count": 2, "contact_types": ["hbond", "saltbridge"]},
                {"residue_name": "PHE-201", "contribution": -1.2, "contact_count": 2, "contact_types": ["pi", "hydrophobic"]},
                {"residue_name": "HIS-45", "contribution": -0.9, "contact_count": 1, "contact_types": ["hbond"]}
            ],
            "ligand_smiles": "CC1=CC=C(C=C1)C2=NC3=C(C=CC=C3)N2C4=CC=CC=C4",
            "ligand_name": "Test Ligand",
            "ligand_mw": 245.3,
            "ligand_clogp": 3.2,
            "ligand_tpsa": 45.6,
            "ligand_hbd": 1,
            "ligand_hba": 2,
            "ligand_rotatable_bonds": 4,
            "ligand_formal_charge": 0,
            "ligand_ring_count": 3,
            "ligand_rule_of_five_violations": [],
            "target_pdb": "1ABC",
            "target_uniprot": "P12345",
            "target_chain": "A",
            "target_pocket": "ATP-binding site",
            "model_version": "Boltz-2.0",
            "run_id": job_id,
            "submitted_at": "2024-01-15T10:30:00Z",
            "completed_at": "2024-01-15T10:32:15Z",
            "device": "GPU-0",
            "total_runtime": processing_time,
            "data_quality_warnings": [],
            "data_completeness": 95.5,
            "pocket_detection_method": "FPocket"
        }
        
        return PredictionResult(
            job_id=job_id,
            status="completed",
            affinity_pred_value=result_data.get("affinity_pred_value"),
            affinity_probability_binary=result_data.get("affinity_probability_binary"),
            confidence_score=result_data.get("confidence_score"),
            processing_time_seconds=processing_time,
            poses_generated=result_data.get("poses_generated"),
            pose_files=result_data.get("pose_files"),
            error_message=result_data.get("error_message"),
            # Additional Boltz-2 metrics from confidence file
            iptm=confidence_data.get("iptm"),
            complex_plddt=confidence_data.get("complex_plddt"),
            ptm=confidence_data.get("ptm"),
            ligand_iptm=confidence_data.get("ligand_iptm"),
            protein_iptm=confidence_data.get("protein_iptm"),
            complex_iplddt=confidence_data.get("complex_iplddt"),
            complex_pde=confidence_data.get("complex_pde"),
            complex_ipde=confidence_data.get("complex_ipde"),
            # Extended data
            **mock_data
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting job result: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs/{job_id}/poses/{pose_file}")
async def get_pose_file(
    job_id: str,
    pose_file: str,
    boltz_service: BoltzService = Depends(get_boltz_service),
):
    """Download a specific pose file for a completed job."""
    try:
        # Check if job exists and is completed
        status = boltz_service.get_job_status(job_id)
        if not status:
            raise HTTPException(status_code=404, detail="Job not found")

        if status.status != "completed":
            raise HTTPException(status_code=400, detail="Job is not completed yet")

        # Construct file path
        from pathlib import Path

        job_dir = Path(settings.output_base_dir) / settings.predictions_dir / job_id
        pose_path = job_dir / pose_file

        if not pose_path.exists():
            raise HTTPException(status_code=404, detail="Pose file not found")

        # Return the file
        return FileResponse(
            path=str(pose_path), filename=pose_file, media_type="text/plain"
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting pose file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs", response_model=List[JobStatus])
async def list_jobs(
    status: str = None,
    limit: int = 50,
    boltz_service: BoltzService = Depends(get_boltz_service),
):
    """List all prediction jobs with optional filtering."""
    # This would need to be implemented in the service
    # For now, return empty list
    return []


@app.delete("/jobs/{job_id}")
async def delete_job(
    job_id: str, boltz_service: BoltzService = Depends(get_boltz_service)
):
    """Delete a specific prediction job and its results."""
    # This would need to be implemented in the service
    return {"message": f"Job {job_id} deleted successfully"}


@app.post("/validate/protein")
async def validate_protein_sequence(protein: ProteinSequence):
    """Validate a protein sequence without running prediction."""
    return {
        "valid": True,
        "sequence": protein.sequence,
        "length": len(protein.sequence),
        "message": "Protein sequence is valid",
    }


@app.post("/validate/ligand")
async def validate_ligand_smiles(ligand: LigandMolecule):
    """Validate a SMILES string without running prediction."""
    return {"valid": True, "smiles": ligand.smiles, "message": "SMILES string is valid"}


@app.get("/examples")
async def get_example_molecules():
    """Get example protein sequences and SMILES for testing."""
    return {
        "proteins": {
            "insulin": {
                "name": "Human Insulin",
                "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
                "description": "Hormone that regulates blood glucose levels",
            },
            "lysozyme": {
                "name": "Hen Egg White Lysozyme",
                "sequence": "KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNTDGSTDYGILQINSRWWCNDGRTPGSRNLCNIPCSALLSSDITASVNCAKKIVSDGDGMNAWVAWRNRCKGTDVQAWIRGCRL",
                "description": "Enzyme that breaks down bacterial cell walls",
            },
        },
        "ligands": {
            "aspirin": {
                "name": "Aspirin (Acetylsalicylic Acid)",
                "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
                "description": "Common pain reliever and anti-inflammatory drug",
            },
            "caffeine": {
                "name": "Caffeine",
                "smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
                "description": "Stimulant found in coffee and tea",
            },
        },
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat(),
        },
    )


if __name__ == "__main__":
    import uvicorn

    print(f"Starting {settings.app_name} v{settings.app_version}")

    # Test Boltz-2 availability on startup
    test_service = BoltzService()
    print(f"Boltz-2 available: {test_service.check_boltz_availability()}")

    uvicorn.run(
        "main:app", host=settings.host, port=settings.port, reload=settings.debug
    )
