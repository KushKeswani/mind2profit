import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { ArrowRight, Brain, TrendingUp, Zap, Shield, Users, BarChart3, Clock, Target, Mail, CheckCircle, Calendar, BookOpen } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";

const ComingSoonPage = () => {
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();

  const scrollToFeatures = () => {
    const featuresSection = document.getElementById('features-section');
    if (featuresSection) {
      featuresSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !email.includes('@')) {
      toast({
        title: "Invalid Email",
        description: "Please enter a valid email address.",
        variant: "destructive",
      });
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch('/api/waitlist', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        toast({
          title: "Success!",
          description: "You've been added to the waitlist. We'll notify you when we launch!",
        });
        setEmail("");
      } else {
        throw new Error('Failed to submit');
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to join waitlist. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="h-8 w-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
              <Target className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold text-white">Mind2Profit</span>
          </div>
          <div className="flex space-x-6">
            <button 
              onClick={scrollToFeatures}
              className="text-gray-300 hover:text-white transition-colors"
            >
              Features
            </button>
            <Link to="/about" className="text-gray-300 hover:text-white transition-colors">
              About
            </Link>
            <Link to="/beta" className="text-gray-300 hover:text-white transition-colors">
              Beta
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <Badge variant="secondary" className="mb-4 bg-purple-100 text-purple-800">
          🚀 Coming Soon
        </Badge>
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
          The Future of
          <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            {" "}Trading Tools
          </span>
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
          Mind2Profit is launching in October 2025. Get early access and be among the first to experience the next generation of trading education, psychology tools, and strategy development.
        </p>
        
        {/* Countdown */}
        <div className="mb-12">
          <div className="text-4xl md:text-6xl font-bold text-white mb-4">
            Launch Date: October 2025
          </div>
          <p className="text-gray-300 text-lg">
            Join the waitlist and get notified when we launch
          </p>
        </div>

        {/* Email Signup */}
        <div className="max-w-md mx-auto mb-12">
          <form onSubmit={handleEmailSubmit} className="flex space-x-2">
            <Input 
              type="email" 
              placeholder="Enter your email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="bg-white/10 border-white/20 text-white placeholder-gray-400"
              required
            />
            <Button 
              type="submit"
              disabled={isSubmitting}
              className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:opacity-50"
            >
              {isSubmitting ? "Joining..." : "Notify Me"}
            </Button>
          </form>
        </div>

        {/* Beta Tester CTA */}
        <div className="mb-12">
          <p className="text-gray-300 mb-4">
            Want to help shape the future? Apply to become a beta tester!
          </p>
          <Link to="/beta">
            <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600">
              Become a Beta Tester
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section id="features-section" className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            What's Coming
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            A comprehensive suite of educational tools and trading resources designed by traders, for traders.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <Card className="bg-white/5 border-white/10 text-white hover:bg-white/10 transition-all duration-300">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-white">AI-Powered Strategies</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-gray-300">
                Generate and backtest trading strategies using advanced AI algorithms.
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white/5 border-white/10 text-white hover:bg-white/10 transition-all duration-300">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <BookOpen className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-white">Trading Education</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-gray-300">
                Comprehensive learning resources covering technical analysis, risk management, and trading psychology.
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white/5 border-white/10 text-white hover:bg-white/10 transition-all duration-300">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Calendar className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-white">Economic Calendar</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-gray-300">
                Stay informed with real-time economic events and market-moving news.
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white/5 border-white/10 text-white hover:bg-white/10 transition-all duration-300">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <BookOpen className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-white">Trading Journal</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-gray-300">
                Track your trades, analyze performance, and improve your process.
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white/5 border-white/10 text-white hover:bg-white/10 transition-all duration-300">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Zap className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-white">Automated Trading</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-gray-300">
                Execute trades automatically based on your predefined strategies.
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white/5 border-white/10 text-white hover:bg-white/10 transition-all duration-300">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-white">Trading Psychology Tools</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-gray-300">
                Master your mindset with guided psychology tools and affirmations.
              </CardDescription>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Social Proof */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Built by Traders, for Traders
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Every feature is designed from real trading experience, educational needs, and common pain points.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <Card className="bg-white/5 border-white/10 text-white text-center">
            <CardContent className="pt-8 pb-8">
              <div className="text-4xl mb-4">🧠</div>
              <h3 className="text-xl font-semibold mb-2">Psychology First</h3>
              <p className="text-gray-300">
                Built around the mental game that makes or breaks traders.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white/5 border-white/10 text-white text-center">
            <CardContent className="pt-8 pb-8">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold mb-2">Lightning Fast</h3>
              <p className="text-gray-300">
                Optimized for speed and efficiency in fast-moving markets.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white/5 border-white/10 text-white text-center">
            <CardContent className="pt-8 pb-8">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold mb-2">Purpose Built</h3>
              <p className="text-gray-300">
                Every tool serves a specific purpose in your trading workflow.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-12 border-t border-white/10">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <div className="h-6 w-6 bg-gradient-to-r from-purple-500 to-pink-500 rounded flex items-center justify-center">
              <Target className="h-4 w-4 text-white" />
            </div>
            <span className="text-white font-semibold">Mind2Profit</span>
          </div>
          <div className="flex space-x-6 text-gray-400">
            <Link to="/about" className="hover:text-white transition-colors">About</Link>
            <Link to="/beta" className="hover:text-white transition-colors">Beta</Link>
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ComingSoonPage;
