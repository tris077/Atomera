"""
Pydantic models for Atomera API requests and responses.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
import re


class ProteinSequence(BaseModel):
    """Protein sequence input model."""

    sequence: str = Field(
        ..., description="Protein amino acid sequence", min_length=1, max_length=10000
    )
    id: str = Field(default="A", description="Protein identifier")

    @field_validator("sequence")
    @classmethod
    def validate_sequence(cls, v):
        """Validate that sequence contains only valid amino acid codes."""
        if not v or not v.strip():
            raise ValueError("Protein sequence cannot be empty")

        # Convert to uppercase and remove whitespace
        v = v.upper().strip()

        # Check if it's a PDB ID (4-character alphanumeric)
        if len(v) == 4 and v.isalnum():
            # Allow PDB IDs for now (we can expand this later)
            return v

        # Check if it's a valid amino acid sequence
        valid_aa = set("ACDEFGHIKLMNPQRSTVWY")
        invalid_chars = set(v) - valid_aa

        if invalid_chars:
            raise ValueError(
                f'Invalid amino acid characters found: {", ".join(sorted(invalid_chars))}. Valid characters are: {", ".join(sorted(valid_aa))}'
            )

        return v


class LigandMolecule(BaseModel):
    """Ligand molecule input model."""

    smiles: str = Field(
        ...,
        description="SMILES string representation of the ligand",
        min_length=1,
        max_length=1000,
    )
    id: str = Field(default="B", description="Ligand identifier")

    @field_validator("smiles")
    @classmethod
    def validate_smiles(cls, v):
        """Basic SMILES validation."""
        if not v or not v.strip():
            raise ValueError("SMILES string cannot be empty")

        v = v.strip()

        # More permissive SMILES validation
        if not re.match(r"^[A-Za-z0-9@+\-\[\]\(\)=#$%:\.]+$", v):
            raise ValueError(
                "Invalid SMILES string format. Only alphanumeric characters and common chemical symbols are allowed."
            )

        return v


class PredictionRequest(BaseModel):
    """Request model for binding affinity prediction."""

    protein: ProteinSequence
    ligand: LigandMolecule
    use_msa: bool = Field(
        default=True, description="Whether to use MSA server for protein analysis"
    )
    confidence_threshold: Optional[float] = Field(
        default=0.5, description="Confidence threshold for predictions", ge=0.0, le=1.0
    )


class PredictionResult(BaseModel):
    """Result model for binding affinity prediction."""
    
    model_config = {"protected_namespaces": ()}

    job_id: str
    status: str
    affinity_pred_value: Optional[float] = Field(
        None, description="Predicted binding affinity (log(IC50))"
    )
    affinity_probability_binary: Optional[float] = Field(
        None, description="Probability of binding (0-1)"
    )
    confidence_score: Optional[float] = Field(
        None, description="Model confidence in the prediction"
    )
    processing_time_seconds: Optional[float] = Field(
        None, description="Time taken for prediction"
    )
    poses_generated: Optional[int] = Field(
        None, description="Number of poses generated"
    )
    pose_files: Optional[List[str]] = Field(None, description="List of pose file names")
    error_message: Optional[str] = Field(
        None, description="Error message if prediction failed"
    )

    # Extended data for comprehensive display
    kd_nm: Optional[float] = Field(None, description="Predicted Kd in nM")
    ki_nm: Optional[float] = Field(None, description="Predicted Ki in nM")
    ic50_nm: Optional[float] = Field(None, description="Predicted IC50 in nM")
    delta_g: Optional[float] = Field(None, description="Predicted ΔG in kcal/mol")
    confidence_interval_95: Optional[List[float]] = Field(
        None, description="95% confidence interval"
    )
    sigma: Optional[float] = Field(None, description="Prediction uncertainty")

    # Pose quality metrics
    rmsd: Optional[float] = Field(None, description="RMSD in Å")
    hbond_count: Optional[int] = Field(None, description="Number of hydrogen bonds")
    hydrophobic_contacts: Optional[int] = Field(
        None, description="Number of hydrophobic contacts"
    )
    salt_bridges: Optional[int] = Field(None, description="Number of salt bridges")
    pi_stacking: Optional[int] = Field(
        None, description="Number of π-stacking interactions"
    )
    sasa_change: Optional[float] = Field(None, description="SASA change in Å²")
    clash_score: Optional[float] = Field(None, description="Clash score")
    pocket_volume: Optional[float] = Field(None, description="Pocket volume in Å³")
    polarity_index: Optional[float] = Field(None, description="Pocket polarity index")

    # Residue hotspots
    residue_hotspots: Optional[List[dict]] = Field(
        None, description="Residue hotspot contributions"
    )

    # Ligand properties
    ligand_smiles: Optional[str] = Field(None, description="Ligand SMILES string")
    ligand_name: Optional[str] = Field(None, description="Ligand name/ID")
    ligand_mw: Optional[float] = Field(
        None, description="Ligand molecular weight in g/mol"
    )
    ligand_clogp: Optional[float] = Field(None, description="Ligand cLogP")
    ligand_tpsa: Optional[float] = Field(None, description="Ligand TPSA in Å²")
    ligand_hbd: Optional[int] = Field(None, description="Ligand H-bond donors")
    ligand_hba: Optional[int] = Field(None, description="Ligand H-bond acceptors")
    ligand_rotatable_bonds: Optional[int] = Field(
        None, description="Ligand rotatable bonds"
    )
    ligand_formal_charge: Optional[int] = Field(
        None, description="Ligand formal charge"
    )
    ligand_ring_count: Optional[int] = Field(None, description="Ligand ring count")
    ligand_rule_of_five_violations: Optional[List[str]] = Field(
        None, description="Rule of Five violations"
    )

    # Target & run info
    target_pdb: Optional[str] = Field(None, description="Target PDB ID")
    target_uniprot: Optional[str] = Field(None, description="Target UniProt ID")
    target_chain: Optional[str] = Field(None, description="Target chain ID")
    target_pocket: Optional[str] = Field(None, description="Target pocket description")
    model_version: Optional[str] = Field(None, description="Model version")
    run_id: Optional[str] = Field(None, description="Run ID")
    submitted_at: Optional[str] = Field(None, description="Submission timestamp")
    completed_at: Optional[str] = Field(None, description="Completion timestamp")
    device: Optional[str] = Field(None, description="Computing device used")
    total_runtime: Optional[float] = Field(None, description="Total runtime in seconds")
    data_quality_warnings: Optional[List[str]] = Field(
        None, description="Data quality warnings"
    )
    data_completeness: Optional[float] = Field(
        None, description="Data completeness percentage"
    )
    pocket_detection_method: Optional[str] = Field(
        None, description="Pocket detection method"
    )

    # Additional Boltz-2 metrics
    iptm: Optional[float] = Field(None, description="Interface pTM score")
    complex_plddt: Optional[float] = Field(None, description="Complex pLDDT score")
    ptm: Optional[float] = Field(None, description="pTM score")
    ligand_iptm: Optional[float] = Field(None, description="Ligand interface pTM")
    protein_iptm: Optional[float] = Field(None, description="Protein interface pTM")
    complex_iplddt: Optional[float] = Field(None, description="Complex interface pLDDT")
    complex_pde: Optional[float] = Field(None, description="Complex PDE score")
    complex_ipde: Optional[float] = Field(None, description="Complex interface PDE")


class JobStatus(BaseModel):
    """Job status information."""

    job_id: str
    status: str  # "pending", "running", "completed", "failed"
    created_at: str
    updated_at: str
    progress: Optional[float] = Field(None, description="Progress percentage (0-100)")
    estimated_completion: Optional[str] = Field(
        None, description="Estimated completion time"
    )


class HealthCheck(BaseModel):
    """Health check response."""

    status: str
    version: str
    boltz_available: bool
    timestamp: str


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    detail: Optional[str] = None
    job_id: Optional[str] = None
