import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { useNotifications } from "@/contexts/NotificationContext";

const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";

function localDateString(d: Date): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

function parseEntryDate(entry: { date: string | Date }): string {
  if (entry.date instanceof Date) {
    return localDateString(entry.date);
  }
  return String(entry.date).slice(0, 10);
}

/**
 * Pushes in-app notifications: EOD P&L (from journal API), daily journal reminder time, and server EOD email status.
 */
export const InAppNotificationEffects = () => {
  const { pathname } = useLocation();
  const inAppShell = pathname === "/dashboard" || pathname === "/settings";
  const { user, preferences, isAuthenticated, isSubscribed } = useAuth();
  const { upsert } = useNotifications();
  const lastRemindFire = useRef<string | null>(null);
  const lastServerFire = useRef<string | null>(null);

  const userId = user?.id;

  // EOD P&L from journal entries (after 4:00 PM local) + refresh periodically
  useEffect(() => {
    if (!inAppShell) return;
    if (!isAuthenticated || !isSubscribed || !userId || !preferences?.notifyEodPnl) return;

    const run = async () => {
      const now = new Date();
      if (now.getHours() < 16) return; // "end of day" for display after 4pm local

      const today = localDateString(now);

      try {
        const res = await fetch(`${apiUrl}/api/journal/entries`);
        const data = await res.json();
        if (!res.ok || data.error) return;
        const entries = (data.entries || []) as Array<{
          date: string | Date;
          trades?: Array<{ pnl?: number }>;
        }>;
        let total = 0;
        let n = 0;
        for (const e of entries) {
          if (parseEntryDate(e) !== today) continue;
          for (const t of e.trades || []) {
            if (t.pnl != null && !Number.isNaN(Number(t.pnl))) {
              total += Number(t.pnl);
              n += 1;
            }
          }
        }
        const sign = total >= 0 ? "" : "-";
        const abs = Math.abs(total).toFixed(2);
        upsert({
          id: `eod-pnl-${today}`,
          type: "eod_pnl",
          title: "End of day P&L",
          body:
            n > 0
              ? `Today (${today}): ${sign}$${abs} across ${n} trade line(s) in your journal.`
              : `No trade lines logged for ${today} yet. Add entries in the Journal when you're done.`,
          createdAt: new Date().toISOString(),
          read: false,
        });
      } catch {
        /* ignore */
      }
    };

    void run();
    const id = window.setInterval(() => void run(), 5 * 60 * 1000);
    return () => window.clearInterval(id);
  }, [inAppShell, isAuthenticated, isSubscribed, userId, preferences?.notifyEodPnl, upsert]);

  // Journal reminder at user-configured time (local clock)
  useEffect(() => {
    if (!inAppShell) return;
    if (!isAuthenticated || !isSubscribed || !userId || !preferences?.notifyJournalReminder) return;
    const time = preferences.journalReminderTime || "17:00";
    const [hh, mm] = time.split(":").map((x) => parseInt(x, 10));

    const tick = () => {
      const now = new Date();
      if (now.getHours() !== hh || now.getMinutes() !== mm) return;
      const key = `journal-remind-${localDateString(now)}`;
      if (lastRemindFire.current === key) return;
      lastRemindFire.current = key;
      upsert({
        id: key,
        type: "journal_reminder",
        title: "Journal reminder",
        body: "Time to log today’s session — review your trades, mindset, and one takeaway.",
        createdAt: new Date().toISOString(),
        read: false,
      });
    };

    const id = window.setInterval(tick, 15 * 1000);
    tick();
    return () => window.clearInterval(id);
  }, [inAppShell, isAuthenticated, isSubscribed, userId, preferences?.notifyJournalReminder, preferences?.journalReminderTime, upsert]);

  // Server-side daily email status (if backend sends the 5pm email)
  useEffect(() => {
    if (!inAppShell) return;
    if (!isAuthenticated || !isSubscribed || !userId) return;

    const run = async () => {
      try {
        const res = await fetch(`${apiUrl}/api/journal/eod-email-status`);
        const s = await res.json();
        if (!res.ok) return;
        if (!s.enabled) return;
        const today = localDateString(new Date());
        if (s.lastSentDate !== today) return;
        const key = `server-eod-mail-${today}`;
        if (lastServerFire.current === key) return;
        lastServerFire.current = key;
        upsert({
          id: key,
          type: "server_email",
          title: "Daily journal email sent",
          body: s.lastResult
            ? `The server job reported: ${String(s.lastResult).slice(0, 200)}`
            : "The scheduled journal / P&L email job ran for today (see your inbox).",
          createdAt: s.lastSentAt || new Date().toISOString(),
          read: false,
        });
      } catch {
        /* ignore */
      }
    };

    void run();
    const id = window.setInterval(() => void run(), 10 * 60 * 1000);
    return () => window.clearInterval(id);
  }, [inAppShell, isAuthenticated, isSubscribed, userId, upsert]);

  return null;
};
