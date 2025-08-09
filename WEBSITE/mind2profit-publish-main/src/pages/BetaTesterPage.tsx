import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { ArrowLeft, Target, Users, Zap, Brain, TrendingUp, Mail, Send, CheckCircle } from "lucide-react";
import { Link } from "react-router-dom";
import { useState } from "react";

const BetaTesterPage = () => {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    tradingExperience: "",
    tradingStyle: "",
    currentTools: "",
    painPoints: "",
    expectations: "",
    timeCommitment: "",
    deviceAccess: [],
    socialMedia: "",
    additionalInfo: ""
  });

  const handleInputChange = (field: string, value: string | string[]) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/beta-application`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setIsSubmitted(true);
      } else {
        console.error('Failed to submit application');
      }
    } catch (error) {
      console.error('Error submitting application:', error);
    }
  };

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="container mx-auto px-4 py-20 text-center">
          <Card className="max-w-2xl mx-auto bg-white/5 border-white/10 text-white">
            <CardContent className="pt-12 pb-12">
              <CheckCircle className="h-16 w-16 text-green-400 mx-auto mb-6" />
              <h1 className="text-3xl font-bold text-white mb-4">
                Application Submitted!
              </h1>
              <p className="text-gray-300 text-lg mb-8">
                Thank you for your interest in becoming a beta tester for Mind2Profit. 
                We'll review your application and get back to you within 48 hours.
              </p>
              <div className="space-y-4">
                <p className="text-gray-300">
                  What happens next:
                </p>
                <ul className="text-gray-300 space-y-2 text-left max-w-md mx-auto">
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                    <span>We'll review your application</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                    <span>Send you access credentials</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                    <span>Onboard you to the platform</span>
                  </li>
                </ul>
              </div>
              <div className="mt-8">
                <Link to="/">
                  <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600">
                    Back to Home
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

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
          🚀 Beta Testing
        </Badge>
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
          Join the
          <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            {" "}Beta Team
          </span>
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
          Help shape the future of trading tools. Get early access to Mind2Profit and provide valuable feedback.
        </p>
        
        {/* Benefits */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto mt-12">
          <div className="bg-white/5 rounded-lg p-6">
            <Zap className="h-8 w-8 text-purple-400 mx-auto mb-4" />
            <h3 className="text-white font-semibold mb-2">Early Access</h3>
            <p className="text-gray-300 text-sm">Be among the first to test new features</p>
          </div>
          <div className="bg-white/5 rounded-lg p-6">
            <Brain className="h-8 w-8 text-purple-400 mx-auto mb-4" />
            <h3 className="text-white font-semibold mb-2">Direct Input</h3>
            <p className="text-gray-300 text-sm">Shape the product with your feedback</p>
          </div>
          <div className="bg-white/5 rounded-lg p-6">
            <Users className="h-8 w-8 text-purple-400 mx-auto mb-4" />
            <h3 className="text-white font-semibold mb-2">Community</h3>
            <p className="text-gray-300 text-sm">Join our exclusive beta community</p>
          </div>
        </div>
      </section>

      {/* Application Form */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/5 border-white/10 text-white">
            <CardHeader>
              <CardTitle className="text-3xl text-white mb-2">Beta Tester Application</CardTitle>
              <CardDescription className="text-gray-300">
                Tell us about yourself and your trading experience. We're looking for traders who are passionate about improving their process.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Personal Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="firstName" className="text-white">First Name *</Label>
                    <Input
                      id="firstName"
                      value={formData.firstName}
                      onChange={(e) => handleInputChange('firstName', e.target.value)}
                      required
                      className="bg-white/10 border-white/20 text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="lastName" className="text-white">Last Name *</Label>
                    <Input
                      id="lastName"
                      value={formData.lastName}
                      onChange={(e) => handleInputChange('lastName', e.target.value)}
                      required
                      className="bg-white/10 border-white/20 text-white"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email" className="text-white">Email Address *</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    required
                    className="bg-white/10 border-white/20 text-white"
                  />
                </div>

                {/* Trading Experience */}
                <div className="space-y-2">
                  <Label htmlFor="tradingExperience" className="text-white">Trading Experience *</Label>
                  <Select value={formData.tradingExperience} onValueChange={(value) => handleInputChange('tradingExperience', value)}>
                    <SelectTrigger className="bg-white/10 border-white/20 text-white">
                      <SelectValue placeholder="Select your experience level" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="beginner">Beginner (0-1 years)</SelectItem>
                      <SelectItem value="intermediate">Intermediate (1-3 years)</SelectItem>
                      <SelectItem value="advanced">Advanced (3-5 years)</SelectItem>
                      <SelectItem value="expert">Expert (5+ years)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="tradingStyle" className="text-white">Trading Style *</Label>
                  <Select value={formData.tradingStyle} onValueChange={(value) => handleInputChange('tradingStyle', value)}>
                    <SelectTrigger className="bg-white/10 border-white/20 text-white">
                      <SelectValue placeholder="Select your primary trading style" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="day-trading">Day Trading</SelectItem>
                      <SelectItem value="swing-trading">Swing Trading</SelectItem>
                      <SelectItem value="scalping">Scalping</SelectItem>
                      <SelectItem value="position-trading">Position Trading</SelectItem>
                      <SelectItem value="options">Options Trading</SelectItem>
                      <SelectItem value="futures">Futures Trading</SelectItem>
                      <SelectItem value="crypto">Cryptocurrency</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="currentTools" className="text-white">Current Trading Tools</Label>
                  <Textarea
                    id="currentTools"
                    value={formData.currentTools}
                    onChange={(e) => handleInputChange('currentTools', e.target.value)}
                    placeholder="What tools/platforms do you currently use? (TradingView, ThinkOrSwim, etc.)"
                    className="bg-white/10 border-white/20 text-white"
                    rows={3}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="painPoints" className="text-white">Biggest Trading Pain Points *</Label>
                  <Textarea
                    id="painPoints"
                    value={formData.painPoints}
                    onChange={(e) => handleInputChange('painPoints', e.target.value)}
                    placeholder="What are your biggest challenges in trading? (psychology, strategy, execution, etc.)"
                    required
                    className="bg-white/10 border-white/20 text-white"
                    rows={4}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="expectations" className="text-white">What do you hope to get from Mind2Profit? *</Label>
                  <Textarea
                    id="expectations"
                    value={formData.expectations}
                    onChange={(e) => handleInputChange('expectations', e.target.value)}
                    placeholder="What features or improvements are you most excited about?"
                    required
                    className="bg-white/10 border-white/20 text-white"
                    rows={3}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="timeCommitment" className="text-white">Time Commitment *</Label>
                  <Select value={formData.timeCommitment} onValueChange={(value) => handleInputChange('timeCommitment', value)}>
                    <SelectTrigger className="bg-white/10 border-white/20 text-white">
                      <SelectValue placeholder="How much time can you commit to testing?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1-2-hours">1-2 hours per week</SelectItem>
                      <SelectItem value="3-5-hours">3-5 hours per week</SelectItem>
                      <SelectItem value="5-10-hours">5-10 hours per week</SelectItem>
                      <SelectItem value="10-plus-hours">10+ hours per week</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Device Access */}
                <div className="space-y-4">
                  <Label className="text-white">Device Access *</Label>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                      { id: 'desktop', label: 'Desktop/Laptop' },
                      { id: 'mobile', label: 'Mobile' },
                      { id: 'tablet', label: 'Tablet' },
                      { id: 'multiple', label: 'Multiple Devices' }
                    ].map((device) => (
                      <div key={device.id} className="flex items-center space-x-2">
                        <Checkbox
                          id={device.id}
                          checked={formData.deviceAccess.includes(device.id)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              handleInputChange('deviceAccess', [...formData.deviceAccess, device.id]);
                            } else {
                              handleInputChange('deviceAccess', formData.deviceAccess.filter(d => d !== device.id));
                            }
                          }}
                        />
                        <Label htmlFor={device.id} className="text-white text-sm">{device.label}</Label>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="socialMedia" className="text-white">Social Media (Optional)</Label>
                  <Input
                    id="socialMedia"
                    value={formData.socialMedia}
                    onChange={(e) => handleInputChange('socialMedia', e.target.value)}
                    placeholder="Twitter, LinkedIn, or other social profiles"
                    className="bg-white/10 border-white/20 text-white"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="additionalInfo" className="text-white">Additional Information</Label>
                  <Textarea
                    id="additionalInfo"
                    value={formData.additionalInfo}
                    onChange={(e) => handleInputChange('additionalInfo', e.target.value)}
                    placeholder="Anything else you'd like us to know about you or your trading?"
                    className="bg-white/10 border-white/20 text-white"
                    rows={3}
                  />
                </div>

                <div className="pt-6">
                  <Button type="submit" className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600">
                    <Send className="mr-2 h-4 w-4" />
                    Submit Application
                  </Button>
                </div>
              </form>
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

export default BetaTesterPage;
