import React, { useState } from "react";

const tones = [
  "calm",
  "encouraging",
  "serious",
  "tough love"
];
const routines = [
  "Morning routine",
  "Post-trade reset"
];


export const TradingAffirmationForm: React.FC = () => {
  const [challenge, setChallenge] = useState("");
  const [behavior, setBehavior] = useState("");
  const [tone, setTone] = useState(tones[0]);
  const [routine, setRoutine] = useState(routines[0]);
  const [submitted, setSubmitted] = useState(false);
  const [script, setScript] = useState("");
  const [savedText, setSavedText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Generate script
    let intro =
      routine === "Morning routine"
        ? "As you begin your trading day, take a deep breath."
        : "Take a moment to reset and center yourself.";
    let body =
      tone === "tough love"
        ? `You know your biggest challenge is ${challenge}. You are stronger than your impulses. You choose to ${behavior}. You are disciplined, focused, and in control. Each trade is a fresh start. You do not let ${challenge} define you. You are a trader who grows every day.`
        : tone === "serious"
        ? `You recognize that ${challenge} is present. You are aware, and you choose to ${behavior}. You are steady, patient, and mindful. Each moment is a chance to improve. You are committed to your process.`
        : tone === "encouraging"
        ? `You notice ${challenge}, but you are learning to let it go. You remind yourself to ${behavior}. You are capable, resilient, and always improving. Every trade is an opportunity to grow. You trust yourself and your plan.`
        : `You are calm and present. ${challenge} drifts away with each breath. You gently remind yourself to ${behavior}. You are patient, focused, and at ease. You trust the process. You are exactly where you need to be.`;
    let outro =
      routine === "Morning routine"
        ? "Carry this mindset with you as you trade today."
        : "Let this feeling guide you as you move forward.";
    setScript(`${intro}\n${body}\n${outro}`);
    setSubmitted(true);
  };

  const handleSaveText = () => {
    setSavedText(script);
  };

  return (
    <div className="max-w-lg mx-auto mt-10 bg-background rounded-lg shadow-lg p-8 animate-fade-in">
      <h2 className="text-2xl font-bold mb-6 text-center">Personalized Trading Affirmation</h2>
      {!submitted ? (
        <form onSubmit={handleSubmit} className="space-y-6">
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
              {tones.map(t => (
                <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
              ))}
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
              {routines.map(r => (
                <option key={r} value={r}>{r}</option>
              ))}
            </select>
          </div>
          <div className="flex justify-end mt-8">
            <button
              type="submit"
              className="px-4 py-2 rounded bg-primary text-white hover:bg-primary/80 transition"
            >
              Generate Affirmation
            </button>
          </div>
        </form>
      ) : (
        <div className="space-y-6">
          <div className="bg-muted rounded-lg p-6 text-lg whitespace-pre-line leading-relaxed text-foreground">
            {script}
          </div>
          <div className="flex justify-end mt-4">
            <button
              className="px-4 py-2 rounded bg-primary text-white hover:bg-primary/80 transition"
              onClick={handleSaveText}
              type="button"
            >
              Save Text
            </button>
          </div>
        </div>
      )}
      {savedText && (
        <div className="mt-8">
          <h4 className="text-lg font-semibold mb-2">Your Saved Affirmation</h4>
          <div className="bg-muted rounded-lg p-6 text-lg whitespace-pre-line leading-relaxed text-foreground">
            {savedText}
          </div>
          <div className="text-muted-foreground text-sm mt-2">
            Here’s your personalized trading affirmation. Feel free to read this daily or use it when needed.
          </div>
        </div>
      )}
    </div>
  );
};

export default TradingAffirmationForm;
