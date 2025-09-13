"""
Pydantic models for Atomera API requests and responses.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
import re


class ProteinSequence(BaseModel):
    """Protein sequence input model."""
    sequence: str = Field(..., description="Protein amino acid sequence", min_length=1, max_length=10000)
    id: str = Field(default="A", description="Protein identifier")
    
    @field_validator('sequence')
    @classmethod
    def validate_sequence(cls, v):
        """Validate that sequence contains only valid amino acid codes."""
        if not v or not v.strip():
            raise ValueError('Protein sequence cannot be empty')
        
        # Convert to uppercase and remove whitespace
        v = v.upper().strip()
        
        # Check if it's a PDB ID (4-character alphanumeric)
        if len(v) == 4 and v.isalnum():
            # Allow PDB IDs for now (we can expand this later)
            return v
        
        # Check if it's a valid amino acid sequence
        valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
        invalid_chars = set(v) - valid_aa
        
        if invalid_chars:
            raise ValueError(f'Invalid amino acid characters found: {", ".join(sorted(invalid_chars))}. Valid characters are: {", ".join(sorted(valid_aa))}')
        
        return v


class LigandMolecule(BaseModel):
    """Ligand molecule input model."""
    smiles: str = Field(..., description="SMILES string representation of the ligand", min_length=1, max_length=1000)
    id: str = Field(default="B", description="Ligand identifier")
    
    @field_validator('smiles')
    @classmethod
    def validate_smiles(cls, v):
        """Basic SMILES validation."""
        if not v or not v.strip():
            raise ValueError('SMILES string cannot be empty')
        
        v = v.strip()
        
        # More permissive SMILES validation
        if not re.match(r'^[A-Za-z0-9@+\-\[\]\(\)=#$%:\.]+$', v):
            raise ValueError('Invalid SMILES string format. Only alphanumeric characters and common chemical symbols are allowed.')
        
        return v


class PredictionRequest(BaseModel):
    """Request model for binding affinity prediction."""
    protein: ProteinSequence
    ligand: LigandMolecule
    use_msa: bool = Field(default=True, description="Whether to use MSA server for protein analysis")
    confidence_threshold: Optional[float] = Field(default=0.5, description="Confidence threshold for predictions", ge=0.0, le=1.0)


class PredictionResult(BaseModel):
    """Result model for binding affinity prediction."""
    job_id: str
    status: str
    affinity_pred_value: Optional[float] = Field(None, description="Predicted binding affinity (log(IC50))")
    affinity_probability_binary: Optional[float] = Field(None, description="Probability of binding (0-1)")
    confidence_score: Optional[float] = Field(None, description="Model confidence in the prediction")
    processing_time_seconds: Optional[float] = Field(None, description="Time taken for prediction")
    poses_generated: Optional[int] = Field(None, description="Number of poses generated")
    pose_files: Optional[List[str]] = Field(None, description="List of pose file names")
    error_message: Optional[str] = Field(None, description="Error message if prediction failed")


class JobStatus(BaseModel):
    """Job status information."""
    job_id: str
    status: str  # "pending", "running", "completed", "failed"
    created_at: str
    updated_at: str
    progress: Optional[float] = Field(None, description="Progress percentage (0-100)")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time")


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
