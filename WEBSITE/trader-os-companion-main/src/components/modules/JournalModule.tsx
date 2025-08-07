import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Upload, Calendar, TrendingUp, TrendingDown, FileText, Camera, BarChart2, PercentCircle, TrendingUp as TrendingUpIcon } from "lucide-react";
import { ChartContainer, ChartTooltip, ChartLegend } from "@/components/ui/chart";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip as RechartsTooltip,
  CartesianGrid,
} from 'recharts';

interface SingleTrade {
  symbol: string;
  type: "buy" | "sell";
  entry: number | undefined;
  exit: number | undefined;
  pnl: number | undefined;
  riskReward: string;
  time?: string;
}

interface TradeEntry {
  id: string;
  date: Date;
  trades: SingleTrade[];
  reflection: string;
  tags: string[];
  good?: string;
  bad?: string;
  ugly?: string;
  goals?: string;
}

export const JournalModule = () => {
  const [entries, setEntries] = useState<TradeEntry[]>([
    {
      id: "1",
      date: new Date("2024-01-15"),
      trades: [
        {
          symbol: "EURUSD",
          type: "buy",
          entry: 1.0850,
          exit: 1.0920,
          pnl: 350,
          riskReward: "1:2.5",
        }
      ],
      reflection: "Perfect entry at support level. Followed the trading plan exactly. Market showed strong bullish momentum after London open.",
      tags: ["support", "london-open", "trend-following"]
    },
    {
      id: "2",
      date: new Date("2024-01-14"),
      trades: [
        {
          symbol: "GBPJPY",
          type: "sell",
          entry: 185.40,
          exit: 184.95,
          pnl: -120,
          riskReward: "1:2",
        }
      ],
      reflection: "Stop loss hit due to unexpected news release. Should have checked economic calendar before entering.",
      tags: ["news-impact", "stop-loss", "lesson-learned"]
    }
  ]);

  const [showAddEntry, setShowAddEntry] = useState(false);
  const [newEntry, setNewEntry] = useState<
    Omit<Partial<TradeEntry>, 'date' | 'trades'> & { date: string; trades: SingleTrade[] }
  >({
    trades: [
      { symbol: '', type: 'buy', entry: undefined, exit: undefined, pnl: undefined, riskReward: '', time: '' }
    ],
    reflection: '',
    tags: [],
    date: '',
    good: '',
    bad: '',
    ugly: '',
    goals: '',
  });

  const handleInputChange = (field: keyof TradeEntry, value: any) => {
    setNewEntry((prev) => ({ ...prev, [field]: value }));
  };

  const handleTradeChange = (idx: number, field: keyof SingleTrade, value: any) => {
    setNewEntry((prev) => ({
      ...prev,
      trades: prev.trades.map((trade, i) =>
        i === idx ? { ...trade, [field]: value } : trade
      ),
    }));
  };

  const addTrade = () => {
    setNewEntry((prev) => ({
      ...prev,
      trades: [
        ...prev.trades,
        { symbol: '', type: 'buy', entry: undefined, exit: undefined, pnl: undefined, riskReward: '', time: '' },
      ],
    }));
  };

  const removeTrade = (idx: number) => {
    setNewEntry((prev) => ({
      ...prev,
      trades: prev.trades.length > 1 ? prev.trades.filter((_, i) => i !== idx) : prev.trades,
    }));
  };

  const handleSaveEntry = () => {
    if (
      newEntry.trades.every(t => t.symbol && t.type && t.entry !== undefined && t.exit !== undefined && t.pnl !== undefined && t.riskReward) &&
      newEntry.reflection &&
      newEntry.date
    ) {
      setEntries([
        ...entries,
        {
          id: Date.now().toString(),
          trades: newEntry.trades.map(t => ({
            symbol: t.symbol,
            type: t.type,
            entry: Number(t.entry),
            exit: Number(t.exit),
            pnl: Number(t.pnl),
            riskReward: t.riskReward,
            time: t.time || '',
          })),
          reflection: newEntry.reflection,
          tags: newEntry.tags || [],
          date: new Date(newEntry.date),
          good: newEntry.good,
          bad: newEntry.bad,
          ugly: newEntry.ugly,
          goals: newEntry.goals,
        },
      ]);
      setNewEntry({
        trades: [
          { symbol: '', type: 'buy', entry: undefined, exit: undefined, pnl: undefined, riskReward: '', time: '' }
        ],
        reflection: '',
        tags: [],
        date: '',
        good: '',
        bad: '',
        ugly: '',
        goals: '',
      });
      setShowAddEntry(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Trade Journal</h1>
          <p className="text-muted-foreground">Reflect, learn, and improve your trading</p>
        </div>
        <Button 
          onClick={() => setShowAddEntry(!showAddEntry)}
          className="bg-gradient-primary"
        >
          <FileText className="h-4 w-4 mr-2" />
          Add Trade Entry
        </Button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total Entries</p>
              <p className="text-2xl font-bold text-foreground">{entries.length}</p>
            </div>
            <FileText className="h-6 w-6 text-primary" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Win Rate</p>
              <p className="text-2xl font-bold text-foreground">
                {(() => {
                  const allTrades = entries.flatMap(e => e.trades);
                  if (allTrades.length === 0) return '0%';
                  const wins = allTrades.filter(t => t.pnl !== undefined && t.pnl > 0).length;
                  return Math.round((wins / allTrades.length) * 100) + '%';
                })()}
              </p>
            </div>
            <TrendingUp className="h-6 w-6 text-success" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Avg P&L</p>
              <p className="text-2xl font-bold text-profit">
                {(() => {
                  const allTrades = entries.flatMap(e => e.trades);
                  if (allTrades.length === 0) return '$0';
                  const avg = allTrades.reduce((acc, t) => acc + (t.pnl ?? 0), 0) / allTrades.length;
                  return '$' + Math.round(avg);
                })()}
              </p>
            </div>
            <TrendingUp className="h-6 w-6 text-profit" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">This Month</p>
              <p className="text-2xl font-bold text-foreground">12</p>
            </div>
            <Calendar className="h-6 w-6 text-primary" />
          </div>
        </Card>
      </div>

      {/* Add Entry Form */}
      {showAddEntry && (
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Add New Trade Entry</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {newEntry.trades.map((trade, idx) => (
              <div key={idx} className="border border-border rounded-lg p-4 mb-2 relative">
                <button
                  type="button"
                  className="absolute top-2 right-2 text-xs text-muted-foreground hover:text-destructive"
                  onClick={() => removeTrade(idx)}
                  disabled={newEntry.trades.length === 1}
                  title="Remove trade"
                >
                  ×
                </button>
                <div className="mb-2">
                  <label className="text-sm font-medium text-foreground mb-2 block">Time (optional)</label>
                  <Input
                    type="time"
                    value={trade.time ?? ''}
                    onChange={e => handleTradeChange(idx, 'time', e.target.value)}
                  />
                </div>
                <div className="mb-2">
                  <label className="text-sm font-medium text-foreground mb-2 block">Symbol</label>
                  <Input
                    placeholder="e.g. EURUSD"
                    value={trade.symbol}
                    onChange={e => handleTradeChange(idx, 'symbol', e.target.value)}
                  />
                </div>
                <div className="mb-2">
                  <label className="text-sm font-medium text-foreground mb-2 block">Trade Type</label>
                  <select
                    className="w-full p-2 border border-border rounded-md bg-background"
                    value={trade.type}
                    onChange={e => handleTradeChange(idx, 'type', e.target.value.toLowerCase())}
                  >
                    <option value="buy">Buy</option>
                    <option value="sell">Sell</option>
                  </select>
                </div>
                <div className="mb-2">
                  <label className="text-sm font-medium text-foreground mb-2 block">Entry Price</label>
                  <Input
                    type="number"
                    step="0.00001"
                    placeholder="1.08500"
                    value={trade.entry ?? ''}
                    onChange={e => handleTradeChange(idx, 'entry', e.target.value)}
                  />
                </div>
                <div className="mb-2">
                  <label className="text-sm font-medium text-foreground mb-2 block">Exit Price</label>
                  <Input
                    type="number"
                    step="0.00001"
                    placeholder="1.09200"
                    value={trade.exit ?? ''}
                    onChange={e => handleTradeChange(idx, 'exit', e.target.value)}
                  />
                </div>
                <div className="mb-2">
                  <label className="text-sm font-medium text-foreground mb-2 block">P&L ($)</label>
                  <Input
                    type="number"
                    placeholder="350"
                    value={trade.pnl ?? ''}
                    onChange={e => handleTradeChange(idx, 'pnl', e.target.value)}
                  />
                </div>
                <div className="mb-2">
                  <label className="text-sm font-medium text-foreground mb-2 block">Risk:Reward</label>
                  <Input
                    placeholder="1:2.5"
                    value={trade.riskReward}
                    onChange={e => handleTradeChange(idx, 'riskReward', e.target.value)}
                  />
                </div>
              </div>
            ))}
            <div className="md:col-span-2 flex justify-end mb-4">
              <Button type="button" variant="outline" onClick={addTrade}>
                + Add Trade
              </Button>
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-medium text-foreground mb-2 block">Date</label>
              <Input
                type="date"
                value={newEntry.date}
                onChange={e => handleInputChange('date', e.target.value)}
              />
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-medium text-foreground mb-2 block">Reflection</label>
              <Textarea
                placeholder="What went well? What could be improved? Key lessons learned..."
                rows={4}
                value={newEntry.reflection}
                onChange={e => handleInputChange('reflection', e.target.value)}
              />
            </div>
            {/* End of Day Report */}
            <div className="md:col-span-2 mt-6">
              <h4 className="text-lg font-semibold mb-2">End of Trading Day Report</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium text-foreground mb-2 block">The Good</label>
                  <Textarea
                    placeholder="What went well today?"
                    rows={2}
                    value={newEntry.good}
                    onChange={e => handleInputChange('good', e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground mb-2 block">The Bad</label>
                  <Textarea
                    placeholder="What didn't go well?"
                    rows={2}
                    value={newEntry.bad}
                    onChange={e => handleInputChange('bad', e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground mb-2 block">The Ugly</label>
                  <Textarea
                    placeholder="What was the worst part?"
                    rows={2}
                    value={newEntry.ugly}
                    onChange={e => handleInputChange('ugly', e.target.value)}
                  />
                </div>
              </div>
              <div className="mt-4">
                <label className="text-sm font-medium text-foreground mb-2 block">Goals for Next Trading Day</label>
                <Textarea
                  placeholder="Set your goals for tomorrow..."
                  rows={2}
                  value={newEntry.goals}
                  onChange={e => handleInputChange('goals', e.target.value)}
                />
              </div>
            </div>
          </div>
          <div className="flex justify-end space-x-3 mt-6">
            <Button variant="outline" onClick={() => setShowAddEntry(false)}>
              Cancel
            </Button>
            <Button className="bg-gradient-primary" onClick={handleSaveEntry}>
              Save Entry
            </Button>
          </div>
        </Card>
      )}

      {/* Trade Entries */}
      <div className="space-y-4">
        {entries.map((entry) => (
          <Card key={entry.id} className="p-6 hover:shadow-medium transition-all duration-200">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-4 mb-3">
                  <span className="text-sm text-muted-foreground">
                    {entry.date.toLocaleDateString()}
                  </span>
                </div>
                {entry.trades.map((trade, idx) => (
                  <div key={idx} className="mb-4 border-b border-border pb-2">
                    <div className="flex items-center space-x-2 mb-1">
                      {trade.time && (
                        <span className="text-xs text-muted-foreground">{trade.time}</span>
                      )}
                      <Badge variant="outline" className="font-mono">
                        {trade.symbol}
                      </Badge>
                      <Badge variant={trade.type === "buy" ? "default" : "secondary"}>
                        {trade.type.toUpperCase()}
                      </Badge>
                      <Badge className={trade.pnl && trade.pnl > 0 ? "bg-success" : "bg-destructive"}>
                        {trade.pnl && trade.pnl > 0 ? "WIN" : "LOSS"}
                      </Badge>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      <div>
                        <p className="text-xs text-muted-foreground">Entry</p>
                        <p className="font-mono text-sm">{trade.entry}</p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">Exit</p>
                        <p className="font-mono text-sm">{trade.exit}</p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">P&L</p>
                        <p className={`font-bold text-sm ${trade.pnl && trade.pnl > 0 ? "text-profit" : "text-loss"}`}>
                          ${trade.pnl}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">R:R</p>
                        <p className="font-mono text-sm">{trade.riskReward}</p>
                      </div>
                    </div>
                  </div>
                ))}
                <div className="mb-3">
                  <p className="text-sm text-foreground leading-relaxed">
                    {entry.reflection}
                  </p>
                </div>
                <div className="flex items-center space-x-2 mb-2">
                  {entry.tags.map((tag) => (
                    <Badge key={tag} variant="secondary" className="text-xs">
                      #{tag}
                    </Badge>
                  ))}
                </div>
                {(entry.good || entry.bad || entry.ugly) && (
                  <div className="mb-2">
                    <h4 className="font-semibold text-sm mb-1">End of Day Report</h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                      <div>
                        <span className="block text-xs font-medium text-success mb-1">Good</span>
                        <span className="block text-xs text-muted-foreground">{entry.good}</span>
                      </div>
                      <div>
                        <span className="block text-xs font-medium text-warning mb-1">Bad</span>
                        <span className="block text-xs text-muted-foreground">{entry.bad}</span>
                      </div>
                      <div>
                        <span className="block text-xs font-medium text-destructive mb-1">Ugly</span>
                        <span className="block text-xs text-muted-foreground">{entry.ugly}</span>
                      </div>
                    </div>
                  </div>
                )}
                {entry.goals && (
                  <div className="mb-2">
                    <span className="block text-xs font-medium text-primary mb-1">Goals for Next Trading Day</span>
                    <span className="block text-xs text-muted-foreground">{entry.goals}</span>
                  </div>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};