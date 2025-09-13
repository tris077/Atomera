import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Home, List, Plus } from 'lucide-react';

const Navigation: React.FC = () => {
  const location = useLocation();
  const currentPath = location.pathname;

  const isActive = (path: string) => {
    if (path === '/' && currentPath === '/') return true;
    if (path !== '/' && currentPath.startsWith(path)) return true;
    return false;
  };

  return (
    <header className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-3 hover:opacity-80 transition-smooth">
          <img 
            src="/lovable-uploads/85ff6cb2-f21e-49a1-9a52-13a6ff2a50ff.png" 
            alt="Atomera" 
            className="h-8"
          />
        </Link>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-2">
          <Button 
            asChild 
            variant={isActive('/') ? 'secondary' : 'ghost'} 
            size="sm"
          >
            <Link to="/">
              <Home className="h-4 w-4 mr-2" />
              Home
            </Link>
          </Button>
          <Button 
            asChild 
            variant={isActive('/jobs') ? 'secondary' : 'ghost'} 
            size="sm"
          >
            <Link to="/jobs">
              <List className="h-4 w-4 mr-2" />
              Jobs
            </Link>
          </Button>
          <Button 
            asChild 
            variant={isActive('/job/new') ? 'hero' : 'molecular'} 
            size="sm"
          >
            <Link to="/job/new">
              <Plus className="h-4 w-4 mr-2" />
              New Job
            </Link>
          </Button>
        </nav>

        {/* Mobile Navigation */}
        <nav className="md:hidden flex items-center gap-1">
          <Button 
            asChild 
            variant={isActive('/') ? 'secondary' : 'ghost'} 
            size="sm"
          >
            <Link to="/">
              <Home className="h-4 w-4" />
            </Link>
          </Button>
          <Button 
            asChild 
            variant={isActive('/jobs') ? 'secondary' : 'ghost'} 
            size="sm"
          >
            <Link to="/jobs">
              <List className="h-4 w-4" />
            </Link>
          </Button>
          <Button 
            asChild 
            variant={isActive('/job/new') ? 'hero' : 'molecular'} 
            size="sm"
          >
            <Link to="/job/new">
              <Plus className="h-4 w-4" />
            </Link>
          </Button>
        </nav>
      </div>
    </header>
  );
};

export default Navigation;