import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import MolecularBackground from '@/components/MolecularBackground';
import Navigation from '@/components/Navigation';
import { Upload, Zap, BarChart3, ArrowRight, Sparkles, Target, DollarSign, Box, Users, FlaskConical, Microscope, TrendingUp } from 'lucide-react';
import heroImage from '@/assets/molecular-hero.png';
import { addMockJobToLocalStorage } from '@/utils/createMockJob';
import { VALUE_PROPOSITIONS } from '@/lib/scientificContent';

const Landing: React.FC = () => {
  const navigate = useNavigate();

  const handleCreateDemoJob = () => {
    const mockJob = addMockJobToLocalStorage();
    navigate(`/job/${mockJob.id}/results`);
  };

  const benefitIcons = {
    target: Target,
    dollarSign: DollarSign,
    box: Box,
    users: Users
  };

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
              <p className="text-xl md:text-2xl text-foreground font-medium max-w-2xl mx-auto">
                {VALUE_PROPOSITIONS.hero}
              </p>
              <p className="text-lg text-muted-foreground max-w-xl mx-auto">
                {VALUE_PROPOSITIONS.subhero}
              </p>
            </div>

            {/* CTA */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button asChild variant="hero" size="xl" className="min-w-48">
                <Link to="/job/new">
                  Start Analysis
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button asChild variant="molecular" size="xl" className="min-w-48">
                <Link to="/jobs">
                  View Jobs
                </Link>
              </Button>
            </div>

            {/* Demo Mode Button */}
            <div className="pt-4 space-y-3">
              <Button
                onClick={handleCreateDemoJob}
                variant="outline"
                size="lg"
                className="border-dashed border-2 hover:bg-primary/10 hover:border-primary transition-all"
              >
                <Sparkles className="mr-2 h-4 w-4 text-primary" />
                Try Demo: EGFR Kinase Inhibitor Screen
              </Button>
              <p className="text-xs text-muted-foreground">
                Instant results • No setup required • See what Atomera can do
              </p>
            </div>

            {/* Built on note */}
            <div className="flex items-center justify-center gap-4 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <FlaskConical className="h-4 w-4" />
                Powered by Boltz-2
              </span>
              <span className="text-muted-foreground/50">•</span>
              <span className="flex items-center gap-1">
                <Microscope className="h-4 w-4" />
                Structure-based predictions
              </span>
              <span className="text-muted-foreground/50">•</span>
              <span className="flex items-center gap-1">
                <TrendingUp className="h-4 w-4" />
                Interpretable results
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Value Proposition Section */}
      <section className="py-16 bg-gradient-to-b from-primary/5 to-background">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-bold mb-3">
              Why Atomera?
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Accelerate your drug discovery pipeline with AI-powered virtual screening
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
            {VALUE_PROPOSITIONS.keyBenefits.map((benefit, idx) => {
              const IconComponent = benefitIcons[benefit.icon as keyof typeof benefitIcons] || Target;
              return (
                <div
                  key={idx}
                  className="text-center p-6 rounded-lg bg-card border border-border hover:border-primary/30 hover:shadow-lg transition-all"
                >
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                    <IconComponent className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="font-semibold mb-2">{benefit.title}</h3>
                  <p className="text-sm text-muted-foreground">{benefit.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-gradient-to-b from-background to-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Structure-Based Virtual Screening
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              From protein structure to binding predictions in minutes
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <Card className="shadow-card hover:shadow-molecular transition-smooth molecular-float">
              <CardHeader className="text-center">
                <div className="w-16 h-16 gradient-primary rounded-full flex items-center justify-center mx-auto mb-4 molecular-glow">
                  <Upload className="h-8 w-8 text-primary-foreground" />
                </div>
                <CardTitle>1. Upload Target</CardTitle>
                <CardDescription>
                  PDB structures, sequences, or AlphaFold predictions
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground text-center">
                  Supports PDB, PDBQT, FASTA formats with automatic validation and pocket detection
                </p>
              </CardContent>
            </Card>

            <Card className="shadow-card hover:shadow-molecular transition-smooth molecular-float" style={{ animationDelay: '0.2s' }}>
              <CardHeader className="text-center">
                <div className="w-16 h-16 gradient-secondary rounded-full flex items-center justify-center mx-auto mb-4 molecular-glow">
                  <Zap className="h-8 w-8 text-secondary-foreground" />
                </div>
                <CardTitle>2. Add Compounds</CardTitle>
                <CardDescription>
                  SMILES strings, SDF libraries, or draw structures
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground text-center">
                  Screen single compounds or batches with automatic drug-likeness assessment
                </p>
              </CardContent>
            </Card>

            <Card className="shadow-card hover:shadow-molecular transition-smooth molecular-float" style={{ animationDelay: '0.4s' }}>
              <CardHeader className="text-center">
                <div className="w-16 h-16 gradient-tertiary rounded-full flex items-center justify-center mx-auto mb-4 molecular-glow">
                  <BarChart3 className="h-8 w-8 text-tertiary-foreground" />
                </div>
                <CardTitle>3. Get Predictions</CardTitle>
                <CardDescription>
                  Binding affinity, poses, and residue interactions
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground text-center">
                  Interpretable results with 3D visualization, exportable reports, and confidence scores
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="py-16 bg-muted/20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-bold mb-3">
              Built for Drug Discovery Teams
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto text-sm">
            <div className="p-5 rounded-lg bg-card border border-border">
              <h4 className="font-semibold mb-2 text-primary">Academic Research</h4>
              <p className="text-muted-foreground">
                Enable structure-based design in university labs without ML expertise or GPU infrastructure
              </p>
            </div>
            <div className="p-5 rounded-lg bg-card border border-border">
              <h4 className="font-semibold mb-2 text-primary">Biotech Startups</h4>
              <p className="text-muted-foreground">
                Accelerate hit-to-lead optimization with rapid virtual screening before synthesis
              </p>
            </div>
            <div className="p-5 rounded-lg bg-card border border-border">
              <h4 className="font-semibold mb-2 text-primary">Contract Research</h4>
              <p className="text-muted-foreground">
                Provide clients with detailed, interpretable binding analyses and exportable reports
              </p>
            </div>
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
                AI-powered virtual screening for structure-based drug discovery
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
              © 2024 Atomera. All rights reserved. For research use only.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
