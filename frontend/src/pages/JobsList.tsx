import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { jobService, Job } from '@/lib/jobService';
import StatusBadge, { JobStatus } from '@/components/StatusBadge';
import MolecularBackground from '@/components/MolecularBackground';
import Navigation from '@/components/Navigation';
import { Plus, Search, Eye, RefreshCw } from 'lucide-react';

const JobsList: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [filteredJobs, setFilteredJobs] = useState<Job[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [isRefreshing, setIsRefreshing] = useState(false);

  const loadJobs = async () => {
    setIsRefreshing(true);
    try {
      const allJobs = await jobService.getAllJobs();
      setJobs(allJobs);
    } catch (error) {
      console.error('Failed to load jobs:', error);
    } finally {
      setTimeout(() => setIsRefreshing(false), 300);
    }
  };

  useEffect(() => {
    loadJobs();
  }, []);

  useEffect(() => {
    let filtered = jobs;

    // Filter by search query
    if (searchQuery.trim()) {
      filtered = filtered.filter(job =>
        job.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.id.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Filter by status
    if (statusFilter !== 'all') {
      filtered = filtered.filter(job => job.status === statusFilter);
    }

    setFilteredJobs(filtered);
  }, [jobs, searchQuery, statusFilter]);

  const formatDateTime = (date: Date) => {
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getStatusCounts = () => {
    const counts = {
      all: jobs.length,
      queued: jobs.filter(j => j.status === 'queued').length,
      running: jobs.filter(j => j.status === 'running').length,
      completed: jobs.filter(j => j.status === 'completed').length,
      failed: jobs.filter(j => j.status === 'failed').length,
    };
    return counts;
  };

  const statusCounts = getStatusCounts();

  return (
    <div className="min-h-screen bg-background relative">
      <Navigation />
      <MolecularBackground intensity="light" />
      
      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold">Jobs</h1>
            <p className="text-muted-foreground">Manage your binding affinity analyses</p>
          </div>
          
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={loadJobs}
              disabled={isRefreshing}
            >
              <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
            </Button>
            <Button asChild variant="hero">
              <Link to="/job/new">
                <Plus className="h-4 w-4 mr-2" />
                New Job
              </Link>
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <Card className="shadow-card">
            <CardContent className="pt-4">
              <div className="text-2xl font-bold">{statusCounts.all}</div>
              <p className="text-xs text-muted-foreground">Total Jobs</p>
            </CardContent>
          </Card>
          <Card className="shadow-card">
            <CardContent className="pt-4">
              <div className="text-2xl font-bold text-muted-foreground">{statusCounts.queued}</div>
              <p className="text-xs text-muted-foreground">Queued</p>
            </CardContent>
          </Card>
          <Card className="shadow-card">
            <CardContent className="pt-4">
              <div className="text-2xl font-bold text-primary">{statusCounts.running}</div>
              <p className="text-xs text-muted-foreground">Running</p>
            </CardContent>
          </Card>
          <Card className="shadow-card">
            <CardContent className="pt-4">
              <div className="text-2xl font-bold text-success">{statusCounts.completed}</div>
              <p className="text-xs text-muted-foreground">Completed</p>
            </CardContent>
          </Card>
          <Card className="shadow-card">
            <CardContent className="pt-4">
              <div className="text-2xl font-bold text-destructive">{statusCounts.failed}</div>
              <p className="text-xs text-muted-foreground">Failed</p>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card className="shadow-card mb-6">
          <CardHeader>
            <CardTitle>Filters</CardTitle>
            <CardDescription>Search and filter your jobs</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search by job name or ID..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger className="w-full sm:w-48">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status ({statusCounts.all})</SelectItem>
                  <SelectItem value="queued">Queued ({statusCounts.queued})</SelectItem>
                  <SelectItem value="running">Running ({statusCounts.running})</SelectItem>
                  <SelectItem value="completed">Completed ({statusCounts.completed})</SelectItem>
                  <SelectItem value="failed">Failed ({statusCounts.failed})</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Jobs Table */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle>Jobs List</CardTitle>
            <CardDescription>
              {filteredJobs.length} of {jobs.length} jobs
            </CardDescription>
          </CardHeader>
          <CardContent>
            {filteredJobs.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-muted-foreground mb-4">
                  {jobs.length === 0 ? (
                    <>
                      <div className="text-4xl mb-2">🧬</div>
                      <h3 className="text-lg font-semibold mb-2">No jobs yet</h3>
                      <p>Create your first binding affinity analysis</p>
                    </>
                  ) : (
                    <>
                      <div className="text-4xl mb-2">🔍</div>
                      <h3 className="text-lg font-semibold mb-2">No jobs found</h3>
                      <p>Try adjusting your search or filters</p>
                    </>
                  )}
                </div>
                {jobs.length === 0 && (
                  <Button asChild variant="hero">
                    <Link to="/job/new">
                      <Plus className="h-4 w-4 mr-2" />
                      Create First Job
                    </Link>
                  </Button>
                )}
              </div>
            ) : (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Job ID</TableHead>
                      <TableHead>Name</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Created</TableHead>
                      <TableHead>Last Updated</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredJobs.map((job) => (
                      <TableRow key={job.id}>
                        <TableCell className="font-mono text-sm">
                          {job.id.substring(0, 12)}...
                        </TableCell>
                        <TableCell className="font-medium">{job.name}</TableCell>
                        <TableCell>
                          <StatusBadge status={job.status} />
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground">
                          {formatDateTime(job.created)}
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground">
                          {formatDateTime(job.updated)}
                        </TableCell>
                        <TableCell>
                          <div className="flex gap-1">
                            {job.status === 'completed' ? (
                              <Button asChild variant="ghost" size="sm">
                                <Link to={`/job/${job.id}/results`}>
                                  <Eye className="h-3 w-3 mr-1" />
                                  Results
                                </Link>
                              </Button>
                            ) : (
                              <Button asChild variant="ghost" size="sm">
                                <Link to={`/job/${job.id}/status`}>
                                  <Eye className="h-3 w-3 mr-1" />
                                  Status
                                </Link>
                              </Button>
                            )}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default JobsList;