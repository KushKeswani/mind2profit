import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Check, Star, ArrowLeft, Zap, Crown, Target } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";

const UpgradePage = () => {
  const { upgrade } = useAuth();
  const navigate = useNavigate();

  const handleUpgrade = async (plan: string) => {
    await upgrade(plan);
    navigate('/dashboard');
  };
  const plans = [
    {
      name: "Starter",
      price: "$29",
      period: "month",
      description: "Perfect for beginners getting started with trading",
      features: [
        "3 Automatic Backtesting per month",
        "Economic Calendar Access",
        "Trading Journal",
        "Email Support",
        "Basic Strategy Library"
      ],
      popular: false,
      icon: <Target className="h-6 w-6" />
    },
    {
      name: "Professional",
      price: "$99",
      period: "month",
      description: "For serious traders who want to scale their operations",
      features: [
        "Unlimited AI Strategy Generations",
        "Unlimited Backtesting",
        "Real-time Market Data",
        "Priority Support",
        "Automated Trading",
        "Risk Management Tools",
        "Custom Alerts",
        "API Access"
      ],
      popular: true,
      icon: <Zap className="h-6 w-6" />
    },
    {
      name: "Enterprise",
      price: "$299",
      period: "month",
      description: "For professional trading firms and institutions",
      features: [
        "Everything in Professional",
        "White-label Solutions",
        "Dedicated Account Manager",
        "Custom Strategy Development",
        "Advanced Analytics",
        "Multi-account Management",
        "24/7 Phone Support",
        "Onboarding Training"
      ],
      popular: false,
      icon: <Crown className="h-6 w-6" />
    }
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
      <section className="container mx-auto px-4 py-20 text-center">
        <Badge variant="secondary" className="mb-4 bg-purple-100 text-purple-800">
          🚀 Choose Your Plan
        </Badge>
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
          Unlock Your
          <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            {" "}Trading Potential
          </span>
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
          Choose the perfect plan for your trading journey. Start with a free trial and upgrade as you grow.
        </p>
      </section>

      {/* Pricing Cards */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => (
            <Card 
              key={index} 
              className={`relative ${
                plan.popular 
                  ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white border-2 border-purple-400' 
                  : 'bg-white/5 border-white/10 text-white'
              } hover:scale-105 transition-all duration-300`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <Badge className="bg-yellow-500 text-black px-4 py-1">
                    <Star className="h-4 w-4 mr-1" />
                    Most Popular
                  </Badge>
                </div>
              )}
              
              <CardHeader className="text-center">
                <div className="flex justify-center mb-4">
                  <div className={`p-3 rounded-lg ${
                    plan.popular ? 'bg-white/20' : 'bg-gradient-to-r from-purple-500 to-pink-500'
                  }`}>
                    {plan.icon}
                  </div>
                </div>
                <CardTitle className="text-2xl">{plan.name}</CardTitle>
                <CardDescription className={plan.popular ? 'text-white/80' : 'text-gray-300'}>
                  {plan.description}
                </CardDescription>
                <div className="mt-4">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  <span className="text-lg opacity-80">/{plan.period}</span>
                </div>
              </CardHeader>
              
              <CardContent>
                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center space-x-3">
                      <Check className="h-5 w-5 text-green-400 flex-shrink-0" />
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
                
                <Button 
                  className={`w-full ${
                    plan.popular 
                      ? 'bg-white text-purple-600 hover:bg-gray-100' 
                      : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600'
                  }`}
                  onClick={() => handleUpgrade(plan.name.toLowerCase())}
                >
                  {plan.name === "Starter" ? "Start Free Trial" : "Get Started"}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Features Comparison */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Compare Features
          </h2>
          <p className="text-xl text-gray-300">
            See what's included in each plan
          </p>
        </div>
        
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/5 border-white/10">
            <CardHeader>
              <CardTitle className="text-white text-center">Feature Comparison</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-4 gap-4 text-sm">
                <div className="font-semibold text-white">Feature</div>
                <div className="text-center font-semibold text-white">Starter</div>
                <div className="text-center font-semibold text-white">Professional</div>
                <div className="text-center font-semibold text-white">Enterprise</div>
                
                <div className="text-gray-300">AI Strategy Generations</div>
                <div className="text-center text-red-400">✗</div>
                <div className="text-center text-green-400">Unlimited</div>
                <div className="text-center text-green-400">Unlimited</div>
                
                <div className="text-gray-300">Automatic Backtesting</div>
                <div className="text-center text-gray-300">3/month</div>
                <div className="text-center text-green-400">Unlimited</div>
                <div className="text-center text-green-400">Unlimited</div>
                
                <div className="text-gray-300">Real-time Data</div>
                <div className="text-center text-red-400">✗</div>
                <div className="text-center text-green-400">✓</div>
                <div className="text-center text-green-400">✓</div>
                
                <div className="text-gray-300">Economic Calendar</div>
                <div className="text-center text-green-400">✓</div>
                <div className="text-center text-green-400">✓</div>
                <div className="text-center text-green-400">✓</div>
                
                <div className="text-gray-300">Trading Journal</div>
                <div className="text-center text-green-400">✓</div>
                <div className="text-center text-green-400">✓</div>
                <div className="text-center text-green-400">✓</div>
                
                <div className="text-gray-300">Automated Trading</div>
                <div className="text-center text-red-400">✗</div>
                <div className="text-center text-green-400">✓</div>
                <div className="text-center text-green-400">✓</div>
                
                <div className="text-gray-300">API Access</div>
                <div className="text-center text-red-400">✗</div>
                <div className="text-center text-green-400">✓</div>
                <div className="text-center text-green-400">✓</div>
                
                <div className="text-gray-300">Support</div>
                <div className="text-center text-gray-300">Email</div>
                <div className="text-center text-green-400">Priority</div>
                <div className="text-center text-green-400">24/7 Phone</div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">
            Frequently Asked Questions
          </h2>
        </div>
        
        <div className="max-w-3xl mx-auto space-y-6">
          <Card className="bg-white/5 border-white/10">
            <CardHeader>
              <CardTitle className="text-white">Can I cancel my subscription anytime?</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-gray-300">
                Yes, you can cancel your subscription at any time. Your access will continue until the end of your current billing period.
              </CardDescription>
            </CardContent>
          </Card>
          
          <Card className="bg-white/5 border-white/10">
            <CardHeader>
              <CardTitle className="text-white">Is there a free trial available?</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-gray-300">
                Yes! We offer a 14-day free trial for all plans. No credit card required to start your trial.
              </CardDescription>
            </CardContent>
          </Card>
          
          <Card className="bg-white/5 border-white/10">
            <CardHeader>
              <CardTitle className="text-white">What payment methods do you accept?</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-gray-300">
                We accept all major credit cards (Visa, MasterCard, American Express) and PayPal.
              </CardDescription>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <Card className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-center">
          <CardContent className="pt-12 pb-12">
            <h2 className="text-4xl font-bold mb-4">
              Ready to Start Trading?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Join thousands of successful traders and start your journey today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                variant="secondary" 
                className="text-lg px-8 py-6"
                onClick={() => handleUpgrade('starter')}
              >
                Start Free Trial
              </Button>
              <Button size="lg" variant="outline" className="text-white border-white hover:bg-white/10 text-lg px-8 py-6">
                Contact Sales
              </Button>
            </div>
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

export default UpgradePage;
