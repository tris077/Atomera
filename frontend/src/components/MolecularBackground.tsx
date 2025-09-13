import React from 'react';

interface MolecularBackgroundProps {
  className?: string;
  intensity?: 'light' | 'medium' | 'strong';
}

const MolecularBackground: React.FC<MolecularBackgroundProps> = ({ 
  className = "", 
  intensity = 'medium' 
}) => {
  const particles = Array.from({ length: intensity === 'light' ? 15 : intensity === 'medium' ? 25 : 35 });

  return (
    <div className={`absolute inset-0 overflow-hidden pointer-events-none ${className}`}>
      {/* Gradient overlay */}
      <div className="absolute inset-0 gradient-hero opacity-40" />
      
      {/* Floating particles */}
      <div className="relative w-full h-full">
        {particles.map((_, i) => (
          <div
            key={i}
            className={`absolute w-2 h-2 rounded-full molecular-pulse`}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              background: i % 3 === 0 
                ? 'hsl(var(--primary) / 0.3)' 
                : i % 3 === 1 
                ? 'hsl(var(--secondary) / 0.3)' 
                : 'hsl(var(--tertiary) / 0.3)',
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${3 + Math.random() * 3}s`
            }}
          />
        ))}
        
        {/* Connection lines */}
        <svg className="absolute inset-0 w-full h-full">
          <defs>
            <linearGradient id="connectionGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity="0.1" />
              <stop offset="50%" stopColor="hsl(var(--secondary))" stopOpacity="0.2" />
              <stop offset="100%" stopColor="hsl(var(--tertiary))" stopOpacity="0.1" />
            </linearGradient>
          </defs>
          {Array.from({ length: 8 }).map((_, i) => (
            <line
              key={i}
              x1={`${Math.random() * 100}%`}
              y1={`${Math.random() * 100}%`}
              x2={`${Math.random() * 100}%`}
              y2={`${Math.random() * 100}%`}
              stroke="url(#connectionGradient)"
              strokeWidth="1"
              className="molecular-float"
              style={{
                animationDelay: `${Math.random() * 6}s`,
                animationDuration: `${6 + Math.random() * 4}s`
              }}
            />
          ))}
        </svg>
      </div>
    </div>
  );
};

export default MolecularBackground;