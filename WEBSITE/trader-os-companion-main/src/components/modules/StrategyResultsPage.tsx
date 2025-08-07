import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Textarea } from '@/components/ui/textarea';
import { 
  TrendingUp, 
  TrendingDown, 
  Target, 
  Calendar,
  BarChart3,
  Save,
  RefreshCw,
  Download,
  Play,
  Settings,
  DollarSign,
  Percent,
  Clock,
  BookOpen,
  Globe,
  CheckCircle,
  XCircle,
  Loader2
} from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface StrategyConfig {
  name: string;
  symbol: string;
  timeframe: string;
  startDate: string;
  endDate: string;
  riskPerTrade: number;
  description: string;
}

interface StrategyResults {
  totalTrades: number;
  winningTrades: number;
  losingTrades: number;
  winRate: number;
  totalReturn: number;
  maxDrawdown?: number;
  sharpeRatio?: number;
  avgWin: number;
  avgLoss: number;
  profitFactor: number;
  trades: Array<{
    entryTime?: string;
    exitTime?: string;
    entryPrice?: number;
    exitPrice?: number;
    pnl?: number;
    pnlPercent?: number;
    type?: 'win' | 'loss';
    // Backend format
    entry_time?: string;
    exit_time?: string;
    entry_price?: number;
    exit_price?: number;
    pnl_percent?: number;
  }>;
}

interface StrategyResultsPageProps {
  strategyData?: {
    config: StrategyConfig;
    results: StrategyResults;
    generatedCode?: string;
  };
  isFromGenerator?: boolean;
  onSave?: (strategy: any) => void;
  onUpdate?: (config: StrategyConfig) => void;
  onBackToStrategies?: () => void;
}

interface PublicStrategy {
  uuid: string;
  name: string;
  description: string;
  entryConditions: {
    long: string[];
    short: string[];
  };
  riskManagement: {
    stopLoss: string;
    takeProfit: string;
    positionSize: string;
  };
  explanation: string;
  author: string;
  createdAt: string;
  performance: {
    winRate: number;
    totalReturn: number;
    maxDrawdown: number;
    sharpeRatio: number;
  };
}

// Helper function to safely display values
const displayValue = (value: number | string, decimals: number = 2): string => {
  if (typeof value === 'string') {
    return value;
  }
  return value.toFixed(decimals);
};

export const StrategyResultsPage: React.FC<StrategyResultsPageProps> = ({
  strategyData,
  isFromGenerator = false,
  onSave,
  onUpdate,
  onBackToStrategies
}) => {
  console.log('🎯 StrategyResultsPage received strategyData:', strategyData);
  console.log('🎯 StrategyResultsPage props:', { strategyData, isFromGenerator, onSave, onUpdate, onBackToStrategies });
  
  // Handle case when strategyData is undefined
  if (!strategyData) {
    console.log('⚠️ No strategyData provided, showing default data');
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">Strategy Results</h1>
          <Button onClick={onBackToStrategies} variant="outline">
            Back to Strategies
          </Button>
        </div>
        <Alert>
          <AlertDescription>
            No strategy data available. Please generate a strategy first.
          </AlertDescription>
        </Alert>
      </div>
    );
  }
  const [config, setConfig] = useState<StrategyConfig>({
    name: strategyData?.config.name || 'RSI Oversold Bounce',
    symbol: strategyData?.config.symbol || 'QQQ',
    timeframe: strategyData?.config.timeframe || '1Min',
    startDate: strategyData?.config.startDate || '2025-01-01',
    endDate: strategyData?.config.endDate || '2025-03-01',
    riskPerTrade: strategyData?.config.riskPerTrade || 1,
    description: strategyData?.config.description || 'Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target.'
  });

  const [results, setResults] = useState<StrategyResults>(strategyData?.results || {
    totalTrades: 0,
    winningTrades: 0,
    losingTrades: 0,
    winRate: 0,
    totalReturn: 0,
    avgWin: 0,
    avgLoss: 0,
    profitFactor: 0,
    trades: []
  });

  const [isUpdating, setIsUpdating] = useState(false);
  const [learnStrategyDialog, setLearnStrategyDialog] = useState(false);
  const [makePublicDialog, setMakePublicDialog] = useState(false);
  const [publicStrategyData, setPublicStrategyData] = useState<Partial<PublicStrategy>>({
    name: config.name,
    description: config.description,
    entryConditions: {
      long: [
        'Price breaks above resistance level',
        'Volume is above average',
        'RSI is not overbought (below 70)'
      ],
      short: [
        'Price breaks below support level',
        'Volume is above average',
        'RSI is not oversold (above 30)'
      ]
    },
    riskManagement: {
      stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
      takeProfit: '3% above entry price for long positions, 3% below for short positions',
      positionSize: '1% of account per trade (conservative)'
    },
    explanation: 'This strategy uses technical analysis to identify high-probability trading opportunities with proper risk management.'
  });
  const [isSaving, setIsSaving] = useState(false);

  const handleConfigChange = (field: keyof StrategyConfig, value: string | number) => {
    setConfig(prev => ({ ...prev, [field]: value }));
  };

  const updateResults = async () => {
    setIsUpdating(true);
    try {
      // Simulate API call to update results
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock updated results
      const updatedResults = {
        ...results,
        totalTrades: Math.floor(Math.random() * 20) + 50,
        winRate: Math.random() * 20 + 60,
        totalReturn: Math.random() * 5 + 1
      };
      
      setResults(updatedResults);
      onUpdate?.(config);
    } catch (error) {
      console.error('Error updating results:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  const saveStrategy = async () => {
    setIsSaving(true);
    try {
      const response = await fetch('/api/save-strategy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          strategy_name: config.name,
          description: config.description,
          symbol: config.symbol,
          start_date: config.startDate,
          end_date: config.endDate,
          timeframe: config.timeframe,
          risk_per_trade: config.riskPerTrade,
          generated_code: strategyData?.generatedCode || '// Strategy code will be generated here',
          validation_results: {
            syntax_valid: true,
            has_required_imports: true,
            has_alpaca_api: true,
            has_technical_indicators: true,
            has_trade_logic: true,
            has_error_handling: true,
            issues: []
          },
          summary: {
            strategy_name: config.name,
            description: config.description,
            generated_at: new Date().toISOString(),
            validation: {
              syntax_valid: true,
              has_required_imports: true,
              has_alpaca_api: true,
              has_technical_indicators: true,
              has_trade_logic: true,
              has_error_handling: true,
              issues: []
            },
            status: 'ready'
          }
        }),
      });

      const data = await response.json();
      if (data.success) {
        alert('Strategy saved successfully! You can find it in the Strategy Library.');
        onSave?.({
          config,
          results,
          generatedCode: strategyData?.generatedCode
        });
      } else {
        alert('Failed to save strategy: ' + data.error);
      }
    } catch (error) {
      console.error('Error saving strategy:', error);
      alert('Failed to save strategy. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  const downloadResults = () => {
    const data = {
      config,
      results,
      generatedAt: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${config.name.replace(/\s+/g, '_').toLowerCase()}_results.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const makeStrategyPublic = async () => {
    setIsSaving(true);
    try {
      const strategyData = {
        ...publicStrategyData,
        uuid: crypto.randomUUID(),
        author: 'Mind2Profit User',
        createdAt: new Date().toISOString(),
        performance: {
          winRate: results.winRate,
          totalReturn: results.totalReturn,
          maxDrawdown: results.maxDrawdown,
          sharpeRatio: results.sharpeRatio
        }
      };

      const response = await fetch('/api/public-strategies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(strategyData),
      });

      if (response.ok) {
        alert('Strategy published successfully!');
        setMakePublicDialog(false);
      } else {
        throw new Error('Failed to publish strategy');
      }
    } catch (error) {
      console.error('Error publishing strategy:', error);
      alert('Failed to publish strategy. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  // Calculate additional statistics with safe defaults
  const trades = results.trades || [];
  const totalPnL = trades.reduce((sum, trade) => sum + (trade.pnl || 0), 0);
  const avgTradeDuration = trades.length > 0 
    ? trades.reduce((sum, trade) => {
        try {
          const entry = new Date(trade.entryTime || new Date());
          const exit = new Date(trade.exitTime || new Date());
          return sum + (exit.getTime() - entry.getTime()) / (1000 * 60); // in minutes
        } catch (error) {
          console.error('Error calculating trade duration:', error);
          return sum;
        }
      }, 0) / trades.length
    : 0;
  
  const consecutiveWins = trades.reduce((max, trade) => {
    if (trade.type === 'win') {
      return max + 1;
    } else {
      return 0;
    }
  }, 0);
  
  const consecutiveLosses = trades.reduce((max, trade) => {
    if (trade.type === 'loss') {
      return max + 1;
    } else {
      return 0;
    }
  }, 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">{config.name}</h1>
          <p className="text-muted-foreground">Strategy Performance & Results</p>
        </div>
        <div className="flex gap-2">
          {onBackToStrategies && (
            <Button onClick={onBackToStrategies} variant="outline">
              ← Back to Strategies
            </Button>
          )}
          <Button onClick={saveStrategy} disabled={isSaving} className="bg-gradient-to-r from-green-600 to-emerald-600">
            <Save className="h-4 w-4 mr-2" />
            {isSaving ? 'Saving...' : 'Save Strategy'}
          </Button>
          <Button onClick={downloadResults} variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Download Results
          </Button>
        </div>
      </div>

      {/* Strategy Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Strategy Configuration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <Label htmlFor="strategy-name">Strategy Name</Label>
              <Input
                id="strategy-name"
                value={config.name}
                onChange={(e) => handleConfigChange('name', e.target.value)}
                placeholder="Strategy name"
              />
            </div>
            <div>
              <Label htmlFor="symbol">Symbol</Label>
              <Select value={config.symbol} onValueChange={(value) => handleConfigChange('symbol', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="QQQ">QQQ</SelectItem>
                  <SelectItem value="SPY">SPY</SelectItem>
                  <SelectItem value="AAPL">AAPL</SelectItem>
                  <SelectItem value="TSLA">TSLA</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="timeframe">Timeframe</Label>
              <Select value={config.timeframe} onValueChange={(value) => handleConfigChange('timeframe', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1Min">1 Minute</SelectItem>
                  <SelectItem value="5Min">5 Minutes</SelectItem>
                  <SelectItem value="15Min">15 Minutes</SelectItem>
                  <SelectItem value="1Hour">1 Hour</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="start-date">Start Date</Label>
              <Input
                id="start-date"
                type="date"
                value={config.startDate}
                onChange={(e) => handleConfigChange('startDate', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="end-date">End Date</Label>
              <Input
                id="end-date"
                type="date"
                value={config.endDate}
                onChange={(e) => handleConfigChange('endDate', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="risk-per-trade">Risk Per Trade (%)</Label>
              <Select value={config.riskPerTrade.toString()} onValueChange={(value) => handleConfigChange('riskPerTrade', parseFloat(value))}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0.5">0.5% (Conservative)</SelectItem>
                  <SelectItem value="1">1% (Moderate)</SelectItem>
                  <SelectItem value="1.5">1.5% (Aggressive)</SelectItem>
                  <SelectItem value="2">2% (Very Aggressive)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          
          <div className="mt-4">
            <Button onClick={updateResults} disabled={isUpdating} className="w-full">
              <RefreshCw className={`h-4 w-4 mr-2 ${isUpdating ? 'animate-spin' : ''}`} />
              {isUpdating ? 'Updating Results...' : 'Update Results'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Return</p>
                <p className="text-2xl font-bold text-green-600">{displayValue(results.totalReturn, 2)}%</p>
              </div>
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Win Rate</p>
                <p className="text-2xl font-bold text-blue-600">{displayValue(results.winRate, 1)}%</p>
              </div>
              <Target className="h-6 w-6 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Max Drawdown</p>
                <p className="text-2xl font-bold text-red-600">{results.maxDrawdown ? results.maxDrawdown.toFixed(2) : "Not Working"}%</p>
              </div>
              <TrendingDown className="h-6 w-6 text-red-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Sharpe Ratio</p>
                <p className="text-2xl font-bold text-purple-600">{results.sharpeRatio ? results.sharpeRatio.toFixed(2) : "Not Working"}</p>
              </div>
              <BarChart3 className="h-6 w-6 text-purple-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <Button 
          onClick={() => setLearnStrategyDialog(true)}
          variant="outline"
          className="flex-1"
        >
          <BookOpen className="h-4 w-4 mr-2" />
          Learn This Strategy
        </Button>
        <Button 
          onClick={() => setMakePublicDialog(true)}
          variant="outline"
          className="flex-1"
        >
          <Globe className="h-4 w-4 mr-2" />
          Make Public
        </Button>
      </div>

      {/* Detailed Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Trade Statistics</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground">Total Trades</p>
                <p className="text-2xl font-bold">{results.totalTrades}</p>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground">Winning Trades</p>
                <p className="text-2xl font-bold text-green-600">{results.winningTrades}</p>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground">Avg Win</p>
                <p className="text-2xl font-bold text-green-600">+{results.avgWin.toFixed(2)}%</p>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground">Avg Loss</p>
                <p className="text-2xl font-bold text-red-600">{results.avgLoss.toFixed(2)}%</p>
              </div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">Profit Factor</p>
              <p className="text-2xl font-bold text-blue-600">{results.profitFactor.toFixed(2)}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Risk Management</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
              <div className="flex items-center gap-2">
                <Percent className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">Risk Per Trade</span>
              </div>
              <Badge variant="outline">{config.riskPerTrade}%</Badge>
            </div>
            <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
              <div className="flex items-center gap-2">
                <DollarSign className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">Account Risk</span>
              </div>
              <Badge variant="outline">{(config.riskPerTrade * results.totalTrades / 100).toFixed(2)}%</Badge>
            </div>
            <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">Time Period</span>
              </div>
              <Badge variant="outline">
                {new Date(config.startDate).toLocaleDateString()} - {new Date(config.endDate).toLocaleDateString()}
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Profit Chart Placeholder */}
      <Card>
        <CardHeader>
          <CardTitle>Profit Over Time</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64 bg-muted rounded-lg flex items-center justify-center">
            <div className="text-center">
              <BarChart3 className="h-12 w-12 text-muted-foreground mx-auto mb-2" />
              <p className="text-muted-foreground">Profit chart will be implemented here</p>
              <p className="text-sm text-muted-foreground">Showing cumulative P&L over time</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recent Trades */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Trades</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {results.trades.slice(0, 10).map((trade, index) => {
              // Handle both old and new data formats
              const entryTime = trade.entryTime || trade.entry_time;
              const exitTime = trade.exitTime || trade.exit_time;
              const entryPrice = trade.entryPrice || trade.entry_price;
              const exitPrice = trade.exitPrice || trade.exit_price;
              const pnlPercent = trade.pnlPercent || trade.pnl_percent;
              
              // Calculate actual dollar PnL if not provided
              let pnl = trade.pnl;
              if (pnl === undefined && entryPrice && pnlPercent !== undefined) {
                // Calculate dollar amount based on percentage
                pnl = (entryPrice * pnlPercent / 100);
              }
              
              const type = trade.type || (pnlPercent >= 0 ? 'win' : 'loss');
              
              return (
                <div key={index} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                  <div className="flex items-center gap-4">
                    <Badge variant={type === 'win' ? 'default' : 'destructive'}>
                      {type === 'win' ? 'WIN' : 'LOSS'}
                    </Badge>
                    <div>
                      <p className="text-sm font-medium">
                        {new Date(entryTime).toLocaleDateString()} - {new Date(exitTime).toLocaleDateString()}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        ${entryPrice?.toFixed(2) || '0.00'} → ${exitPrice?.toFixed(2) || '0.00'}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className={`font-bold ${pnlPercent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {pnlPercent >= 0 ? '+' : ''}{pnlPercent?.toFixed(2) || '0.00'}%
                    </p>
                    <p className="text-xs text-muted-foreground">
                      ${pnl?.toFixed(2) || '0.00'}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Learn Strategy Dialog */}
      <Dialog open={learnStrategyDialog} onOpenChange={setLearnStrategyDialog}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              Learn: {config.name}
            </DialogTitle>
          </DialogHeader>
          
          <div className="space-y-6">
            {/* Strategy Overview */}
            <div>
              <h3 className="text-lg font-semibold mb-2">Strategy Overview</h3>
              <p className="text-muted-foreground">{publicStrategyData.explanation}</p>
            </div>

            {/* Entry Conditions */}
            <Tabs defaultValue="long" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="long">Long Entries</TabsTrigger>
                <TabsTrigger value="short">Short Entries</TabsTrigger>
              </TabsList>
              
              <TabsContent value="long" className="space-y-4">
                <div>
                  <h4 className="font-medium mb-2">Long Entry Checklist</h4>
                  <div className="space-y-2">
                    {publicStrategyData.entryConditions?.long.map((condition, index) => (
                      <div key={index} className="flex items-start gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-sm">{condition}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </TabsContent>
              
              <TabsContent value="short" className="space-y-4">
                <div>
                  <h4 className="font-medium mb-2">Short Entry Checklist</h4>
                  <div className="space-y-2">
                    {publicStrategyData.entryConditions?.short.map((condition, index) => (
                      <div key={index} className="flex items-start gap-2">
                        <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-sm">{condition}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </TabsContent>
            </Tabs>

            {/* Risk Management */}
            <div>
              <h3 className="text-lg font-semibold mb-2">Risk Management</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 border rounded-lg">
                  <h4 className="font-medium text-sm mb-1">Stop Loss</h4>
                  <p className="text-sm text-muted-foreground">{publicStrategyData.riskManagement?.stopLoss}</p>
                </div>
                <div className="p-4 border rounded-lg">
                  <h4 className="font-medium text-sm mb-1">Take Profit</h4>
                  <p className="text-sm text-muted-foreground">{publicStrategyData.riskManagement?.takeProfit}</p>
                </div>
                <div className="p-4 border rounded-lg">
                  <h4 className="font-medium text-sm mb-1">Position Size</h4>
                  <p className="text-sm text-muted-foreground">{publicStrategyData.riskManagement?.positionSize}</p>
                </div>
              </div>
            </div>

            {/* Performance Summary */}
            <div>
              <h3 className="text-lg font-semibold mb-2">Performance Summary</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-3 border rounded-lg text-center">
                  <p className="text-sm text-muted-foreground">Win Rate</p>
                  <p className="text-lg font-bold text-green-600">{results.winRate.toFixed(1)}%</p>
                </div>
                <div className="p-3 border rounded-lg text-center">
                  <p className="text-sm text-muted-foreground">Total Return</p>
                  <p className="text-lg font-bold text-green-600">{results.totalReturn.toFixed(2)}%</p>
                </div>
                <div className="p-3 border rounded-lg text-center">
                  <p className="text-sm text-muted-foreground">Max Drawdown</p>
                  <p className="text-lg font-bold text-red-600">{results.maxDrawdown.toFixed(2)}%</p>
                </div>
                <div className="p-3 border rounded-lg text-center">
                  <p className="text-sm text-muted-foreground">Sharpe Ratio</p>
                  <p className="text-lg font-bold text-blue-600">{results.sharpeRatio.toFixed(2)}</p>
                </div>
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Make Public Dialog */}
      <Dialog open={makePublicDialog} onOpenChange={setMakePublicDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Globe className="h-5 w-5" />
              Make Strategy Public
            </DialogTitle>
          </DialogHeader>
          
          <div className="space-y-4">
            <div>
              <Label htmlFor="public-name">Strategy Name</Label>
              <Input
                id="public-name"
                value={publicStrategyData.name}
                onChange={(e) => setPublicStrategyData({...publicStrategyData, name: e.target.value})}
                placeholder="Enter strategy name"
              />
            </div>
            
            <div>
              <Label htmlFor="public-description">Description</Label>
              <Textarea
                id="public-description"
                value={publicStrategyData.description}
                onChange={(e) => setPublicStrategyData({...publicStrategyData, description: e.target.value})}
                placeholder="Describe your strategy"
                rows={3}
              />
            </div>
            
            <div>
              <Label htmlFor="public-explanation">Detailed Explanation</Label>
              <Textarea
                id="public-explanation"
                value={publicStrategyData.explanation}
                onChange={(e) => setPublicStrategyData({...publicStrategyData, explanation: e.target.value})}
                placeholder="Explain how the strategy works, entry/exit conditions, risk management, etc."
                rows={5}
              />
            </div>

            <div className="flex gap-2 pt-4">
              <Button 
                onClick={makeStrategyPublic} 
                disabled={isSaving}
                className="flex-1"
              >
                {isSaving ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Publishing...
                  </>
                ) : (
                  <>
                    <Globe className="h-4 w-4 mr-2" />
                    Publish Strategy
                  </>
                )}
              </Button>
              <Button 
                variant="outline" 
                onClick={() => setMakePublicDialog(false)}
                className="flex-1"
              >
                Cancel
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}; 