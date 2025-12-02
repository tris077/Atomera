import React, { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import Protein3DViewer from '@/components/Protein3DViewer';
import MolecularBackground from '@/components/MolecularBackground';
import Navigation from '@/components/Navigation';
import { ArrowLeft, Download, Share2, Maximize2, Info, FileText, Lightbulb, ChevronRight, GitCompare, Sparkles } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { StatusChip, ConfidenceBar, MetricLabel } from '@/components/ui/scientific-tooltip';
import { METRIC_TOOLTIPS, SCIENTIFIC_NARRATIVES, STATUS_CHIPS, VALUE_PROPOSITIONS, EGFR_CONTEXT } from '@/lib/scientificContent';
import { ComparePosesModal } from '@/components/ComparePosesModal';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { ChevronDown } from 'lucide-react';

const Viewer3D: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [selectedPose, setSelectedPose] = useState(0);
  const [showDemoGuide, setShowDemoGuide] = useState(true);
  const [showCompareModal, setShowCompareModal] = useState(false);

  // Mock pose data - in real app, this would come from job results
  const poses = [
    { id: 0, name: 'Pose 1 (Top)', affinity: 2.3, deltaG: -12.1, confidence: 0.95, rmsd: 0.8, hbonds: 4, hydrophobic: 7, saltBridges: 2, clashScore: 2.1 },
    { id: 1, name: 'Pose 2', affinity: 3.1, deltaG: -11.5, confidence: 0.92, rmsd: 1.2, hbonds: 3, hydrophobic: 6, saltBridges: 1, clashScore: 2.8 },
    { id: 2, name: 'Pose 3', affinity: 4.5, deltaG: -10.9, confidence: 0.88, rmsd: 1.5, hbonds: 3, hydrophobic: 5, saltBridges: 2, clashScore: 3.2 },
    { id: 3, name: 'Pose 4', affinity: 6.2, deltaG: -10.2, confidence: 0.84, rmsd: 1.9, hbonds: 2, hydrophobic: 6, saltBridges: 1, clashScore: 3.7 },
    { id: 4, name: 'Pose 5', affinity: 8.1, deltaG: -9.8, confidence: 0.79, rmsd: 2.3, hbonds: 2, hydrophobic: 4, saltBridges: 0, clashScore: 4.1 },
  ];

  const currentPose = poses[selectedPose];

  // Status chips for current pose
  const affinityStatus = STATUS_CHIPS.affinity(currentPose.affinity);
  const confidenceStatus = STATUS_CHIPS.confidence(currentPose.confidence);
  const poseStatus = STATUS_CHIPS.pose(currentPose.rmsd);

  const handlePoseChange = (poseId: number) => {
    setSelectedPose(poseId);
  };

  // Generate pose-specific narrative
  const poseNarrative = SCIENTIFIC_NARRATIVES.poseNarrative(currentPose, selectedPose + 1);

  return (
    <div className="min-h-screen bg-background relative">
      <Navigation />
      <MolecularBackground intensity="light" />

      <div className="relative z-10 container mx-auto px-4 py-8 max-w-7xl">
        {/* Demo Guide Banner */}
        {showDemoGuide && id?.startsWith('demo-') && (
          <div className="mb-6 bg-gradient-to-r from-primary/10 via-secondary/10 to-primary/10 border border-primary/20 rounded-lg p-4">
            <div className="flex items-start justify-between">
              <div className="flex gap-3">
                <Lightbulb className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                <div>
                  <h3 className="font-semibold text-sm text-primary mb-1">Interactive 3D Exploration</h3>
                  <p className="text-sm text-muted-foreground mb-2">
                    This view shows the predicted binding pose in the EGFR kinase ATP-binding pocket. Explore how the inhibitor interacts with key residues.
                  </p>
                  <div className="flex flex-wrap gap-2 text-xs">
                    <span className="text-muted-foreground">Try:</span>
                    <span className="bg-white/50 px-2 py-0.5 rounded">Click "Binding View" preset</span>
                    <ChevronRight className="h-3 w-3 text-muted-foreground" />
                    <span className="bg-white/50 px-2 py-0.5 rounded">Click residues to highlight</span>
                    <ChevronRight className="h-3 w-3 text-muted-foreground" />
                    <span className="bg-white/50 px-2 py-0.5 rounded">Switch poses in dropdown</span>
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
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate(-1)}
              className="hover:bg-primary/10"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Results
            </Button>
            <div>
              <h1 className="text-3xl font-bold">3D Structure Viewer</h1>
              <p className="text-muted-foreground">Interactive binding pose visualization • EGFR ATP-binding pocket</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <StatusChip label={affinityStatus.label} colorClass={affinityStatus.color} />
            <StatusChip label={poseStatus.label} colorClass={poseStatus.color} />
          </div>
        </div>

        {/* Scientific Context Card */}
        <Card className="shadow-card mb-6 border-blue-200 bg-blue-50/50">
          <CardContent className="pt-4 pb-4">
            <div className="flex items-start gap-3">
              <Info className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm text-blue-800 font-medium mb-1">What you're viewing</p>
                <p className="text-sm text-blue-700">{poseNarrative}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Main Viewer */}
        <Protein3DViewer
          jobId={id}
          height="700px"
          poses={poses}
          onPoseChange={handlePoseChange}
        />

        {/* Pose-Specific Data Cards - Collapsible */}
        <Collapsible defaultOpen>
          <Card className="shadow-card mt-6">
            <CollapsibleTrigger asChild>
              <CardHeader className="cursor-pointer hover:bg-muted/50 transition-colors">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-base flex items-center gap-2">
                    <Info className="h-5 w-5 text-primary" />
                    Binding Metrics — {currentPose.name}
                  </CardTitle>
                  <div className="flex items-center gap-2">
                    <StatusChip label={confidenceStatus.label} colorClass={confidenceStatus.color} />
                    <ChevronDown className="h-4 w-4 transition-transform data-[state=open]:rotate-180" />
                  </div>
                </div>
                <CardDescription>Predicted binding affinity, molecular interactions, and pose quality assessment</CardDescription>
              </CardHeader>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <CardContent className="pt-0">
                <div className="grid md:grid-cols-3 gap-6">
                  {/* Binding Affinity */}
                  <div className="space-y-3">
                    <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">Binding Affinity</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <MetricLabel label="Kd" tooltip={METRIC_TOOLTIPS.kd.tooltip} />
                        <Badge className="bg-primary">{currentPose.affinity} nM</Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <MetricLabel label="ΔG" tooltip={METRIC_TOOLTIPS.deltaG.tooltip} />
                        <Badge className="bg-secondary">{currentPose.deltaG} kcal/mol</Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <MetricLabel label="Confidence" tooltip={METRIC_TOOLTIPS.confidence.tooltip} />
                        <span className="text-sm font-medium">{(currentPose.confidence * 100).toFixed(0)}%</span>
                      </div>
                      <ConfidenceBar value={currentPose.confidence} />
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {METRIC_TOOLTIPS.kd.interpretation(currentPose.affinity)}
                    </p>
                  </div>

                  {/* Key Interactions */}
                  <div className="space-y-3">
                    <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">Key Interactions</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <MetricLabel label="H-bonds" tooltip={METRIC_TOOLTIPS.hbonds.tooltip} />
                        <span className="font-semibold">{currentPose.hbonds}</span>
                      </div>
                      <div className="flex justify-between">
                        <MetricLabel label="Hydrophobic" tooltip={METRIC_TOOLTIPS.hydrophobic.tooltip} />
                        <span className="font-semibold">{currentPose.hydrophobic}</span>
                      </div>
                      <div className="flex justify-between">
                        <MetricLabel label="Salt bridges" tooltip={METRIC_TOOLTIPS.saltBridges.tooltip} />
                        <span className="font-semibold">{currentPose.saltBridges}</span>
                      </div>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Total contacts: {currentPose.hbonds + currentPose.hydrophobic + currentPose.saltBridges}
                    </p>
                  </div>

                  {/* Pose Quality */}
                  <div className="space-y-3">
                    <h4 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">Pose Quality</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <MetricLabel label="RMSD" tooltip={METRIC_TOOLTIPS.rmsd.tooltip} />
                        <span className="font-mono font-semibold">{currentPose.rmsd} Å</span>
                      </div>
                      <div className="flex justify-between">
                        <MetricLabel label="Clash score" tooltip={METRIC_TOOLTIPS.clashScore.tooltip} />
                        <span className="font-mono font-semibold">{currentPose.clashScore}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Quality</span>
                        <Badge variant="outline" className={`text-xs ${
                          currentPose.confidence > 0.9 ? 'bg-green-50 text-green-700 border-green-300' :
                          currentPose.confidence > 0.8 ? 'bg-yellow-50 text-yellow-700 border-yellow-300' :
                          'bg-orange-50 text-orange-700 border-orange-300'
                        }`}>
                          {currentPose.confidence > 0.9 ? 'Excellent' :
                           currentPose.confidence > 0.8 ? 'Good' : 'Fair'}
                        </Badge>
                      </div>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {METRIC_TOOLTIPS.rmsd.interpretation(currentPose.rmsd)}
                    </p>
                  </div>
                </div>
              </CardContent>
            </CollapsibleContent>
          </Card>
        </Collapsible>

        {/* EGFR Scientific Context */}
        {id?.startsWith('demo-') && (
          <Card className="shadow-card mt-6">
            <CardHeader>
              <CardTitle className="text-base">Target Context: EGFR Kinase</CardTitle>
              <CardDescription>Background information about the target protein</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="font-medium mb-1">{EGFR_CONTEXT.targetInfo.name}</p>
                  <p className="text-muted-foreground text-xs mb-2">{EGFR_CONTEXT.targetInfo.description}</p>
                  <p className="text-xs"><strong>Disease relevance:</strong> {EGFR_CONTEXT.targetInfo.diseaseRelevance}</p>
                </div>
                <div>
                  <p className="text-xs mb-2"><strong>Known inhibitors:</strong></p>
                  <div className="flex flex-wrap gap-1">
                    {EGFR_CONTEXT.targetInfo.knownInhibitors.map((drug, i) => (
                      <Badge key={i} variant="outline" className="text-xs">{drug}</Badge>
                    ))}
                  </div>
                  <p className="text-xs mt-2 text-muted-foreground">
                    <strong>Binding site:</strong> {EGFR_CONTEXT.targetInfo.bindingSite}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Action Buttons */}
        <div className="flex justify-center gap-4 mt-8 flex-wrap">
          {poses.length > 1 && (
            <Button
              variant="outline"
              size="lg"
              onClick={() => setShowCompareModal(true)}
              className="hover:bg-primary/10"
            >
              <GitCompare className="mr-2 h-4 w-4" />
              Compare with Pose 2
            </Button>
          )}
          <Button variant="outline" size="lg" asChild>
            <Link to={`/job/${id}/results`}>
              <FileText className="mr-2 h-4 w-4" />
              View Full Results
            </Link>
          </Button>
          <Button variant="hero" size="lg" asChild>
            <Link to="/job/new">
              Create New Analysis
            </Link>
          </Button>
        </div>

        {/* Why This Matters Section */}
        <div className="mt-8 p-6 bg-gradient-to-br from-primary/5 via-background to-secondary/5 rounded-lg border border-primary/20">
          <div className="flex items-start gap-3">
            <Sparkles className="h-6 w-6 text-primary mt-1 flex-shrink-0" />
            <div>
              <h3 className="text-lg font-semibold mb-2">Why This Matters</h3>
              <p className="text-muted-foreground leading-relaxed">
                These results give medicinal chemists rapid, structure-based insight into how potential inhibitors bind EGFR.
                By examining predicted affinity, pose quality, and key stabilizing residues, researchers can prioritize the most
                promising analogs before committing to costly synthesis and wet-lab assays. This accelerates hit-to-lead optimization
                and reduces the time and cost of early-stage drug discovery.
              </p>
            </div>
          </div>
        </div>

        {/* Value Proposition Footer */}
        <div className="mt-6 p-4 bg-muted/30 rounded-lg border border-border">
          <p className="text-sm text-center text-muted-foreground">
            <strong className="text-foreground">How to use this view:</strong> {VALUE_PROPOSITIONS.useCaseDescriptions.viewer}
          </p>
        </div>
      </div>

      {/* Compare Poses Modal */}
      <ComparePosesModal
        open={showCompareModal}
        onOpenChange={setShowCompareModal}
        pose1={poses[0]}
        pose2={poses[1]}
      />
    </div>
  );
};

export default Viewer3D;
