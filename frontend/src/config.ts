// Configuration for the frontend application

export const config = {
  // API Configuration
  api: {
    baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    timeout: 30000, // 30 seconds
    retryAttempts: 3,
  },
  
  // Application settings
  app: {
    name: 'Atomera Affinity Lab',
    version: '1.0.0',
    description: 'Protein-ligand binding affinity prediction using Boltz-2',
  },
  
  // Job polling settings
  jobs: {
    pollInterval: 5000, // 5 seconds
    maxPollAttempts: 100, // Stop polling after ~8 minutes
  },
  
  // File upload settings
  upload: {
    maxFileSize: 10 * 1024 * 1024, // 10MB
    allowedProteinFormats: ['.fasta', '.fa', '.txt'],
    allowedLigandFormats: ['.smi', '.txt'],
  },
};
