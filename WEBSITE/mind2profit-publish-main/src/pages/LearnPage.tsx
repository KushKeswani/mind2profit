import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const lessons = [
  {
    id: "1",
    title: "The Plan vs. Emotion Split",
    content:
      "Every trade you take is either planned or emotional. There is no middle ground. If you cannot clearly define why this setup matches your written plan, you are trading emotionally. Emotional trading leads to revenge trading, overtrading, and blown accounts. The solution: gate every trade through your plan verification process.",
  },
  {
    id: "2",
    title: "Walking Away is Winning",
    content:
      "The best traders know when not to trade. If you walk away after a loss, that is a winning decision. If you walk away because the setups are not clear, that is a winning decision. Your discipline score improves when you stay flat, not when you force trades. Accept that zero trades some days is the correct outcome.",
  },
  {
    id: "3",
    title: "The Revenge Trap",
    content:
      "Revenge trading happens when you try to make back a loss immediately. This is not trading. This is gambling. Your brain is in tilt mode, making decisions from emotion, not logic. The only cure: stop. Use the reset script. Do not trade again until you are calm. One bad trade does not define you. One revenge trade can end your account.",
  },
  {
    id: "4",
    title: "Gate Questions Are Filters",
    content:
      "The three gate questions exist to filter out emotional trades. If you cannot answer 'yes' to all three, you are about to take an emotional trade. The questions force you to confront reality: Do you have a plan? Do you know your exit? Are you okay with zero trades? If any answer is 'no,' the gate should stop you. Trust the gate.",
  },
  {
    id: "5",
    title: "Check-Ins Create Accountability",
    content:
      "Every trade you log should trigger a check-in: Was this planned? If you answer 'no,' you log a violation. This is not punishment. This is data. The check-in forces you to be honest with yourself in the moment, not in hindsight. Over time, the check-ins build awareness of when you are drifting off-plan.",
  },
  {
    id: "6",
    title: "Reflection Completes the Loop",
    content:
      "After every session, you reflect: Did you follow the plan? What was your emotion? This reflection closes the loop. It turns experience into learning. Without reflection, you repeat the same mistakes. With reflection, you build discipline. The 15 seconds it takes to reflect are worth more than hours of strategy study.",
  },
];

export default function LearnPage() {
  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Trading Psychology Lessons</h1>
          <p className="text-muted-foreground">Short lessons on trading discipline and psychology.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {lessons.map((lesson) => (
            <Card key={lesson.id}>
              <CardHeader>
                <CardTitle className="text-lg">{lesson.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground leading-relaxed">{lesson.content}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}


