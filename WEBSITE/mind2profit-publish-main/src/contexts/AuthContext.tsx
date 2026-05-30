import React, { createContext, useContext, useEffect, useMemo, useState, ReactNode } from 'react';
import { supabase, isSupabaseConfigured } from "@/lib/supabase";

export interface UserPreferences {
  notifyEodPnl: boolean;
  notifyJournalReminder: boolean;
  /** Local wall-clock, HH:MM 24h */
  journalReminderTime: string;
  billingName: string;
  billingLine1: string;
  billingLine2: string;
  billingCity: string;
  billingRegion: string;
  billingPostal: string;
  billingCountry: string;
}

const defaultUserPreferences: UserPreferences = {
  notifyEodPnl: true,
  notifyJournalReminder: true,
  journalReminderTime: "17:00",
  billingName: "",
  billingLine1: "",
  billingLine2: "",
  billingCity: "",
  billingRegion: "",
  billingPostal: "",
  billingCountry: "US",
};

function mapMetadataToPreferences(m: Record<string, unknown> | null | undefined): UserPreferences {
  if (!m || typeof m !== "object") {
    return { ...defaultUserPreferences };
  }
  return {
    notifyEodPnl: m.notify_eod_pnl !== false,
    notifyJournalReminder: m.notify_journal_reminder !== false,
    journalReminderTime: typeof m.journal_reminder_time === "string" && m.journal_reminder_time
      ? (m.journal_reminder_time as string)
      : "17:00",
    billingName: typeof m.billing_contact_name === "string" ? m.billing_contact_name : "",
    billingLine1: typeof m.billing_line1 === "string" ? m.billing_line1 : "",
    billingLine2: typeof m.billing_line2 === "string" ? m.billing_line2 : "",
    billingCity: typeof m.billing_city === "string" ? m.billing_city : "",
    billingRegion: typeof m.billing_region === "string" ? m.billing_region : "",
    billingPostal: typeof m.billing_postal === "string" ? m.billing_postal : "",
    billingCountry: typeof m.billing_country === "string" && m.billing_country ? m.billing_country as string : "US",
  };
}

interface AuthContextType {
  isSubscribed: boolean;
  isAuthenticated: boolean;
  isLoading: boolean;
  plan: string;
  user: User | null;
  preferences: UserPreferences;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, fullName?: string) => Promise<void>;
  requestPasswordReset: (email: string) => Promise<void>;
  logout: () => void;
  upgrade: (plan: string) => Promise<void>;
  updateDisplayName: (name: string) => Promise<void>;
  updatePreferences: (next: Partial<UserPreferences>) => Promise<void>;
  updateBilling: (next: Pick<UserPreferences, "billingName" | "billingLine1" | "billingLine2" | "billingCity" | "billingRegion" | "billingPostal" | "billingCountry">) => Promise<void>;
}

export interface User {
  id: string;
  email: string;
  name: string;
  subscription: {
    plan: string;
    status: 'active' | 'trial' | 'expired';
    expiresAt: string;
  };
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const AUTH_STORAGE_KEY = "mind2profit_auth_v1";

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const initialState = useMemo(() => ({ user: null as User | null, isSubscribed: false, plan: "none" }), []);
  const [user, setUser] = useState<User | null>(initialState.user);
  const [isSubscribed, setIsSubscribed] = useState(initialState.isSubscribed);
  const [plan, setPlan] = useState(initialState.plan);
  const [isLoading, setIsLoading] = useState(true);
  const [preferences, setPreferences] = useState<UserPreferences>(defaultUserPreferences);

  const persistAuth = (nextUser: User | null, nextSubscribed: boolean, nextPlan: string) => {
    localStorage.setItem(
      AUTH_STORAGE_KEY,
      JSON.stringify({
        user: nextUser,
        isSubscribed: nextSubscribed,
        plan: nextPlan,
      })
    );
  };

  const hydrateFromSupabaseUser = (supabaseUser: any) => {
    const metadata = supabaseUser?.user_metadata || {};
    const paid = Boolean(metadata.paid);
    const currentPlan = (metadata.plan as string) || "none";
    const mappedUser: User = {
      id: supabaseUser.id,
      email: supabaseUser.email || "",
      name: metadata.full_name || supabaseUser.email?.split("@")[0] || "Trader",
      subscription: {
        plan: currentPlan,
        status: paid ? "active" : "expired",
        expiresAt: metadata.subscription_expires_at || new Date().toISOString(),
      },
    };
    setUser(mappedUser);
    setIsSubscribed(paid);
    setPlan(currentPlan);
    setPreferences(mapMetadataToPreferences(metadata as Record<string, unknown>));
    persistAuth(mappedUser, paid, currentPlan);
  };

  useEffect(() => {
    let isMounted = true;

    const finishLoading = () => {
      if (isMounted) setIsLoading(false);
    };

    const loadSession = async () => {
      if (!isSupabaseConfigured || !supabase) {
        // No Supabase client — do not trust localStorage as "signed in" (causes /signin redirect loops).
        setUser(null);
        setIsSubscribed(false);
        setPlan("none");
        setPreferences(defaultUserPreferences);
        finishLoading();
        return;
      }
      try {
        const { data } = await supabase.auth.getSession();
        if (!isMounted) return;
        if (data.session?.user) {
          hydrateFromSupabaseUser(data.session.user);
        } else {
          // Server has no session — clear stale client cache so public auth pages stay usable.
          setUser(null);
          setIsSubscribed(false);
          setPlan("none");
          setPreferences(defaultUserPreferences);
          localStorage.removeItem(AUTH_STORAGE_KEY);
        }
      } catch (e) {
        console.error("Auth session load failed:", e);
        setUser(null);
        setIsSubscribed(false);
        setPlan("none");
        setPreferences(defaultUserPreferences);
        localStorage.removeItem(AUTH_STORAGE_KEY);
      } finally {
        finishLoading();
      }
    };

    void loadSession();

    if (!isSupabaseConfigured || !supabase) {
      return () => {
        isMounted = false;
      };
    }

    const { data: authListener } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session?.user) {
        hydrateFromSupabaseUser(session.user);
      } else {
        setUser(null);
        setIsSubscribed(false);
        setPlan("none");
        setPreferences(defaultUserPreferences);
        localStorage.removeItem(AUTH_STORAGE_KEY);
      }
    });

    return () => {
      isMounted = false;
      authListener.subscription.unsubscribe();
    };
  }, []);

  const login = async (email: string, password: string) => {
    if (!supabase) {
      throw new Error("Sign-in is unavailable: set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
    }
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      throw error;
    }
    if (data.user) {
      hydrateFromSupabaseUser(data.user);
    }
  };

  const signup = async (email: string, password: string, fullName?: string) => {
    if (!supabase) {
      throw new Error("Sign-up is unavailable: set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
    }
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName || "",
          paid: false,
          plan: "none",
        },
      },
    });
    if (error) {
      throw error;
    }
  };

  const requestPasswordReset = async (email: string) => {
    if (!supabase) {
      throw new Error("Password reset is unavailable: set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
    }
    const redirectTo = `${window.location.origin}/signin`;
    const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo });
    if (error) {
      throw error;
    }
  };

  const logout = () => {
    void supabase?.auth.signOut();
    setUser(null);
    setIsSubscribed(false);
    setPlan("none");
    setPreferences(defaultUserPreferences);
    localStorage.removeItem(AUTH_STORAGE_KEY);
  };

  const updateDisplayName = async (name: string) => {
    if (!supabase) {
      throw new Error("Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
    }
    const { data, error } = await supabase.auth.updateUser({ data: { full_name: name } });
    if (error) throw error;
    if (data.user) {
      hydrateFromSupabaseUser(data.user);
    }
  };

  const updatePreferences = async (next: Partial<UserPreferences>) => {
    if (!supabase) {
      throw new Error("Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
    }
    const merged: UserPreferences = { ...preferences, ...next };
    const { data, error } = await supabase.auth.updateUser({
      data: {
        notify_eod_pnl: merged.notifyEodPnl,
        notify_journal_reminder: merged.notifyJournalReminder,
        journal_reminder_time: merged.journalReminderTime,
      },
    });
    if (error) {
      throw error;
    }
    if (data.user) {
      hydrateFromSupabaseUser(data.user);
    }
  };

  const updateBilling = async (next: Pick<UserPreferences, "billingName" | "billingLine1" | "billingLine2" | "billingCity" | "billingRegion" | "billingPostal" | "billingCountry">) => {
    if (!supabase) {
      throw new Error("Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
    }
    const merged: UserPreferences = { ...preferences, ...next };
    const { data, error } = await supabase.auth.updateUser({
      data: {
        billing_contact_name: merged.billingName,
        billing_line1: merged.billingLine1,
        billing_line2: merged.billingLine2,
        billing_city: merged.billingCity,
        billing_region: merged.billingRegion,
        billing_postal: merged.billingPostal,
        billing_country: merged.billingCountry,
      },
    });
    if (error) {
      throw error;
    }
    if (data.user) {
      hydrateFromSupabaseUser(data.user);
    }
  };

  const upgrade = async (plan: string) => {
    if (user) {
      if (!supabase) {
        throw new Error("Upgrade is unavailable: set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
      }
      const subscriptionExpiry = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString();
      const { data, error } = await supabase.auth.updateUser({
        data: {
          paid: true,
          plan,
          subscription_expires_at: subscriptionExpiry,
        },
      });
      if (error) {
        throw error;
      }
      if (data.user) {
        hydrateFromSupabaseUser(data.user);
      }
    }
  };

  const value: AuthContextType = {
    isSubscribed,
    isAuthenticated: Boolean(user),
    isLoading,
    plan,
    user,
    preferences,
    login,
    signup,
    requestPasswordReset,
    logout,
    upgrade,
    updateDisplayName,
    updatePreferences,
    updateBilling,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
