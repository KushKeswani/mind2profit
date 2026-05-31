import type { AppState, Script, LiveSession, Streaks, ScriptVariant } from "./types";

const STORAGE_KEY = "psych_app_state_v1";

const defaultStreaks: Streaks = {
  planFollowedDays: 0,
  noRevengeDays: 0,
  acceptedNoTradeDays: 0,
  bestPlanFollowedDays: 0,
};

const defaultState: AppState = {
  scripts: [],
  sessions: [],
  streaks: defaultStreaks,
};

export function loadAppState(): AppState {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) {
      return defaultState;
    }
    const parsed = JSON.parse(stored);
    // Ensure all required fields exist
    return {
      scripts: parsed.scripts || [],
      sessions: parsed.sessions || [],
      currentSessionId: parsed.currentSessionId,
      streaks: parsed.streaks || defaultStreaks,
      lockedUntil: parsed.lockedUntil,
    };
  } catch (error) {
    console.error("Failed to load app state:", error);
    return defaultState;
  }
}

export function saveAppState(state: AppState): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    console.error("Failed to save app state:", error);
  }
}

export function resetAppData(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.error("Failed to reset app data:", error);
  }
}

export function isLockedForToday(): boolean {
  const state = loadAppState();
  if (!state.lockedUntil) {
    return false;
  }
  const lockedDate = new Date(state.lockedUntil);
  const today = new Date();
  today.setHours(23, 59, 59, 999);
  return lockedDate > today;
}

export function setLockedUntilEndOfDay(): void {
  const state = loadAppState();
  const today = new Date();
  today.setHours(23, 59, 59, 999);
  state.lockedUntil = today.toISOString();
  saveAppState(state);
}

export function getCurrentSession(): LiveSession | undefined {
  const state = loadAppState();
  if (!state.currentSessionId) {
    return undefined;
  }
  return state.sessions.find((s) => s.id === state.currentSessionId);
}

export function updateSession(session: LiveSession): void {
  const state = loadAppState();
  const index = state.sessions.findIndex((s) => s.id === session.id);
  if (index >= 0) {
    state.sessions[index] = session;
  } else {
    state.sessions.push(session);
  }
  saveAppState(state);
}

export function getScriptByVariant(variant: ScriptVariant): Script | undefined {
  const state = loadAppState();
  return state.scripts.find((s) => s.variant === variant);
}

