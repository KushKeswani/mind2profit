import { useMemo, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, DollarSign, Activity, Target, Brain } from "lucide-react";
import { SessionClock } from "@/components/ui/session-clock";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type MockTrade = {
  id: string;
  date: string;
  symbol: "NQ" | "ES" | "CL" | "GC";
  side: "buy" | "sell";
  pnl: number;
  risk: number;
  quantity: number;
};

type PeriodFilter = "all" | "week1" | "week2" | "week3" | "week4";
type ChartMetric = "cumulativePnl" | "dailyPnl" | "winRate" | "tradeCount";

const symbols: Array<MockTrade["symbol"]> = ["NQ", "ES", "CL", "GC"];

const createAprilTrades = (): MockTrade[] => {
  const trades: MockTrade[] = [];
  for (let day = 1; day <= 30; day += 1) {
    const dailyTradeCount = (day % 3) + 2;
    for (let i = 0; i < dailyTradeCount; i += 1) {
      const symbol = symbols[(day + i) % symbols.length];
      const risk = 90 + ((day * 7 + i * 11) % 70);
      const rr = ((day + i) % 6) / 2 - 1;
      const pnl = Math.round(risk * rr);
      trades.push({
        id: `apr-${day}-${i}`,
        date: `2026-04-${String(day).padStart(2, "0")}`,
        symbol,
        side: (day + i) % 2 === 0 ? "buy" : "sell",
        pnl,
        risk,
        quantity: ((day + i) % 4) + 1,
      });
    }
  }
  return trades;
};

const aprilTrades = createAprilTrades();

export const DashboardModule = () => {
  const [periodFilter, setPeriodFilter] = useState<PeriodFilter>("all");
  const [chartMetric, setChartMetric] = useState<ChartMetric>("cumulativePnl");

  const filteredTrades = useMemo(() => {
    const dayInRange = (date: string): boolean => {
      const day = Number(date.split("-")[2]);
      if (periodFilter === "week1") return day <= 7;
      if (periodFilter === "week2") return day >= 8 && day <= 14;
      if (periodFilter === "week3") return day >= 15 && day <= 21;
      if (periodFilter === "week4") return day >= 22;
      return true;
    };

    return aprilTrades.filter((trade) => dayInRange(trade.date));
  }, [periodFilter]);

  const stats = useMemo(() => {
    const wins = filteredTrades.filter((trade) => trade.pnl > 0);
    const losses = filteredTrades.filter((trade) => trade.pnl <= 0);
    const totalPnl = filteredTrades.reduce((sum, trade) => sum + trade.pnl, 0);
    const grossProfit = wins.reduce((sum, trade) => sum + trade.pnl, 0);
    const grossLoss = Math.abs(losses.reduce((sum, trade) => sum + trade.pnl, 0));
    const winRate = filteredTrades.length ? (wins.length / filteredTrades.length) * 100 : 0;
    const avgWin = wins.length ? grossProfit / wins.length : 0;
    const avgLoss = losses.length ? grossLoss / losses.length : 0;
    const profitFactor = grossLoss > 0 ? grossProfit / grossLoss : grossProfit;
    const expectancy = filteredTrades.length ? totalPnl / filteredTrades.length : 0;
    const avgRiskMultiple =
      filteredTrades.length > 0
        ? filteredTrades.reduce((sum, trade) => sum + trade.pnl / trade.risk, 0) / filteredTrades.length
        : 0;

    let runningPnl = 0;
    let peakPnl = 0;
    let maxDrawdown = 0;
    filteredTrades.forEach((trade) => {
      runningPnl += trade.pnl;
      peakPnl = Math.max(peakPnl, runningPnl);
      maxDrawdown = Math.max(maxDrawdown, peakPnl - runningPnl);
    });

    return {
      totalPnl,
      winRate,
      tradeCount: filteredTrades.length,
      avgWin,
      avgLoss,
      profitFactor,
      expectancy,
      avgRiskMultiple,
      maxDrawdown,
    };
  }, [filteredTrades]);

  const dailySeries = useMemo(() => {
    const dayMap = new Map<
      string,
      { date: string; dayLabel: string; dailyPnl: number; wins: number; losses: number; tradeCount: number }
    >();
    filteredTrades.forEach((trade) => {
      if (!dayMap.has(trade.date)) {
        dayMap.set(trade.date, {
          date: trade.date,
          dayLabel: trade.date.slice(8),
          dailyPnl: 0,
          wins: 0,
          losses: 0,
          tradeCount: 0,
        });
      }
      const item = dayMap.get(trade.date)!;
      item.dailyPnl += trade.pnl;
      item.tradeCount += 1;
      if (trade.pnl > 0) item.wins += 1;
      else item.losses += 1;
    });

    let cumulative = 0;
    return [...dayMap.values()]
      .sort((a, b) => a.date.localeCompare(b.date))
      .map((item) => {
        cumulative += item.dailyPnl;
        return {
          ...item,
          cumulativePnl: cumulative,
          winRate: item.tradeCount ? (item.wins / item.tradeCount) * 100 : 0,
        };
      });
  }, [filteredTrades]);

  const symbolBreakdown = useMemo(() => {
    const map = new Map<string, { name: string; pnl: number; trades: number }>();
    filteredTrades.forEach((trade) => {
      if (!map.has(trade.symbol)) {
        map.set(trade.symbol, { name: trade.symbol, pnl: 0, trades: 0 });
      }
      const item = map.get(trade.symbol)!;
      item.pnl += trade.pnl;
      item.trades += 1;
    });
    return [...map.values()];
  }, [filteredTrades]);

  const winLossData = useMemo(
    () => [
      { name: "Wins", value: filteredTrades.filter((t) => t.pnl > 0).length },
      { name: "Losses", value: filteredTrades.filter((t) => t.pnl <= 0).length },
    ],
    [filteredTrades]
  );

  const chartDataKey: ChartMetric = chartMetric;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground">April performance simulation for product demos and UI testing.</p>
        </div>
        <div className="flex flex-col md:items-end gap-1">
          <Badge className="bg-success text-success-foreground mb-1 md:mb-0">
            Data Mode: Mock April 2026
          </Badge>
          <SessionClock />
        </div>
      </div>

      <Card className="p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label className="text-xs text-muted-foreground">Period</label>
            <select
              value={periodFilter}
              onChange={(event) => setPeriodFilter(event.target.value as PeriodFilter)}
              className="mt-1 w-full rounded-md border border-border bg-background p-2 text-sm"
            >
              <option value="all">Full April</option>
              <option value="week1">Week 1 (Apr 1-7)</option>
              <option value="week2">Week 2 (Apr 8-14)</option>
              <option value="week3">Week 3 (Apr 15-21)</option>
              <option value="week4">Week 4+ (Apr 22-30)</option>
            </select>
          </div>
          <div>
            <label className="text-xs text-muted-foreground">Primary Chart Metric</label>
            <select
              value={chartMetric}
              onChange={(event) => setChartMetric(event.target.value as ChartMetric)}
              className="mt-1 w-full rounded-md border border-border bg-background p-2 text-sm"
            >
              <option value="cumulativePnl">Cumulative P&L</option>
              <option value="dailyPnl">Daily P&L</option>
              <option value="winRate">Daily Win Rate %</option>
              <option value="tradeCount">Trades Per Day</option>
            </select>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="p-6 bg-gradient-secondary shadow-soft">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total P&L</p>
              <p className={`text-2xl font-bold ${stats.totalPnl >= 0 ? "text-profit" : "text-loss"}`}>
                {stats.totalPnl >= 0 ? "+" : ""}${stats.totalPnl.toLocaleString()}
              </p>
              <p className="text-xs text-success flex items-center mt-1">
                <TrendingUp className="h-3 w-3 mr-1" />
                Profit Factor {stats.profitFactor.toFixed(2)}
              </p>
            </div>
            <DollarSign className="h-8 w-8 text-profit" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary shadow-soft">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Win Rate</p>
              <p className="text-2xl font-bold text-foreground">{stats.winRate.toFixed(1)}%</p>
              <p className="text-xs text-success flex items-center mt-1">
                <TrendingUp className="h-3 w-3 mr-1" />
                Avg Win ${stats.avgWin.toFixed(0)}
              </p>
            </div>
            <Target className="h-8 w-8 text-primary" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary shadow-soft">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total Trades</p>
              <p className="text-2xl font-bold text-foreground">{stats.tradeCount}</p>
              <p className="text-xs text-neutral flex items-center mt-1">
                <Activity className="h-3 w-3 mr-1" />
                Expectancy ${stats.expectancy.toFixed(0)}
              </p>
            </div>
            <Activity className="h-8 w-8 text-primary" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary shadow-soft">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Risk & Discipline</p>
              <p className="text-2xl font-bold text-foreground">{stats.avgRiskMultiple.toFixed(2)}R</p>
              <p className="text-xs text-success flex items-center mt-1">
                <Brain className="h-3 w-3 mr-1" />
                Max Drawdown ${stats.maxDrawdown.toFixed(0)}
              </p>
            </div>
            <Brain className="h-8 w-8 text-primary" />
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Performance Trend</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dailySeries}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="dayLabel" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey={chartDataKey}
                  name={chartMetric}
                  stroke="#3b82f6"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Daily P&L Breakdown</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dailySeries}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="dayLabel" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="dailyPnl" name="Daily P&L">
                  {dailySeries.map((entry) => (
                    <Cell key={entry.date} fill={entry.dailyPnl >= 0 ? "#10b981" : "#ef4444"} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Win vs Loss Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={winLossData} dataKey="value" nameKey="name" outerRadius={90} label>
                  <Cell fill="#10b981" />
                  <Cell fill="#ef4444" />
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Symbol Allocation</h3>
          <div className="space-y-3">
            {symbolBreakdown.map((item) => (
              <div key={item.name} className="flex items-center justify-between rounded-lg bg-muted p-3">
                <div className="flex items-center gap-2">
                  <Badge variant="outline">{item.name}</Badge>
                  <span className="text-sm text-muted-foreground">{item.trades} trades</span>
                </div>
                <span className={`font-semibold ${item.pnl >= 0 ? "text-profit" : "text-loss"}`}>
                  {item.pnl >= 0 ? "+" : ""}${item.pnl.toLocaleString()}
                </span>
              </div>
            ))}
            <div className="mt-3 rounded-lg border border-border p-3 text-sm text-muted-foreground">
              Avg Loss ${stats.avgLoss.toFixed(0)} · Max Drawdown ${stats.maxDrawdown.toFixed(0)}
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};