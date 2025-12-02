// Utility to create a mock completed job for demo purposes
import { Job } from '@/lib/jobService';

export const createMockCompletedJob = (): Job => {
  const jobId = 'demo-' + Date.now();

  return {
    id: jobId,
    name: 'EGFR Kinase Inhibitor Screen',
    status: 'completed',
    created: new Date(Date.now() - 1000 * 60 * 15), // 15 minutes ago
    updated: new Date(Date.now() - 1000 * 60 * 2),  // 2 minutes ago

    // Required job input fields
    proteinInput: 'FKKIKVLGSGAFGTVYKGLWIPEGEKVKIPVAIKELREATSPKANKEILDEAYVMASVDNPHVCRLLGIC',
    proteinType: 'text' as const,
    ligandInput: 'COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN1CCOCC1',
    ligandType: 'text' as const,

    // Job details
    job_id: jobId,

    // Binding affinity predictions
    kd_nm: 2.3,
    ic50_nm: null,
    ki_nm: null,
    delta_g: -12.1,
    confidence_score: 0.95,
    sigma: 0.15,
    affinity_probability_binary: 0.98,
    confidence_interval_95: [-12.4, -11.8],

    // Pose quality metrics
    rmsd: 0.8,
    hbond_count: 4,
    hydrophobic_contacts: 7,
    salt_bridges: 2,
    pi_stacking: 1,
    sasa_change: 425.3,
    clash_score: 2.1,
    pocket_volume: 1250.5,
    polarity_index: 0.65,

    // Residue hotspots
    residue_hotspots: [
      {
        residue_name: 'LEU-718',
        contribution: -2.8,
        contact_count: 3,
        contact_types: ['Hydrophobic', 'VDW']
      },
      {
        residue_name: 'MET-793',
        contribution: -2.3,
        contact_count: 2,
        contact_types: ['Hydrophobic']
      },
      {
        residue_name: 'GLN-791',
        contribution: -1.9,
        contact_count: 2,
        contact_types: ['H-bond']
      },
      {
        residue_name: 'THR-854',
        contribution: -1.6,
        contact_count: 1,
        contact_types: ['H-bond']
      },
      {
        residue_name: 'ASP-855',
        contribution: -1.4,
        contact_count: 1,
        contact_types: ['Salt bridge', 'H-bond']
      }
    ],

    // Ligand properties
    ligand_smiles: 'COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN1CCOCC1',
    ligand_name: 'Erlotinib Analog',
    ligand_mw: 393.44,
    ligand_clogp: 3.2,
    ligand_tpsa: 74.73,
    ligand_hbd: 1,
    ligand_hba: 6,
    ligand_rotatable_bonds: 8,
    ligand_formal_charge: 0,
    ligand_ring_count: 3,

    // Target information
    target_pdb: '1M17',
    target_uniprot: 'P00533',
    target_chain: 'A',
    target_pocket: 'ATP_binding_site',

    // Run information
    model_version: 'Boltz-2.0',
    run_id: jobId,
    device: 'NVIDIA A100',
    total_runtime: 245.7,
    data_completeness: 98.5,
    pocket_detection_method: 'fpocket',
    data_quality_warnings: [],

    // Pose files
    pose_files: [
      'pose_0.cif',
      'pose_1.cif',
      'pose_2.cif',
      'pose_3.cif',
      'pose_4.cif'
    ],

    error_message: null
  };
};

export const addMockJobToLocalStorage = () => {
  const mockJob = createMockCompletedJob();

  // Get existing jobs from localStorage
  const existingJobsStr = localStorage.getItem('atomera_jobs');
  const existingJobs = existingJobsStr ? JSON.parse(existingJobsStr) : [];

  // Add mock job
  existingJobs.push(mockJob);

  // Save back to localStorage
  localStorage.setItem('atomera_jobs', JSON.stringify(existingJobs));

  console.log('✅ Mock job created:', mockJob.name, '(ID:', mockJob.id, ')');

  return mockJob;
};
