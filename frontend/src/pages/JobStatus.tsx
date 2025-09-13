import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { useToast } from '@/hooks/use-toast';
import { jobService } from '@/lib/jobService';
import StatusBadge from '@/components/StatusBadge';
import MolecularBackground from '@/components/MolecularBackground';
import Navigation from '@/components/Navigation';
import { RefreshCw, X, Clock, Eye } from 'lucide-react';
import { Job } from '@/lib/jobService';

const JobStatus: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { toast } = useToast();
  
  const [job, setJob] = useState<Job | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  const refreshJob = async () => {
    if (!id) return;
    
    setIsRefreshing(true);
    setLoadError(null);
    try {
      const updatedJob = await jobService.getJobStatus(id);
      if (updatedJob) {
        setJob(updatedJob);
        setLoadError(null);
      } else {
        // Job not found, but don't show error immediately - wait a bit
        console.log('Job not found, will retry...');
        setLoadError('Job not found, retrying...');
      }
    } catch (error) {
      console.error('Failed to refresh job:', error);
      setLoadError('Failed to load job, retrying...');
    } finally {
      setTimeout(() => setIsRefreshing(false), 500);
    }
  };

  useEffect(() => {
    if (id) {
      setIsLoading(true);
      setLoadError(null);
      refreshJob().finally(() => {
        setIsLoading(false);
      });
    }
  }, [id]);

  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      refreshJob();
    }, 3000);

    return () => clearInterval(interval);
  }, [autoRefresh, id]);

  // Auto-enable refresh if job is not found
  useEffect(() => {
    if (!job && !isLoading && id) {
      setAutoRefresh(true);
    } else if (job && job.status === 'completed') {
      setAutoRefresh(false);
    }
  }, [job, isLoading, id]);

  const handleCancel = () => {
    if (!job) return;
    
    toast({
      title: "Job Cancelled",
      description: `Job "${job.name}" has been cancelled`,
      variant: "destructive",
    });
  };

  const getProgressValue = () => {
    if (!job) return 0;
    switch (job.status) {
      case 'queued': return 10;
      case 'running': return 50;
      case 'completed': return 100;
      case 'failed': return 100;
      default: return 0;
    }
  };

  const getStatusMessage = () => {
    if (!job) return '';
    switch (job.status) {
      case 'queued': return 'Job is in queue, waiting to be processed...';
      case 'running': return 'Running binding affinity analysis...';
      case 'completed': return 'Analysis completed successfully!';
      case 'failed': return 'Job failed to complete. Please check your inputs.';
      default: return '';
    }
  };

  // Show loading state while job is being fetched
  if (isLoading || (!job && !loadError)) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6 text-center">
            <h2 className="text-xl font-semibold mb-2">Loading Job...</h2>
            <p className="text-muted-foreground mb-4">
              Fetching job status and results...
            </p>
            <div className="flex justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Only show error after multiple failed attempts
  if (!job && loadError && !isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6 text-center">
            <h2 className="text-xl font-semibold mb-2">Unable to Load Job</h2>
            <p className="text-muted-foreground mb-4">
              {loadError}
            </p>
            <div className="flex gap-2 justify-center">
              <Button onClick={() => window.location.reload()}>
                Retry
              </Button>
              <Button asChild variant="outline">
                <Link to="/jobs">Back to Jobs</Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background relative">
      <Navigation />
      <MolecularBackground intensity="light" />
      
      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold">{job.name}</h1>
            <p className="text-muted-foreground">Job Status & Progress</p>
          </div>
          
          <div className="flex items-center gap-2">
            <StatusBadge status={job.status} />
          </div>
        </div>

        <div className="max-w-4xl mx-auto space-y-6">
          {/* Status Card */}
          <Card className="shadow-card">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Progress
                </CardTitle>
                <div className="flex items-center gap-4">
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="auto-refresh"
                      checked={autoRefresh}
                      onCheckedChange={setAutoRefresh}
                    />
                    <Label htmlFor="auto-refresh" className="text-sm">
                      Auto-refresh
                    </Label>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={refreshJob}
                    disabled={isRefreshing}
                  >
                    <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>{getStatusMessage()}</span>
                  <span>{getProgressValue()}%</span>
                </div>
                <Progress value={getProgressValue()} className="w-full" />
              </div>
              
              <div className="grid md:grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">Created:</span>
                  <p className="font-medium">{job.created.toLocaleString()}</p>
                </div>
                <div>
                  <span className="text-muted-foreground">Last Updated:</span>
                  <p className="font-medium">{job.updated.toLocaleString()}</p>
                </div>
                <div>
                  <span className="text-muted-foreground">Runtime:</span>
                  <p className="font-medium">
                    {job.runtime ? `${(job.runtime / 1000).toFixed(1)}s` : 'N/A'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Job Details */}
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="shadow-card">
              <CardHeader>
                <CardTitle>Protein Input</CardTitle>
                <CardDescription>Input method: {job.proteinType}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-muted rounded-lg p-4">
                  <p className="text-sm font-mono text-muted-foreground">
                    {job.proteinInput.length > 100 
                      ? `${job.proteinInput.substring(0, 100)}...` 
                      : job.proteinInput}
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card className="shadow-card">
              <CardHeader>
                <CardTitle>Ligand Input</CardTitle>
                <CardDescription>Input method: {job.ligandType}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-muted rounded-lg p-4">
                  <p className="text-sm font-mono text-muted-foreground">
                    {job.ligandInput.length > 100 
                      ? `${job.ligandInput.substring(0, 100)}...` 
                      : job.ligandInput}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Notes */}
          {job.notes && (
            <Card className="shadow-card">
              <CardHeader>
                <CardTitle>Notes</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">{job.notes}</p>
              </CardContent>
            </Card>
          )}

          {/* Status Log */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle>Status Log</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-2 h-2 rounded-full bg-primary"></div>
                  <span className="text-muted-foreground">{job.created.toLocaleString()}</span>
                  <span>Job created and queued</span>
                </div>
                
                {job.status !== 'queued' && (
                  <div className="flex items-center gap-3 text-sm">
                    <div className="w-2 h-2 rounded-full bg-secondary"></div>
                    <span className="text-muted-foreground">{job.updated.toLocaleString()}</span>
                    <span>Analysis started</span>
                  </div>
                )}
                
                {(job.status === 'completed' || job.status === 'failed') && (
                  <div className="flex items-center gap-3 text-sm">
                    <div className={`w-2 h-2 rounded-full ${job.status === 'completed' ? 'bg-success' : 'bg-destructive'}`}></div>
                    <span className="text-muted-foreground">{job.updated.toLocaleString()}</span>
                    <span>
                      {job.status === 'completed' ? 'Analysis completed' : 'Analysis failed'}
                    </span>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Actions */}
          <div className="flex justify-center gap-4">
            {job.status === 'completed' && (
              <Button asChild variant="hero" size="lg">
                <Link to={`/job/${job.id}/results`}>
                  <Eye className="mr-2 h-4 w-4" />
                  View Results
                </Link>
              </Button>
            )}
            
            {(job.status === 'queued' || job.status === 'running') && (
              <Button variant="destructive" size="lg" onClick={handleCancel}>
                <X className="mr-2 h-4 w-4" />
                Cancel Job
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobStatus;