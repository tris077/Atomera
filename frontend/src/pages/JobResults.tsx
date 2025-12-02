import React from 'react';
import { Link, useParams, Navigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { jobService, Job } from '@/lib/jobService';
import StatusBadge from '@/components/StatusBadge';
import MolecularBackground from '@/components/MolecularBackground';
import Navigation from '@/components/Navigation';
import { ScientificTooltip, MetricLabel, ConfidenceBar, StatusChip, ContributionIndicator } from '@/components/ui/scientific-tooltip';
import { METRIC_TOOLTIPS, SCIENTIFIC_NARRATIVES, VALUE_PROPOSITIONS, STATUS_CHIPS, EGFR_CONTEXT } from '@/lib/scientificContent';
import {
  Download, Box, Target, Atom, Clock, Maximize2,
  FileText, Sparkles, CheckCircle2, Info, ChevronRight, Lightbulb,
  FlaskConical, Beaker, BarChart3
} from 'lucide-react';
import { checkRuleOfFiveViolations } from '@/lib/boltzUtils';

const JobResults: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [job, setJob] = React.useState<Job | null>(null);
  const [isLoading, setIsLoading] = React.useState(true);
  const [showDemoGuide, setShowDemoGuide] = React.useState(true);

  const downloadPoseFile = async (poseFile: string) => {
    if (!job?.job_id) return;

    try {
      const downloadUrl = `http://localhost:8000/jobs/${job.job_id}/poses/${poseFile}`;
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = poseFile;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Failed to download pose file:', error);
      window.open(`http://localhost:8000/jobs/${job.job_id}/poses/${poseFile}`, '_blank');
    }
  };

  const downloadCSV = () => {
    if (!job) return;

    const headers = ['Metric', 'Value', 'Unit', 'Interpretation'];
    const rows = [
      ['Predicted Kd', job.kd_nm || 'N/A', 'nM', job.kd_nm ? METRIC_TOOLTIPS.kd.interpretation(job.kd_nm) : ''],
      ['Binding Free Energy (ΔG)', job.delta_g || 'N/A', 'kcal/mol', job.delta_g ? METRIC_TOOLTIPS.deltaG.interpretation(job.delta_g) : ''],
      ['Confidence Score', job.confidence_score || 'N/A', '%', job.confidence_score ? METRIC_TOOLTIPS.confidence.interpretation(job.confidence_score) : ''],
      ['RMSD', job.rmsd || 'N/A', 'Å', job.rmsd ? METRIC_TOOLTIPS.rmsd.interpretation(job.rmsd) : ''],
      ['Clash Score', job.clash_score || 'N/A', '', job.clash_score ? METRIC_TOOLTIPS.clashScore.interpretation(job.clash_score) : ''],
      ['H-Bonds', job.hbond_count || 'N/A', 'count', ''],
      ['Hydrophobic Contacts', job.hydrophobic_contacts || 'N/A', 'count', ''],
      ['Salt Bridges', job.salt_bridges || 'N/A', 'count', ''],
      ['π-Stacking', job.pi_stacking || 'N/A', 'count', ''],
    ];

    // Add residue hotspots
    if (job.residue_hotspots) {
      rows.push(['', '', '', '']);
      rows.push(['Residue Hotspots', '', '', '']);
      job.residue_hotspots.forEach(h => {
        rows.push([h.residue_name, h.contribution.toFixed(2), 'kcal/mol', h.contact_types.join(', ')]);
      });
    }

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `atomera-results-${job.id}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const downloadPDFReport = () => {
    if (!job) return;

    // Generate a printable HTML report that can be saved as PDF
    const reportHTML = `
<!DOCTYPE html>
<html>
<head>
  <title>Atomera Analysis Report - ${job.name}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; color: #1a1a1a; }
    h1 { color: #d946ef; border-bottom: 2px solid #d946ef; padding-bottom: 10px; }
    h2 { color: #374151; margin-top: 30px; }
    .summary { background: linear-gradient(135deg, #fdf4ff 0%, #f5f3ff 100%); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #d946ef; }
    .metric-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
    .metric { background: #f9fafb; padding: 15px; border-radius: 6px; }
    .metric-label { font-size: 12px; color: #6b7280; text-transform: uppercase; }
    .metric-value { font-size: 24px; font-weight: bold; color: #111827; }
    .metric-unit { font-size: 14px; color: #6b7280; }
    table { width: 100%; border-collapse: collapse; margin: 15px 0; }
    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #e5e7eb; }
    th { background: #f9fafb; font-weight: 600; }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 500; }
    .badge-green { background: #d1fae5; color: #065f46; }
    .badge-blue { background: #dbeafe; color: #1e40af; }
    .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280; }
  </style>
</head>
<body>
  <h1>Atomera Binding Affinity Analysis</h1>
  <p><strong>Job:</strong> ${job.name}</p>
  <p><strong>Date:</strong> ${new Date().toLocaleDateString()}</p>
  <p><strong>Target:</strong> ${job.target_pdb || 'N/A'} (${job.target_uniprot || 'N/A'})</p>
  <p><strong>Ligand:</strong> ${job.ligand_name || 'Unnamed'}</p>

  <div class="summary">
    <h3 style="margin-top:0;color:#7c3aed;">Key Finding</h3>
    <p>${job.kd_nm && job.delta_g && job.confidence_score && job.rmsd ?
      SCIENTIFIC_NARRATIVES.generateSummary({
        affinity: job.kd_nm,
        deltaG: job.delta_g,
        confidence: job.confidence_score,
        rmsd: job.rmsd,
        targetName: job.target_pdb,
        ligandName: job.ligand_name
      }) : 'Analysis complete. See detailed metrics below.'}</p>
  </div>

  <h2>Binding Affinity Predictions</h2>
  <div class="metric-grid">
    <div class="metric">
      <div class="metric-label">Predicted Kd</div>
      <div class="metric-value">${job.kd_nm?.toFixed(1) || 'N/A'} <span class="metric-unit">nM</span></div>
    </div>
    <div class="metric">
      <div class="metric-label">Binding Free Energy (ΔG)</div>
      <div class="metric-value">${job.delta_g?.toFixed(1) || 'N/A'} <span class="metric-unit">kcal/mol</span></div>
    </div>
    <div class="metric">
      <div class="metric-label">Confidence Score</div>
      <div class="metric-value">${job.confidence_score ? (job.confidence_score * 100).toFixed(0) : 'N/A'}<span class="metric-unit">%</span></div>
    </div>
    <div class="metric">
      <div class="metric-label">Binding Probability</div>
      <div class="metric-value">${job.affinity_probability_binary ? (job.affinity_probability_binary * 100).toFixed(0) : 'N/A'}<span class="metric-unit">%</span></div>
    </div>
  </div>

  <h2>Pose Quality Metrics</h2>
  <table>
    <tr><th>Metric</th><th>Value</th><th>Assessment</th></tr>
    <tr><td>RMSD</td><td>${job.rmsd?.toFixed(2) || 'N/A'} Å</td><td>${job.rmsd ? METRIC_TOOLTIPS.rmsd.interpretation(job.rmsd) : '-'}</td></tr>
    <tr><td>Clash Score</td><td>${job.clash_score?.toFixed(2) || 'N/A'}</td><td>${job.clash_score ? METRIC_TOOLTIPS.clashScore.interpretation(job.clash_score) : '-'}</td></tr>
    <tr><td>H-Bonds</td><td>${job.hbond_count || 'N/A'}</td><td>-</td></tr>
    <tr><td>Hydrophobic Contacts</td><td>${job.hydrophobic_contacts || 'N/A'}</td><td>-</td></tr>
    <tr><td>Salt Bridges</td><td>${job.salt_bridges || 'N/A'}</td><td>-</td></tr>
    <tr><td>π-Stacking</td><td>${job.pi_stacking || 'N/A'}</td><td>-</td></tr>
  </table>

  ${job.residue_hotspots && job.residue_hotspots.length > 0 ? `
  <h2>Residue Hotspots</h2>
  <table>
    <tr><th>Residue</th><th>Contribution (kcal/mol)</th><th>Interaction Types</th><th>Role</th></tr>
    ${job.residue_hotspots.map(h => `
      <tr>
        <td><strong>${h.residue_name}</strong></td>
        <td style="color:${h.contribution < 0 ? '#059669' : '#dc2626'}">${h.contribution.toFixed(2)}</td>
        <td>${h.contact_types.join(', ')}</td>
        <td>${h.contribution < -2 ? 'Strong stabilizer' : h.contribution < 0 ? 'Stabilizing' : 'Destabilizing'}</td>
      </tr>
    `).join('')}
  </table>
  ` : ''}

  <h2>Ligand Properties</h2>
  <table>
    <tr><th>Property</th><th>Value</th><th>Rule of Five</th></tr>
    <tr><td>Molecular Weight</td><td>${job.ligand_mw?.toFixed(1) || 'N/A'} g/mol</td><td>${job.ligand_mw && job.ligand_mw <= 500 ? '<span class="badge badge-green">Pass</span>' : '<span class="badge" style="background:#fef2f2;color:#991b1b">Fail</span>'}</td></tr>
    <tr><td>cLogP</td><td>${job.ligand_clogp?.toFixed(2) || 'N/A'}</td><td>${job.ligand_clogp && job.ligand_clogp <= 5 ? '<span class="badge badge-green">Pass</span>' : '<span class="badge" style="background:#fef2f2;color:#991b1b">Fail</span>'}</td></tr>
    <tr><td>H-Bond Donors</td><td>${job.ligand_hbd || 'N/A'}</td><td>${job.ligand_hbd && job.ligand_hbd <= 5 ? '<span class="badge badge-green">Pass</span>' : '<span class="badge" style="background:#fef2f2;color:#991b1b">Fail</span>'}</td></tr>
    <tr><td>H-Bond Acceptors</td><td>${job.ligand_hba || 'N/A'}</td><td>${job.ligand_hba && job.ligand_hba <= 10 ? '<span class="badge badge-green">Pass</span>' : '<span class="badge" style="background:#fef2f2;color:#991b1b">Fail</span>'}</td></tr>
    <tr><td>TPSA</td><td>${job.ligand_tpsa?.toFixed(1) || 'N/A'} Å²</td><td>-</td></tr>
    <tr><td>Rotatable Bonds</td><td>${job.ligand_rotatable_bonds || 'N/A'}</td><td>-</td></tr>
  </table>

  <div class="footer">
    <p>Generated by <strong>Atomera</strong> - AI-powered virtual screening platform</p>
    <p>Model: ${job.model_version || 'Boltz-2.0'} | Runtime: ${job.total_runtime?.toFixed(1) || 'N/A'}s</p>
    <p style="font-size:11px;color:#9ca3af;">This report is for research purposes only. Results should be validated experimentally.</p>
  </div>
</body>
</html>`;

    const blob = new Blob([reportHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const win = window.open(url, '_blank');
    if (win) {
      win.onload = () => {
        win.print();
      };
    }
    URL.revokeObjectURL(url);
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
            <h2 className="text-xl font-semibold mb-2">Loading Analysis Results</h2>
            <p className="text-muted-foreground mb-4">Fetching binding affinity predictions...</p>
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

  // Calculate status chips
  const affinityStatus = job.kd_nm ? STATUS_CHIPS.affinity(job.kd_nm) : null;
  const confidenceStatus = job.confidence_score ? STATUS_CHIPS.confidence(job.confidence_score) : null;
  const poseStatus = job.rmsd ? STATUS_CHIPS.pose(job.rmsd) : null;
  const violations = job.ligand_mw && job.ligand_clogp && job.ligand_hbd && job.ligand_hba
    ? checkRuleOfFiveViolations(job.ligand_mw, job.ligand_clogp, job.ligand_hbd, job.ligand_hba)
    : [];
  const drugLikenessStatus = STATUS_CHIPS.drugLikeness(violations.length);

  // Generate summary text
  const summaryText = job.kd_nm && job.delta_g && job.confidence_score && job.rmsd
    ? SCIENTIFIC_NARRATIVES.generateSummary({
        affinity: job.kd_nm,
        deltaG: job.delta_g,
        confidence: job.confidence_score,
        rmsd: job.rmsd,
        targetName: job.target_pdb,
        ligandName: job.ligand_name,
        topResidue: job.residue_hotspots?.[0]?.residue_name
      })
    : null;

  return (
    <div className="min-h-screen bg-background relative">
      <Navigation />
      <MolecularBackground intensity="light" />

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Demo Guide Banner */}
        {showDemoGuide && id?.startsWith('demo-') && (
          <div className="mb-6 bg-gradient-to-r from-primary/10 via-secondary/10 to-primary/10 border border-primary/20 rounded-lg p-4">
            <div className="flex items-start justify-between">
              <div className="flex gap-3">
                <Lightbulb className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                <div>
                  <h3 className="font-semibold text-sm text-primary mb-1">Demo Walkthrough</h3>
                  <p className="text-sm text-muted-foreground mb-2">
                    You're viewing an EGFR kinase inhibitor screen. This demonstrates how Atomera helps researchers prioritize compounds before synthesis.
                  </p>
                  <div className="flex flex-wrap gap-2 text-xs">
                    <span className="text-muted-foreground">Try:</span>
                    <span className="bg-white/50 px-2 py-0.5 rounded">Review affinity rankings</span>
                    <ChevronRight className="h-3 w-3 text-muted-foreground" />
                    <span className="bg-white/50 px-2 py-0.5 rounded">Examine hotspots</span>
                    <ChevronRight className="h-3 w-3 text-muted-foreground" />
                    <span className="bg-white/50 px-2 py-0.5 rounded">View 3D structure</span>
                  </div>
                </div>
              </div>
              <button
                onClick={() => setShowDemoGuide(false)}
                className="text-muted-foreground hover:text-foreground text-sm"
              >
                Dismiss
              </button>
            </div>
          </div>
        )}

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <FlaskConical className="h-6 w-6 text-primary" />
              <h1 className="text-3xl font-bold">{job.name}</h1>
            </div>
            <p className="text-muted-foreground">Virtual Screening Results • Structure-Based Binding Analysis</p>
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            <StatusBadge status={job.status} />
            <Button
              asChild
              variant="hero"
              size="lg"
              className="shadow-lg hover:shadow-xl transition-all duration-300"
            >
              <Link to={`/job/${job.id || id}/viewer`}>
                <Maximize2 className="mr-2 h-4 w-4" />
                View Top Pose in 3D
              </Link>
            </Button>
          </div>
        </div>

        <div className="max-w-7xl mx-auto space-y-6">
          {/* KEY INSIGHT SUMMARY */}
          {summaryText && (
            <Card className="shadow-card border-primary/30 bg-gradient-to-br from-primary/5 via-background to-secondary/5">
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-primary">
                  <Sparkles className="h-5 w-5" />
                  Key Finding
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-base leading-relaxed">{summaryText}</p>
                <div className="flex flex-wrap gap-2 mt-4">
                  {affinityStatus && <StatusChip label={affinityStatus.label} colorClass={affinityStatus.color} />}
                  {confidenceStatus && <StatusChip label={confidenceStatus.label} colorClass={confidenceStatus.color} />}
                  {poseStatus && <StatusChip label={poseStatus.label} colorClass={poseStatus.color} />}
                  {drugLikenessStatus && <StatusChip label={drugLikenessStatus.label} colorClass={drugLikenessStatus.color} />}
                </div>
              </CardContent>
            </Card>
          )}

          {/* 1. AFFINITY & ENERGY */}
          <Card className="shadow-card border-primary/20">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center gap-2 text-primary">
                    <BarChart3 className="h-5 w-5" />
                    Binding Affinity Predictions
                    <Badge variant="secondary" className="text-xs bg-gradient-to-r from-primary/20 to-secondary/20 border-primary/30">
                      <Sparkles className="h-3 w-3 mr-1" />
                      ML-Powered
                    </Badge>
                  </CardTitle>
                  <CardDescription>
                    Thermodynamic binding parameters predicted using Boltz-2 (ML-based structure prediction)
                  </CardDescription>
                </div>
                <Badge variant="outline" className="text-xs">
                  Top Pose
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* Predicted Kd */}
                <div className="text-center p-4 bg-primary/5 rounded-lg border border-primary/10">
                  <div className="text-3xl font-bold text-primary">
                    {job.kd_nm ? `${job.kd_nm.toFixed(1)}` : 'N/A'}
                    <span className="text-lg ml-1">nM</span>
                  </div>
                  <MetricLabel
                    label="Predicted Kd"
                    tooltip={METRIC_TOOLTIPS.kd.tooltip}
                    interpretation={job.kd_nm ? METRIC_TOOLTIPS.kd.interpretation(job.kd_nm) : undefined}
                    className="mt-1"
                  />
                </div>

                {/* ΔG */}
                <div className="text-center p-4 bg-secondary/5 rounded-lg border border-secondary/10">
                  <div className="text-3xl font-bold text-secondary">
                    {job.delta_g ? `${job.delta_g.toFixed(1)}` : 'N/A'}
                    <span className="text-lg ml-1">kcal/mol</span>
                  </div>
                  <MetricLabel
                    label="ΔG (Binding Energy)"
                    tooltip={METRIC_TOOLTIPS.deltaG.tooltip}
                    interpretation={job.delta_g ? METRIC_TOOLTIPS.deltaG.interpretation(job.delta_g) : undefined}
                    className="mt-1"
                  />
                </div>

                {/* Confidence */}
                <div className="text-center p-4 bg-success/5 rounded-lg border border-success/10">
                  <div className="text-3xl font-bold text-success">
                    {job.confidence_score ? `${(job.confidence_score * 100).toFixed(0)}%` : 'N/A'}
                  </div>
                  <MetricLabel
                    label="Confidence Score"
                    tooltip={METRIC_TOOLTIPS.confidence.tooltip}
                    interpretation={job.confidence_score ? METRIC_TOOLTIPS.confidence.interpretation(job.confidence_score) : undefined}
                    className="mt-1"
                  />
                  {job.confidence_score && (
                    <ConfidenceBar value={job.confidence_score} className="mt-2" showLabel={false} />
                  )}
                </div>

                {/* Binding Probability */}
                <div className="text-center p-4 bg-warning/5 rounded-lg border border-warning/10">
                  <div className="text-3xl font-bold text-warning">
                    {job.affinity_probability_binary ? `${(job.affinity_probability_binary * 100).toFixed(0)}%` : 'N/A'}
                  </div>
                  <MetricLabel
                    label="Binding Probability"
                    tooltip={METRIC_TOOLTIPS.bindingProbability.tooltip}
                    className="mt-1"
                  />
                </div>
              </div>

              {/* Energy Interpretation */}
              {job.delta_g && (
                <div className="mt-4 p-3 bg-muted/50 rounded-lg border-l-4 border-primary/50">
                  <p className="text-sm text-muted-foreground flex items-start gap-2">
                    <Info className="h-4 w-4 mt-0.5 text-primary flex-shrink-0" />
                    <span>{SCIENTIFIC_NARRATIVES.energyInterpretation(job.delta_g)}</span>
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* 2. POSE QUALITY */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5" />
                Pose Quality Assessment
              </CardTitle>
              <CardDescription>
                Structural validation metrics for predicted binding geometry
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-3 lg:grid-cols-5 gap-4">
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.rmsd ? `${job.rmsd.toFixed(1)} Å` : 'N/A'}
                  </div>
                  <MetricLabel
                    label="RMSD"
                    tooltip={METRIC_TOOLTIPS.rmsd.tooltip}
                    interpretation={job.rmsd ? METRIC_TOOLTIPS.rmsd.interpretation(job.rmsd) : undefined}
                  />
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">{job.hbond_count ?? 'N/A'}</div>
                  <MetricLabel label="H-Bonds" tooltip={METRIC_TOOLTIPS.hbonds.tooltip} />
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">{job.hydrophobic_contacts ?? 'N/A'}</div>
                  <MetricLabel label="Hydrophobic" tooltip={METRIC_TOOLTIPS.hydrophobic.tooltip} />
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">{job.salt_bridges ?? 'N/A'}</div>
                  <MetricLabel label="Salt Bridges" tooltip={METRIC_TOOLTIPS.saltBridges.tooltip} />
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">{job.pi_stacking ?? 'N/A'}</div>
                  <MetricLabel label="π-Stacking" tooltip={METRIC_TOOLTIPS.piStacking.tooltip} />
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.clash_score ? job.clash_score.toFixed(1) : 'N/A'}
                  </div>
                  <MetricLabel
                    label="Clash Score"
                    tooltip={METRIC_TOOLTIPS.clashScore.tooltip}
                    interpretation={job.clash_score ? METRIC_TOOLTIPS.clashScore.interpretation(job.clash_score) : undefined}
                  />
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.sasa_change ? `${job.sasa_change.toFixed(0)} Å²` : 'N/A'}
                  </div>
                  <MetricLabel label="SASA Change" tooltip={METRIC_TOOLTIPS.sasa.tooltip} />
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.pocket_volume ? `${job.pocket_volume.toFixed(0)} Å³` : 'N/A'}
                  </div>
                  <MetricLabel label="Pocket Volume" tooltip={METRIC_TOOLTIPS.pocketVolume.tooltip} />
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <div className="text-xl font-bold">
                    {job.polarity_index ? job.polarity_index.toFixed(2) : 'N/A'}
                  </div>
                  <MetricLabel label="Polarity Index" tooltip={METRIC_TOOLTIPS.polarityIndex.tooltip} />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 3. RESIDUE HOTSPOTS */}
          {job.residue_hotspots && job.residue_hotspots.length > 0 && (
            <Card className="shadow-card">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Atom className="h-5 w-5" />
                  Binding Site Hotspots
                </CardTitle>
                <CardDescription>
                  Per-residue energy contributions to binding. Negative values (green) stabilize the complex; positive values (red) indicate strain.
                </CardDescription>
              </CardHeader>
              <CardContent>
                {/* Scientific context for EGFR */}
                {job.target_pdb === '1M17' && (
                  <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="text-sm text-blue-800">
                      <strong>EGFR Context:</strong> {EGFR_CONTEXT.scientificStory}
                    </p>
                  </div>
                )}

                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Residue</TableHead>
                      <TableHead>
                        <ScientificTooltip content={METRIC_TOOLTIPS.residueContribution.tooltip}>
                          Contribution
                        </ScientificTooltip>
                      </TableHead>
                      <TableHead>Contacts</TableHead>
                      <TableHead>Interaction Types</TableHead>
                      <TableHead>Role</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {job.residue_hotspots.map((hotspot, index) => {
                      const contribInfo = METRIC_TOOLTIPS.residueContribution.interpretContribution(hotspot.contribution);
                      const egfrInfo = EGFR_CONTEXT.keyResidues[hotspot.residue_name as keyof typeof EGFR_CONTEXT.keyResidues];

                      return (
                        <TableRow key={index}>
                          <TableCell className="font-mono font-medium">
                            {hotspot.residue_name}
                            {egfrInfo && (
                              <span className="block text-xs text-muted-foreground font-normal">
                                {egfrInfo.role}
                              </span>
                            )}
                          </TableCell>
                          <TableCell>
                            <ContributionIndicator value={hotspot.contribution} />
                          </TableCell>
                          <TableCell>{hotspot.contact_count}</TableCell>
                          <TableCell>
                            <div className="flex flex-wrap gap-1">
                              {hotspot.contact_types.map((type, i) => (
                                <Badge key={i} variant="outline" className="text-xs">
                                  {type}
                                </Badge>
                              ))}
                            </div>
                          </TableCell>
                          <TableCell>
                            <span className={contribInfo.color}>{contribInfo.label}</span>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>

                <p className="text-xs text-muted-foreground mt-3">
                  {VALUE_PROPOSITIONS.useCaseDescriptions.hotspots}
                </p>
              </CardContent>
            </Card>
          )}

          {/* 4. LIGAND PROPERTIES */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Box className="h-5 w-5" />
                Ligand Properties & Drug-Likeness
              </CardTitle>
              <CardDescription>
                Physicochemical properties and Lipinski Rule of Five compliance assessment
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                {/* Basic Properties */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide flex items-center gap-2">
                    <Beaker className="h-4 w-4" />
                    Molecular Properties
                  </h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <MetricLabel label="Molecular Weight" tooltip={METRIC_TOOLTIPS.mw.tooltip} />
                      <p className="font-semibold">{job.ligand_mw ? `${job.ligand_mw.toFixed(1)} g/mol` : 'N/A'}</p>
                    </div>
                    <div>
                      <MetricLabel label="cLogP" tooltip={METRIC_TOOLTIPS.clogp.tooltip} />
                      <p className="font-semibold">{job.ligand_clogp ? job.ligand_clogp.toFixed(2) : 'N/A'}</p>
                    </div>
                    <div>
                      <MetricLabel label="TPSA" tooltip={METRIC_TOOLTIPS.tpsa.tooltip} />
                      <p className="font-semibold">{job.ligand_tpsa ? `${job.ligand_tpsa.toFixed(1)} Å²` : 'N/A'}</p>
                    </div>
                    <div>
                      <MetricLabel label="H-Bond Donors" tooltip={METRIC_TOOLTIPS.hbd.tooltip} />
                      <p className="font-semibold">{job.ligand_hbd ?? 'N/A'}</p>
                    </div>
                    <div>
                      <MetricLabel label="H-Bond Acceptors" tooltip={METRIC_TOOLTIPS.hba.tooltip} />
                      <p className="font-semibold">{job.ligand_hba ?? 'N/A'}</p>
                    </div>
                    <div>
                      <MetricLabel label="Rotatable Bonds" tooltip={METRIC_TOOLTIPS.rotBonds.tooltip} />
                      <p className="font-semibold">{job.ligand_rotatable_bonds ?? 'N/A'}</p>
                    </div>
                  </div>

                  {job.ligand_smiles && (
                    <div className="mt-4">
                      <p className="text-sm text-muted-foreground mb-1">SMILES</p>
                      <p className="font-mono text-xs break-all bg-muted/50 p-2 rounded">{job.ligand_smiles}</p>
                    </div>
                  )}
                </div>

                {/* Rule of Five */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4" />
                    <ScientificTooltip content={METRIC_TOOLTIPS.ruleOfFive.tooltip}>
                      Lipinski Rule of Five
                    </ScientificTooltip>
                  </h4>

                  {job.ligand_mw && job.ligand_clogp !== undefined && job.ligand_hbd !== undefined && job.ligand_hba !== undefined ? (
                    <div className="space-y-3">
                      <div className="flex items-center gap-3">
                        <StatusChip label={drugLikenessStatus.label} colorClass={drugLikenessStatus.color} />
                        <span className="text-sm text-muted-foreground">
                          {violations.length === 0 ? 'All criteria met' : `${violations.length} violation(s)`}
                        </span>
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <span>MW ≤ 500 Da</span>
                          <Badge variant={job.ligand_mw <= 500 ? 'default' : 'destructive'} className="text-xs">
                            {job.ligand_mw <= 500 ? 'Pass' : 'Fail'}
                          </Badge>
                        </div>
                        <div className="flex items-center justify-between text-sm">
                          <span>cLogP ≤ 5</span>
                          <Badge variant={job.ligand_clogp <= 5 ? 'default' : 'destructive'} className="text-xs">
                            {job.ligand_clogp <= 5 ? 'Pass' : 'Fail'}
                          </Badge>
                        </div>
                        <div className="flex items-center justify-between text-sm">
                          <span>HBD ≤ 5</span>
                          <Badge variant={job.ligand_hbd <= 5 ? 'default' : 'destructive'} className="text-xs">
                            {job.ligand_hbd <= 5 ? 'Pass' : 'Fail'}
                          </Badge>
                        </div>
                        <div className="flex items-center justify-between text-sm">
                          <span>HBA ≤ 10</span>
                          <Badge variant={job.ligand_hba <= 10 ? 'default' : 'destructive'} className="text-xs">
                            {job.ligand_hba <= 10 ? 'Pass' : 'Fail'}
                          </Badge>
                        </div>
                      </div>

                      <p className="text-xs text-muted-foreground mt-2">
                        {VALUE_PROPOSITIONS.useCaseDescriptions.properties}
                      </p>
                    </div>
                  ) : (
                    <p className="text-muted-foreground text-sm">Insufficient data for Rule of Five assessment</p>
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
                Target & Analysis Details
              </CardTitle>
              <CardDescription>
                Target protein information, model parameters, and computational details
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                {/* Target Information */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">Target Protein</h4>
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
                      <p className="text-sm text-muted-foreground">Binding Site</p>
                      <p className="font-medium">{job.target_pocket || 'N/A'}</p>
                    </div>
                  </div>

                  {/* EGFR specific context */}
                  {job.target_pdb === '1M17' && (
                    <div className="p-3 bg-muted/50 rounded-lg text-sm">
                      <p className="font-medium">{EGFR_CONTEXT.targetInfo.name}</p>
                      <p className="text-muted-foreground text-xs mt-1">{EGFR_CONTEXT.targetInfo.description}</p>
                    </div>
                  )}
                </div>

                {/* Run Information */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">Computation Details</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <p className="text-sm text-muted-foreground">Model Version</p>
                      <p className="font-medium">{job.model_version || 'Boltz-2.0'}</p>
                    </div>
                    <div className="flex justify-between">
                      <p className="text-sm text-muted-foreground">Device</p>
                      <p className="font-medium">{job.device || 'N/A'}</p>
                    </div>
                    <div className="flex justify-between">
                      <p className="text-sm text-muted-foreground">Runtime</p>
                      <p className="font-medium">{job.total_runtime ? `${job.total_runtime.toFixed(1)}s` : 'N/A'}</p>
                    </div>
                    <div className="flex justify-between">
                      <p className="text-sm text-muted-foreground">Data Completeness</p>
                      <p className="font-medium">{job.data_completeness ? `${job.data_completeness.toFixed(1)}%` : 'N/A'}</p>
                    </div>
                    <div className="flex justify-between">
                      <p className="text-sm text-muted-foreground">Pocket Detection</p>
                      <p className="font-medium">{job.pocket_detection_method || 'fpocket'}</p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Actions & Export */}
          <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">
            <Button variant="outline" size="lg" onClick={downloadCSV}>
              <FileText className="mr-2 h-4 w-4" />
              Download CSV
            </Button>
            <Button variant="outline" size="lg" onClick={downloadPDFReport}>
              <Download className="mr-2 h-4 w-4" />
              Download Report (PDF)
            </Button>
            <Button asChild variant="hero" size="lg">
              <Link to={`/job/${job.id || id}/viewer`}>
                <Maximize2 className="mr-2 h-4 w-4" />
                View Top Pose in 3D
              </Link>
            </Button>
            <Button asChild variant="molecular" size="lg">
              <Link to="/job/new">
                New Analysis
              </Link>
            </Button>
          </div>

          {/* Why This Matters Section */}
          <div className="mt-8 p-6 bg-gradient-to-br from-primary/5 via-background to-secondary/5 rounded-lg border border-primary/20">
            <div className="flex items-start gap-3">
              <Sparkles className="h-6 w-6 text-primary mt-1 flex-shrink-0" />
              <div>
                <h3 className="text-lg font-semibold mb-2">🧬 Why This Matters</h3>
                <p className="text-muted-foreground leading-relaxed">
                  These results give medicinal chemists rapid, structure-based insight into how potential inhibitors bind {job.target_pdb === '1M17' ? 'EGFR' : 'the target protein'}.
                  By examining predicted affinity, pose quality, and key stabilizing residues, researchers can <strong className="text-foreground">prioritize the most
                  promising analogs before committing to costly synthesis and wet-lab assays</strong>. This accelerates hit-to-lead optimization
                  and reduces both the time and cost of early-stage drug discovery.
                </p>
              </div>
            </div>
          </div>

          {/* Value Proposition Footer */}
          <div className="mt-6 p-4 bg-muted/30 rounded-lg border border-border">
            <p className="text-sm text-center text-muted-foreground">
              <strong className="text-foreground">How to use these results:</strong> {VALUE_PROPOSITIONS.useCaseDescriptions.results}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobResults;
