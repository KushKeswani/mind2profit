import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Code, Play, Download, CheckCircle, XCircle, X, BookOpen, Trash2 } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface StrategyTemplate {
  name: string;
  description: string;
  parameters: Record<string, any>;
  entryConditions?: {
    long: string[];
    short: string[];
  };
  riskManagement?: {
    stopLoss: string;
    takeProfit: string;
    positionSize: string;
  };
  explanation?: string;
}

interface StrategyResponse {
  success: boolean;
  strategy_name: string;
  generated_code?: string;
  validation_results?: {
    syntax_valid: boolean;
    has_required_imports: boolean;
    has_alpaca_api: boolean;
    has_technical_indicators: boolean;
    has_trade_logic: boolean;
    has_error_handling: boolean;
    issues: string[];
  };
  filename?: string;
  summary?: any;
  error?: string;
}

interface StrategyTesterModuleProps {
  onStrategyGenerated?: (strategyData: any) => void;
}

export const StrategyTesterModule: React.FC<StrategyTesterModuleProps> = ({ onStrategyGenerated }) => {
  const [strategyName, setStrategyName] = useState('');
  const [description, setDescription] = useState('');
  const [symbol, setSymbol] = useState('QQQ');
  const [startDate, setStartDate] = useState('2025-01-01');
  const [endDate, setEndDate] = useState('2025-03-01');
  const [timeframe, setTimeframe] = useState('1Min');
  const [isGenerating, setIsGenerating] = useState(false);
  const [strategyResponse, setStrategyResponse] = useState<StrategyResponse | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<string>('');

  const [strategyTemplates, setStrategyTemplates] = useState<Record<string, StrategyTemplate>>({
    'moving_average_crossover': {
      name: 'Moving Average Crossover',
      description: 'Buy when short SMA crosses above long SMA, sell when it crosses below. Use 20-period and 50-period simple moving averages.',
      parameters: { short_period: 20, long_period: 50 },
      entryConditions: {
        long: [
          'Short SMA (20-period) crosses above long SMA (50-period)',
          'Price is above both moving averages',
          'Volume is above average'
        ],
        short: [
          'Short SMA (20-period) crosses below long SMA (50-period)',
          'Price is below both moving averages',
          'Volume is above average'
        ]
      },
      riskManagement: {
        stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
        takeProfit: '3% above entry price for long positions, 3% below for short positions',
        positionSize: '1% of account per trade'
      },
      explanation: 'This strategy uses the crossover of two moving averages to identify trend changes. When the faster moving average crosses above the slower one, it signals a potential uptrend. The opposite signals a downtrend.'
    },
    'rsi_oversold_bounce': {
      name: 'RSI Oversold Bounce',
      description: 'Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target. Use 14-period RSI with 30/50 levels.',
      parameters: { rsi_period: 14, oversold_level: 30, exit_level: 50 },
      entryConditions: {
        long: [
          'RSI drops below 30 (oversold condition)',
          'Price shows signs of reversal (hammer, doji, or bullish engulfing)',
          'Volume increases on the bounce'
        ],
        short: [
          'RSI rises above 70 (overbought condition)',
          'Price shows signs of reversal (shooting star, bearish engulfing)',
          'Volume increases on the decline'
        ]
      },
      riskManagement: {
        stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
        takeProfit: '3% above entry price for long positions, 3% below for short positions',
        positionSize: '1% of account per trade'
      },
      explanation: 'This strategy capitalizes on oversold and overbought conditions. When RSI indicates extreme conditions, we look for price reversals with confirmation from candlestick patterns and volume.'
    },
    'macd_crossover': {
      name: 'MACD Crossover',
      description: 'Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.',
      parameters: { fast_period: 12, slow_period: 26, signal_period: 9 },
      entryConditions: {
        long: [
          'MACD line crosses above signal line',
          'MACD histogram is positive',
          'Price is above the 200-period moving average'
        ],
        short: [
          'MACD line crosses below signal line',
          'MACD histogram is negative',
          'Price is below the 200-period moving average'
        ]
      },
      riskManagement: {
        stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
        takeProfit: '3% above entry price for long positions, 3% below for short positions',
        positionSize: '1% of account per trade'
      },
      explanation: 'MACD crossover strategy identifies momentum changes. When the MACD line crosses above the signal line, it indicates increasing momentum and potential buying opportunity.'
    },
    'bollinger_bands': {
      name: 'Bollinger Bands Strategy',
      description: 'Buy when price touches lower band, sell when it reaches middle band. Use 20-period with 2 standard deviations.',
      parameters: { period: 20, std_dev: 2 },
      entryConditions: {
        long: [
          'Price touches or breaks below the lower Bollinger Band',
          'RSI is oversold (below 30)',
          'Volume increases on the bounce'
        ],
        short: [
          'Price touches or breaks above the upper Bollinger Band',
          'RSI is overbought (above 70)',
          'Volume increases on the decline'
        ]
      },
      riskManagement: {
        stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
        takeProfit: '3% above entry price for long positions, 3% below for short positions',
        positionSize: '1% of account per trade'
      },
      explanation: 'Bollinger Bands strategy trades mean reversion. When price touches the bands, it often reverts to the mean. We combine this with RSI for confirmation.'
    },
    'volume_price_trend': {
      name: 'Volume Price Trend',
      description: 'Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.',
      parameters: { volume_threshold: 1.5, price_threshold: 0.5 },
      entryConditions: {
        long: [
          'Price breaks above resistance with above-average volume',
          'Volume is 1.5x higher than average',
          'Price shows strong momentum'
        ],
        short: [
          'Price breaks below support with above-average volume',
          'Volume is 1.5x higher than average',
          'Price shows strong downward momentum'
        ]
      },
      riskManagement: {
        stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
        takeProfit: '3% above entry price for long positions, 3% below for short positions',
        positionSize: '1% of account per trade'
      },
      explanation: 'Volume Price Trend strategy focuses on high-volume breakouts. When price breaks key levels with significant volume, it often indicates strong institutional interest.'
    }
  });

  const [learnStrategyDialog, setLearnStrategyDialog] = useState<{
    isOpen: boolean;
    template: StrategyTemplate | null;
  }>({
    isOpen: false,
    template: null
  });

  const handleTemplateSelect = (templateKey: string) => {
    try {
      console.log('🎯 Selecting template:', templateKey);
      const template = strategyTemplates[templateKey];
      if (template) {
        setSelectedTemplate(templateKey);
        setStrategyName(template.name);
        setDescription(template.description);
        console.log('✅ Template selected:', template.name);
      } else {
        console.error('❌ Template not found:', templateKey);
      }
    } catch (error) {
      console.error('❌ Error selecting template:', error);
    }
  };

  const removeTemplate = (templateKey: string) => {
    const newTemplates = { ...strategyTemplates };
    delete newTemplates[templateKey];
    setStrategyTemplates(newTemplates);
    if (selectedTemplate === templateKey) {
      setSelectedTemplate('');
      setStrategyName('');
      setDescription('');
    }
  };

  const generateStrategy = async () => {
    if (!strategyName.trim() || !description.trim()) {
      alert('Please fill in strategy name and description');
      return;
    }

    setIsGenerating(true);
    setStrategyResponse(null);

    try {
      const response = await fetch('/api/generate-strategy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          strategy_name: strategyName,
          description: description,
          symbol: symbol,
          start_date: startDate,
          end_date: endDate,
          timeframe: timeframe,
          risk_per_trade: 1.0
        }),
      });

      const data: StrategyResponse = await response.json();
      console.log('📡 API Response:', data);
      setStrategyResponse(data);
      
      if (data.success && onStrategyGenerated) {
        console.log('✅ Strategy generation successful, data:', data);
        try {
          // Run the strategy to get real results
          console.log('🔄 Running strategy with filename:', data.filename);
          const runResponse = await fetch('/api/run-strategy', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              strategy_file: data.filename
            }),
          });

          const runData = await runResponse.json();
          console.log('📊 Strategy execution result:', runData);
          
          if (runData.success && runData.results) {
            // Use real results from the strategy execution
            const realResults = runData.results;
            
            const strategyData = {
              config: {
                name: data.strategy_name || strategyName,
                symbol,
                timeframe,
                startDate,
                endDate,
                riskPerTrade: 1.0,
                description
              },
              results: {
                totalTrades: realResults.totalTrades,
                winningTrades: realResults.winningTrades,
                losingTrades: realResults.losingTrades,
                winRate: realResults.winRate,
                totalReturn: realResults.totalReturn,
                avgWin: realResults.avgWin,
                avgLoss: realResults.avgLoss,
                profitFactor: Math.abs(realResults.avgWin / realResults.avgLoss) || 1.0,
                trades: realResults.trades || []
                // maxDrawdown and sharpeRatio are optional and will be calculated later
              },
              generatedCode: data.generated_code || `# ${strategyName} Strategy Code\n# Generated strategy code would go here`
            };
            
            console.log('🚀 Calling onStrategyGenerated with real data:', strategyData);
            onStrategyGenerated(strategyData);
          } else {
            // Strategy execution failed - show "Not Working" for all metrics
            console.warn('Strategy execution failed, showing "Not Working" for metrics:', runData.error);
            
            const strategyData = {
              config: {
                name: data.strategy_name || strategyName,
                symbol,
                timeframe,
                startDate,
                endDate,
                riskPerTrade: 1.0,
                description
              },
              results: {
                totalTrades: 0,
                winningTrades: 0,
                losingTrades: 0,
                winRate: 0,
                totalReturn: 0,
                avgWin: 0,
                avgLoss: 0,
                profitFactor: 0,
                trades: []
                // maxDrawdown and sharpeRatio are optional and will be calculated later
              },
              generatedCode: data.generated_code || `# ${strategyName} Strategy Code\n# Generated strategy code would go here`
            };
            
            onStrategyGenerated(strategyData);
          }
        } catch (callbackError) {
          console.error('Error in onStrategyGenerated callback:', callbackError);
        }
      } else if (!data.success) {
        alert(`Strategy generation failed: ${data.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('❌ Error generating strategy:', error);
      console.error('❌ Error details:', {
        message: error.message,
        stack: error.stack,
        type: error.constructor.name
      });
      setStrategyResponse({
        success: false,
        strategy_name: strategyName,
        error: `Failed to generate strategy: ${error.message}`
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const runStrategy = async () => {
    if (!strategyResponse?.filename) return;

    try {
      const response = await fetch('/api/run-strategy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          strategy_file: strategyResponse.filename
        }),
      });

      const data = await response.json();
      console.log('Strategy execution result:', data);
    } catch (error) {
      console.error('Error running strategy:', error);
    }
  };

  const downloadCode = () => {
    if (!strategyResponse?.generated_code) return;

    const blob = new Blob([strategyResponse.generated_code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${strategyName.replace(/\s+/g, '_')}_strategy.py`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Code className="h-5 w-5" />
            Strategy Tester
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Strategy Templates */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <Label className="text-sm font-medium">Strategy Templates</Label>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  console.log('🔄 Resetting templates to default...');
                  setStrategyTemplates({
                    'moving_average_crossover': {
                      name: 'Moving Average Crossover',
                      description: 'Buy when short SMA crosses above long SMA, sell when it crosses below. Use 20-period and 50-period simple moving averages.',
                      parameters: { short_period: 20, long_period: 50 },
                      entryConditions: {
                        long: [
                          'Short SMA (20-period) crosses above long SMA (50-period)',
                          'Price is above both moving averages',
                          'Volume is above average'
                        ],
                        short: [
                          'Short SMA (20-period) crosses below long SMA (50-period)',
                          'Price is below both moving averages',
                          'Volume is above average'
                        ]
                      },
                      riskManagement: {
                        stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
                        takeProfit: '3% above entry price for long positions, 3% below for short positions',
                        positionSize: '1% of account per trade'
                      },
                      explanation: 'This strategy uses the crossover of two moving averages to identify trend changes. When the faster moving average crosses above the slower one, it signals a potential uptrend. The opposite signals a downtrend.'
                    },
                    'rsi_oversold_bounce': {
                      name: 'RSI Oversold Bounce',
                      description: 'Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target. Use 14-period RSI with 30/50 levels.',
                      parameters: { rsi_period: 14, oversold_level: 30, exit_level: 50 },
                      entryConditions: {
                        long: [
                          'RSI drops below 30 (oversold condition)',
                          'Price shows signs of reversal (hammer, doji, or bullish engulfing)',
                          'Volume increases on the bounce'
                        ],
                        short: [
                          'RSI rises above 70 (overbought condition)',
                          'Price shows signs of reversal (shooting star, bearish engulfing)',
                          'Volume increases on the decline'
                        ]
                      },
                      riskManagement: {
                        stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
                        takeProfit: '3% above entry price for long positions, 3% below for short positions',
                        positionSize: '1% of account per trade'
                      },
                      explanation: 'This strategy capitalizes on oversold and overbought conditions. When RSI indicates extreme conditions, we look for price reversals with confirmation from candlestick patterns and volume.'
                    },
                    'macd_crossover': {
                      name: 'MACD Crossover',
                      description: 'Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.',
                      parameters: { fast_period: 12, slow_period: 26, signal_period: 9 },
                      entryConditions: {
                        long: [
                          'MACD line crosses above signal line',
                          'MACD histogram is positive',
                          'Price is above the 200-period moving average'
                        ],
                        short: [
                          'MACD line crosses below signal line',
                          'MACD histogram is negative',
                          'Price is below the 200-period moving average'
                        ]
                      },
                      riskManagement: {
                        stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
                        takeProfit: '3% above entry price for long positions, 3% below for short positions',
                        positionSize: '1% of account per trade'
                      },
                      explanation: 'MACD crossover strategy identifies momentum changes. When the MACD line crosses above the signal line, it indicates increasing momentum and potential buying opportunity.'
                    },
                    'bollinger_bands': {
                      name: 'Bollinger Bands Strategy',
                      description: 'Buy when price touches lower band, sell when it reaches middle band. Use 20-period with 2 standard deviations.',
                      parameters: { period: 20, std_dev: 2 },
                      entryConditions: {
                        long: [
                          'Price touches or breaks below the lower Bollinger Band',
                          'RSI is oversold (below 30)',
                          'Volume increases on the bounce'
                        ],
                        short: [
                          'Price touches or breaks above the upper Bollinger Band',
                          'RSI is overbought (above 70)',
                          'Volume increases on the decline'
                        ]
                      },
                      riskManagement: {
                        stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
                        takeProfit: '3% above entry price for long positions, 3% below for short positions',
                        positionSize: '1% of account per trade'
                      },
                      explanation: 'Bollinger Bands strategy trades mean reversion. When price touches the bands, it often reverts to the mean. We combine this with RSI for confirmation.'
                    },
                    'volume_price_trend': {
                      name: 'Volume Price Trend',
                      description: 'Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.',
                      parameters: { volume_threshold: 1.5, price_threshold: 0.5 },
                      entryConditions: {
                        long: [
                          'Price breaks above resistance with above-average volume',
                          'Volume is 1.5x higher than average',
                          'Price shows strong momentum'
                        ],
                        short: [
                          'Price breaks below support with above-average volume',
                          'Volume is 1.5x higher than average',
                          'Price shows strong downward momentum'
                        ]
                      },
                      riskManagement: {
                        stopLoss: '1.5% below entry price for long positions, 1.5% above for short positions',
                        takeProfit: '3% above entry price for long positions, 3% below for short positions',
                        positionSize: '1% of account per trade'
                      },
                      explanation: 'Volume Price Trend strategy focuses on high-volume breakouts. When price breaks key levels with significant volume, it often indicates strong institutional interest.'
                    }
                  });
                }}
              >
                Reset Templates
              </Button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mt-2">
              {Object.entries(strategyTemplates).map(([key, template]) => (
                <Card
                  key={key}
                  className={`cursor-pointer transition-colors relative ${
                    selectedTemplate === key ? 'border-primary bg-primary/5' : ''
                  }`}
                  onClick={() => handleTemplateSelect(key)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="font-medium text-sm">{template.name}</h4>
                        <p className="text-xs text-muted-foreground mt-1">
                          {template.description}
                        </p>
                      </div>
                      <div className="flex items-center gap-1 ml-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-6 w-6 p-0"
                          onClick={(e) => {
                            e.stopPropagation();
                            setLearnStrategyDialog({
                              isOpen: true,
                              template: template
                            });
                          }}
                        >
                          <BookOpen className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Strategy Configuration */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="strategy-name">Strategy Name</Label>
              <Input
                id="strategy-name"
                value={strategyName}
                onChange={(e) => setStrategyName(e.target.value)}
                placeholder="e.g., Moving Average Crossover"
              />
            </div>
            <div>
              <Label htmlFor="symbol">Symbol</Label>
              <Select value={symbol} onValueChange={setSymbol}>
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
              <Label htmlFor="start-date">Start Date</Label>
              <Input
                id="start-date"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="end-date">End Date</Label>
              <Input
                id="end-date"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="timeframe">Timeframe</Label>
              <Select value={timeframe} onValueChange={setTimeframe}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1Min">1 Minute</SelectItem>
                  <SelectItem value="5Min">5 Minutes</SelectItem>
                  <SelectItem value="15Min">15 Minutes</SelectItem>
                  <SelectItem value="1Hour">1 Hour</SelectItem>
                  <SelectItem value="1Day">1 Day</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Strategy Description */}
          <div>
            <Label htmlFor="description">Strategy Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe your trading strategy..."
              rows={4}
            />
          </div>

          {/* Generate Button */}
          <Button 
            onClick={generateStrategy} 
            disabled={isGenerating || !strategyName.trim() || !description.trim()}
            className="w-full"
          >
            {isGenerating ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Generating Strategy...
              </>
            ) : (
              <>
                <Code className="h-4 w-4 mr-2" />
                Generate Strategy
              </>
            )}
          </Button>

          {/* Test button for debugging */}
          <Button 
            onClick={() => {
              console.log('🧪 Test button clicked');
              if (onStrategyGenerated) {
                console.log('🧪 Calling onStrategyGenerated with test data');
                onStrategyGenerated({
                  config: {
                    name: 'Test Strategy',
                    symbol: 'QQQ',
                    timeframe: '1Min',
                    startDate: '2025-01-01',
                    endDate: '2025-03-01',
                    riskPerTrade: 1.0,
                    description: 'Test strategy for debugging'
                  },
                  results: {
                    totalTrades: 10,
                    winningTrades: 6,
                    losingTrades: 4,
                    winRate: 60,
                    totalReturn: 2.5,
                    maxDrawdown: -1.2,
                    sharpeRatio: 1.8,
                    avgWin: 0.5,
                    avgLoss: -0.3,
                    profitFactor: 2.0,
                    trades: []
                  },
                  generatedCode: '# Test strategy code'
                });
              } else {
                console.log('❌ onStrategyGenerated is not provided');
              }
            }}
            variant="outline"
            className="w-full mt-2"
          >
            🧪 Test Navigation
          </Button>

          {/* Strategy Response */}
          {strategyResponse && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {strategyResponse.success ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : (
                    <XCircle className="h-5 w-5 text-red-500" />
                  )}
                  Strategy Generation {strategyResponse.success ? 'Successful' : 'Failed'}
                </CardTitle>
              </CardHeader>
              <CardContent>
                {strategyResponse.success ? (
                  <>
                    <div className="space-y-4">
                      <div>
                        <Label className="text-sm font-medium">Strategy Name</Label>
                        <p className="text-sm text-muted-foreground">{strategyResponse.strategy_name}</p>
                      </div>

                      {strategyResponse.validation_results && (
                        <div>
                          <Label className="text-sm font-medium">Validation Results</Label>
                          <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mt-2">
                            {Object.entries(strategyResponse.validation_results)
                              .filter(([key]) => key !== 'issues')
                              .map(([key, value]) => (
                                <Badge
                                  key={key}
                                  variant={value ? 'default' : 'destructive'}
                                  className="text-xs"
                                >
                                  {key.replace(/_/g, ' ').toUpperCase()}: {value ? 'PASS' : 'FAIL'}
                                </Badge>
                              ))}
                          </div>
                          {strategyResponse.validation_results.issues.length > 0 && (
                            <Alert className="mt-2">
                              <AlertDescription>
                                <strong>Issues found:</strong>
                                <ul className="list-disc list-inside mt-1">
                                  {strategyResponse.validation_results.issues.map((issue, index) => (
                                    <li key={index} className="text-sm">{issue}</li>
                                  ))}
                                </ul>
                              </AlertDescription>
                            </Alert>
                          )}
                        </div>
                      )}

                      {/* Action Buttons */}
                      <div className="flex gap-2">
                        <Button onClick={downloadCode} variant="outline" size="sm">
                          <Download className="h-4 w-4 mr-2" />
                          Download Code
                        </Button>
                        <Button onClick={runStrategy} variant="outline" size="sm">
                          <Play className="h-4 w-4 mr-2" />
                          Run Strategy
                        </Button>
                      </div>

                      {/* Generated Code Preview */}
                      {strategyResponse.generated_code && (
                        <div>
                          <Label className="text-sm font-medium">Generated Code Preview</Label>
                          <div className="mt-2 p-4 bg-muted rounded-md max-h-60 overflow-y-auto">
                            <pre className="text-xs">
                              <code>{strategyResponse.generated_code.substring(0, 500)}...</code>
                            </pre>
                          </div>
                        </div>
                      )}
                    </div>
                  </>
                ) : (
                  <Alert>
                    <AlertDescription>
                      <strong>Error:</strong> {strategyResponse.error}
                    </AlertDescription>
                  </Alert>
                )}
              </CardContent>
            </Card>
          )}
        </CardContent>
      </Card>

      {/* Learn Strategy Dialog */}
      <Dialog open={learnStrategyDialog.isOpen} onOpenChange={(open) => setLearnStrategyDialog({ isOpen: open, template: null })}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              Learn: {learnStrategyDialog.template?.name}
            </DialogTitle>
          </DialogHeader>
          
          {learnStrategyDialog.template && (
            <div className="space-y-6">
              {/* Strategy Overview */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Strategy Overview</h3>
                <p className="text-muted-foreground">{learnStrategyDialog.template.explanation}</p>
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
                      {learnStrategyDialog.template.entryConditions?.long.map((condition, index) => (
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
                      {learnStrategyDialog.template.entryConditions?.short.map((condition, index) => (
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
                    <p className="text-sm text-muted-foreground">{learnStrategyDialog.template.riskManagement?.stopLoss}</p>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <h4 className="font-medium text-sm mb-1">Take Profit</h4>
                    <p className="text-sm text-muted-foreground">{learnStrategyDialog.template.riskManagement?.takeProfit}</p>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <h4 className="font-medium text-sm mb-1">Position Size</h4>
                    <p className="text-sm text-muted-foreground">{learnStrategyDialog.template.riskManagement?.positionSize}</p>
                  </div>
                </div>
              </div>

              {/* Strategy Parameters */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Strategy Parameters</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {Object.entries(learnStrategyDialog.template.parameters).map(([key, value]) => (
                    <div key={key} className="p-3 border rounded-lg">
                      <h4 className="font-medium text-sm mb-1">{key.replace(/_/g, ' ').toUpperCase()}</h4>
                      <p className="text-sm text-muted-foreground">{value}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};
