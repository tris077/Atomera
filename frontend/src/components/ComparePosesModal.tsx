import React from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { ArrowRight, TrendingDown, TrendingUp } from 'lucide-react';

interface PoseData {
  id: number;
  name: string;
  affinity: number;
  deltaG: number;
  confidence: number;
  rmsd: number;
  hbonds: number;
  hydrophobic: number;
  saltBridges: number;
  clashScore: number;
}

interface ComparePosesModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  pose1: PoseData;
  pose2: PoseData;
}

export function ComparePosesModal({ open, onOpenChange, pose1, pose2 }: ComparePosesModalProps) {
  const getDelta = (val1: number, val2: number, lowerIsBetter: boolean = true) => {
    const delta = val2 - val1;
    const isBetter = lowerIsBetter ? delta < 0 : delta > 0;
    return { delta, isBetter };
  };

  const affinityDelta = getDelta(pose1.affinity, pose2.affinity, true);
  const deltaGDelta = getDelta(pose1.deltaG, pose2.deltaG, true);
  const confidenceDelta = getDelta(pose1.confidence, pose2.confidence, false);
  const rmsdDelta = getDelta(pose1.rmsd, pose2.rmsd, true);
  const clashDelta = getDelta(pose1.clashScore, pose2.clashScore, true);

  const DeltaIndicator = ({ delta, isBetter }: { delta: number; isBetter: boolean }) => {
    if (Math.abs(delta) < 0.01) return <span className="text-muted-foreground">~</span>;
    return (
      <span className={isBetter ? 'text-green-600' : 'text-red-600'}>
        {isBetter ? <TrendingDown className="h-3 w-3 inline" /> : <TrendingUp className="h-3 w-3 inline" />}
        {Math.abs(delta).toFixed(2)}
      </span>
    );
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            Pose Comparison
            <ArrowRight className="h-4 w-4 text-muted-foreground" />
          </DialogTitle>
          <DialogDescription>
            Side-by-side comparison of binding predictions for informed medicinal chemistry decisions
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Header Row */}
          <div className="grid grid-cols-3 gap-4 items-center">
            <div className="text-center">
              <Badge className="bg-primary mb-2">{pose1.name}</Badge>
              <p className="text-xs text-muted-foreground">Reference</p>
            </div>
            <div className="text-center">
              <p className="text-xs font-medium text-muted-foreground uppercase">Metric</p>
            </div>
            <div className="text-center">
              <Badge className="bg-secondary mb-2">{pose2.name}</Badge>
              <p className="text-xs text-muted-foreground">Comparison</p>
            </div>
          </div>

          {/* Binding Affinity */}
          <div className="border rounded-lg p-4 bg-muted/20">
            <h4 className="font-semibold text-sm mb-3 text-primary">Binding Affinity</h4>

            <div className="grid grid-cols-3 gap-4 items-center mb-2">
              <div className="text-center">
                <p className="text-2xl font-bold text-primary">{pose1.affinity.toFixed(1)}</p>
                <p className="text-xs text-muted-foreground">nM</p>
              </div>
              <div className="text-center">
                <p className="text-sm font-medium">Kd</p>
                <DeltaIndicator delta={affinityDelta.delta} isBetter={affinityDelta.isBetter} />
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-secondary">{pose2.affinity.toFixed(1)}</p>
                <p className="text-xs text-muted-foreground">nM</p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 items-center">
              <div className="text-center">
                <p className="text-xl font-bold">{pose1.deltaG.toFixed(1)}</p>
                <p className="text-xs text-muted-foreground">kcal/mol</p>
              </div>
              <div className="text-center">
                <p className="text-sm font-medium">ΔG</p>
                <DeltaIndicator delta={deltaGDelta.delta} isBetter={deltaGDelta.isBetter} />
              </div>
              <div className="text-center">
                <p className="text-xl font-bold">{pose2.deltaG.toFixed(1)}</p>
                <p className="text-xs text-muted-foreground">kcal/mol</p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 items-center mt-2">
              <div className="text-center">
                <p className="text-lg font-bold">{(pose1.confidence * 100).toFixed(0)}%</p>
              </div>
              <div className="text-center">
                <p className="text-sm font-medium">Confidence</p>
                <DeltaIndicator delta={confidenceDelta.delta * 100} isBetter={confidenceDelta.isBetter} />
              </div>
              <div className="text-center">
                <p className="text-lg font-bold">{(pose2.confidence * 100).toFixed(0)}%</p>
              </div>
            </div>
          </div>

          {/* Pose Quality */}
          <div className="border rounded-lg p-4 bg-muted/20">
            <h4 className="font-semibold text-sm mb-3 text-primary">Pose Quality</h4>

            <div className="grid grid-cols-3 gap-4 items-center mb-2">
              <div className="text-center">
                <p className="text-xl font-bold">{pose1.rmsd.toFixed(1)} Å</p>
              </div>
              <div className="text-center">
                <p className="text-sm font-medium">RMSD</p>
                <DeltaIndicator delta={rmsdDelta.delta} isBetter={rmsdDelta.isBetter} />
              </div>
              <div className="text-center">
                <p className="text-xl font-bold">{pose2.rmsd.toFixed(1)} Å</p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 items-center">
              <div className="text-center">
                <p className="text-xl font-bold">{pose1.clashScore.toFixed(1)}</p>
              </div>
              <div className="text-center">
                <p className="text-sm font-medium">Clash Score</p>
                <DeltaIndicator delta={clashDelta.delta} isBetter={clashDelta.isBetter} />
              </div>
              <div className="text-center">
                <p className="text-xl font-bold">{pose2.clashScore.toFixed(1)}</p>
              </div>
            </div>
          </div>

          {/* Key Interactions */}
          <div className="border rounded-lg p-4 bg-muted/20">
            <h4 className="font-semibold text-sm mb-3 text-primary">Molecular Interactions</h4>

            <div className="space-y-2">
              <div className="grid grid-cols-3 gap-4 items-center text-sm">
                <div className="text-center font-semibold">{pose1.hbonds}</div>
                <div className="text-center text-muted-foreground">H-bonds</div>
                <div className="text-center font-semibold">{pose2.hbonds}</div>
              </div>
              <div className="grid grid-cols-3 gap-4 items-center text-sm">
                <div className="text-center font-semibold">{pose1.hydrophobic}</div>
                <div className="text-center text-muted-foreground">Hydrophobic</div>
                <div className="text-center font-semibold">{pose2.hydrophobic}</div>
              </div>
              <div className="grid grid-cols-3 gap-4 items-center text-sm">
                <div className="text-center font-semibold">{pose1.saltBridges}</div>
                <div className="text-center text-muted-foreground">Salt Bridges</div>
                <div className="text-center font-semibold">{pose2.saltBridges}</div>
              </div>
              <div className="grid grid-cols-3 gap-4 items-center text-sm border-t pt-2 mt-2">
                <div className="text-center font-bold text-primary">
                  {pose1.hbonds + pose1.hydrophobic + pose1.saltBridges}
                </div>
                <div className="text-center text-muted-foreground font-medium">Total Contacts</div>
                <div className="text-center font-bold text-secondary">
                  {pose2.hbonds + pose2.hydrophobic + pose2.saltBridges}
                </div>
              </div>
            </div>
          </div>

          {/* Summary */}
          <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-sm text-blue-800">
              <strong>Analysis:</strong> {pose1.name} shows{' '}
              {pose1.affinity < pose2.affinity ? 'stronger' : 'weaker'} predicted binding (
              {Math.abs(affinityDelta.delta).toFixed(1)}x difference in Kd) and{' '}
              {pose1.rmsd < pose2.rmsd ? 'better' : 'lower'} pose stability. Consider {pose1.name} as the
              lead optimization candidate for further SAR studies.
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
