import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { useToast } from '@/hooks/use-toast';
import { jobService } from '@/lib/jobService';
import MolecularBackground from '@/components/MolecularBackground';
import Navigation from '@/components/Navigation';
import { Upload, FileText, Play } from 'lucide-react';

const NewJob: React.FC = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [formData, setFormData] = useState({
    name: '',
    proteinInput: '',
    proteinType: 'file' as 'file' | 'text',
    ligandInput: '',
    ligandType: 'file' as 'file' | 'text',
    notes: ''
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Job name is required';
    }
    
    if (!formData.proteinInput.trim()) {
      newErrors.proteinInput = 'Protein input is required';
    }
    
    if (!formData.ligandInput.trim()) {
      newErrors.ligandInput = 'Ligand input is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast({
        title: "Validation Error",
        description: "Please fix the errors below",
        variant: "destructive",
      });
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const job = await jobService.createJob(formData);
      
      toast({
        title: "Job Created",
        description: `Job "${job.name}" has been created successfully and sent to Boltz-2 backend`,
      });
      
      navigate(`/job/${job.id}/status`);
    } catch (error) {
      console.error('Job creation error:', error);
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to create job. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  return (
    <div className="min-h-screen bg-background relative">
      <Navigation />
      <MolecularBackground intensity="light" />
      
      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Create New Job</h1>
          <p className="text-muted-foreground">Set up a new binding affinity prediction</p>
        </div>

        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto space-y-8">
          {/* Job Details */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle>Job Details</CardTitle>
              <CardDescription>Basic information about your analysis</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="jobName">Job Name *</Label>
                  <Input
                    id="jobName"
                    placeholder="e.g., Protein-Ligand Analysis 1"
                    value={formData.name}
                    onChange={(e) => handleInputChange('name', e.target.value)}
                    className={errors.name ? 'border-destructive' : ''}
                  />
                  {errors.name && (
                    <p className="text-sm text-destructive">{errors.name}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="notes">Notes (Optional)</Label>
                  <Input
                    id="notes"
                    placeholder="Brief description or notes"
                    value={formData.notes}
                    onChange={(e) => handleInputChange('notes', e.target.value)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Protein Input */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <div className="w-8 h-8 gradient-primary rounded-lg flex items-center justify-center">
                  <Upload className="h-4 w-4 text-primary-foreground" />
                </div>
                Protein Input
              </CardTitle>
              <CardDescription>Upload a protein file or paste sequence/ID</CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs 
                value={formData.proteinType} 
                onValueChange={(value) => handleInputChange('proteinType', value)}
              >
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="file">File Upload</TabsTrigger>
                  <TabsTrigger value="text">Text Input</TabsTrigger>
                </TabsList>
                
                <TabsContent value="file" className="space-y-4">
                  <Alert>
                    <FileText className="h-4 w-4" />
                    <AlertDescription>
                      Supported formats: PDB, PDBQT. Max file size: 10MB
                    </AlertDescription>
                  </Alert>
                  <div className="space-y-2">
                    <Label htmlFor="proteinFile">Protein File *</Label>
                    <Input
                      id="proteinFile"
                      type="file"
                      accept=".pdb,.pdbqt"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        handleInputChange('proteinInput', file?.name || '');
                      }}
                      className={errors.proteinInput ? 'border-destructive' : ''}
                    />
                  </div>
                </TabsContent>
                
                <TabsContent value="text" className="space-y-4">
                  <Alert>
                    <FileText className="h-4 w-4" />
                    <AlertDescription>
                      Paste protein sequence, PDB ID, or structure data
                    </AlertDescription>
                  </Alert>
                  <div className="space-y-2">
                    <Label htmlFor="proteinText">Protein Data *</Label>
                    <Textarea
                      id="proteinText"
                      placeholder="Paste protein sequence, PDB ID (e.g., 1ABC), or structure data..."
                      value={formData.proteinInput}
                      onChange={(e) => handleInputChange('proteinInput', e.target.value)}
                      rows={6}
                      className={errors.proteinInput ? 'border-destructive' : ''}
                    />
                  </div>
                </TabsContent>
              </Tabs>
              {errors.proteinInput && (
                <p className="text-sm text-destructive mt-2">{errors.proteinInput}</p>
              )}
            </CardContent>
          </Card>

          {/* Ligand Input */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <div className="w-8 h-8 gradient-secondary rounded-lg flex items-center justify-center">
                  <Upload className="h-4 w-4 text-secondary-foreground" />
                </div>
                Ligand Input
              </CardTitle>
              <CardDescription>Upload a ligand file or paste SMILES string</CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs 
                value={formData.ligandType} 
                onValueChange={(value) => handleInputChange('ligandType', value)}
              >
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="file">File Upload</TabsTrigger>
                  <TabsTrigger value="text">SMILES Input</TabsTrigger>
                </TabsList>
                
                <TabsContent value="file" className="space-y-4">
                  <Alert>
                    <FileText className="h-4 w-4" />
                    <AlertDescription>
                      Supported formats: SDF, MOL2. Max file size: 5MB
                    </AlertDescription>
                  </Alert>
                  <div className="space-y-2">
                    <Label htmlFor="ligandFile">Ligand File *</Label>
                    <Input
                      id="ligandFile"
                      type="file"
                      accept=".sdf,.mol2"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        handleInputChange('ligandInput', file?.name || '');
                      }}
                      className={errors.ligandInput ? 'border-destructive' : ''}
                    />
                  </div>
                </TabsContent>
                
                <TabsContent value="text" className="space-y-4">
                  <Alert>
                    <FileText className="h-4 w-4" />
                    <AlertDescription>
                      Enter SMILES string for the ligand molecule
                    </AlertDescription>
                  </Alert>
                  <div className="space-y-2">
                    <Label htmlFor="ligandSmiles">SMILES String *</Label>
                    <Textarea
                      id="ligandSmiles"
                      placeholder="e.g., CCO (ethanol) or more complex SMILES..."
                      value={formData.ligandInput}
                      onChange={(e) => handleInputChange('ligandInput', e.target.value)}
                      rows={3}
                      className={errors.ligandInput ? 'border-destructive' : ''}
                    />
                  </div>
                </TabsContent>
              </Tabs>
              {errors.ligandInput && (
                <p className="text-sm text-destructive mt-2">{errors.ligandInput}</p>
              )}
            </CardContent>
          </Card>

          {/* Submit */}
          <div className="flex justify-center">
            <Button 
              type="submit" 
              variant="hero" 
              size="xl" 
              disabled={isSubmitting}
              className="min-w-64"
            >
              {isSubmitting ? (
                <>Creating Job...</>
              ) : (
                <>
                  <Play className="mr-2 h-5 w-5" />
                  Create Job
                </>
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NewJob;