# Atomera Field Mapping Specification

## Backend → Frontend Field Mapping

### Core Prediction Fields (Highest Priority)

| Backend Field | Frontend Field | UI Label | Type | Units | Required | Default/Placeholder |
|---------------|----------------|----------|------|-------|----------|-------------------|
| `affinity_pred_value` | `affinity_pred_value` | "Predicted Kd" | number | nM | ✅ | "N/A" |
| `delta_g` | `delta_g` | "ΔG" | number | kcal/mol | ✅ | "N/A" |
| `affinity_probability_binary` | `affinity_probability_binary` | "Binding Probability" | number | % | ✅ | "N/A" |
| `confidence_score` | `confidence_score` | "Confidence" | number | % | ✅ | "N/A" |
| `confidence_interval_95` | `confidence_interval_95` | "95% Confidence Interval" | [number, number] | nM | ❌ | null |
| `sigma` | `sigma` | "Uncertainty" | number | ±nM | ❌ | null |

### Identifiers (High Priority)

| Backend Field | Frontend Field | UI Label | Type | Required | Default/Placeholder |
|---------------|----------------|----------|------|----------|-------------------|
| `target_pdb` | `target_pdb` | "PDB ID" | string | ❌ | "N/A" |
| `target_uniprot` | `target_uniprot` | "UniProt ID" | string | ❌ | "N/A" |
| `ligand_smiles` | `ligand_smiles` | "SMILES" | string | ✅ | "N/A" |
| `ligand_name` | `ligand_name` | "Ligand Name" | string | ❌ | "N/A" |

### Provenance (High Priority)

| Backend Field | Frontend Field | UI Label | Type | Required | Default/Placeholder |
|---------------|----------------|----------|------|----------|-------------------|
| `model_version` | `model_version` | "Model Version" | string | ✅ | "Boltz-2.0" |
| `run_id` | `run_id` | "Run ID" | string | ✅ | job_id |
| `submitted_at` | `submitted_at` | "Submitted" | string | ✅ | created_at |
| `completed_at` | `completed_at` | "Completed" | string | ✅ | updated_at |
| `device` | `device` | "Device" | string | ❌ | "N/A" |

### Pose Information (High Priority)

| Backend Field | Frontend Field | UI Label | Type | Required | Default/Placeholder |
|---------------|----------------|----------|------|----------|-------------------|
| `poses_generated` | `poses_generated` | "Poses Generated" | number | ✅ | 0 |
| `pose_files` | `pose_files` | "Pose Files" | string[] | ✅ | [] |
| `rmsd` | `rmsd` | "RMSD" | number | Å | ❌ | "N/A" |
| `hbond_count` | `hbond_count` | "H-bond Count" | number | ❌ | "N/A" |
| `hydrophobic_contacts` | `hydrophobic_contacts` | "Hydrophobic Contacts" | number | ❌ | "N/A" |
| `salt_bridges` | `salt_bridges` | "Salt Bridges" | number | ❌ | "N/A" |
| `pi_stacking` | `pi_stacking` | "π-stacking" | number | ❌ | "N/A" |

### Flags & Warnings (High Priority)

| Backend Field | Frontend Field | UI Label | Type | Required | Default/Placeholder |
|---------------|----------------|----------|------|----------|-------------------|
| `data_quality_warnings` | `data_quality_warnings` | "Data Quality Warnings" | string[] | ❌ | [] |
| `error_message` | `error_message` | "Error Message" | string | ❌ | null |
| `data_completeness` | `data_completeness` | "Data Completeness" | number | % | ❌ | "N/A" |

### Throughput & Timing (Medium Priority)

| Backend Field | Frontend Field | UI Label | Type | Required | Default/Placeholder |
|---------------|----------------|----------|------|----------|-------------------|
| `processing_time_seconds` | `processing_time_seconds` | "Processing Time" | number | s | ✅ | 0 |
| `total_runtime` | `total_runtime` | "Total Runtime" | number | s | ❌ | "N/A" |

### Job Status (System)

| Backend Field | Frontend Field | UI Label | Type | Required | Default/Placeholder |
|---------------|----------------|----------|------|----------|-------------------|
| `status` | `status` | "Status" | string | ✅ | "pending" |
| `created_at` | `created` | "Created" | Date | ✅ | new Date() |
| `updated_at` | `updated` | "Updated" | Date | ✅ | new Date() |

### Extended Scientific Data (Lower Priority)

| Backend Field | Frontend Field | UI Label | Type | Units | Required | Default/Placeholder |
|---------------|----------------|----------|------|-------|----------|-------------------|
| `iptm` | `iptm` | "Interface pTM" | number | 0-1 | ❌ | "N/A" |
| `complex_plddt` | `complex_plddt` | "Complex pLDDT" | number | 0-1 | ❌ | "N/A" |
| `ptm` | `ptm` | "pTM" | number | 0-1 | ❌ | "N/A" |
| `ligand_iptm` | `ligand_iptm` | "Ligand Interface pTM" | number | 0-1 | ❌ | "N/A" |
| `protein_iptm` | `protein_iptm` | "Protein Interface pTM" | number | 0-1 | ❌ | "N/A" |
| `sasa_change` | `sasa_change` | "SASA Change" | number | Å² | ❌ | "N/A" |
| `clash_score` | `clash_score` | "Clash Score" | number | - | ❌ | "N/A" |
| `pocket_volume` | `pocket_volume` | "Pocket Volume" | number | Å³ | ❌ | "N/A" |
| `polarity_index` | `polarity_index` | "Polarity Index" | number | - | ❌ | "N/A" |

### Ligand Properties (Lower Priority)

| Backend Field | Frontend Field | UI Label | Type | Units | Required | Default/Placeholder |
|---------------|----------------|----------|------|-------|----------|-------------------|
| `ligand_mw` | `ligand_mw` | "Molecular Weight" | number | g/mol | ❌ | "N/A" |
| `ligand_clogp` | `ligand_clogp` | "cLogP" | number | - | ❌ | "N/A" |
| `ligand_tpsa` | `ligand_tpsa` | "TPSA" | number | Å² | ❌ | "N/A" |
| `ligand_hbd` | `ligand_hbd` | "HBD" | number | - | ❌ | "N/A" |
| `ligand_hba` | `ligand_hba` | "HBA" | number | - | ❌ | "N/A" |
| `ligand_rotatable_bonds` | `ligand_rotatable_bonds` | "Rotatable Bonds" | number | - | ❌ | "N/A" |
| `ligand_formal_charge` | `ligand_formal_charge` | "Formal Charge" | number | - | ❌ | "N/A" |
| `ligand_ring_count` | `ligand_ring_count` | "Ring Count" | number | - | ❌ | "N/A" |
| `ligand_rule_of_five_violations` | `ligand_rule_of_five_violations` | "Rule of Five Violations" | string[] | - | ❌ | [] |

### Residue Hotspots (Lower Priority)

| Backend Field | Frontend Field | UI Label | Type | Required | Default/Placeholder |
|---------------|----------------|----------|------|----------|-------------------|
| `residue_hotspots` | `residue_hotspots` | "Residue Hotspots" | ResidueHotspot[] | ❌ | [] |

## Result Schema Contract

### PredictionResult Interface
```typescript
interface PredictionResult {
  // Core prediction (REQUIRED)
  job_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  affinity_pred_value?: number;  // log(IC50)
  affinity_probability_binary?: number;  // 0-1
  confidence_score?: number;  // 0-1
  processing_time_seconds?: number;
  
  // Identifiers (REQUIRED)
  ligand_smiles: string;
  
  // Provenance (REQUIRED)
  model_version: string;
  run_id: string;
  submitted_at: string;
  completed_at?: string;
  
  // Pose information (REQUIRED)
  poses_generated: number;
  pose_files: string[];
  
  // Flags (OPTIONAL)
  data_quality_warnings?: string[];
  error_message?: string;
  
  // Extended data (OPTIONAL)
  delta_g?: number;
  kd_nm?: number;
  ic50_nm?: number;
  confidence_interval_95?: [number, number];
  sigma?: number;
  // ... additional fields as needed
}
```

## UI Display Priority

### Tier 1: Critical Scientific Fields (Always Visible)
1. **Prediction Quality**: Kd/IC50, ΔG, Confidence, Binding Probability
2. **Identifiers**: Target ID, Ligand ID/SMILES
3. **Provenance**: Model version, Run ID, Timestamps
4. **Top Poses**: Number generated, Download links
5. **Flags**: Warnings, Errors

### Tier 2: Pose Quality (Collapsible Section)
1. **Structural Metrics**: RMSD, H-bonds, Contacts
2. **Quality Scores**: Clash score, SASA change

### Tier 3: Extended Data (Details Section)
1. **Boltz-2 Metrics**: pTM, pLDDT, Interface scores
2. **Ligand Properties**: Drug-likeness, Rule of Five
3. **Residue Analysis**: Hotspots, Contributions

## Error Handling

### Graceful Degradation
- Missing fields show "N/A" placeholder
- Partial data displays available information
- Error states show clear messages with retry options
- Network failures trigger automatic retry

### Status Mapping
- `pending` → "Queued" (10% progress)
- `running` → "Running" (50% progress)  
- `completed` → "Completed" (100% progress)
- `failed` → "Failed" (100% progress, error message)
