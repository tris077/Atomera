import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import MolecularBackground from '@/components/MolecularBackground';
import Navigation from '@/components/Navigation';
import { Upload, Zap, BarChart3, ArrowRight } from 'lucide-react';
import heroImage from '@/assets/molecular-hero.png';

const Landing: React.FC = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Hero Section */}
      <section className="relative min-h-[calc(100vh-4rem)] flex items-center justify-center overflow-hidden">
        <MolecularBackground intensity="medium" />
        
        <div className="relative z-10 container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto space-y-8">
            {/* Brand */}
            <div className="space-y-4">
              <div className="flex items-center justify-center gap-4 molecular-float">
                <img 
                  src="/lovable-uploads/85ff6cb2-f21e-49a1-9a52-13a6ff2a50ff.png" 
                  alt="Atomera Logo" 
                  className="h-32 md:h-48"
                />
              </div>
              <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto">
                Predict binding affinity. Explore protein–ligand interactions.
              </p>
            </div>

            {/* CTA */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button asChild variant="hero" size="xl" className="min-w-48">
                <Link to="/job/new">
                  Start a Job
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button asChild variant="molecular" size="xl" className="min-w-48">
                <Link to="/jobs">
                  View Jobs
                </Link>
              </Button>
            </div>

            {/* Built on note */}
            <p className="text-sm text-muted-foreground">
              Built on Boltz-2 (planned) • Advanced molecular dynamics simulation
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-gradient-to-b from-background to-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Molecular Interaction Analysis
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Advanced computational tools for understanding protein-ligand binding mechanisms
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <Card className="shadow-card hover:shadow-molecular transition-smooth molecular-float">
              <CardHeader className="text-center">
                <div className="w-16 h-16 gradient-primary rounded-full flex items-center justify-center mx-auto mb-4 molecular-glow">
                  <Upload className="h-8 w-8 text-primary-foreground" />
                </div>
                <CardTitle>Upload Proteins</CardTitle>
                <CardDescription>
                  Support for PDB, PDBQT formats or paste sequences directly
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground text-center">
                  Flexible input methods for protein structures and sequences with automatic validation
                </p>
              </CardContent>
            </Card>

            <Card className="shadow-card hover:shadow-molecular transition-smooth molecular-float" style={{ animationDelay: '0.2s' }}>
              <CardHeader className="text-center">
                <div className="w-16 h-16 gradient-secondary rounded-full flex items-center justify-center mx-auto mb-4 molecular-glow">
                  <Zap className="h-8 w-8 text-secondary-foreground" />
                </div>
                <CardTitle>Upload Ligands</CardTitle>
                <CardDescription>
                  SDF, MOL2, SMILES support with intelligent parsing
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground text-center">
                  Multiple ligand format support with SMILES string validation and structure preview
                </p>
              </CardContent>
            </Card>

            <Card className="shadow-card hover:shadow-molecular transition-smooth molecular-float" style={{ animationDelay: '0.4s' }}>
              <CardHeader className="text-center">
                <div className="w-16 h-16 gradient-tertiary rounded-full flex items-center justify-center mx-auto mb-4 molecular-glow">
                  <BarChart3 className="h-8 w-8 text-tertiary-foreground" />
                </div>
                <CardTitle>Run Jobs</CardTitle>
                <CardDescription>
                  High-performance binding affinity prediction
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground text-center">
                  Real-time job monitoring with detailed results including poses and interaction maps
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-card border-t border-border">
        <div className="container mx-auto px-4 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <img 
                  src="/lovable-uploads/85ff6cb2-f21e-49a1-9a52-13a6ff2a50ff.png" 
                  alt="Atomera Logo" 
                  className="h-6"
                />
              </div>
              <p className="text-sm text-muted-foreground">
                Advanced molecular interaction prediction platform
              </p>
            </div>

            <div className="space-y-4">
              <h4 className="font-medium">Resources</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-smooth">
                    Documentation
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-smooth">
                    API Reference
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-smooth">
                    Tutorials
                  </Link>
                </li>
              </ul>
            </div>

            <div className="space-y-4">
              <h4 className="font-medium">Support</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-smooth">
                    Contact
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-smooth">
                    Help Center
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-smooth">
                    Status
                  </Link>
                </li>
              </ul>
            </div>

            <div className="space-y-4">
              <h4 className="font-medium">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-smooth">
                    Terms
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-smooth">
                    Privacy
                  </Link>
                </li>
                <li>
                  <Link to="#" className="text-muted-foreground hover:text-foreground transition-smooth">
                    Cookies
                  </Link>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-border mt-8 pt-8 text-center">
            <p className="text-sm text-muted-foreground">
              © 2024 Atomera. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;