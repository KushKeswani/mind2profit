import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, Brain, TrendingUp, Zap, Shield, Users, BarChart3, Clock, Target, Calendar } from "lucide-react";
import { Link } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";

const LandingPage = () => {
  const { isAuthenticated, isSubscribed } = useAuth();
  const ctaPath = isAuthenticated ? (isSubscribed ? "/dashboard" : "/upgrade") : "/signin";
  const ctaLabel = isAuthenticated ? (isSubscribed ? "Open Dashboard" : "Choose a Plan") : "Sign In to Start";
  const headerCtaLabel = isAuthenticated ? (isSubscribed ? "Dashboard" : "Upgrade") : "Get Started";

  const features = [
    {
      icon: <Brain className="h-6 w-6" />,
      title: "AI Trade Coach",
      description: "Review recent trades and get actionable coaching on risk and execution."
    },
    {
      icon: <TrendingUp className="h-6 w-6" />,
      title: "Performance Dashboard",
      description: "Track P&L, win rate, expectancy, drawdown, and symbol-level performance."
    },
    {
      icon: <BarChart3 className="h-6 w-6" />,
      title: "Journal Analytics",
      description: "Turn daily logs into trends you can act on."
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: "Trading Journal",
      description: "Capture trade details and end-of-day reflections in one workflow."
    },
    {
      icon: <Calendar className="h-6 w-6" />,
      title: "Economic Calendar",
      description: "Plan around high-impact events and protect capital during volatility."
    },
    {
      icon: <Clock className="h-6 w-6" />,
      title: "Broker Sync",
      description: "Connect accounts like Tradovate so trades auto-load into your journal."
    }
  ];

  const testimonials = [
    {
      name: "Sarah Johnson",
      role: "Professional Trader",
      content: "The journal and dashboard finally make my mistakes visible. I can actually improve week to week."
    },
    {
      name: "Mike Chen",
      role: "Day Trader",
      content: "The economic calendar plus risk reminders helped me stop trading through news spikes."
    },
    {
      name: "Emily Rodriguez",
      role: "Swing Trader",
      content: "The AI coach gives useful feedback from my own recent trades, not generic advice."
    }
  ];

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
          <div className="flex items-center space-x-4">
            <Button variant="ghost" className="text-white hover:bg-white/10">
              Features
            </Button>
            <Button variant="ghost" className="text-white hover:bg-white/10">
              Pricing
            </Button>
            <Link to={ctaPath}>
              <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600">
                {headerCtaLabel}
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <Badge variant="secondary" className="mb-4 bg-purple-100 text-purple-800">
          🚀 Journal-First Trading Platform
        </Badge>
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
          Improve Trading with
          <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            {" "}Execution Discipline
          </span>
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
          Mind2Profit helps you log trades, learn from data, and sharpen risk control with AI coaching, calendar context, and broker sync.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to={ctaPath}>
            <Button size="lg" className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-lg px-8 py-6">
              {ctaLabel}
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
          <Button size="lg" variant="outline" className="text-white border-white bg-transparent hover:bg-white/10 hover:text-white text-lg px-8 py-6">
            Watch Demo
          </Button>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Everything You Need to Succeed
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Powerful tools designed by traders, for traders. Take your trading to the next level.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="bg-white/5 border-white/10 text-white hover:bg-white/10 transition-all duration-300">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-white">{feature.title}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-300">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Trusted by Traders Worldwide
          </h2>
          <p className="text-xl text-gray-300">
            See what our users are saying about Mind2Profit
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="bg-white/5 border-white/10 text-white">
              <CardContent className="pt-6">
                <p className="text-gray-300 mb-4">"{testimonial.content}"</p>
                <div className="flex items-center space-x-3">
                  <div className="h-10 w-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                    <Users className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <p className="font-semibold text-white">{testimonial.name}</p>
                    <p className="text-sm text-gray-400">{testimonial.role}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <Card className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-center">
          <CardContent className="pt-12 pb-12">
            <h2 className="text-4xl font-bold mb-4">
              Ready to Transform Your Trading?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Join thousands of successful traders and start your journey today.
            </p>
            <Link to={ctaPath}>
              <Button size="lg" variant="secondary" className="text-lg px-8 py-6">
                {isAuthenticated ? (isSubscribed ? "Open Dashboard" : "Choose a Plan") : "Sign In to Continue"}
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </CardContent>
        </Card>
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
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
            <a href="#" className="hover:text-white transition-colors">Support</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
