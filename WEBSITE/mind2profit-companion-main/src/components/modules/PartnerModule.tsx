import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { 
  Heart, 
  Brain, 
  Coffee, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle,
  Zap,
  Target
} from "lucide-react";
import { Link } from "react-router-dom";
import { AIChat } from "@/components/ai/AIChat";

export const PartnerModule = () => {
  const [sleepHours, setSleepHours] = useState([7]);
  const [emotionLevel, setEmotionLevel] = useState([7]);
  const [confidenceLevel, setConfidenceLevel] = useState([8]);
  const [hasCheckedIn, setHasCheckedIn] = useState(false);

  const handleCheckIn = () => {
    setHasCheckedIn(true);
  };

  const getEmotionLabel = (value: number) => {
    if (value <= 3) return "Stressed";
    if (value <= 5) return "Neutral";
    if (value <= 7) return "Good";
    return "Excellent";
  };

  const getConfidenceLabel = (value: number) => {
    if (value <= 3) return "Low";
    if (value <= 5) return "Moderate";
    if (value <= 7) return "High";
    return "Very High";
  };

  const getRecommendation = () => {
    const sleep = sleepHours[0];
    const emotion = emotionLevel[0];
    const confidence = confidenceLevel[0];

    if (sleep < 6 || emotion < 5) {
      return {
        type: "warning",
        title: "Consider reducing position sizes today",
        message: "Your sleep or emotional state suggests taking a more conservative approach.",
        icon: AlertTriangle
      };
    }

    if (emotion >= 8 && confidence >= 8) {
      return {
        type: "success",
        title: "Perfect trading conditions",
        message: "You're in an optimal state for executing your trading plan.",
        icon: CheckCircle
      };
    }

    return {
      type: "info",
      title: "Good trading conditions",
      message: "You're ready to trade according to your plan. Stay disciplined.",
      icon: Target
    };
  };

  // Helper to determine if user is not feeling good
  const notFeelingGood = emotionLevel[0] <= 5 || confidenceLevel[0] <= 5;

  const recommendation = getRecommendation();

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Virtual Trading Partner</h1>
          <p className="text-muted-foreground">Your daily check-in and mindset companion</p>
        </div>
        <Badge className={hasCheckedIn ? "bg-success" : "bg-warning"}>
          {hasCheckedIn ? "Checked In" : "Pending Check-in"}
        </Badge>
      </div>

      {/* Daily Check-in */}
      <Card className="p-6">
        <div className="flex items-center space-x-3 mb-6">
          <Heart className="h-6 w-6 text-primary" />
          <h2 className="text-xl font-semibold">Daily Check-in</h2>
        </div>

        <div className="space-y-6">
          {/* Sleep */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <Coffee className="h-5 w-5 text-primary" />
                <span className="font-medium">Hours of Sleep</span>
              </div>
              <Badge variant="outline">{sleepHours[0]} hours</Badge>
            </div>
            <Slider
              value={sleepHours}
              onValueChange={setSleepHours}
              max={12}
              min={3}
              step={0.5}
              className="mb-2"
            />
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>3h</span>
              <span>12h</span>
            </div>
          </div>

          {/* Emotional State */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <Brain className="h-5 w-5 text-primary" />
                <span className="font-medium">Emotional State</span>
              </div>
              <Badge variant="outline">{getEmotionLabel(emotionLevel[0])}</Badge>
            </div>
            <Slider
              value={emotionLevel}
              onValueChange={setEmotionLevel}
              max={10}
              min={1}
              step={1}
              className="mb-2"
            />
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>Stressed</span>
              <span>Excellent</span>
            </div>
          </div>

          {/* Confidence Level */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <Zap className="h-5 w-5 text-primary" />
                <span className="font-medium">Confidence Level</span>
              </div>
              <Badge variant="outline">{getConfidenceLabel(confidenceLevel[0])}</Badge>
            </div>
            <Slider
              value={confidenceLevel}
              onValueChange={setConfidenceLevel}
              max={10}
              min={1}
              step={1}
              className="mb-2"
            />
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>Low</span>
              <span>Very High</span>
            </div>
          </div>

          <Button 
            onClick={handleCheckIn}
            disabled={hasCheckedIn}
            className="w-full bg-gradient-primary"
          >
            {hasCheckedIn ? "✓ Checked In" : "Complete Check-in"}
          </Button>
        </div>
      </Card>

      {/* AI Recommendation */}
      {hasCheckedIn && (
        <Card className={`p-6 border-l-4 ${
          recommendation.type === "warning" ? "border-l-warning bg-warning/5" :
          recommendation.type === "success" ? "border-l-success bg-success/5" :
          "border-l-primary bg-primary/5"
        }`}>
          <div className="flex items-start space-x-4">
            <recommendation.icon className={`h-6 w-6 ${
              recommendation.type === "warning" ? "text-warning" :
              recommendation.type === "success" ? "text-success" :
              "text-primary"
            }`} />
            <div>
              <h3 className="font-semibold text-foreground mb-2">
                {recommendation.title}
              </h3>
              <p className="text-muted-foreground">
                {recommendation.message}
      {/* Hypnosis Prep Link after check-in */}
      <Card className="p-6 mt-6">
        <h2 className="text-xl font-semibold mb-4">Get Ready for Hypnosis</h2>
        <div className="mb-4 text-muted-foreground text-sm">
          {notFeelingGood ? (
            <>
              It looks like you're not feeling your best today. <b>Click below to get in the right mindset.</b> When you start your hypnosis, make sure to explain your concerns so the affirmation can help you most.
            </>
          ) : (
            <>
              Ready to reinforce your trading mindset? <b>Click below to begin your hypnosis session.</b>
            </>
          )}
        </div>
        <Link to="/hypnosis">
          <Button className="bg-gradient-primary" size="lg">
            Go to Hypnosis Studio
          </Button>
        </Link>
      </Card>
              </p>
            </div>
          </div>
        </Card>
      )}

      {/* Prop Firm Chatbot */}
      <Card className="p-6 mt-6">
        <h2 className="text-xl font-semibold mb-4">Prop Firm Rules & Advice Chatbot</h2>
        <div className="mb-2 text-muted-foreground text-sm">Ask anything about prop firm rules, risk management, or get advice for passing your challenge.</div>
        <AIChat />
      </Card>

        <AIChat />
      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Conversations</h2>
        <div className="space-y-4">
          <div className="p-4 bg-muted rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium">Strategy Discussion</span>
              <span className="text-sm text-muted-foreground">Yesterday</span>
            </div>
            <p className="text-sm text-muted-foreground">
              "Should I stick to my ICT strategy during high-impact news?" - Discussed patience and avoiding FOMO.
            </p>
          </div>
          <div className="p-4 bg-muted rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium">Trade Review</span>
              <span className="text-sm text-muted-foreground">2 days ago</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Reviewed your GBPUSD loss - identified early entry as the main issue. Practice waiting for confirmation.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};