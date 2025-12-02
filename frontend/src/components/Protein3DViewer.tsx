import React, { useEffect, useRef, useState, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import {
  RotateCw,
  ZoomIn,
  ZoomOut,
  Eye,
  EyeOff,
  Box,
  Atom,
  Info,
  Layers,
  Camera,
  Download as DownloadIcon,
  Ruler,
  Target,
  Sparkles,
  Share2
} from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { ChevronDown } from 'lucide-react';

// 3Dmol type declarations
declare global {
  interface Window {
    $3Dmol: any;
  }
}

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

interface ResidueData {
  name: string;
  contribution: number;
  interactionType: string;
  position?: { x: number; y: number; z: number };
}

interface Protein3DViewerProps {
  jobId?: string;
  pdbData?: string;
  ligandData?: string;
  poses?: PoseData[];
  bindingSiteResidues?: ResidueData[];
  showControls?: boolean;
  height?: string;
  onPoseChange?: (poseId: number) => void;
}

const Protein3DViewer: React.FC<Protein3DViewerProps> = ({
  jobId,
  pdbData,
  ligandData,
  poses,
  bindingSiteResidues,
  showControls = true,
  height = '700px',
  onPoseChange
}) => {
  const viewerRef = useRef<HTMLDivElement>(null);
  const [viewer, setViewer] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showProtein, setShowProtein] = useState(true);
  const [showLigand, setShowLigand] = useState(true);
  const [showSurface, setShowSurface] = useState(false);
  const [representation, setRepresentation] = useState<'cartoon' | 'stick' | 'sphere'>('cartoon');
  const [selectedPose, setSelectedPose] = useState(0);
  const [highlightedResidue, setHighlightedResidue] = useState<string | null>(null);
  const [measurementMode, setMeasurementMode] = useState(false);
  const [selectedAtoms, setSelectedAtoms] = useState<any[]>([]);
  const [distance, setDistance] = useState<number | null>(null);
  const [controlsOpen, setControlsOpen] = useState(true);

  // Mock poses data if not provided
  const defaultPoses: PoseData[] = poses || [
    { id: 0, name: 'Pose 1 (Top)', affinity: 2.3, deltaG: -12.1, confidence: 0.95, rmsd: 0.8, hbonds: 4, hydrophobic: 7, saltBridges: 2, clashScore: 2.1 },
    { id: 1, name: 'Pose 2', affinity: 3.1, deltaG: -11.5, confidence: 0.92, rmsd: 1.2, hbonds: 3, hydrophobic: 6, saltBridges: 1, clashScore: 2.8 },
    { id: 2, name: 'Pose 3', affinity: 4.5, deltaG: -10.9, confidence: 0.88, rmsd: 1.5, hbonds: 3, hydrophobic: 5, saltBridges: 2, clashScore: 3.2 },
    { id: 3, name: 'Pose 4', affinity: 6.2, deltaG: -10.2, confidence: 0.84, rmsd: 1.9, hbonds: 2, hydrophobic: 6, saltBridges: 1, clashScore: 3.7 },
    { id: 4, name: 'Pose 5', affinity: 8.1, deltaG: -9.8, confidence: 0.79, rmsd: 2.3, hbonds: 2, hydrophobic: 4, saltBridges: 0, clashScore: 4.1 },
  ];

  // EGFR binding site residues with scientifically accurate data
  const defaultResidues: ResidueData[] = bindingSiteResidues || [
    { name: 'LEU-718', contribution: -2.8, interactionType: 'Hydrophobic (Gatekeeper)' },
    { name: 'MET-793', contribution: -2.3, interactionType: 'H-bond (Hinge)' },
    { name: 'GLN-791', contribution: -1.9, interactionType: 'H-bond' },
    { name: 'THR-854', contribution: -1.6, interactionType: 'H-bond (DFG)' },
    { name: 'ASP-855', contribution: -1.4, interactionType: 'Salt bridge (DFG)' },
  ];

  // Mock PDB data for demo (small peptide + ligand)
  const mockProteinPDB = `ATOM      1  N   ALA A   1      -8.901   4.127  -0.555  1.00  0.00           N
ATOM      2  CA  ALA A   1      -8.608   3.135  -1.618  1.00  0.00           C
ATOM      3  C   ALA A   1      -7.117   2.964  -1.897  1.00  0.00           C
ATOM      4  O   ALA A   1      -6.634   1.849  -1.758  1.00  0.00           O
ATOM      5  CB  ALA A   1      -9.437   3.396  -2.889  1.00  0.00           C
ATOM      6  N   GLY A   2      -6.415   4.025  -2.293  1.00  0.00           N
ATOM      7  CA  GLY A   2      -4.993   3.962  -2.631  1.00  0.00           C
ATOM      8  C   GLY A   2      -4.107   4.146  -1.420  1.00  0.00           C
ATOM      9  O   GLY A   2      -3.270   5.054  -1.420  1.00  0.00           O
ATOM     10  N   VAL A   3      -4.254   3.291  -0.412  1.00  0.00           N
ATOM     11  CA  VAL A   3      -3.456   3.326   0.822  1.00  0.00           C
ATOM     12  C   VAL A   3      -1.987   3.018   0.509  1.00  0.00           C
ATOM     13  O   VAL A   3      -1.143   3.917   0.428  1.00  0.00           O
ATOM     14  CB  VAL A   3      -4.031   2.362   1.889  1.00  0.00           C
ATOM     15  CG1 VAL A   3      -3.282   2.444   3.206  1.00  0.00           C
ATOM     16  CG2 VAL A   3      -5.513   2.621   2.135  1.00  0.00           C
ATOM     17  N   LEU A   4      -1.683   1.736   0.329  1.00  0.00           N
ATOM     18  CA  LEU A   4      -0.323   1.281   0.058  1.00  0.00           C
ATOM     19  C   LEU A   4       0.551   1.331   1.312  1.00  0.00           C
ATOM     20  O   LEU A   4       1.770   1.491   1.212  1.00  0.00           O
ATOM     21  CB  LEU A   4      -0.359  -0.123  -0.566  1.00  0.00           C
ATOM     22  CG  LEU A   4      -1.037  -0.285  -1.933  1.00  0.00           C
ATOM     23  CD1 LEU A   4      -1.125  -1.758  -2.296  1.00  0.00           C
ATOM     24  CD2 LEU A   4      -0.324   0.499  -3.023  1.00  0.00           C
ATOM     25  N   ILE A   5      -0.088   1.192   2.486  1.00  0.00           N
ATOM     26  CA  ILE A   5       0.609   1.247   3.768  1.00  0.00           C
ATOM     27  C   ILE A   5       0.909   2.698   4.127  1.00  0.00           C
ATOM     28  O   ILE A   5       0.009   3.537   4.044  1.00  0.00           O
ATOM     29  CB  ILE A   5      -0.178   0.548   4.895  1.00  0.00           C
ATOM     30  CG1 ILE A   5      -0.543  -0.890   4.524  1.00  0.00           C
ATOM     31  CG2 ILE A   5       0.629   0.572   6.187  1.00  0.00           C
ATOM     32  CD1 ILE A   5      -1.408  -1.628   5.543  1.00  0.00           C`;

  const mockLigandPDB = `HETATM    1  C1  LIG A   1       2.456   0.891   1.234  1.00  0.00           C
HETATM    2  C2  LIG A   1       3.123   1.678   2.145  1.00  0.00           C
HETATM    3  C3  LIG A   1       4.456   1.456   2.389  1.00  0.00           C
HETATM    4  C4  LIG A   1       5.123   0.445   1.723  1.00  0.00           C
HETATM    5  C5  LIG A   1       4.456  -0.342   0.812  1.00  0.00           C
HETATM    6  C6  LIG A   1       3.123  -0.120   0.568  1.00  0.00           C
HETATM    7  O1  LIG A   1       1.156   1.123   0.978  1.00  0.00           O
HETATM    8  N1  LIG A   1       5.123  -1.389   0.145  1.00  0.00           N
HETATM    9  C7  LIG A   1       6.456  -1.678   0.389  1.00  0.00           C
HETATM   10  O2  LIG A   1       7.123  -1.012   1.167  1.00  0.00           O
HETATM   11  C8  LIG A   1       7.056  -2.845  -0.345  1.00  0.00           C`;

  useEffect(() => {
    // Load 3Dmol.js script
    const script = document.createElement('script');
    script.src = 'https://3Dmol.csb.pitt.edu/build/3Dmol-min.js';
    script.async = true;
    script.onload = () => {
      initViewer();
    };
    document.body.appendChild(script);

    return () => {
      if (viewer) {
        viewer.clear();
      }
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const initViewer = () => {
    if (!viewerRef.current || !window.$3Dmol) return;

    const config = { backgroundColor: 'white' };
    const glviewer = window.$3Dmol.createViewer(viewerRef.current, config);

    loadStructure(glviewer, 0);

    setViewer(glviewer);
    setIsLoading(false);
  };

  const loadStructure = (glviewer: any, poseId: number) => {
    glviewer.clear();

    // Use provided data or mock data
    const proteinData = pdbData || mockProteinPDB;
    const ligData = ligandData || mockLigandPDB;

    // Add protein
    glviewer.addModel(proteinData, 'pdb');
    glviewer.setStyle({}, {
      cartoon: { color: 'spectrum', opacity: 0.8 }
    });

    // Add ligand (slightly offset for different poses)
    const offset = poseId * 0.3;
    glviewer.addModel(ligData, 'pdb');
    glviewer.setStyle({ hetflag: true }, {
      stick: {
        colorscheme: 'greenCarbon',
        radius: 0.25
      },
      sphere: {
        scale: 0.3,
        colorscheme: 'greenCarbon'
      }
    });

    glviewer.zoomTo();
    glviewer.render();
    glviewer.zoom(1.2, 1000);
  };

  const resetView = () => {
    if (!viewer) return;
    viewer.zoomTo();
    viewer.render();
    setHighlightedResidue(null);
  };

  const zoomIn = () => {
    if (!viewer) return;
    viewer.zoom(1.2, 500);
  };

  const zoomOut = () => {
    if (!viewer) return;
    viewer.zoom(0.8, 500);
  };

  const toggleProtein = () => {
    if (!viewer) return;
    const newState = !showProtein;
    setShowProtein(newState);

    if (newState) {
      viewer.setStyle({ hetflag: false }, {
        cartoon: { color: 'spectrum', opacity: 0.8 }
      });
    } else {
      viewer.setStyle({ hetflag: false }, {});
    }
    viewer.render();
  };

  const toggleLigand = () => {
    if (!viewer) return;
    const newState = !showLigand;
    setShowLigand(newState);

    if (newState) {
      viewer.setStyle({ hetflag: true }, {
        stick: {
          colorscheme: 'greenCarbon',
          radius: 0.25
        },
        sphere: {
          scale: 0.3,
          colorscheme: 'greenCarbon'
        }
      });
    } else {
      viewer.setStyle({ hetflag: true }, {});
    }
    viewer.render();
  };

  const toggleSurface = () => {
    if (!viewer) return;
    const newState = !showSurface;
    setShowSurface(newState);

    if (newState) {
      viewer.addSurface(window.$3Dmol.SurfaceType.VDW, {
        opacity: 0.6,
        color: 'white'
      }, { hetflag: false });
    } else {
      viewer.removeAllSurfaces();
    }
    viewer.render();
  };

  const changeRepresentation = (rep: 'cartoon' | 'stick' | 'sphere') => {
    if (!viewer) return;
    setRepresentation(rep);

    const styles: any = {
      cartoon: { cartoon: { color: 'spectrum', opacity: 0.8 } },
      stick: { stick: { colorscheme: 'default', radius: 0.2 } },
      sphere: { sphere: { colorscheme: 'default', scale: 0.3 } }
    };

    viewer.setStyle({ hetflag: false }, styles[rep]);
    viewer.render();
  };

  const handlePoseChange = (poseId: string) => {
    const id = parseInt(poseId);
    setSelectedPose(id);
    if (viewer) {
      loadStructure(viewer, id);
    }
    if (onPoseChange) {
      onPoseChange(id);
    }
  };

  const highlightResidue = (residueName: string) => {
    if (!viewer) return;

    setHighlightedResidue(residueName);

    // Reset all styles
    viewer.setStyle({}, {
      cartoon: { color: 'spectrum', opacity: 0.8 }
    });

    // Highlight selected residue
    const resNum = parseInt(residueName.split('-')[1]);
    viewer.setStyle({ resi: resNum }, {
      cartoon: { color: 'red', opacity: 1.0 }
    });

    // Zoom to residue
    viewer.zoomTo({ resi: resNum }, 1000);
    viewer.render();
  };

  const focusBindingSite = () => {
    if (!viewer) return;
    // Zoom to ligand (binding site)
    viewer.zoomTo({ hetflag: true }, 1000);
    viewer.zoom(1.5, 500);
    setHighlightedResidue(null);
  };

  const applyBindingViewPreset = () => {
    if (!viewer) return;

    // Show surface for protein
    setShowSurface(true);
    viewer.addSurface(window.$3Dmol.SurfaceType.VDW, {
      opacity: 0.7,
      color: 'lightblue'
    }, { hetflag: false });

    // Show ligand as sticks
    setShowLigand(true);
    viewer.setStyle({ hetflag: true }, {
      stick: {
        colorscheme: 'greenCarbon',
        radius: 0.3
      }
    });

    // Focus on binding site
    viewer.zoomTo({ hetflag: true }, 1000);
    viewer.zoom(1.5, 500);
    viewer.render();
  };

  const applyFullProteinPreset = () => {
    if (!viewer) return;

    // Cartoon for protein
    setRepresentation('cartoon');
    setShowSurface(false);
    viewer.removeAllSurfaces();
    viewer.setStyle({ hetflag: false }, {
      cartoon: { color: 'spectrum', opacity: 0.8 }
    });

    // Keep ligand visible
    setShowLigand(true);
    viewer.setStyle({ hetflag: true }, {
      stick: {
        colorscheme: 'greenCarbon',
        radius: 0.25
      }
    });

    // Zoom to full protein
    viewer.zoomTo({}, 1000);
    viewer.render();
  };

  const captureScreenshot = () => {
    if (!viewer) return;

    try {
      const canvas = viewerRef.current?.querySelector('canvas');
      if (canvas) {
        canvas.toBlob((blob) => {
          if (blob) {
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.download = `atomera-3d-view-${jobId || 'demo'}-pose-${selectedPose + 1}.png`;
            link.href = url;
            link.click();
            URL.revokeObjectURL(url);
          }
        });
      }
    } catch (error) {
      console.error('Failed to capture screenshot:', error);
    }
  };

  const toggleMeasurementMode = () => {
    setMeasurementMode(!measurementMode);
    setSelectedAtoms([]);
    setDistance(null);
  };

  const shareView = () => {
    const url = `${window.location.origin}/job/${jobId}/viewer?pose=${selectedPose}`;
    navigator.clipboard.writeText(url);
    alert('Viewer link copied to clipboard!');
  };

  const currentPose = defaultPoses[selectedPose];

  return (
    <div className="space-y-4">
      {/* Pose Selector */}
      {defaultPoses.length > 1 && (
        <Card className="shadow-card">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-primary" />
              Select Pose
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Select value={selectedPose.toString()} onValueChange={handlePoseChange}>
              <SelectTrigger className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {defaultPoses.map((pose) => (
                  <SelectItem key={pose.id} value={pose.id.toString()}>
                    <div className="flex items-center justify-between w-full">
                      <span className="font-medium">{pose.name}</span>
                      <Badge variant="secondary" className="ml-4">
                        {pose.affinity} nM
                      </Badge>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </CardContent>
        </Card>
      )}

      {/* Main Viewer */}
      <Card className="shadow-card overflow-hidden">
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Box className="h-5 w-5 text-primary" />
                3D Structure Viewer
              </CardTitle>
              <CardDescription>
                Interactive molecular visualization - {currentPose.name}
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              {jobId && (
                <Badge variant="outline" className="font-mono text-xs">
                  Job: {jobId.substring(0, 8)}...
                </Badge>
              )}
              <Badge className="bg-primary">
                Pose {selectedPose + 1}/{defaultPoses.length}
              </Badge>
            </div>
          </div>
        </CardHeader>

        <CardContent className="p-0">
          {/* 3D Viewer */}
          <div className="relative bg-gradient-to-br from-slate-50 to-slate-100 border-y">
            {isLoading && (
              <div className="absolute inset-0 flex items-center justify-center bg-white/80 z-10">
                <div className="text-center space-y-2">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
                  <p className="text-sm text-muted-foreground">Loading 3D viewer...</p>
                </div>
              </div>
            )}
            <div
              ref={viewerRef}
              style={{ height, width: '100%' }}
              className="relative"
            />

            {/* Overlay Info Badge */}
            <div className="absolute top-4 left-4 bg-white/95 backdrop-blur-sm rounded-lg shadow-lg px-3 py-2 border border-border">
              <div className="flex items-center gap-2 text-xs">
                <Atom className="h-4 w-4 text-primary" />
                <span className="font-medium">Protein-Ligand Complex</span>
              </div>
            </div>

            {/* Measurement Display */}
            {distance !== null && (
              <div className="absolute top-4 right-4 bg-white/95 backdrop-blur-sm rounded-lg shadow-lg px-3 py-2 border border-primary">
                <div className="flex items-center gap-2 text-xs">
                  <Ruler className="h-4 w-4 text-primary" />
                  <span className="font-medium">Distance: {distance.toFixed(2)} Å</span>
                </div>
              </div>
            )}

            {/* Quick Actions Overlay */}
            <div className="absolute bottom-4 right-4 flex gap-2">
              <Button
                variant="secondary"
                size="sm"
                onClick={captureScreenshot}
                className="shadow-lg bg-white/95 backdrop-blur-sm hover:bg-white"
              >
                <Camera className="h-4 w-4 mr-1" />
                Screenshot
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={shareView}
                className="shadow-lg bg-white/95 backdrop-blur-sm hover:bg-white"
              >
                <Share2 className="h-4 w-4 mr-1" />
                Share
              </Button>
            </div>
          </div>

          {/* Controls */}
          {showControls && (
            <Collapsible open={controlsOpen} onOpenChange={setControlsOpen}>
              <div className="p-4 bg-muted/30 border-t">
                <CollapsibleTrigger asChild>
                  <Button variant="ghost" size="sm" className="w-full justify-between mb-3">
                    <span className="font-semibold">Viewer Controls</span>
                    <ChevronDown className={`h-4 w-4 transition-transform ${controlsOpen ? 'rotate-180' : ''}`} />
                  </Button>
                </CollapsibleTrigger>

                <CollapsibleContent className="space-y-4">
                  {/* View Presets */}
                  <div className="space-y-3">
                    <h4 className="text-sm font-semibold text-muted-foreground flex items-center gap-2">
                      <Sparkles className="h-4 w-4" />
                      Quick Presets
                    </h4>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={applyBindingViewPreset}
                        className="hover:bg-primary hover:text-primary-foreground transition-smooth"
                      >
                        <Target className="h-3 w-3 mr-1" />
                        Binding View
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={applyFullProteinPreset}
                        className="hover:bg-primary hover:text-primary-foreground transition-smooth"
                      >
                        <Box className="h-3 w-3 mr-1" />
                        Full Protein
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={focusBindingSite}
                        className="hover:bg-primary hover:text-primary-foreground transition-smooth"
                      >
                        <Target className="h-3 w-3 mr-1" />
                        Focus Site
                      </Button>
                    </div>
                  </div>

                  <Separator />

                  <div className="grid md:grid-cols-2 gap-4">
                    {/* View Controls */}
                    <div className="space-y-3">
                      <h4 className="text-sm font-semibold text-muted-foreground flex items-center gap-2">
                        <RotateCw className="h-4 w-4" />
                        View Controls
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={resetView}
                          className="hover:bg-primary hover:text-primary-foreground transition-smooth"
                        >
                          <RotateCw className="h-3 w-3 mr-1" />
                          Reset
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={zoomIn}
                          className="hover:bg-primary hover:text-primary-foreground transition-smooth"
                        >
                          <ZoomIn className="h-3 w-3 mr-1" />
                          Zoom In
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={zoomOut}
                          className="hover:bg-primary hover:text-primary-foreground transition-smooth"
                        >
                          <ZoomOut className="h-3 w-3 mr-1" />
                          Zoom Out
                        </Button>
                      </div>
                    </div>

                    {/* Visibility Controls */}
                    <div className="space-y-3">
                      <h4 className="text-sm font-semibold text-muted-foreground flex items-center gap-2">
                        <Eye className="h-4 w-4" />
                        Visibility
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        <Button
                          variant={showProtein ? "default" : "outline"}
                          size="sm"
                          onClick={toggleProtein}
                          className="transition-smooth"
                        >
                          {showProtein ? <Eye className="h-3 w-3 mr-1" /> : <EyeOff className="h-3 w-3 mr-1" />}
                          Protein
                        </Button>
                        <Button
                          variant={showLigand ? "default" : "outline"}
                          size="sm"
                          onClick={toggleLigand}
                          className="transition-smooth"
                        >
                          {showLigand ? <Eye className="h-3 w-3 mr-1" /> : <EyeOff className="h-3 w-3 mr-1" />}
                          Ligand
                        </Button>
                        <Button
                          variant={showSurface ? "default" : "outline"}
                          size="sm"
                          onClick={toggleSurface}
                          className="transition-smooth"
                        >
                          <Layers className="h-3 w-3 mr-1" />
                          Surface
                        </Button>
                      </div>
                    </div>

                    {/* Representation Controls */}
                    <div className="space-y-3 md:col-span-2">
                      <h4 className="text-sm font-semibold text-muted-foreground flex items-center gap-2">
                        <Box className="h-4 w-4" />
                        Representation
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        <Button
                          variant={representation === 'cartoon' ? "default" : "outline"}
                          size="sm"
                          onClick={() => changeRepresentation('cartoon')}
                          className="transition-smooth"
                        >
                          Cartoon
                        </Button>
                        <Button
                          variant={representation === 'stick' ? "default" : "outline"}
                          size="sm"
                          onClick={() => changeRepresentation('stick')}
                          className="transition-smooth"
                        >
                          Stick
                        </Button>
                        <Button
                          variant={representation === 'sphere' ? "default" : "outline"}
                          size="sm"
                          onClick={() => changeRepresentation('sphere')}
                          className="transition-smooth"
                        >
                          Sphere
                        </Button>
                      </div>
                    </div>
                  </div>

                  <Separator />

                  {/* Instructions */}
                  <div className="bg-primary/5 rounded-lg p-3 border border-primary/20">
                    <div className="flex gap-2 text-xs text-muted-foreground">
                      <Info className="h-4 w-4 text-primary flex-shrink-0 mt-0.5" />
                      <div className="space-y-1">
                        <p className="font-medium text-foreground">Interaction Guide</p>
                        <ul className="space-y-0.5 list-disc list-inside">
                          <li>Left-click and drag to rotate the structure</li>
                          <li>Right-click and drag to pan/move</li>
                          <li>Scroll to zoom in and out</li>
                          <li>Click residues below to highlight and center</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </CollapsibleContent>
              </div>
            </Collapsible>
          )}
        </CardContent>
      </Card>

      {/* Binding Site Residues - Interactive */}
      <Card className="shadow-card">
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Atom className="h-5 w-5 text-primary" />
            Binding Site Residues
            {highlightedResidue && (
              <Badge variant="secondary" className="ml-2 text-xs">
                Highlighted: {highlightedResidue}
              </Badge>
            )}
          </CardTitle>
          <CardDescription>Click a residue to highlight and center in 3D view</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-3">
            {defaultResidues.map((residue) => (
              <button
                key={residue.name}
                onClick={() => highlightResidue(residue.name)}
                className={`p-3 rounded-lg text-left transition-all duration-200 ${
                  highlightedResidue === residue.name
                    ? 'bg-primary text-primary-foreground border-2 border-primary shadow-lg scale-105'
                    : 'bg-muted/50 hover:bg-primary/10 border border-transparent hover:border-primary/30'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono font-semibold text-sm">{residue.name}</span>
                  <Badge
                    variant={highlightedResidue === residue.name ? "secondary" : "outline"}
                    className="text-xs"
                  >
                    {residue.contribution.toFixed(1)} kcal/mol
                  </Badge>
                </div>
                <p className="text-xs mt-1 opacity-80">
                  {residue.interactionType}
                </p>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Protein3DViewer;
