export type ScriptVariant = "pre_market" | "after_loss" | "fomo_overtrade" | "confidence";

export type Emotion = "calm" | "anxious" | "excited" | "rushed" | "tilted";

export type Intent = "longs" | "shorts" | "waiting" | "not_sure";

export type GateQuestion = "defined_setup" | "know_stop" | "ok_no_trade";

export type SessionState = "idle" | "gating" | "live" | "stopped" | "completed";

export interface Script {
  id: string;
  variant: ScriptVariant;
  title: string;
  lines: string[];
  audioUrl?: string;
}

export interface Violation {
  id: string;
  ts: number;
  type: "gate_failed_trade_attempt" | "off_plan_trade" | "overtrade" | "revenge" | "ignored_stop_button";
  note?: string;
}

export interface CheckIn {
  id: string;
  ts: number;
  question: "was_this_planned";
  answer: boolean;
}

export interface Reflection {
  ts: number;
  followedPlan: boolean;
  emotionDuring: Emotion;
  note?: string;
}

export interface LiveSession {
  id: string;
  startedAt: number;
  endedAt?: number;
  state: SessionState;
  variantUsed: ScriptVariant;
  intent: Intent;
  emotionStart: Emotion;
  gateAnswers: Record<GateQuestion, boolean>;
  gatePassed: boolean;
  violations: Violation[];
  checkIns: CheckIn[];
  reflection?: Reflection;
}

export interface Streaks {
  planFollowedDays: number;
  noRevengeDays: number;
  acceptedNoTradeDays: number;
  bestPlanFollowedDays: number;
}

export interface AppState {
  scripts: Script[];
  sessions: LiveSession[];
  currentSessionId?: string;
  streaks: Streaks;
  lockedUntil?: string; // ISO date string for end of day lockout
}


