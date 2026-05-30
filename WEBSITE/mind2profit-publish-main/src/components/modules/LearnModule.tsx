import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const termCards = [
  {
    title: "R-Multiple",
    content:
      "An R-multiple measures profit or loss relative to your initial risk. If you risk $100 and make $200, that trade is +2R.",
  },
  {
    title: "Drawdown",
    content:
      "Drawdown is the drop from your peak account value to a lower point. Tracking max drawdown helps you size risk and protect capital.",
  },
  {
    title: "Position Size",
    content:
      "Position size is how much you trade on a setup. Strong traders size from risk first, not from emotion or conviction.",
  },
  {
    title: "Expectancy",
    content:
      "Expectancy is average outcome per trade over a large sample. Positive expectancy comes from edge plus discipline.",
  },
];

const disciplineTips = [
  "Use a fixed risk cap per trade and per day before the session starts.",
  "Log every trade with setup, entry, exit, and emotional state.",
  "When your rules are unclear, the trade is not valid yet.",
  "Avoid adding to losers without a pre-defined plan.",
];

const psychologyTips = [
  "Pause after a loss and review your checklist before the next order.",
  "Separate outcome from process: a good trade can lose, a bad trade can win.",
  "If you feel urgency, reduce size or step away for 5 minutes.",
  "Build confidence from repeated rule-following, not from one big winner.",
];

export const LearnModule = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Learn</h1>
        <p className="text-muted-foreground">
          Core trading terms, risk management basics, and practical psychology habits.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {termCards.map((card) => (
          <Card key={card.title}>
            <CardHeader>
              <CardTitle className="text-lg">{card.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground leading-relaxed">{card.content}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Risk Management Checklist</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {disciplineTips.map((tip) => (
              <p key={tip} className="text-sm text-muted-foreground">
                - {tip}
              </p>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Trading Psychology Habits</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {psychologyTips.map((tip) => (
              <p key={tip} className="text-sm text-muted-foreground">
                - {tip}
              </p>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
