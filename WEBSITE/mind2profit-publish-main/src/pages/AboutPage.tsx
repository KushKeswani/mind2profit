import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Target, Brain, TrendingUp, Zap, Shield, Users, BarChart3, Clock, Mail, Quote, Code, Rocket, Heart, Star, Award, Lightbulb, Coffee, Mountain, Camera, Dumbbell } from "lucide-react";
import { Link } from "react-router-dom";

const AboutPage = () => {
  const builtFeatures = [
    {
      icon: <BarChart3 className="h-6 w-6" />,
      title: "Trade Journaling System",
      description: "Comprehensive trade tracking and analysis"
    },
    {
      icon: <Brain className="h-6 w-6" />,
      title: "Strategy Lab",
      description: "Testing and refining edge with backtesting"
    },
    {
      icon: <Users className="h-6 w-6" />,
      title: "AI Trading Psychology",
      description: "Chatbot for psychology + affirmation generation"
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: "Hypnosis Studio",
      description: "Personalized audio scripts for mindset"
    },
    {
      icon: <TrendingUp className="h-6 w-6" />,
      title: "Custom Indicators",
      description: "Coded in Pine Script for TradingView"
    },
    {
      icon: <Zap className="h-6 w-6" />,
      title: "Future Automation",
      description: "Webhooks + Alpaca API integration"
    }
  ];

  const tradingPhilosophy = [
    "Trading is 80% mental, 20% technical",
    "Systems > signals",
    "Discipline beats predictions",
    "You don't need more alerts — you need to follow your plan",
    "Build tools to support habits, not hype"
  ];

  const personalInterests = [
    { name: "Snowboarding", icon: <Mountain className="h-5 w-5" /> },
    { name: "Flying drones", icon: <Rocket className="h-5 w-5" /> },
    { name: "Photography", icon: <Camera className="h-5 w-5" /> },
    { name: "Fitness", icon: <Dumbbell className="h-5 w-5" /> }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <ArrowLeft className="h-5 w-5 text-white" />
            <span className="text-white">Back to Home</span>
          </Link>
          <div className="flex items-center space-x-2">
            <div className="h-8 w-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
              <Target className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold text-white">Mind2Profit</span>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-12 text-center">
        <Badge variant="secondary" className="mb-4 bg-purple-100 text-purple-800">
          🧠 Meet the Builder
        </Badge>
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
          Meet the Builder Behind
          <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            {" "}Mind2Profit
          </span>
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
          Real trader. Real tools. Real problems being solved.
        </p>
        
        {/* Hero Graphics */}
        <div className="flex justify-center space-x-8 mt-8">
          <div className="flex flex-col items-center space-y-2">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <Brain className="h-8 w-8 text-white" />
            </div>
            <span className="text-sm text-gray-300">Trader</span>
          </div>
          <div className="flex flex-col items-center space-y-2">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <Code className="h-8 w-8 text-white" />
            </div>
            <span className="text-sm text-gray-300">Builder</span>
          </div>
          <div className="flex flex-col items-center space-y-2">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <Heart className="h-8 w-8 text-white" />
            </div>
            <span className="text-sm text-gray-300">Student</span>
          </div>
        </div>
      </section>

      {/* Who I Am */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/5 border-white/10 text-white relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full -translate-y-16 translate-x-16"></div>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Star className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-3xl text-white mb-4">Who I Am</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-300 text-lg">
                I'm a trader, builder, and student focused on solving real problems traders face daily. 
                I'm passionate about psychology, journaling, and strategy building.
              </p>
              <p className="text-gray-300 text-lg">
                I'm obsessed with performance and consistency, with a strong background in automation and coding. 
                Every tool I build comes from personal experience and real trading challenges.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Why I Built This */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/5 border-white/10 text-white relative overflow-hidden">
            <div className="absolute top-0 left-0 w-24 h-24 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full -translate-y-12 -translate-x-12"></div>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Lightbulb className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-3xl text-white mb-4">Why I Built This</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-300 text-lg">
                I've experienced the damage of emotional trading — FOMO, overtrading, revenge trading. 
                I was tired of switching between tools that don't talk to each other.
              </p>
              <p className="text-gray-300 text-lg">
                I wanted one system that handles psychology, strategy, and execution. 
                I built this to help myself — now making it available to other traders.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* What Makes Me Different */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/5 border-white/10 text-white relative overflow-hidden">
            <div className="absolute bottom-0 right-0 w-20 h-20 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full translate-y-10 translate-x-10"></div>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Award className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-3xl text-white mb-4">What Makes Me Different</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-300 text-lg">
                I'm not selling a course — I'm building real tools from scratch. 
                Everything I ship is based on personal trading struggles.
              </p>
              <p className="text-gray-300 text-lg">
                I journal every trade, track strategy stats, and backtest with logic. 
                I'm actively trading and iterating — not just talking.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* My Trading Style */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/5 border-white/10 text-white relative overflow-hidden">
            <div className="absolute top-0 right-0 w-28 h-28 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full -translate-y-14 translate-x-14"></div>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Target className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-3xl text-white mb-4">My Trading Style</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-300 text-lg">
                I'm focused on price action and structure. My main strategies are:
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                <div className="bg-white/5 rounded-lg p-4 text-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <TrendingUp className="h-6 w-6 text-white" />
                  </div>
                  <h4 className="text-white font-semibold">Trendline Breakout</h4>
                </div>
                <div className="bg-white/5 rounded-lg p-4 text-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <Zap className="h-6 w-6 text-white" />
                  </div>
                  <h4 className="text-white font-semibold">BOS + FVG</h4>
                  <p className="text-sm text-gray-400">Break of Structure + Fair Value Gap</p>
                </div>
                <div className="bg-white/5 rounded-lg p-4 text-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <Shield className="h-6 w-6 text-white" />
                  </div>
                  <h4 className="text-white font-semibold">Liquidity Sweeps</h4>
                </div>
              </div>
              <p className="text-gray-300 text-lg mt-4">
                I trade NQ futures and prioritize: discipline, risk-reward, confluences, and execution.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* What I've Built So Far */}
      <section className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h2 className="text-4xl font-bold text-white mb-4">
            What I've Built So Far
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Real tools for real traders. Everything built from personal need.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {builtFeatures.map((feature, index) => (
            <Card key={index} className="bg-white/5 border-white/10 text-white hover:bg-white/10 transition-all duration-300 hover:scale-105">
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

      {/* My Philosophy */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/5 border-white/10 text-white relative overflow-hidden">
            <div className="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full translate-y-12 -translate-x-12"></div>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-3xl text-white mb-4">My Philosophy</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {tradingPhilosophy.map((philosophy, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="w-3 h-3 bg-purple-400 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-300">{philosophy}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Quick Personal Touch */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/5 border-white/10 text-white relative overflow-hidden">
            <div className="absolute top-0 left-0 w-20 h-20 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full -translate-y-10 -translate-x-10"></div>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Heart className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-3xl text-white mb-4">Quick Personal Touch</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <p className="text-gray-300 text-lg">
                Started trading young — learned by doing, failing, refining. 
                I love building + backtesting as much as trading.
              </p>
              <div>
                <p className="text-gray-300 text-lg mb-4">
                  Outside of trading, I enjoy:
                </p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {personalInterests.map((interest, index) => (
                    <div key={index} className="flex items-center space-x-2 bg-white/5 rounded-lg p-3">
                      <div className="text-purple-400">
                        {interest.icon}
                      </div>
                      <span className="text-gray-300">{interest.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* What's Coming Next */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/5 border-white/10 text-white relative overflow-hidden">
            <div className="absolute bottom-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full translate-y-16 translate-x-16"></div>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Rocket className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-3xl text-white mb-4">What's Coming Next</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <ul className="list-disc list-inside text-gray-300 space-y-2 ml-4">
                <li>Full automation lab (connect Pine Script to execution)</li>
                <li>More guided psychology tools</li>
                <li>User accounts and full dashboards</li>
                <li>Public launch of Mind2Profit v1</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Quote */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto text-center">
          <Card className="bg-gradient-to-r from-purple-500 to-pink-500 text-white relative overflow-hidden">
            <div className="absolute top-0 left-0 w-40 h-40 bg-white/10 rounded-full -translate-y-20 -translate-x-20"></div>
            <div className="absolute bottom-0 right-0 w-32 h-32 bg-white/10 rounded-full translate-y-16 translate-x-16"></div>
            <CardContent className="pt-12 pb-12 relative z-10">
              <Quote className="h-12 w-12 mx-auto mb-6 opacity-80" />
              <blockquote className="text-3xl font-bold mb-4">
                "You don't need to trade more — you need to trade better."
              </blockquote>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Contact */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto text-center">
          <Card className="bg-white/5 border-white/10 text-white relative overflow-hidden">
            <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full -translate-y-12 translate-x-12"></div>
            <CardHeader>
              <div className="flex items-center justify-center space-x-3">
                <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                  <Mail className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-3xl text-white mb-4">Want to Get in Touch?</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <p className="text-gray-300 text-lg">
                I'm always open to connecting with fellow traders and builders.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                  onClick={() => window.open('mailto:kushkeswani@mind2profit.com', '_blank')}
                >
                  <Mail className="mr-2 h-4 w-4" />
                  kushkeswani@mind2profit.com
                </Button>
                <Button variant="outline" className="text-white border-white hover:bg-white/10">
                  Follow on Twitter
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 border-t border-white/10">
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
            <a href="#" className="hover:text-white transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default AboutPage;
