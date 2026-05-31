import { useCallback, useEffect, useMemo, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import {
  addDays,
  addMonths,
  addWeeks,
  endOfMonth,
  endOfWeek,
  eachDayOfInterval,
  format,
  getISOWeek,
  isBefore,
  isSameMonth,
  isToday,
  startOfDay,
  startOfMonth,
  startOfWeek,
} from "date-fns";
import {
  ChevronLeft,
  ChevronRight,
  AlertTriangle,
  Clock,
  BarChart3,
} from "lucide-react";

const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";

const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

type Impact = "low" | "medium" | "high";

export interface EconEvent {
  id: string;
  title: string;
  dateIso: string;
  time?: string;
  impact: Impact;
  currency?: string;
  country?: string;
  actual?: string | null;
  forecast?: string | null;
  previous?: string | null;
  category?: string;
}

function normalizeImpact(v: string | undefined): Impact {
  const s = String(v || "medium").toLowerCase();
  if (s === "high" || s === "2" || s === "3") return "high";
  if (s === "medium" || s === "1") return "medium";
  return "low";
}

function eventIsPast(d: string): boolean {
  return isBefore(startOfDay(new Date(d + "T12:00:00")), startOfDay(new Date()));
}

function buildRange(mode: "month" | "week" | "day", cursor: Date): { from: string; to: string } {
  if (mode === "month") {
    const a = startOfMonth(cursor);
    const b = endOfMonth(cursor);
    return { from: format(a, "yyyy-MM-dd"), to: format(b, "yyyy-MM-dd") };
  }
  if (mode === "week") {
    const a = startOfWeek(cursor, { weekStartsOn: 1 });
    const b = endOfWeek(cursor, { weekStartsOn: 1 });
    return { from: format(a, "yyyy-MM-dd"), to: format(b, "yyyy-MM-dd") };
  }
  const d = format(startOfDay(cursor), "yyyy-MM-dd");
  return { from: d, to: d };
}

function impactStyle(impact: Impact) {
  switch (impact) {
    case "high":
      return {
        dot: "bg-destructive",
        badge: "bg-destructive text-destructive-foreground border-0",
        label: "High",
      };
    case "medium":
      return {
        dot: "bg-amber-500",
        badge: "bg-amber-500/90 text-amber-950 border-0",
        label: "Med",
      };
    default:
      return {
        dot: "bg-muted-foreground/50",
        badge: "bg-muted text-muted-foreground border border-border",
        label: "Low",
      };
  }
}

const ImpactIcon = ({ impact }: { impact: Impact }) => {
  switch (impact) {
    case "high":
      return <AlertTriangle className="h-3.5 w-3.5" aria-hidden />;
    case "medium":
      return <Clock className="h-3.5 w-3.5" aria-hidden />;
    default:
      return <BarChart3 className="h-3.5 w-3.5 opacity-60" aria-hidden />;
  }
};

export const CalendarModule = () => {
  const [mode, setMode] = useState<"month" | "week" | "day">("month");
  const [cursor, setCursor] = useState(() => new Date());
  const [events, setEvents] = useState<EconEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [source, setSource] = useState<string | null>(null);

  const range = useMemo(() => buildRange(mode, cursor), [mode, cursor]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setErr(null);
    const q = new URLSearchParams({ from: range.from, to: range.to });
    fetch(`${apiBase}/api/economic-calendar/range?${q.toString()}`)
      .then((r) => r.json())
      .then((data) => {
        if (cancelled) return;
        if (data.error && (!data.events || !Array.isArray(data.events) || data.events.length === 0)) {
          setErr(data.error);
          setEvents([]);
        } else {
          setErr(null);
          const list = (data.events || []) as EconEvent[];
          setSource(data.source || null);
          setEvents(
            list.map((e) => ({
              ...e,
              id: e.id + "",
              dateIso: e.dateIso || (e as { date?: string }).date || range.from,
              impact: normalizeImpact((e as { impact?: string }).impact),
            }))
          );
        }
        setLoading(false);
      })
      .catch(() => {
        if (!cancelled) {
          setErr("Could not load calendar.");
          setEvents([]);
          setLoading(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [range.from, range.to]);

  const byDate = useMemo(() => {
    const m: Record<string, EconEvent[]> = {};
    for (const e of events) {
      const d = (e.dateIso || "").slice(0, 10);
      if (!d) continue;
      if (!m[d]) m[d] = [];
      m[d].push(e);
    }
    for (const d of Object.keys(m)) {
      m[d].sort((a, b) => (a.time || "").localeCompare(b.time || ""));
    }
    return m;
  }, [events]);

  const navPrev = useCallback(() => {
    if (mode === "month") setCursor((c) => addMonths(c, -1));
    else if (mode === "week") setCursor((c) => addWeeks(c, -1));
    else setCursor((c) => addDays(c, -1));
  }, [mode]);

  const navNext = useCallback(() => {
    if (mode === "month") setCursor((c) => addMonths(c, 1));
    else if (mode === "week") setCursor((c) => addWeeks(c, 1));
    else setCursor((c) => addDays(c, 1));
  }, [mode]);

  const monthStart = startOfMonth(cursor);
  const monthEnd = endOfMonth(cursor);
  const gridFrom = startOfWeek(monthStart, { weekStartsOn: 1 });
  const gridTo = endOfWeek(monthEnd, { weekStartsOn: 1 });
  const monthDays = eachDayOfInterval({ start: gridFrom, end: gridTo });

  const weekDays = useMemo(
    () =>
      eachDayOfInterval({
        start: startOfWeek(cursor, { weekStartsOn: 1 }),
        end: endOfWeek(cursor, { weekStartsOn: 1 }),
      }),
    [cursor]
  );

  const rangeTitle = useMemo(() => {
    if (mode === "month") return format(cursor, "MMMM yyyy");
    if (mode === "week") {
      const a = startOfWeek(cursor, { weekStartsOn: 1 });
      const b = endOfWeek(cursor, { weekStartsOn: 1 });
      return `${format(a, "MMM d")} – ${format(b, "MMM d, yyyy")}`;
    }
    return format(cursor, "EEEE, MMM d, yyyy");
  }, [mode, cursor]);

  const goToDay = (d: Date) => {
    setCursor(d);
    setMode("day");
  };

  const goToWeekOf = (d: Date) => {
    setCursor(d);
    setMode("week");
  };

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Economic calendar</h1>
          <p className="text-muted-foreground text-sm max-w-2xl">
            Browse US macro and scheduled releases. High (red), medium (orange), and low (grey) impact. For past
            days, <span className="text-foreground font-medium">Actual</span> is shown when the data source
            provides it. Add{" "}
            <code className="text-xs bg-muted px-1 py-0.5 rounded">TRADING_ECONOMICS_API_KEY</code> in the
            backend for a full time-based calendar; otherwise the Massive FRED window shows monthly releases
            in range.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {(["month", "week", "day"] as const).map((m) => (
            <Button
              key={m}
              variant={mode === m ? "default" : "outline"}
              size="sm"
              onClick={() => {
                if (m === "week" && mode !== "week") {
                  setCursor((c) => startOfWeek(c, { weekStartsOn: 1 }));
                }
                if (m === "day" && mode !== "day") {
                  setCursor((c) => startOfDay(c));
                }
                if (m === "month" && mode !== "month") {
                  setCursor((c) => startOfMonth(c));
                }
                setMode(m);
              }}
            >
              {m === "month" ? "Month" : m === "week" ? "Week" : "Day"}
            </Button>
          ))}
        </div>
      </div>

      <Card className="p-3 sm:p-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-border/60 pb-3 mb-4">
          <div className="flex items-center gap-1">
            <Button variant="ghost" size="icon" onClick={navPrev} aria-label="Previous">
              <ChevronLeft className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" onClick={navNext} aria-label="Next">
              <ChevronRight className="h-5 w-5" />
            </Button>
            <h2 className="text-lg font-semibold pl-1">{rangeTitle}</h2>
          </div>
          <div className="text-xs text-muted-foreground">
            {loading && "Loading… "}
            {err && <span className="text-destructive">{err}</span>}
            {!err && !loading && source && (
              <span>
                Source: {source}
                {range.from !== range.to
                  ? ` · ${format(new Date(range.from + "T12:00:00"), "MMM d")} – ${format(new Date(range.to + "T12:00:00"), "MMM d")}`
                  : ` · ${format(new Date(range.from + "T12:00:00"), "MMM d")}`}
              </span>
            )}
          </div>
        </div>

        {mode === "month" && (
          <div>
            <div className="grid grid-cols-[2.5rem_repeat(7,minmax(0,1fr))] gap-px sm:gap-0 text-center text-xs font-medium text-muted-foreground mb-1">
              <span className="hidden sm:block" />
              {WEEKDAYS.map((w) => (
                <div key={w} className="py-1">
                  {w}
                </div>
              ))}
            </div>
            {Array.from({ length: Math.ceil(monthDays.length / 7) }, (_, w) => {
              const slice = monthDays.slice(w * 7, w * 7 + 7);
              if (slice.length === 0) return null;
              const wkNo = getISOWeek(slice[0]!);
              return (
                <div
                  key={w + slice[0]!.toISOString()}
                  className="grid grid-cols-[2.5rem_repeat(7,minmax(0,1fr))] border-t border-border/40 first:border-t-0"
                >
                  <button
                    type="button"
                    className="text-[10px] sm:text-xs text-muted-foreground hover:text-primary hover:underline p-1 flex items-center justify-center"
                    onClick={() => goToWeekOf(slice[0]!)}
                    title="Open this week"
                  >
                    <span className="hidden sm:inline">W{wkNo}</span>
                    <span className="sm:hidden">Wk</span>
                  </button>
                  {slice.map((day) => {
                    const key = format(day, "yyyy-MM-dd");
                    const dayEvs = byDate[key] || [];
                    const inM = isSameMonth(day, cursor);
                    return (
                      <div
                        key={key}
                        className={cn(
                          "min-h-[4.5rem] sm:min-h-[5.5rem] border-l border-border/30 p-1.5",
                          !inM && "bg-muted/30 opacity-60"
                        )}
                      >
                        <div className="flex items-center justify-between gap-1">
                          <button
                            type="button"
                            onClick={() => goToDay(day)}
                            className={cn(
                              "text-xs font-medium rounded-full w-6 h-6 flex items-center justify-center shrink-0",
                              isToday(day) && "bg-primary text-primary-foreground",
                              !isToday(day) && "hover:bg-muted"
                            )}
                          >
                            {format(day, "d")}
                          </button>
                        </div>
                        <div className="flex flex-wrap gap-0.5 mt-1" aria-hidden>
                          {(["high", "medium", "low"] as const).map((imp) => {
                            const n = dayEvs.filter((e) => e.impact === imp).length;
                            if (!n) return null;
                            const s = impactStyle(imp);
                            return (
                              <div key={imp} className="flex items-center gap-0.5" title={`${imp}: ${n}`}>
                                <span className={cn("h-1.5 w-1.5 rounded-full", s.dot)} />
                                {n > 1 && <span className="text-[9px] text-muted-foreground">{n}</span>}
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    );
                  })}
                </div>
              );
            })}
          </div>
        )}

        {mode === "week" && (
          <div className="grid grid-cols-1 sm:grid-cols-7 gap-2">
            {weekDays.map((d) => {
              const key = format(d, "yyyy-MM-dd");
              const list = byDate[key] || [];
              return (
                <div key={key} className="rounded-lg border border-border/60 p-2 flex flex-col min-h-[12rem]">
                  <button
                    type="button"
                    onClick={() => goToDay(d)}
                    className="text-left mb-2 pb-2 border-b border-border/40 w-full"
                  >
                    <div className="text-sm font-medium">{format(d, "EEE")}</div>
                    <div
                      className={cn(
                        "text-lg",
                        isToday(d) && "text-primary"
                      )}
                    >
                      {format(d, "MMM d")}
                    </div>
                  </button>
                  <ul className="space-y-1.5 text-xs flex-1 overflow-y-auto max-h-48">
                    {list.length === 0 && (
                      <li className="text-muted-foreground/70">—</li>
                    )}
                    {list.map((e) => {
                      const s = impactStyle(e.impact);
                      const past = eventIsPast(key);
                      return (
                        <li
                          key={e.id}
                          className="rounded border border-border/50 bg-card/50 p-1.5"
                        >
                          <div className="flex items-center gap-1">
                            <Badge className={cn("text-[9px] px-1 h-4", s.badge)}>
                              <span className="inline-flex items-center gap-0.5">
                                <ImpactIcon impact={e.impact} />
                                {s.label}
                              </span>
                            </Badge>
                            {e.time && e.time !== "00:00" && (
                              <span className="text-muted-foreground text-[9px]">{e.time}</span>
                            )}
                          </div>
                          <p className="font-medium leading-tight mt-0.5 line-clamp-2">{e.title}</p>
                          {past && e.actual != null && String(e.actual) !== "" && (
                            <p className="text-[10px] text-muted-foreground mt-0.5">
                              Actual: <span className="text-foreground">{String(e.actual)}</span>
                            </p>
                          )}
                          {!past && e.forecast != null && e.forecast !== "" && (
                            <p className="text-[10px] text-muted-foreground mt-0.5">
                              Fcst: {String(e.forecast)}
                            </p>
                          )}
                        </li>
                      );
                    })}
                  </ul>
                </div>
              );
            })}
          </div>
        )}

        {mode === "day" && (() => {
          const key = format(startOfDay(cursor), "yyyy-MM-dd");
          const list = byDate[key] || [];
          const past = eventIsPast(key);
          return (
            <div>
              {list.length === 0 && !loading && !err && (
                <p className="text-muted-foreground">No events for this day in the loaded window.</p>
              )}
              <ul className="space-y-3">
                {list.map((e) => {
                  const s = impactStyle(e.impact);
                  return (
                    <li
                      key={e.id}
                      className="rounded-lg border border-border/60 p-3 flex flex-col sm:flex-row sm:items-start gap-2"
                    >
                      <Badge className={cn("shrink-0", s.badge)}>
                        <span className="inline-flex items-center gap-1">
                          <ImpactIcon impact={e.impact} />
                          {s.label}
                        </span>
                      </Badge>
                      <div className="min-w-0 flex-1">
                        <h3 className="font-medium">{e.title}</h3>
                        {e.category && <p className="text-xs text-muted-foreground">{e.category}</p>}
                        {e.time && e.time !== "00:00" && (
                          <p className="text-sm text-muted-foreground mt-1">Release time: {e.time} (as reported)</p>
                        )}
                        <dl className="mt-2 grid grid-cols-1 sm:grid-cols-3 gap-2 text-sm">
                          {e.forecast != null && e.forecast !== "" && (
                            <div>
                              <dt className="text-xs text-muted-foreground">Forecast</dt>
                              <dd>{String(e.forecast)}</dd>
                            </div>
                          )}
                          <div>
                            <dt className="text-xs text-muted-foreground">Previous</dt>
                            <dd>{e.previous != null && e.previous !== "" ? String(e.previous) : "—"}</dd>
                          </div>
                          <div>
                            <dt className="text-xs text-muted-foreground">Actual {past && "(realized if released)"}</dt>
                            <dd
                              className={cn(
                                e.actual != null && String(e.actual) !== "" && "font-medium text-foreground"
                              )}
                            >
                              {e.actual != null && String(e.actual) !== "" ? String(e.actual) : "—"}
                            </dd>
                          </div>
                        </dl>
                      </div>
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })()}
      </Card>

      <p className="text-xs text-muted-foreground text-center sm:text-left">
        Tip: in <strong>Month</strong> view, click a <strong>week number</strong> to open the week, or a{" "}
        <strong>day</strong> for full detail. Use the Week / Day toggles to jump between views.
      </p>
    </div>
  );
};
