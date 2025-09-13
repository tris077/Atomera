import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Clock, Play, CheckCircle, XCircle } from 'lucide-react';

export type JobStatus = 'queued' | 'running' | 'completed' | 'failed';

interface StatusBadgeProps {
  status: JobStatus;
  className?: string;
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status, className = "" }) => {
  const statusConfig = {
    queued: {
      icon: Clock,
      label: 'Queued',
      variant: 'secondary' as const,
      className: 'bg-muted text-muted-foreground'
    },
    running: {
      icon: Play,
      label: 'Running',
      variant: 'default' as const,
      className: 'gradient-primary text-primary-foreground molecular-pulse'
    },
    completed: {
      icon: CheckCircle,
      label: 'Completed',
      variant: 'secondary' as const,
      className: 'bg-success text-success-foreground'
    },
    failed: {
      icon: XCircle,
      label: 'Failed',
      variant: 'destructive' as const,
      className: 'bg-destructive text-destructive-foreground'
    }
  };

  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <Badge variant={config.variant} className={`${config.className} ${className}`}>
      <Icon className="w-3 h-3 mr-1" />
      {config.label}
    </Badge>
  );
};

export default StatusBadge;