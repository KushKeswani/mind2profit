import { useEffect, useState } from "react";

// Futures/forex session times in UTC (example, adjust as needed)
const SESSIONS = [
  { name: "Sydney", start: 22, end: 6 },   // 10pm - 6am UTC
  { name: "Tokyo", start: 0, end: 9 },    // 12am - 9am UTC
  { name: "London", start: 7, end: 16 },  // 7am - 4pm UTC
  { name: "New York", start: 13, end: 22 } // 1pm - 10pm UTC
];

function getCurrentSession(date = new Date()) {
  const hour = date.getUTCHours();
  for (const session of SESSIONS) {
    if (session.start < session.end) {
      if (hour >= session.start && hour < session.end) return session;
    } else {
      // Overnight session (e.g., Sydney)
      if (hour >= session.start || hour < session.end) return session;
    }
  }
  return null;
}

function getNextSession(date = new Date()) {
  const hour = date.getUTCHours();
  let minDiff = 24;
  let next = SESSIONS[0];
  for (const session of SESSIONS) {
    let diff = (session.start - hour + 24) % 24;
    if (diff > 0 && diff < minDiff) {
      minDiff = diff;
      next = session;
    }
  }
  return next;
}

function getCountdownToSession(session, date = new Date()) {
  const now = date;
  let target = new Date(now);
  target.setUTCHours(session.start, 0, 0, 0);
  if (target <= now) target.setUTCDate(target.getUTCDate() + 1);
  const diff = target.getTime() - now.getTime();
  const hours = Math.floor(diff / 1000 / 60 / 60);
  const minutes = Math.floor((diff / 1000 / 60) % 60);
  const seconds = Math.floor((diff / 1000) % 60);
  return { hours, minutes, seconds };
}

export function SessionClock() {
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);
  const current = getCurrentSession(now);
  const next = getNextSession(now);
  const countdown = getCountdownToSession(next, now);
  return (
    <div className="flex flex-col items-start gap-1">
      <span className="text-xs text-muted-foreground">Current Session:</span>
      <span className="font-semibold text-primary">
        {current ? current.name : "No Active Session"}
      </span>
      <span className="text-xs text-muted-foreground mt-1">Next: {next.name} in</span>
      <span className="font-mono text-lg">
        {countdown.hours.toString().padStart(2, "0")}:
        {countdown.minutes.toString().padStart(2, "0")}:
        {countdown.seconds.toString().padStart(2, "0")}
      </span>
    </div>
  );
}
