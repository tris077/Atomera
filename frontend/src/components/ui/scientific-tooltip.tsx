import * as React from 'react';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { HelpCircle, Info } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ScientificTooltipProps {
  content: string;
  children: React.ReactNode;
  interpretation?: string;
  icon?: 'help' | 'info';
  className?: string;
}

export function ScientificTooltip({
  content,
  children,
  interpretation,
  icon = 'help',
  className
}: ScientificTooltipProps) {
  const Icon = icon === 'help' ? HelpCircle : Info;

  return (
    <TooltipProvider delayDuration={200}>
      <Tooltip>
        <TooltipTrigger asChild>
          <span className={cn('inline-flex items-center gap-1 cursor-help', className)}>
            {children}
            <Icon className="h-3.5 w-3.5 text-muted-foreground hover:text-primary transition-colors" />
          </span>
        </TooltipTrigger>
        <TooltipContent className="max-w-xs p-3" side="top">
          <p className="text-sm">{content}</p>
          {interpretation && (
            <p className="text-xs text-muted-foreground mt-1.5 pt-1.5 border-t">
              {interpretation}
            </p>
          )}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}

// Metric label with built-in tooltip
interface MetricLabelProps {
  label: string;
  tooltip: string;
  interpretation?: string;
  className?: string;
}

export function MetricLabel({ label, tooltip, interpretation, className }: MetricLabelProps) {
  return (
    <ScientificTooltip content={tooltip} interpretation={interpretation}>
      <span className={cn('text-sm text-muted-foreground', className)}>{label}</span>
    </ScientificTooltip>
  );
}

// Confidence progress bar
interface ConfidenceBarProps {
  value: number; // 0-1
  className?: string;
  showLabel?: boolean;
}

export function ConfidenceBar({ value, className, showLabel = true }: ConfidenceBarProps) {
  const percentage = Math.round(value * 100);
  const color = value > 0.9 ? 'bg-green-500' : value > 0.8 ? 'bg-blue-500' : value > 0.7 ? 'bg-yellow-500' : 'bg-red-500';

  return (
    <div className={cn('w-full', className)}>
      <div className="flex items-center gap-2">
        <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
          <div
            className={cn('h-full transition-all duration-500', color)}
            style={{ width: `${percentage}%` }}
          />
        </div>
        {showLabel && (
          <span className="text-xs font-medium tabular-nums w-10 text-right">{percentage}%</span>
        )}
      </div>
    </div>
  );
}

// Status chip component
interface StatusChipProps {
  label: string;
  colorClass: string;
  className?: string;
}

export function StatusChip({ label, colorClass, className }: StatusChipProps) {
  return (
    <span className={cn(
      'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border',
      colorClass,
      className
    )}>
      {label}
    </span>
  );
}

// Contribution indicator (green for stabilizing, red for destabilizing)
interface ContributionIndicatorProps {
  value: number;
  showValue?: boolean;
  className?: string;
}

export function ContributionIndicator({ value, showValue = true, className }: ContributionIndicatorProps) {
  const isStabilizing = value < 0;
  const intensity = Math.min(Math.abs(value) / 3, 1); // Normalize to 0-1 scale (max at 3 kcal/mol)

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div className="w-16 h-2 bg-muted rounded-full overflow-hidden flex">
        {isStabilizing ? (
          <>
            <div className="flex-1" />
            <div
              className="bg-green-500 transition-all duration-300"
              style={{ width: `${intensity * 50}%` }}
            />
          </>
        ) : (
          <>
            <div
              className="bg-red-500 transition-all duration-300"
              style={{ width: `${intensity * 50}%` }}
            />
            <div className="flex-1" />
          </>
        )}
      </div>
      {showValue && (
        <span className={cn(
          'text-xs font-mono tabular-nums',
          isStabilizing ? 'text-green-600' : 'text-red-600'
        )}>
          {value > 0 ? '+' : ''}{value.toFixed(1)}
        </span>
      )}
    </div>
  );
}
