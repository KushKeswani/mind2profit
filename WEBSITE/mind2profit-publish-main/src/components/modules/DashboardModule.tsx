import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, DollarSign, Activity, Target, Brain } from "lucide-react";
import { SessionClock } from "@/components/ui/session-clock";

export const DashboardModule = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground">Your trading performance at a glance</p>
        </div>
        <div className="flex flex-col md:items-end gap-1">
          <Badge className="bg-success text-success-foreground mb-1 md:mb-0">
            Performance: Excellent
          </Badge>
          <SessionClock />
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="p-6 bg-gradient-secondary shadow-soft">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total P&L</p>
              <p className="text-2xl font-bold text-profit">+$12,450</p>
              <p className="text-xs text-success flex items-center mt-1">
                <TrendingUp className="h-3 w-3 mr-1" />
                +8.2% this month
              </p>
            </div>
            <DollarSign className="h-8 w-8 text-profit" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary shadow-soft">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Win Rate</p>
              <p className="text-2xl font-bold text-foreground">68.5%</p>
              <p className="text-xs text-success flex items-center mt-1">
                <TrendingUp className="h-3 w-3 mr-1" />
                +3.1% vs last month
              </p>
            </div>
            <Target className="h-8 w-8 text-primary" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary shadow-soft">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total Trades</p>
              <p className="text-2xl font-bold text-foreground">142</p>
              <p className="text-xs text-neutral flex items-center mt-1">
                <Activity className="h-3 w-3 mr-1" />
                18 this week
              </p>
            </div>
            <Activity className="h-8 w-8 text-primary" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary shadow-soft">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Mindset Score</p>
              <p className="text-2xl font-bold text-foreground">8.2/10</p>
              <p className="text-xs text-success flex items-center mt-1">
                <Brain className="h-3 w-3 mr-1" />
                Excellent discipline
              </p>
            </div>
            <Brain className="h-8 w-8 text-primary" />
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Recent Trades</h3>
          <div className="space-y-3">
            {[
              { pair: "EURUSD", result: "win", pnl: "+$285", time: "10:30 AM" },
              { pair: "GBPJPY", result: "win", pnl: "+$150", time: "09:15 AM" },
              { pair: "USDJPY", result: "loss", pnl: "-$95", time: "08:45 AM" },
            ].map((trade, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                <div className="flex items-center space-x-3">
                  <Badge variant={trade.result === "win" ? "default" : "destructive"}>
                    {trade.pair}
                  </Badge>
                  <span className="text-sm text-muted-foreground">{trade.time}</span>
                </div>
                <span className={`font-semibold ${
                  trade.result === "win" ? "text-profit" : "text-loss"
                }`}>
                  {trade.pnl}
                </span>
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Today's Focus</h3>
          <div className="space-y-4">
            <div className="p-4 bg-primary/10 border border-primary/20 rounded-lg">
              <h4 className="font-medium text-primary">Market Session: London Open</h4>
              <p className="text-sm text-muted-foreground mt-1">
                High volatility expected on GBP pairs due to inflation data at 14:00
              </p>
            </div>
            <div className="p-4 bg-warning/10 border border-warning/20 rounded-lg">
              <h4 className="font-medium text-warning">Psychology Check</h4>
              <p className="text-sm text-muted-foreground mt-1">
                You've won 4 trades in a row. Stay disciplined and stick to your risk management.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};