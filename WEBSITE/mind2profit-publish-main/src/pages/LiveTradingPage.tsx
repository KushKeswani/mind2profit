import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { ChipSelect } from "@/components/psych/ChipSelect";
import { YesNoToggle } from "@/components/psych/YesNoToggle";
import { Stepper } from "@/components/psych/Stepper";
import {
  loadAppState,
  saveAppState,
  isLockedForToday,
  setLockedUntilEndOfDay,
  getCurrentSession,
  updateSession,
  getScriptByVariant,
} from "@/lib/storage";
import { seedDefaultScriptsIfNeeded } from "@/lib/seedScripts";
import type {
  LiveSession,
  ScriptVariant,
  Emotion,
  Intent,
  GateQuestion,
  Violation,
  CheckIn,
  Reflection,
} from "@/lib/types";
import { Play, Pause, AlertTriangle } from "lucide-react";

type GatingStep = "script" | "intent" | "emotion" | "gate" | "external_conscience";

export default function LiveTradingPage() {
  const [appState, setAppState] = useState(loadAppState());
  const [showGating, setShowGating] = useState(false);
  const [gatingStep, setGatingStep] = useState<GatingStep>("script");
  const [currentSession, setCurrentSession] = useState<LiveSession | undefined>(
    getCurrentSession()
  );
  const [selectedVariant, setSelectedVariant] = useState<ScriptVariant>("pre_market");
  const [selectedIntent, setSelectedIntent] = useState<Intent | undefined>();
  const [selectedEmotion, setSelectedEmotion] = useState<Emotion | undefined>();
  const [gateAnswers, setGateAnswers] = useState<Record<GateQuestion, boolean | undefined>>({
    defined_setup: undefined,
    know_stop: undefined,
    ok_no_trade: undefined,
  });
  const [scriptReadTime, setScriptReadTime] = useState(0);
  const [showCheckIn, setShowCheckIn] = useState(false);
  const [showReflection, setShowReflection] = useState(false);
  const [reflectionData, setReflectionData] = useState<Partial<Reflection>>({});
  const [audioPlaying, setAudioPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);
  const scriptTimerRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    seedDefaultScriptsIfNeeded();
    const state = loadAppState();
    setAppState(state);
    setCurrentSession(getCurrentSession());
  }, []);

  useEffect(() => {
    // Auto-advance script reading timer
    if (gatingStep === "script" && scriptReadTime < 20) {
      scriptTimerRef.current = setTimeout(() => {
        setScriptReadTime((prev) => prev + 1);
      }, 1000);
    }
    return () => {
      if (scriptTimerRef.current) {
        clearTimeout(scriptTimerRef.current);
      }
    };
  }, [gatingStep, scriptReadTime]);

  const handleStartTrading = () => {
    if (isLockedForToday()) {
      alert("Trading is locked for today after using STOP TRADING.");
      return;
    }
    setShowGating(true);
    setGatingStep("script");
    setScriptReadTime(0);
  };

  const handleScriptContinue = () => {
    if (scriptReadTime < 20) {
      alert("Please spend at least 20 seconds reading or listening to the script.");
      return;
    }
    setGatingStep("intent");
  };

  const handleIntentContinue = () => {
    if (!selectedIntent) {
      alert("Please select your trading intent.");
      return;
    }
    setGatingStep("emotion");
  };

  const handleEmotionContinue = () => {
    if (!selectedEmotion) {
      alert("Please select your starting emotion.");
      return;
    }
    setGatingStep("gate");
  };

  const handleGateContinue = () => {
    const allAnswered = Object.values(gateAnswers).every((a) => a !== undefined);
    if (!allAnswered) {
      alert("Please answer all gate questions.");
      return;
    }

    const gatePassed = Object.values(gateAnswers).every((a) => a === true);
    if (!gatePassed) {
      // Gate failed - show options
      return;
    }

    setGatingStep("external_conscience");
  };

  const handleEnterLiveMode = () => {
    const session: LiveSession = {
      id: Date.now().toString(),
      startedAt: Date.now(),
      state: "live",
      variantUsed: selectedVariant,
      intent: selectedIntent!,
      emotionStart: selectedEmotion!,
      gateAnswers: gateAnswers as Record<GateQuestion, boolean>,
      gatePassed: true,
      violations: [],
      checkIns: [],
    };

    const state = loadAppState();
    state.currentSessionId = session.id;
    state.sessions.push(session);
    saveAppState(state);
    setAppState(state);
    setCurrentSession(session);
    setShowGating(false);
  };

  const handleStopTrading = () => {
    if (!currentSession) return;

    const updated: LiveSession = {
      ...currentSession,
      state: "stopped",
      endedAt: Date.now(),
    };

    updateSession(updated);
    setLockedUntilEndOfDay();
    const state = loadAppState();
    state.currentSessionId = undefined;
    saveAppState(state);
    setAppState(state);
    setCurrentSession(undefined);

    // Play reset audio if available
    const resetScript = getScriptByVariant("after_loss");
    if (resetScript?.audioUrl) {
      // Would play audio here
    }

    alert("Walking away is a winning decision.");
    setShowReflection(true);
  };

  const handleLogTrade = () => {
    setShowCheckIn(true);
  };

  const handleCheckInSubmit = (wasPlanned: boolean) => {
    if (!currentSession) return;

    const checkIn: CheckIn = {
      id: Date.now().toString(),
      ts: Date.now(),
      question: "was_this_planned",
      answer: wasPlanned,
    };

    let violations = [...currentSession.violations];
    if (!wasPlanned) {
      const violation: Violation = {
        id: Date.now().toString(),
        ts: Date.now(),
        type: "off_plan_trade",
      };
      violations.push(violation);
    }

    const updated: LiveSession = {
      ...currentSession,
      checkIns: [...currentSession.checkIns, checkIn],
      violations,
    };

    updateSession(updated);
    setCurrentSession(updated);
    setShowCheckIn(false);
  };

  const handleReflectionSubmit = () => {
    if (!currentSession || reflectionData.followedPlan === undefined || !reflectionData.emotionDuring) {
      alert("Please complete the reflection.");
      return;
    }

    const reflection: Reflection = {
      ts: Date.now(),
      followedPlan: reflectionData.followedPlan!,
      emotionDuring: reflectionData.emotionDuring!,
      note: reflectionData.note,
    };

    const updated: LiveSession = {
      ...currentSession,
      state: "completed",
      endedAt: Date.now(),
      reflection,
    };

    updateSession(updated);
    const state = loadAppState();
    state.currentSessionId = undefined;
    
    // Update streaks
    if (reflection.followedPlan) {
      state.streaks.planFollowedDays += 1;
      if (state.streaks.planFollowedDays > state.streaks.bestPlanFollowedDays) {
        state.streaks.bestPlanFollowedDays = state.streaks.planFollowedDays;
      }
    } else {
      state.streaks.planFollowedDays = 0;
    }

    saveAppState(state);
    setAppState(state);
    setCurrentSession(undefined);
    setShowReflection(false);
  };

  const script = getScriptByVariant(selectedVariant);
  const gatePassed = Object.values(gateAnswers).every((a) => a === true);
  const allGateAnswered = Object.values(gateAnswers).every((a) => a !== undefined);
  const locked = isLockedForToday();

  // Calculate session duration with auto-update
  const [sessionDuration, setSessionDuration] = useState(0);

  useEffect(() => {
    if (currentSession?.state === "live") {
      const interval = setInterval(() => {
        setSessionDuration(Math.floor((Date.now() - currentSession.startedAt) / 1000));
      }, 1000);
      return () => clearInterval(interval);
    } else {
      setSessionDuration(0);
    }
  }, [currentSession]);

  const minutes = Math.floor(sessionDuration / 60);
  const seconds = sessionDuration % 60;

  if (currentSession?.state === "live") {
    // Live Mode View
    return (
      <div className="min-h-screen bg-background p-6">
        {/* Status Bar */}
        <Card className="mb-6 sticky top-0 z-10">
          <CardContent className="p-4">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div className="flex items-center gap-4">
                <Badge className="bg-destructive">LIVE</Badge>
                <span className="text-sm">Bias: {currentSession.intent}</span>
                <span className="text-sm">Emotion: {currentSession.emotionStart}</span>
                <span className="text-sm">Script: {currentSession.variantUsed}</span>
              </div>
              <div className="text-sm font-mono">
                {String(minutes).padStart(2, "0")}:{String(seconds).padStart(2, "0")}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Main Actions */}
        <div className="max-w-2xl mx-auto space-y-4">
          <Button onClick={handleLogTrade} className="w-full" size="lg">
            Log Trade
          </Button>
          <Button
            onClick={() => setShowCheckIn(true)}
            variant="outline"
            className="w-full"
            size="lg"
          >
            Manual Check-In
          </Button>
          <Button
            onClick={handleStopTrading}
            variant="destructive"
            className="w-full"
            size="lg"
          >
            STOP TRADING
          </Button>
        </div>

        {/* Check-In Modal */}
        <Dialog open={showCheckIn} onOpenChange={setShowCheckIn}>
          <DialogContent>
            <h2 className="text-xl font-bold mb-4">Check-In</h2>
            <p className="mb-4">Was this trade part of the plan you confirmed?</p>
            <div className="flex gap-2">
              <Button
                onClick={() => handleCheckInSubmit(true)}
                className="flex-1"
                variant="default"
              >
                Yes
              </Button>
              <Button
                onClick={() => handleCheckInSubmit(false)}
                className="flex-1"
                variant="destructive"
              >
                No
              </Button>
            </div>
            {!currentSession?.violations.every((v) => v.type !== "off_plan_trade") && (
              <div className="mt-4 p-4 bg-warning/10 border border-warning rounded-lg">
                <p className="text-sm text-warning-foreground mb-2">
                  You've logged an off-plan trade. Consider playing the reset audio.
                </p>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    // Play after_loss script audio if available
                    const resetScript = getScriptByVariant("after_loss");
                    if (resetScript?.audioUrl && audioRef.current) {
                      audioRef.current.src = resetScript.audioUrl;
                      audioRef.current.play();
                    }
                  }}
                >
                  Play Reset Audio
                </Button>
              </div>
            )}
          </DialogContent>
        </Dialog>
      </div>
    );
  }

  // Live Hub View
  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-2xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Live Trading</h1>
          <p className="text-muted-foreground">Prepare, gate, and trade with discipline.</p>
        </div>

        {locked && (
          <Card className="border-destructive">
            <CardContent className="p-4">
              <div className="flex items-center gap-2 text-destructive">
                <AlertTriangle className="h-5 w-5" />
                <span>Trading is locked for today after using STOP TRADING.</span>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Stats Summary */}
        <Card>
          <CardContent className="p-6">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Plan Followed Streak</p>
                <p className="text-2xl font-bold">{appState.streaks.planFollowedDays} days</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Best Streak</p>
                <p className="text-2xl font-bold">{appState.streaks.bestPlanFollowedDays} days</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Start Button */}
        <Button
          onClick={handleStartTrading}
          disabled={locked}
          className="w-full"
          size="lg"
        >
          START TRADING
        </Button>

        {/* Gating Modal */}
        <Dialog open={showGating} onOpenChange={() => {}}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <Stepper
              currentStep={
                gatingStep === "script"
                  ? 1
                  : gatingStep === "intent"
                  ? 2
                  : gatingStep === "emotion"
                  ? 3
                  : gatingStep === "gate"
                  ? 4
                  : 5
              }
              totalSteps={5}
              steps={["Script", "Intent", "Emotion", "Gate", "Confirm"]}
            />

            {gatingStep === "script" && script && (
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium block mb-2">Script Variant</label>
                  <select
                    value={selectedVariant}
                    onChange={(e) => setSelectedVariant(e.target.value as ScriptVariant)}
                    className="w-full p-2 border rounded"
                  >
                    <option value="pre_market">Pre-Market</option>
                    <option value="after_loss">After Loss</option>
                    <option value="fomo_overtrade">FOMO/Overtrade</option>
                    <option value="confidence">Confidence</option>
                  </select>
                </div>

                <div>
                  <h3 className="font-semibold mb-2">{script.title}</h3>
                  <div className="space-y-2">
                    {script.lines.map((line, idx) => (
                      <p key={idx} className="text-sm">
                        {line}
                      </p>
                    ))}
                  </div>
                </div>

                {script.audioUrl ? (
                  <div>
                    <audio ref={audioRef} src={script.audioUrl} />
                    <Button
                      onClick={() => {
                        if (audioRef.current) {
                          if (audioPlaying) {
                            audioRef.current.pause();
                            setAudioPlaying(false);
                          } else {
                            audioRef.current.play();
                            setAudioPlaying(true);
                          }
                        }
                      }}
                      variant="outline"
                    >
                      {audioPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                    </Button>
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">Audio coming soon</p>
                )}

                <div className="text-sm text-muted-foreground">
                  Time reading: {scriptReadTime}s / 20s
                </div>

                <Button
                  onClick={handleScriptContinue}
                  disabled={scriptReadTime < 20}
                  className="w-full"
                >
                  I read/listened
                </Button>
              </div>
            )}

            {gatingStep === "intent" && (
              <div className="space-y-4">
                <h3 className="font-semibold">What is your trading intent?</h3>
                <ChipSelect
                  options={[
                    { value: "longs", label: "Longs" },
                    { value: "shorts", label: "Shorts" },
                    { value: "waiting", label: "Waiting" },
                    { value: "not_sure", label: "Not Sure" },
                  ]}
                  value={selectedIntent}
                  onChange={(val) => setSelectedIntent(val as Intent)}
                />
                <Button
                  onClick={handleIntentContinue}
                  disabled={!selectedIntent}
                  className="w-full"
                >
                  Continue
                </Button>
              </div>
            )}

            {gatingStep === "emotion" && (
              <div className="space-y-4">
                <h3 className="font-semibold">What is your starting emotion?</h3>
                <ChipSelect
                  options={[
                    { value: "calm", label: "Calm" },
                    { value: "anxious", label: "Anxious" },
                    { value: "excited", label: "Excited" },
                    { value: "rushed", label: "Rushed" },
                    { value: "tilted", label: "Tilted" },
                  ]}
                  value={selectedEmotion}
                  onChange={(val) => setSelectedEmotion(val as Emotion)}
                />
                <Button
                  onClick={handleEmotionContinue}
                  disabled={!selectedEmotion}
                  className="w-full"
                >
                  Continue
                </Button>
              </div>
            )}

            {gatingStep === "gate" && (
              <div className="space-y-6">
                <h3 className="font-semibold">Plan Verification Gate</h3>
                <YesNoToggle
                  label="Is this one of your defined setups?"
                  value={gateAnswers.defined_setup}
                  onChange={(val) =>
                    setGateAnswers({ ...gateAnswers, defined_setup: val })
                  }
                />
                <YesNoToggle
                  label="Do you know exactly where you exit if wrong?"
                  value={gateAnswers.know_stop}
                  onChange={(val) => setGateAnswers({ ...gateAnswers, know_stop: val })}
                />
                <YesNoToggle
                  label="Are you okay with taking 0 trades today?"
                  value={gateAnswers.ok_no_trade}
                  onChange={(val) => setGateAnswers({ ...gateAnswers, ok_no_trade: val })}
                />

                {allGateAnswered && !gatePassed && (
                  <Card className="border-destructive bg-destructive/10">
                    <CardContent className="p-4">
                      <p className="font-semibold text-destructive mb-2">
                        Then this is not a valid trade.
                      </p>
                      <div className="space-y-2">
                        <Button
                          variant="outline"
                          className="w-full"
                          onClick={() => setGatingStep("script")}
                        >
                          Replay Script
                        </Button>
                        <Button variant="outline" className="w-full">
                          Switch to SIM
                        </Button>
                        <Button
                          variant="outline"
                          className="w-full"
                          onClick={() => {
                            // Log violation for gate failure
                            const violation: Violation = {
                              id: Date.now().toString(),
                              ts: Date.now(),
                              type: "gate_failed_trade_attempt",
                            };
                            const session: LiveSession = {
                              id: Date.now().toString(),
                              startedAt: Date.now(),
                              state: "completed",
                              variantUsed: selectedVariant,
                              intent: selectedIntent || "not_sure",
                              emotionStart: selectedEmotion || "calm",
                              gateAnswers: gateAnswers as Record<GateQuestion, boolean>,
                              gatePassed: false,
                              violations: [violation],
                              checkIns: [],
                            };
                            const state = loadAppState();
                            state.sessions.push(session);
                            saveAppState(state);
                            setAppState(state);
                            setShowGating(false);
                            setGateAnswers({
                              defined_setup: undefined,
                              know_stop: undefined,
                              ok_no_trade: undefined,
                            });
                          }}
                        >
                          Stay Flat
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                )}

                <Button
                  onClick={handleGateContinue}
                  disabled={!allGateAnswered || !gatePassed}
                  className="w-full"
                >
                  Continue
                </Button>
              </div>
            )}

            {gatingStep === "external_conscience" && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <p>This trade is either planned or emotional. There is no middle.</p>
                  <p>If it loses, you already agreed it's not the market's fault.</p>
                </div>
                <Button onClick={handleEnterLiveMode} className="w-full" size="lg">
                  ENTER LIVE MODE
                </Button>
              </div>
            )}
          </DialogContent>
        </Dialog>

        {/* Reflection Modal */}
        <Dialog open={showReflection} onOpenChange={setShowReflection}>
          <DialogContent>
            <h2 className="text-xl font-bold mb-4">Session Reflection</h2>
            <div className="space-y-4">
              <YesNoToggle
                label="Did you follow your plan?"
                value={reflectionData.followedPlan}
                onChange={(val) => setReflectionData({ ...reflectionData, followedPlan: val })}
              />
              <div>
                <label className="text-sm font-medium block mb-2">Emotion during session</label>
                <ChipSelect
                  options={[
                    { value: "calm", label: "Calm" },
                    { value: "anxious", label: "Anxious" },
                    { value: "excited", label: "Excited" },
                    { value: "rushed", label: "Rushed" },
                    { value: "tilted", label: "Tilted" },
                  ]}
                  value={reflectionData.emotionDuring}
                  onChange={(val) => setReflectionData({ ...reflectionData, emotionDuring: val as Emotion })}
                />
              </div>
              <div>
                <label className="text-sm font-medium block mb-2">Note (optional)</label>
                <Textarea
                  value={reflectionData.note || ""}
                  onChange={(e) => setReflectionData({ ...reflectionData, note: e.target.value })}
                  rows={3}
                />
              </div>
              <Button onClick={handleReflectionSubmit} className="w-full">
                Submit Reflection
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
}

