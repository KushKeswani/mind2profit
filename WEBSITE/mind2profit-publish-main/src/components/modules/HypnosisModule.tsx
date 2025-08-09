import { useState } from "react";
//
import { Card } from "@/components/ui/card";
import React from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import { 
  Brain, 
  Download, 
  Clock, 
  Mail,
  Heart,
  Zap
} from "lucide-react";
import { Link } from "react-router-dom";


interface Affirmation {
  id: string;
  title: string;
  content: string;
  audioUrl?: string;
  duration: string;
  type: "confidence" | "discipline" | "patience" | "focus";
}

export const HypnosisModule: React.FC = () => {

  // Old form fields
  const [challenge, setChallenge] = useState("");
  const [behavior, setBehavior] = useState("");
  const [tone, setTone] = useState("calm");
  const [routine, setRoutine] = useState("Morning routine");
  const [submitted, setSubmitted] = useState(false);
  const [togetherAffirmation, setTogetherAffirmation] = useState("");
  const [isTogetherGenerating, setIsTogetherGenerating] = useState(false);
  const [savedAffirmations, setSavedAffirmations] = useState<string[]>([]);
  const [existingAffirmations] = useState<Affirmation[]>([
    {
      id: "1",
      title: "Trading Confidence",
      content: "I am a disciplined trader who follows my plan with confidence. I trust my analysis and stick to my risk management rules.",
      duration: "3:45",
      type: "confidence"
    },
    {
      id: "2",
      title: "Emotional Control",
      content: "I remain calm and objective in all market conditions. Fear and greed do not control my decisions.",
      duration: "4:20",
      type: "discipline"
    },
    {
      id: "3",
      title: "Patience Mastery",
      content: "I wait for high-probability setups. Quality over quantity guides my trading approach.",
      duration: "3:30",
      type: "patience"
    }
  ]);

  const handleTogetherAffirmation = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setIsTogetherGenerating(true);
    setTogetherAffirmation("");
    setSubmitted(true);
    try {
      const response = await fetch("/api/togetherAffirmation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          challenge,
          behavior,
          tone,
          routine
        })
      });
      if (response.ok) {
        const data = await response.json();
        setTogetherAffirmation(data.affirmation || "[No affirmation returned]");
      } else {
        setTogetherAffirmation("Error generating affirmation. Please try again.");
      }
    } catch (err) {
      setTogetherAffirmation("Error connecting to AI service.");
    }
    setIsTogetherGenerating(false);
  };

  const handleSaveAffirmation = () => {
    if (togetherAffirmation && !savedAffirmations.includes(togetherAffirmation)) {
      setSavedAffirmations([...savedAffirmations, togetherAffirmation]);
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case "confidence": return "bg-primary";
      case "discipline": return "bg-success";
      case "patience": return "bg-warning";
      case "focus": return "bg-purple-500";
      default: return "bg-muted";
    }
  };



  return (
    <div className="space-y-6 animate-fade-in">
      {/* Science Callout */}
      <div className="bg-primary/10 border-l-4 border-primary p-4 rounded flex items-center justify-between mb-2">
        <div className="font-semibold text-primary text-lg">
          Don&apos;t believe us? Read the science behind it.
        </div>
        <Link to="/science-hypnosis">
          <Button className="bg-gradient-primary" size="sm">
            Science & Proof
          </Button>
        </Link>
      </div>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Hypnosis Studio</h1>
          <p className="text-muted-foreground">Transform your trading mindset with personalized affirmations</p>
        </div>
        <Badge className="bg-gradient-primary">
          <Brain className="h-4 w-4 mr-2" />
          AI-Powered
        </Badge>
      </div>

      {/* Old Multi-Field Affirmation Form */}
      <Card className="p-6">
        <div className="flex items-center space-x-3 mb-4">
          <Heart className="h-6 w-6 text-primary" />
          <h2 className="text-xl font-semibold">Personalized Affirmation Generator</h2>
        </div>
        <form onSubmit={handleTogetherAffirmation} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">1. What is your biggest psychological challenge right now while trading?</label>
            <input
              type="text"
              className="w-full border border-border rounded-md p-2 bg-background"
              value={challenge}
              onChange={e => setChallenge(e.target.value)}
              required
              placeholder="e.g. FOMO, revenge trading, hesitation, overconfidence"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">2. What behavior would you like to change or reinforce?</label>
            <input
              type="text"
              className="w-full border border-border rounded-md p-2 bg-background"
              value={behavior}
              onChange={e => setBehavior(e.target.value)}
              required
              placeholder="e.g. wait for confirmation, follow your plan, stop after hitting daily goal"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">3. What emotional tone would you like this to have?</label>
            <select
              className="w-full border border-border rounded-md p-2 bg-background"
              value={tone}
              onChange={e => setTone(e.target.value)}
              required
            >
              <option value="calm">Calm</option>
              <option value="encouraging">Encouraging</option>
              <option value="serious">Serious</option>
              <option value="tough love">Tough Love</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">4. Would you like this as a morning routine or post-trade reset?</label>
            <select
              className="w-full border border-border rounded-md p-2 bg-background"
              value={routine}
              onChange={e => setRoutine(e.target.value)}
              required
            >
              <option value="Morning routine">Morning routine</option>
              <option value="Post-trade reset">Post-trade reset</option>
            </select>
          </div>
          <div className="flex flex-col md:flex-row gap-2 mt-4">
            <Button
              type="submit"
              disabled={isTogetherGenerating || !challenge.trim() || !behavior.trim()}
              className="bg-gradient-primary"
            >
              {isTogetherGenerating ? (
                <>
                  <Zap className="h-4 w-4 mr-2 animate-spin" />
                  Creating Affirmation...
                </>
              ) : (
                <>
                  <Brain className="h-4 w-4 mr-2" />
                  Generate Affirmation
                </>
              )}
            </Button>
            {togetherAffirmation && (
              <Button className="bg-gradient-primary" onClick={handleSaveAffirmation} type="button">
                <Download className="h-4 w-4 mr-2" />
                Save Text
              </Button>
            )}
          </div>
        </form>
        {/* Together AI Affirmation */}
        {togetherAffirmation && (
          <Card className="p-6 border-l-4 border-l-primary bg-primary/5 mt-6">
            <h3 className="text-lg font-semibold mb-4">Your Personalized Affirmation</h3>
            <div className="bg-background p-4 rounded-lg mb-4">
              <p className="text-foreground leading-relaxed italic">
                {togetherAffirmation}
              </p>
            </div>
          </Card>
        )}
      </Card>
      {/* Pre-built Affirmations */}
      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Pre-built Affirmations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {existingAffirmations.map((affirmation) => (
            <Card key={affirmation.id} className="p-4 hover:shadow-medium transition-all duration-200">
              <div className="flex items-center justify-between mb-3">
                <Badge className={getTypeColor(affirmation.type)}>
                  {affirmation.type}
                </Badge>
                <div className="flex items-center text-sm text-muted-foreground">
                  <Clock className="h-3 w-3 mr-1" />
                  {affirmation.duration}
                </div>
              </div>
              <h3 className="font-semibold mb-2">{affirmation.title}</h3>
              <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
                {affirmation.content}
              </p>
            </Card>
          ))}
        </div>
      </Card>

      {/* Saved Affirmations */}
      {savedAffirmations.length > 0 && (
        <Card className="p-6 mt-6">
          <h2 className="text-xl font-semibold mb-4">Your Saved Affirmations</h2>
          <div className="space-y-4">
            {savedAffirmations.map((text, idx) => (
              <div key={idx} className="bg-muted rounded-lg p-4 text-foreground whitespace-pre-line">
                {text}
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
// ...existing code...