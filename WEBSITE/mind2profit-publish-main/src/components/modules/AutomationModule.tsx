import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import { 
  Bot, 
  Plus, 
  Play, 
  Pause, 
  Settings, 
  Trash2,
  ExternalLink,
  Zap,
  ArrowRight,
  Webhook,
  Activity
} from "lucide-react";

interface Automation {
  id: string;
  name: string;
  trigger: string;
  action: string;
  isActive: boolean;
  totalExecutions: number;
  successRate: number;
  lastExecution?: Date;
}

export const AutomationModule = () => {
  const [automations, setAutomations] = useState<Automation[]>([
    {
      id: "1",
      name: "EURUSD Breakout Bot",
      trigger: "TradingView Alert: EURUSD > 1.0950",
      action: "Buy 0.1 lots on Alpaca",
      isActive: true,
      totalExecutions: 23,
      successRate: 78,
      lastExecution: new Date("2024-01-15T10:30:00")
    },
    {
      id: "2",
      name: "Stop Loss Manager",
      trigger: "Position P&L < -$100",
      action: "Close all positions",
      isActive: true,
      totalExecutions: 5,
      successRate: 100,
      lastExecution: new Date("2024-01-12T14:15:00")
    },
    {
      id: "3",
      name: "News Trading Pause",
      trigger: "High impact news in 5 minutes",
      action: "Disable all trading bots",
      isActive: false,
      totalExecutions: 12,
      successRate: 95
    }
  ]);

  const [showWizard, setShowWizard] = useState(false);

  const toggleAutomation = (id: string) => {
    setAutomations(prev => prev.map(automation => 
      automation.id === id 
        ? { ...automation, isActive: !automation.isActive }
        : automation
    ));
  };

  const getSuccessRateColor = (rate: number) => {
    if (rate >= 80) return "text-success";
    if (rate >= 60) return "text-warning";
    return "text-destructive";
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Automation Lab</h1>
          <p className="text-muted-foreground">Build and manage your trading automation workflows</p>
        </div>
        <Button 
          onClick={() => setShowWizard(!showWizard)}
          className="bg-gradient-primary"
        >
          <Plus className="h-4 w-4 mr-2" />
          New Automation
        </Button>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Active Bots</p>
              <p className="text-2xl font-bold text-foreground">
                {automations.filter(a => a.isActive).length}
              </p>
            </div>
            <Bot className="h-6 w-6 text-primary" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total Executions</p>
              <p className="text-2xl font-bold text-foreground">
                {automations.reduce((acc, a) => acc + a.totalExecutions, 0)}
              </p>
            </div>
            <Activity className="h-6 w-6 text-primary" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Avg Success Rate</p>
              <p className="text-2xl font-bold text-success">
                {Math.round(automations.reduce((acc, a) => acc + a.successRate, 0) / automations.length)}%
              </p>
            </div>
            <Zap className="h-6 w-6 text-success" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">This Week</p>
              <p className="text-2xl font-bold text-foreground">8</p>
            </div>
            <Webhook className="h-6 w-6 text-primary" />
          </div>
        </Card>
      </div>

      {/* Automation Wizard */}
      {showWizard && (
        <Card className="p-6 border-2 border-primary/30 bg-primary/5">
          <h3 className="text-lg font-semibold mb-4">Create New Automation</h3>
          
          <div className="space-y-6">
            {/* Step 1: Trigger */}
            <div>
              <h4 className="font-medium mb-3">Step 1: Choose Trigger</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <Card className="p-4 cursor-pointer hover:bg-primary/10 border-2 border-primary">
                  <div className="flex items-center space-x-3">
                    <Webhook className="h-5 w-5 text-primary" />
                    <div>
                      <p className="font-medium">TradingView Alert</p>
                      <p className="text-xs text-muted-foreground">Webhook from TV</p>
                    </div>
                  </div>
                </Card>
                <Card className="p-4 cursor-pointer hover:bg-muted/50">
                  <div className="flex items-center space-x-3">
                    <Activity className="h-5 w-5 text-primary" />
                    <div>
                      <p className="font-medium">Price Level</p>
                      <p className="text-xs text-muted-foreground">Price crosses level</p>
                    </div>
                  </div>
                </Card>
                <Card className="p-4 cursor-pointer hover:bg-muted/50">
                  <div className="flex items-center space-x-3">
                    <Bot className="h-5 w-5 text-primary" />
                    <div>
                      <p className="font-medium">P&L Condition</p>
                      <p className="text-xs text-muted-foreground">Profit/Loss trigger</p>
                    </div>
                  </div>
                </Card>
              </div>
            </div>

            {/* Step 2: Configuration */}
            <div>
              <h4 className="font-medium mb-3">Step 2: Configure Trigger</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-foreground mb-2 block">Webhook URL</label>
                  <Input placeholder="https://tradingview.com/webhook/..." />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground mb-2 block">Alert Message</label>
                  <Input placeholder="EURUSD_BREAKOUT_BUY" />
                </div>
              </div>
            </div>

            {/* Step 3: Action */}
            <div>
              <h4 className="font-medium mb-3">Step 3: Choose Action</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <Card className="p-4 cursor-pointer hover:bg-primary/10 border-2 border-primary">
                  <div className="flex items-center space-x-3">
                    <ExternalLink className="h-5 w-5 text-primary" />
                    <div>
                      <p className="font-medium">Execute Trade on Alpaca</p>
                      <p className="text-xs text-muted-foreground">Place buy/sell order</p>
                    </div>
                  </div>
                </Card>
                <Card className="p-4 cursor-pointer hover:bg-muted/50">
                  <div className="flex items-center space-x-3">
                    <Settings className="h-5 w-5 text-primary" />
                    <div>
                      <p className="font-medium">Modify Positions</p>
                      <p className="text-xs text-muted-foreground">Update SL/TP</p>
                    </div>
                  </div>
                </Card>
              </div>
            </div>

            <div className="flex justify-end space-x-3">
              <Button variant="outline" onClick={() => setShowWizard(false)}>
                Cancel
              </Button>
              <Button className="bg-gradient-primary">
                Create Automation
              </Button>
            </div>
          </div>
        </Card>
      )}

      {/* Existing Automations */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Your Automations</h2>
        
        {automations.map((automation) => (
          <Card key={automation.id} className="p-6 hover:shadow-medium transition-all duration-200">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex flex-col md:flex-row md:items-center space-y-2 md:space-y-0 md:space-x-4 mb-3">
                  <h3 className="text-lg font-semibold">{automation.name}</h3>
                  <Badge className={automation.isActive ? "bg-success" : "bg-muted"}>
                    {automation.isActive ? "Active" : "Inactive"}
                  </Badge>
                  <div className="flex flex-col items-start">
                    <span className="text-xs text-muted-foreground mb-1">Is this still active? <span className="text-[10px] text-muted-foreground">(For stats only)</span></span>
                    <Switch 
                      checked={automation.isActive}
                      onCheckedChange={() => toggleAutomation(automation.id)}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Trigger</p>
                    <div className="flex items-center space-x-2 p-3 bg-muted rounded-lg">
                      <Webhook className="h-4 w-4 text-primary" />
                      <span className="text-sm">{automation.trigger}</span>
                    </div>
                  </div>
                  
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Action</p>
                    <div className="flex items-center space-x-2 p-3 bg-muted rounded-lg">
                      <Bot className="h-4 w-4 text-primary" />
                      <span className="text-sm">{automation.action}</span>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-xs text-muted-foreground">Executions</p>
                    <p className="text-lg font-bold text-foreground">{automation.totalExecutions}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Success Rate</p>
                    <p className={`text-lg font-bold ${getSuccessRateColor(automation.successRate)}`}>
                      {automation.successRate}%
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Last Execution</p>
                    <p className="text-sm text-foreground">
                      {automation.lastExecution?.toLocaleDateString() || "Never"}
                    </p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Button size="sm" variant="outline">
                      <Settings className="h-3 w-3" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Integration Info */}
      <Card className="p-6 border-2 border-dashed border-primary/30 bg-primary/5">
        <div className="flex items-start space-x-4">
          <ExternalLink className="h-8 w-8 text-primary mt-1" />
          <div>
            <h3 className="text-lg font-semibold mb-2">Connected Integrations</h3>
            <p className="text-muted-foreground mb-4">
              Your automations are connected to TradingView for alerts and Alpaca for trade execution. 
              All trades follow your risk management rules automatically.
            </p>
            <div className="flex items-center space-x-4">
              <Badge className="bg-success">TradingView Connected</Badge>
              <Badge className="bg-success">Alpaca Connected</Badge>
              <Button variant="outline" size="sm">
                Manage Connections
              </Button>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
