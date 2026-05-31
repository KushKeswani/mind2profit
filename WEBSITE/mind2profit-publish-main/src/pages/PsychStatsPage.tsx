import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { loadAppState, resetAppData } from "@/lib/storage";
import type { LiveSession } from "@/lib/types";

export default function PsychStatsPage() {
  const [appState, setAppState] = useState(loadAppState());
  const [showResetDialog, setShowResetDialog] = useState(false);

  useEffect(() => {
    setAppState(loadAppState());
  }, []);

  // Calculate discipline score for last 7 days
  const calculateDisciplineScore = (): number => {
    const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
    const recentSessions = appState.sessions.filter(
      (s) => s.startedAt >= sevenDaysAgo
    );

    let score = 100;

    recentSessions.forEach((session) => {
      session.violations.forEach((violation) => {
        if (violation.type === "off_plan_trade") {
          score -= 10;
        } else if (violation.type === "revenge") {
          score -= 15;
        } else if (violation.type === "gate_failed_trade_attempt") {
          score -= 5;
        }
      });
    });

    return Math.max(0, Math.min(100, score));
  };

  const disciplineScore = calculateDisciplineScore();

  // Calculate insights
  const getInsights = (): string[] => {
    const insights: string[] = [];
    const sessionsWithPlanFollowed = appState.sessions.filter(
      (s) => s.reflection?.followedPlan === true
    );
    const sessionsWithoutPlan = appState.sessions.filter(
      (s) => s.reflection?.followedPlan === false
    );

    if (sessionsWithPlanFollowed.length > 0 && sessionsWithoutPlan.length > 0) {
      const avgViolationsWithPlan =
        sessionsWithPlanFollowed.reduce(
          (sum, s) => sum + s.violations.length,
          0
        ) / sessionsWithPlanFollowed.length;
      const avgViolationsWithoutPlan =
        sessionsWithoutPlan.reduce((sum, s) => sum + s.violations.length, 0) /
        sessionsWithoutPlan.length;

      if (avgViolationsWithPlan < avgViolationsWithoutPlan) {
        insights.push(
          "On days you followed plan, violations were lower."
        );
      }
    }

    return insights;
  };

  const insights = getInsights();

  const handleReset = () => {
    resetAppData();
    setAppState(loadAppState());
    setShowResetDialog(false);
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Stats & Discipline</h1>
            <p className="text-muted-foreground">Track your trading discipline and streaks.</p>
          </div>
          <Dialog open={showResetDialog} onOpenChange={setShowResetDialog}>
            <DialogTrigger asChild>
              <Button variant="outline" size="sm">
                Reset Data
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Reset App Data</DialogTitle>
              </DialogHeader>
              <p className="text-sm text-muted-foreground mb-4">
                This will delete all sessions, scripts, and stats. This cannot be undone.
              </p>
              <div className="flex gap-2 justify-end">
                <Button variant="outline" onClick={() => setShowResetDialog(false)}>
                  Cancel
                </Button>
                <Button variant="destructive" onClick={handleReset}>
                  Reset
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        {/* Discipline Score */}
        <Card>
          <CardHeader>
            <CardTitle>Discipline Score (Last 7 Days)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold mb-2">{disciplineScore}/100</div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className="bg-primary h-2 rounded-full transition-all"
                style={{ width: `${disciplineScore}%` }}
              />
            </div>
            <p className="text-sm text-muted-foreground mt-2">
              -10 per off-plan trade, -15 per revenge trade, -5 per gate failure
            </p>
          </CardContent>
        </Card>

        {/* Streaks */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardHeader>
              <CardTitle>Plan Followed Streak</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{appState.streaks.planFollowedDays}</div>
              <p className="text-sm text-muted-foreground mt-1">days</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Best Plan Followed Streak</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{appState.streaks.bestPlanFollowedDays}</div>
              <p className="text-sm text-muted-foreground mt-1">days</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>No Revenge Days</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{appState.streaks.noRevengeDays}</div>
              <p className="text-sm text-muted-foreground mt-1">days</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Accepted No Trade Days</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{appState.streaks.acceptedNoTradeDays}</div>
              <p className="text-sm text-muted-foreground mt-1">days</p>
            </CardContent>
          </Card>
        </div>

        {/* Insights */}
        {insights.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Insights</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {insights.map((insight, idx) => (
                  <li key={idx} className="text-sm">
                    {insight}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}

        {/* Session Summary */}
        <Card>
          <CardHeader>
            <CardTitle>Session Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 text-sm">
              <p>
                Total Sessions: <span className="font-semibold">{appState.sessions.length}</span>
              </p>
              <p>
                Completed Sessions:{" "}
                <span className="font-semibold">
                  {appState.sessions.filter((s) => s.state === "completed").length}
                </span>
              </p>
              <p>
                Stopped Sessions:{" "}
                <span className="font-semibold">
                  {appState.sessions.filter((s) => s.state === "stopped").length}
                </span>
              </p>
              <p>
                Total Violations:{" "}
                <span className="font-semibold">
                  {appState.sessions.reduce((sum, s) => sum + s.violations.length, 0)}
                </span>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}


