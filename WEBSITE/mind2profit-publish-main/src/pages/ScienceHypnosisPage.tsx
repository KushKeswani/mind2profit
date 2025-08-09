import React from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Brain, CheckCircle, AlertTriangle, BookOpen } from "lucide-react";

const sources = [
  {
    title: "Descartes’ Error: Emotion, Reason, and the Human Brain",
    author: "Damasio, A. R.",
    year: 1994,
    link: "https://www.goodreads.com/book/show/29681.Descartes_Error"
  },
  {
    title: "Adaptive Markets Hypothesis, MIT Sloan",
    author: "Lo, A. W.",
    year: 2012,
    link: "https://www.technologyreview.com/2012/01/24/189404/the-adaptive-markets-hypothesis/"
  },
  {
    title: "Study on emotional regulation in trading performance",
    author: "The European Journal of Finance",
    year: 2019,
    link: "https://www.tandfonline.com/doi/abs/10.1080/1351847X.2019.1644365"
  },
  {
    title: "Journal of Behavioral Finance, Volume 6, 2005",
    author: "Journal of Behavioral Finance",
    year: 2005,
    link: "https://www.tandfonline.com/loi/hbhf20"
  },
  {
    title: "Neural mechanisms of habit and repetition",
    author: "Neuropsychologia",
    year: 2010,
    link: "https://www.sciencedirect.com/science/article/abs/pii/S0028393210002542"
  }
];

export default function ScienceHypnosisPage() {
  return (
    <div className="max-w-3xl mx-auto py-10 px-4 space-y-8 animate-fade-in">
      <h1 className="text-4xl font-bold mb-2 text-center flex items-center justify-center gap-2">
        <Brain className="h-8 w-8 text-primary" />
        The Science Behind Hypnosis & Trader Psychology
      </h1>
      <p className="text-lg text-muted-foreground text-center mb-6">
        Why mindset is the real edge in trading—and how this platform uses neuroscience to help you win.
      </p>

      <Card className="p-6 space-y-4">
        <h2 className="text-2xl font-semibold mb-2">🧠 Why Trader Psychology Matters</h2>
        <p>
          Trading is <span className="font-bold">90% psychological</span> and only 10% technical once a trader has a solid strategy.
        </p>
        <div className="bg-warning/10 border-l-4 border-warning p-4 rounded">
          <h3 className="font-semibold flex items-center gap-2 text-warning mb-1">
            <AlertTriangle className="h-4 w-4" /> Repeating Patterns of Destruction
          </h3>
          <ul className="list-disc ml-6 text-sm">
            <li>Fear causes early exits (cutting winners).</li>
            <li>Greed causes revenge trading or oversized positions.</li>
            <li>FOMO causes chasing moves after the setup is gone.</li>
            <li>Frustration leads to overtrading and poor decisions.</li>
          </ul>
          <p className="mt-2 text-xs text-muted-foreground">
            These habits aren’t rational—they’re driven by the limbic system, the part of the brain that hijacks discipline when stakes feel high.
          </p>
        </div>
      </Card>

      <Card className="p-6 space-y-4">
        <h2 className="text-2xl font-semibold mb-2">📉 Data-Driven Proof of the Problem</h2>
        <ul className="list-disc ml-6">
          <li>Only 1 in 10 traders are consistently profitable (source: eToro, IG, and proprietary prop firm data).</li>
          <li>A 2019 study from The European Journal of Finance found traders with poor emotional regulation underperformed by up to 30% over 6 months compared to those who practiced emotional awareness.</li>
          <li>Research by Damasio (1994) shows that decision-making degrades without emotional control, even if logic and information are present.</li>
        </ul>
      </Card>

      <Card className="p-6 space-y-4">
        <h2 className="text-2xl font-semibold mb-2">🎯 How This Platform Helps</h2>
        <p>
          This isn’t just “motivational fluff.” It’s neuroscience + automation built for real traders.
        </p>
        <h3 className="font-semibold mt-4 mb-2">🧬 How the Hypnosis Audio Helps</h3>
        <ol className="list-decimal ml-6">
          <li><span className="font-bold">Neuroplasticity:</span> Repetition of new beliefs (via hypnosis affirmations) rewires neural pathways over time, improving discipline and reducing anxiety (<a href="https://www.sciencedirect.com/science/article/abs/pii/S0028393210002542" className="underline text-primary" target="_blank" rel="noopener noreferrer">Neuropsychologia, 2010</a>).</li>
          <li><span className="font-bold">Subconscious Conditioning:</span> Unlike willpower, which fades under stress, subconscious beliefs drive autopilot behavior. Hypnosis accesses this layer to reinforce rules like “wait for confirmation,” “trust your edge,” or “losses are part of the plan.”</li>
          <li><span className="font-bold">Daily Rituals:</span> Many elite traders (including prop firm coaches and trading psychologists) recommend pre-trade mindset routines. Hypnotic affirmations provide a repeatable, scalable way to do this daily.</li>
        </ol>
      </Card>

      <Card className="p-6 space-y-4">
        <h2 className="text-2xl font-semibold mb-2">🔒 Case Study Logic</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm border rounded">
            <thead>
              <tr className="bg-muted">
                <th className="p-2 text-left">Problem</th>
                <th className="p-2 text-left">Traditional Fix</th>
                <th className="p-2 text-left">Your Platform</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="p-2">Emotional trading</td>
                <td className="p-2">Therapy or coaching ($150+/hr)</td>
                <td className="p-2">Hypnosis audios + chatbot guidance</td>
              </tr>
              <tr>
                <td className="p-2">No confidence</td>
                <td className="p-2">Journals + affirmations</td>
                <td className="p-2">Personalized audio reminders of success and strategy</td>
              </tr>
              <tr>
                <td className="p-2">No discipline</td>
                <td className="p-2">Willpower or accountability partner</td>
                <td className="p-2">Automated mental reinforcement through audio training</td>
              </tr>
              <tr>
                <td className="p-2">No edge</td>
                <td className="p-2">Forum advice and backtesting</td>
                <td className="p-2">Strategy generator + automated backtest results</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>

      <Card className="p-6 space-y-4">
        <h2 className="text-2xl font-semibold mb-2">🧠 Summary</h2>
        <div className="bg-primary/10 border-l-4 border-primary p-4 rounded">
          <p className="mb-2 font-semibold">This isn’t just some self-help app.</p>
          <p>
            We combine real psychology, neuroscience, and automation to fix the real reason most traders fail—their emotions.
          </p>
          <ul className="list-disc ml-6 mt-2">
            <li>Proven hypnotic conditioning methods to reprogram self-sabotaging habits</li>
            <li>Daily mindset audios to reduce FOMO, revenge trading, and impulsiveness</li>
            <li>A chatbot that understands your goals and helps build the discipline to follow them</li>
            <li>Strategy automation and backtesting so you only trade high-confidence setups</li>
          </ul>
          <p className="mt-2">You wouldn’t step into a boxing ring without training. Don’t step into the markets untrained either.</p>
        </div>
      </Card>

      <Card className="p-6 space-y-4">
        <h2 className="text-2xl font-semibold mb-2 flex items-center gap-2"><BookOpen className="h-5 w-5 text-primary" />References & Sources</h2>
        <ul className="list-disc ml-6">
          {sources.map((src, idx) => (
            <li key={idx}>
              <a href={src.link} target="_blank" rel="noopener noreferrer" className="underline text-primary font-medium">{src.title}</a> — {src.author} ({src.year})
            </li>
          ))}
        </ul>
      </Card>

      <Card className="p-6 flex flex-col items-center gap-4 mt-6">
        <h2 className="text-xl font-semibold text-center">Ready to give it a shot?</h2>
        <button
          onClick={() => window.history.back()}
          className="px-6 py-2 rounded bg-gradient-to-r from-primary to-secondary text-white font-bold shadow hover:opacity-90 transition"
        >
          Go Back
        </button>
      </Card>
    </div>
  );
}