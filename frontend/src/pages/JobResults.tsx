import React from 'react';
import { Link, useParams, Navigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { jobService } from '@/lib/jobService';
import StatusBadge from '@/components/StatusBadge';
import MolecularBackground from '@/components/MolecularBackground';
import Navigation from '@/components/Navigation';
import { Download, Eye, BarChart3, Zap, Box, Target, Atom, Clock, AlertTriangle } from 'lucide-react';
import { 
  formatBindingAffinity, 
  formatEnergy, 
  formatConfidenceScore, 
  formatProbability,
  formatConfidenceInterval,
  formatUncertainty,
  formatMolecularWeight,
  formatTPSA,
  formatSASA,
  formatPocketVolume,
  formatRMSD,
  checkRuleOfFiveViolations
} from '@/lib/boltzUtils';

const JobResults: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [job, setJob] = React.useState<Job | null>(null);
  const [isLoading, setIsLoading] = React.useState(true);
  
  const downloadPoseFile = async (poseFile: string) => {
    if (!job?.job_id) return;
    
    try {
      // Construct the download URL for the pose file
      const downloadUrl = `http://localhost:8000/jobs/${job.job_id}/poses/${poseFile}`;
      
      // Create a temporary link and trigger download
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = poseFile;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Failed to download pose file:', error);
      // Fallback: show the file content in a new tab
      window.open(`http://localhost:8000/jobs/${job.job_id}/poses/${poseFile}`, '_blank');
    }
  };
  
  const loadJob = React.useCallback(async () => {
    if (!id) return;
    
    setIsLoading(true);
    try {
      const jobData = await jobService.getJobStatus(id);
      setJob(jobData || null);
    } catch (error) {
      console.error('Failed to load job:', error);
    } finally {
      setIsLoading(false);
    }
  }, [id]);
  
  React.useEffect(() => {
    loadJob();
  }, [loadJob]);
  
  // Auto-retry if job not found
  React.useEffect(() => {
    if (!job && !isLoading && id) {
      const retryInterval = setInterval(() => {
        loadJob();
      }, 2000);
      
      return () => clearInterval(retryInterval);
    }
  }, [job, isLoading, id, loadJob]);

  if (!job || isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6 text-center">
            <h2 className="text-xl font-semibold mb-2">Loading...</h2>
            <p className="text-muted-foreground mb-4">Fetching job results...</p>
            <div className="flex justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (job.status !== 'completed') {
    return <Navigate to={`/job/${job.id}/status`} replace />;
  }

  const formatBindingAffinity = (affinity: number) => {
    return `${affinity.toFixed(2)} kcal/mol`;
  };

  const formatRuntime = (runtime: number) => {
    return `${(runtime / 1000).toFixed(1)}s`;
  };

  return (
    <div className="min-h-screen bg-background relative">
      <Navigation />
      <MolecularBackground intensity="light" />
      
      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold">{job.name}</h1>
            <p className="text-muted-foreground">Binding Affinity Results</p>
          </div>
          
          <div className="flex items-center gap-2">
            <StatusBadge status={job.status} />
          </div>
        </div>

        <div className="max-w-7xl mx-auto space-y-6">
          {/* 1. AFFINITY & ENERGY (Top Pose) - HIGHEST PRIORITY */}
          <Card className="shadow-card border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-primary">
                <BarChart3 className="h-5 w-5" />
                Affinity & Energy (Top Pose)
              </CardTitle>
              <CardDescription>
                Primary binding affinity predictions and energy calculations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* Predicted Kd (nM) */}
                <div className="text-center p-4 bg-primary/5 rounded-lg">
                  <div className="text-3xl font-bold text-primary">
                    {job.kd_nm ? formatBindingAffinity(job.kd_nm, 'kd', 1) : 
                     job.ic50_nm ? formatBindingAffinity(job.ic50_nm, 'ic50', 1) :
                     job.ki_nm ? formatBindingAffinity(job.ki_nm, 'ki', 1) : 'N/A'}
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">
                    {job.kd_nm ? 'Predicted Kd' : 
                     job.ic50_nm ? 'Predicted IC50' : 
                     job.ki_nm ? 'Predicted Ki' : 'Binding Affinity'}
                  </p>
                </div>

                {/* ΔG (kcal/mol) */}
                <div className="text-center p-4 bg-secondary/5 rounded-lg">
                  <div className="text-3xl font-bold text-secondary">
                    {job.delta_g ? formatEnergy(job.delta_g, 'deltaG', 2) : 'N/A'}
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">ΔG (kcal/mol)</p>
                </div>

                {/* Confidence/Uncertainty */}
                <div className="text-center p-4 bg-success/5 rounded-lg">
                  <div className="text-3xl font-bold text-success">
                    {job.confidence_score ? formatConfidenceScore(job.confidence_score) : 'N/A'}
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">Confidence</p>
                  {job.sigma && (
                    <p className="text-xs text-muted-foreground">
                      {formatUncertainty(job.sigma)}
                    </p>
                  )}
                </div>

                {/* Binding Probability */}
                <div className="text-center p-4 bg-warning/5 rounded-lg">
                  <div className="text-3xl font-bold text-warning">
                    {job.affinity_probability_binary ? formatProbability(job.affinity_probability_binary) : 'N/A'}
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">Binding Probability</p>
                </div>
              </div>

              {/* 95% Confidence Interval */}
              {job.confidence_interval_95 && (
                <div className="mt-4 p-3 bg-muted/50 rounded-lg">
                  <p className="text-sm text-muted-foreground">
                    <strong>95% Confidence Interval:</strong> {formatConfidenceInterval(job.confidence_interval_95)}
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* 2. POSE QUALITY (Top Pose) */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5" />
                Pose Quality (Top Pose)
              </CardTitle>
              <CardDescription>
                Structural quality metrics for the best binding pose
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-3 lg:grid-cols-5 gap-4">
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.rmsd ? formatRMSD(job.rmsd) : 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground">RMSD (Å)</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.hbond_count ?? 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground">H-bond count</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.hydrophobic_contacts ?? 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground">Hydrophobic contacts</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.salt_bridges ?? 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground">Salt bridges</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.pi_stacking ?? 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground">π-stacking</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.sasa_change ? formatSASA(job.sasa_change) : 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground">SASA change (Å²)</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.clash_score ? job.clash_score.toFixed(2) : 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground">Clash score</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.pocket_volume ? formatPocketVolume(job.pocket_volume) : 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground">Pocket volume (Å³)</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.polarity_index ? job.polarity_index.toFixed(2) : 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground">Polarity index</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 3. RESIDUE HOTSPOTS (Top Pose) */}
          {job.residue_hotspots && job.residue_hotspots.length > 0 && (
            <Card className="shadow-card">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Atom className="h-5 w-5" />
                  Residue Hotspots (Top Pose)
                </CardTitle>
                <CardDescription>
                  Top contributing residues to binding affinity
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Residue</TableHead>
                      <TableHead>Contribution (kcal/mol)</TableHead>
                      <TableHead>Contact Count</TableHead>
                      <TableHead>Contact Types</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {job.residue_hotspots.map((hotspot, index) => (
                      <TableRow key={index}>
                        <TableCell className="font-mono font-medium">
                          {hotspot.residue_name}
                        </TableCell>
                        <TableCell className="font-semibold text-primary">
                          {hotspot.contribution.toFixed(2)}
                        </TableCell>
                        <TableCell>
                          {hotspot.contact_count}
                        </TableCell>
                        <TableCell>
                          <div className="flex flex-wrap gap-1">
                            {hotspot.contact_types.map((type, i) => (
                              <Badge key={i} variant="outline" className="text-xs">
                                {type}
                              </Badge>
                            ))}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          )}

          {/* 4. LIGAND PROPERTIES */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Box className="h-5 w-5" />
                Ligand Properties
              </CardTitle>
              <CardDescription>
                Molecular properties and drug-likeness assessment
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                {/* Basic Properties */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">Basic Properties</h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-muted-foreground">SMILES</p>
                      <p className="font-mono text-xs break-all">{job.ligand_smiles || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Name/ID</p>
                      <p className="font-medium">{job.ligand_name || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">MW (g/mol)</p>
                      <p className="font-semibold">{job.ligand_mw ? formatMolecularWeight(job.ligand_mw) : 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">cLogP</p>
                      <p className="font-semibold">{job.ligand_clogp ? job.ligand_clogp.toFixed(2) : 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">TPSA (Å²)</p>
                      <p className="font-semibold">{job.ligand_tpsa ? formatTPSA(job.ligand_tpsa) : 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">HBD</p>
                      <p className="font-semibold">{job.ligand_hbd ?? 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">HBA</p>
                      <p className="font-semibold">{job.ligand_hba ?? 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Rotatable Bonds</p>
                      <p className="font-semibold">{job.ligand_rotatable_bonds ?? 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Formal Charge</p>
                      <p className="font-semibold">{job.ligand_formal_charge ?? 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Ring Count</p>
                      <p className="font-semibold">{job.ligand_ring_count ?? 'N/A'}</p>
                    </div>
                  </div>
                </div>

                {/* Rule of Five Assessment */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">Rule of Five Status</h4>
                  {job.ligand_mw && job.ligand_clogp && job.ligand_hbd && job.ligand_hba ? (
                    <div>
                      {(() => {
                        const violations = checkRuleOfFiveViolations(
                          job.ligand_mw,
                          job.ligand_clogp,
                          job.ligand_hbd,
                          job.ligand_hba
                        );
                        return (
                          <div className="space-y-2">
                            <div className="flex items-center gap-2">
                              {violations.length === 0 ? (
                                <Badge className="bg-green-100 text-green-800">Compliant</Badge>
                              ) : (
                                <Badge variant="destructive">{violations.length} Violation(s)</Badge>
                              )}
                            </div>
                            {violations.length > 0 && (
                              <div className="space-y-1">
                                <p className="text-sm text-muted-foreground">Violations:</p>
                                <ul className="text-sm space-y-1">
                                  {violations.map((violation, i) => (
                                    <li key={i} className="flex items-center gap-2">
                                      <AlertTriangle className="h-3 w-3 text-destructive" />
                                      {violation}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>
                        );
                      })()}
                    </div>
                  ) : (
                    <p className="text-muted-foreground">Insufficient data for Rule of Five assessment</p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 5. TARGET & RUN INFO */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                Target & Run Info
              </CardTitle>
              <CardDescription>
                Target identifiers, model information, and run details
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                {/* Target Information */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">Target Information</h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-muted-foreground">PDB ID</p>
                      <p className="font-mono font-medium">{job.target_pdb || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">UniProt ID</p>
                      <p className="font-mono font-medium">{job.target_uniprot || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Chain</p>
                      <p className="font-medium">{job.target_chain || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Pocket Label</p>
                      <p className="font-medium">{job.target_pocket || 'N/A'}</p>
                    </div>
                  </div>
                </div>

                {/* Run Information */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">Run Information</h4>
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-muted-foreground">Model Version</p>
                      <p className="font-medium">{job.model_version || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Run ID</p>
                      <p className="font-mono text-xs">{job.run_id || job.job_id || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Device</p>
                      <p className="font-medium">{job.device || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Total Runtime</p>
                      <p className="font-medium">{job.total_runtime ? `${job.total_runtime.toFixed(1)}s` : 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Data Completeness</p>
                      <p className="font-medium">{job.data_completeness ? `${job.data_completeness.toFixed(1)}%` : 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Pocket Detection</p>
                      <p className="font-medium">{job.pocket_detection_method || 'N/A'}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Data Quality Warnings */}
              {job.data_quality_warnings && job.data_quality_warnings.length > 0 && (
                <div className="mt-4 p-3 bg-warning/10 rounded-lg">
                  <h5 className="font-semibold text-sm text-warning mb-2">Data Quality Warnings</h5>
                  <ul className="text-sm space-y-1">
                    {job.data_quality_warnings.map((warning, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <AlertTriangle className="h-3 w-3 text-warning" />
                        {warning}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Error Display */}
          {job.status === 'failed' && job.error_message && (
            <Card className="shadow-card border-destructive">
              <CardHeader>
                <CardTitle className="text-destructive">Job Failed</CardTitle>
                <CardDescription>Error details from Boltz-2 processing</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="p-4 bg-destructive/10 rounded-lg">
                  <p className="text-destructive font-medium">{job.error_message}</p>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Pose Files Download */}
          {job.pose_files && job.pose_files.length > 0 && (
            <Card className="shadow-card">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Download className="h-5 w-5" />
                  Pose Files
                </CardTitle>
                <CardDescription>
                  Download generated binding conformations
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {job.pose_files.slice(0, 10).map((poseFile, index) => (
                    <div key={poseFile} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                      <div className="flex items-center gap-3">
                        <Badge variant="outline" className="min-w-12">
                          #{index + 1}
                        </Badge>
                        <span className="font-medium">{poseFile}</span>
                      </div>
                      <div className="flex gap-2">
                        <Button variant="ghost" size="sm" className="h-6 text-xs">
                          <Eye className="h-3 w-3 mr-1" />
                          View
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          className="h-6 text-xs"
                          onClick={() => downloadPoseFile(poseFile)}
                        >
                          <Download className="h-3 w-3 mr-1" />
                          Download
                        </Button>
                      </div>
                    </div>
                  ))}
                  {job.pose_files.length > 10 && (
                    <p className="text-muted-foreground text-center text-sm py-2">
                      +{job.pose_files.length - 10} more poses available
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Actions */}
          <div className="flex justify-center gap-4">
            <Button variant="hero" size="lg" disabled>
              <Download className="mr-2 h-4 w-4" />
              Download Results
            </Button>
            <Button asChild variant="molecular" size="lg">
              <Link to="/job/new">
                Create New Job
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobResults;