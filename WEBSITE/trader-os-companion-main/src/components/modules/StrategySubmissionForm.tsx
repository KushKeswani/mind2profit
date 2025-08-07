import React, { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Code, Play, Download, CheckCircle, XCircle, X, Save, BookOpen, Trash2 } from 'lucide-react';

interface StrategyTemplate {
  name: string;
  description: string;
  parameters: Record<string, any>;
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

interface StrategySubmissionFormProps {
  onClose?: () => void;
  onStrategyGenerated?: (strategyData: any) => void;
}

export const StrategySubmissionForm: React.FC<StrategySubmissionFormProps> = ({ onClose, onStrategyGenerated }) => {
  const [strategyName, setStrategyName] = useState('');
  const [description, setDescription] = useState('');
  const [symbol, setSymbol] = useState('QQQ');
  const [startDate, setStartDate] = useState('2025-01-01');
  const [endDate, setEndDate] = useState('2025-03-01');
  const [timeframe, setTimeframe] = useState('1Min');
  const [riskPerTrade, setRiskPerTrade] = useState('1');
  const [isGenerating, setIsGenerating] = useState(false);
  const [strategyResponse, setStrategyResponse] = useState<StrategyResponse | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<string>('');
  const [isSaving, setIsSaving] = useState(false);
  const [savedStrategies, setSavedStrategies] = useState<any[]>([]);
  const [showSavedStrategies, setShowSavedStrategies] = useState(false);

  const strategyTemplates: Record<string, StrategyTemplate> = {
    'moving_average_crossover': {
      name: 'Moving Average Crossover',
      description: 'Buy when short SMA crosses above long SMA, sell when it crosses below. Use 20-period and 50-period simple moving averages.',
      parameters: { short_period: 20, long_period: 50 }
    },
    'rsi_oversold_bounce': {
      name: 'RSI Oversold Bounce',
      description: 'Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target. Use 14-period RSI with 30/50 levels.',
      parameters: { rsi_period: 14, oversold_level: 30, exit_level: 50 }
    },
    'macd_crossover': {
      name: 'MACD Crossover',
      description: 'Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.',
      parameters: { fast_period: 12, slow_period: 26, signal_period: 9 }
    },
    'bollinger_bands': {
      name: 'Bollinger Bands Strategy',
      description: 'Buy when price touches lower band, sell when it reaches middle band. Use 20-period with 2 standard deviations.',
      parameters: { period: 20, std_dev: 2 }
    },
    'volume_price_trend': {
      name: 'Volume Price Trend',
      description: 'Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.',
      parameters: { volume_threshold: 1.5, price_threshold: 0.5 }
    }
  };

  const handleTemplateSelect = (templateKey: string) => {
    const template = strategyTemplates[templateKey];
    if (template) {
      setSelectedTemplate(templateKey);
      setStrategyName(template.name);
      setDescription(template.description);
    }
  };

  const generateStrategy = async () => {
    console.log('Form state:', { strategyName, description, symbol, startDate, endDate, timeframe });
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
          risk_per_trade: parseFloat(riskPerTrade)
        }),
      });

      const data: StrategyResponse = await response.json();
      setStrategyResponse(data);
      
      if (data.success && onStrategyGenerated) {
        onStrategyGenerated({
          config: {
            name: strategyName,
            symbol,
            timeframe,
            startDate,
            endDate,
            riskPerTrade: parseFloat(riskPerTrade),
            description
          },
          results: data.summary,
          generatedCode: data.generated_code
        });
      }
    } catch (error) {
      console.error('Error generating strategy:', error);
      setStrategyResponse({
        success: false,
        strategy_name: strategyName,
        error: 'Failed to generate strategy. Please try again.'
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
    a.download = `${strategyName.replace(/\s+/g, '_').toLowerCase()}.py`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const saveStrategy = async () => {
    if (!strategyResponse?.success || !strategyResponse.generated_code) {
      alert('No strategy to save. Please generate a strategy first.');
      return;
    }

    setIsSaving(true);
    try {
      const response = await fetch('/api/save-strategy', {
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
          risk_per_trade: parseFloat(riskPerTrade),
          generated_code: strategyResponse.generated_code,
          validation_results: strategyResponse.validation_results,
          summary: strategyResponse.summary
        }),
      });

      const data = await response.json();
      if (data.success) {
        alert('Strategy saved successfully!');
        loadSavedStrategies(); // Refresh the saved strategies list
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

  const loadSavedStrategies = async () => {
    try {
      const response = await fetch('/api/saved-strategies');
      const data = await response.json();
      if (data.success) {
        setSavedStrategies(data.strategies);
      }
    } catch (error) {
      console.error('Error loading saved strategies:', error);
    }
  };

  const loadStrategy = (strategy: any) => {
    setStrategyName(strategy.strategy_name);
    setDescription(strategy.description);
    setSymbol(strategy.symbol);
    setStartDate(strategy.start_date);
    setEndDate(strategy.end_date);
    setTimeframe(strategy.timeframe);
    setRiskPerTrade(strategy.risk_per_trade.toString());
    
    // Set the strategy response to show the generated code
    setStrategyResponse({
      success: true,
      strategy_name: strategy.strategy_name,
      generated_code: strategy.generated_code,
      validation_results: strategy.validation_results,
      summary: strategy.summary
    });
    
    setShowSavedStrategies(false);
  };

  const deleteStrategy = async (strategyId: string) => {
    if (!confirm('Are you sure you want to delete this strategy?')) {
      return;
    }

    try {
      const response = await fetch(`/api/saved-strategy/${strategyId}`, {
        method: 'DELETE',
      });

      const data = await response.json();
      if (data.success) {
        alert('Strategy deleted successfully!');
        loadSavedStrategies(); // Refresh the list
      } else {
        alert('Failed to delete strategy: ' + data.error);
      }
    } catch (error) {
      console.error('Error deleting strategy:', error);
      alert('Failed to delete strategy. Please try again.');
    }
  };

  // Load saved strategies when component mounts
  React.useEffect(() => {
    loadSavedStrategies();
  }, []);

  return (
    <div className="w-full max-w-4xl mx-auto p-6 overflow-y-auto">
      <div className="flex items-center justify-between mb-6 sticky top-0 bg-background pt-2 pb-4 z-10">
        <div>
          <h1 className="text-3xl font-bold text-foreground">AI Strategy Generator</h1>
          <p className="text-muted-foreground">Describe your trading strategy and get working Python code</p>
        </div>
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            onClick={() => setShowSavedStrategies(!showSavedStrategies)}
            className="flex items-center gap-2"
          >
            <BookOpen className="h-4 w-4" />
            Saved Strategies ({savedStrategies.length})
          </Button>
          {onClose && (
            <Button variant="outline" size="icon" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>

      {/* Saved Strategies Modal */}
      {showSavedStrategies && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              Saved Strategies
            </CardTitle>
          </CardHeader>
          <CardContent>
            {savedStrategies.length === 0 ? (
              <p className="text-muted-foreground text-center py-4">
                No saved strategies found. Generate and save a strategy to see it here.
              </p>
            ) : (
              <div className="space-y-3">
                {savedStrategies.map((strategy) => (
                  <Card key={strategy.id} className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h4 className="font-medium">{strategy.strategy_name}</h4>
                        <p className="text-sm text-muted-foreground mt-1">
                          {strategy.description.substring(0, 100)}...
                        </p>
                        <div className="flex gap-2 mt-2">
                          <Badge variant="outline" className="text-xs">
                            {strategy.symbol}
                          </Badge>
                          <Badge variant="outline" className="text-xs">
                            {strategy.timeframe}
                          </Badge>
                          <Badge variant="outline" className="text-xs">
                            {strategy.risk_per_trade}% Risk
                          </Badge>
                        </div>
                        <p className="text-xs text-muted-foreground mt-1">
                          Saved: {new Date(strategy.saved_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex gap-2">
                        <Button 
                          size="sm" 
                          onClick={() => loadStrategy(strategy)}
                          variant="outline"
                        >
                          Load
                        </Button>
                        <Button 
                          size="sm" 
                          onClick={() => deleteStrategy(strategy.id)}
                          variant="destructive"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      <div className="space-y-6 pb-6">
        {/* Strategy Templates */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Code className="h-5 w-5" />
              Strategy Templates
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Label className="text-sm font-medium">Quick Start Templates</Label>
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
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-6 w-6 p-0 text-destructive hover:text-destructive ml-2"
                        onClick={(e) => {
                          e.stopPropagation();
                          if (confirm('Are you sure you want to delete this template?')) {
                            const newTemplates = { ...strategyTemplates };
                            delete newTemplates[key];
                            // TODO: Update strategyTemplates state
                            alert(`Template ${template.name} would be deleted`);
                          }
                        }}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Strategy Configuration */}
        <Card>
          <CardHeader>
            <CardTitle>Strategy Configuration</CardTitle>
          </CardHeader>
          <CardContent>
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
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="risk-per-trade">Risk Per Trade (%)</Label>
              <Select value={riskPerTrade} onValueChange={setRiskPerTrade}>
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
          </CardContent>
        </Card>

        {/* Strategy Description */}
        <Card>
          <CardHeader>
            <CardTitle>Strategy Description</CardTitle>
          </CardHeader>
          <CardContent>
            <Label htmlFor="description">Describe your trading strategy in detail</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Include entry/exit conditions, indicators, risk management, etc. Be as detailed as possible."
              rows={8}
              className="mt-2"
            />
          </CardContent>
        </Card>

        {/* Generate Button */}
        <Card>
          <CardContent className="pt-6">
            <Button
              onClick={generateStrategy}
              disabled={isGenerating || !strategyName.trim() || !description.trim()}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 text-lg"
              size="lg"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="h-5 w-5 mr-3 animate-spin" />
                  Generating Strategy Code...
                </>
              ) : (
                <>
                  <Code className="h-5 w-5 mr-3" />
                  Generate Strategy Code
                </>
              )}
            </Button>
            {(!strategyName.trim() || !description.trim()) && (
              <div className="text-sm text-muted-foreground mt-2 text-center space-y-1">
                <p>Please fill in both strategy name and description to generate code</p>
                <div className="text-xs">
                  Strategy Name: {strategyName.trim() ? '✅' : '❌'} | 
                  Description: {description.trim() ? '✅' : '❌'}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Results */}
        {strategyResponse && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                {strategyResponse.success ? (
                  <CheckCircle className="h-5 w-5 text-green-500" />
                ) : (
                  <XCircle className="h-5 w-5 text-red-500" />
                )}
                Strategy Generation Results
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {strategyResponse.success ? (
                <>
                  {/* Validation Results */}
                  {strategyResponse.validation_results && (
                    <div>
                      <Label className="text-sm font-medium">Validation Results</Label>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mt-2">
                        {Object.entries(strategyResponse.validation_results).map(([key, value]) => {
                          if (key === 'issues') return null;
                          return (
                            <Badge
                              key={key}
                              variant={value ? 'default' : 'destructive'}
                              className="text-xs"
                            >
                              {key.replace(/_/g, ' ').toUpperCase()}: {value ? 'PASS' : 'FAIL'}
                            </Badge>
                          );
                        })}
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
                    {/* Make Public button removed - strategy will navigate to results page instead */}
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
      </div>
    </div>
  );
};
