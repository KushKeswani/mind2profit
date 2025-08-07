import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  TrendingUp, 
  Lock, 
  BarChart3, 
  Target, 
  Zap,
  Crown,
  FileText,
  ExternalLink,
  Code,
  TestTube,
  Trash2,
  RefreshCw
} from "lucide-react";
import React, { useState } from "react";
import { StrategyTesterModule } from "./StrategyTesterModule";

interface Strategy {
  id: string;
  name: string;
  description: string;
  winRate: number;
  avgPnL: number;
  totalTrades: number;
  isPremium: boolean;
  complexity: "Beginner" | "Intermediate" | "Advanced";
  timeframe: string;
}

interface StrategiesModuleProps {
  onNavigateToResults?: (strategyData: any) => void;
}

export const StrategiesModule: React.FC<StrategiesModuleProps> = ({ onNavigateToResults }) => {
  const [activeTab, setActiveTab] = useState<'strategies' | 'tester'>('strategies');
  const [savedStrategies, setSavedStrategies] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  const loadSavedStrategies = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/saved-strategies');
      const data = await response.json();
      if (data.success) {
        setSavedStrategies(data.strategies);
      }
    } catch (error) {
      console.error('Error loading saved strategies:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteStrategy = async (strategyId: string) => {
    if (confirm('Are you sure you want to delete this strategy?')) {
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
    }
  };

  // Load saved strategies when component mounts
  React.useEffect(() => {
    loadSavedStrategies();
  }, []);

  // Function to get strategy code based on strategy name
  const getStrategyCode = (strategyName: string) => {
    const strategyTemplates: Record<string, string> = {
      "ICT Smart Money Concepts": `import pandas as pd
import numpy as np
import ta
from datetime import datetime, timedelta
import requests
import json

def get_alpaca_data(symbol, start_date, end_date, timeframe):
    """Fetch data from Alpaca API"""
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        
        headers = {
            'APCA-API-KEY-ID': api_key, 
            'APCA-API-SECRET-KEY': api_secret
        }
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe
        }
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def identify_order_blocks(data):
    """Identify institutional order blocks"""
    data['high_prev'] = data['high'].shift(1)
    data['low_prev'] = data['low'].shift(1)
    
    # Bullish order blocks (after a strong move down)
    data['bullish_ob'] = (data['close'] > data['open']) & (data['high_prev'] > data['low_prev'])
    
    # Bearish order blocks (after a strong move up)
    data['bearish_ob'] = (data['close'] < data['open']) & (data['high_prev'] < data['low_prev'])
    
    return data

def identify_fair_value_gaps(data):
    """Identify fair value gaps"""
    data['gap_up'] = data['low'] > data['high'].shift(1)
    data['gap_down'] = data['high'] < data['low'].shift(1)
    
    return data

def identify_market_structure(data):
    """Identify market structure shifts"""
    data['higher_high'] = data['high'] > data['high'].shift(1)
    data['lower_low'] = data['low'] < data['low'].shift(1)
    
    return data

def ict_strategy(data):
    """ICT Smart Money Concepts Strategy"""
    trades = []
    position = None
    
    for i in range(20, len(data)):
        current = data.iloc[i]
        
        # Entry conditions
        if position is None:
            # Long entry: Price returns to bullish order block
            if current['bullish_ob'] and current['close'] > current['open']:
                position = {
                    'type': 'long',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['low'] * 0.985,  # 1.5% below entry
                    'take_profit': current['close'] * 1.03  # 3% above entry
                }
            
            # Short entry: Price returns to bearish order block
            elif current['bearish_ob'] and current['close'] < current['open']:
                position = {
                    'type': 'short',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['high'] * 1.015,  # 1.5% above entry
                    'take_profit': current['close'] * 0.97  # 3% below entry
                }
        
        # Exit conditions
        elif position is not None:
            if position['type'] == 'long':
                if current['low'] <= position['stop_loss'] or current['high'] >= position['take_profit']:
                    exit_price = position['stop_loss'] if current['low'] <= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (exit_price - position['entry_price']) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price <= position['entry_price'] else 'win'
                    })
                    position = None
            
            elif position['type'] == 'short':
                if current['high'] >= position['stop_loss'] or current['low'] <= position['take_profit']:
                    exit_price = position['stop_loss'] if current['high'] >= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (position['entry_price'] - exit_price) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price >= position['entry_price'] else 'win'
                    })
                    position = None
    
    return trades

def main():
    """Main function"""
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    
    # Get data
    data = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if data is None:
        return
    
    # Apply ICT analysis
    data = identify_order_blocks(data)
    data = identify_fair_value_gaps(data)
    data = identify_market_structure(data)
    
    # Run strategy
    trades = ict_strategy(data)
    
    # Calculate performance
    if trades:
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['type'] == 'win'])
        win_rate = (winning_trades / total_trades) * 100
        total_pnl = sum(t['pnl'] for t in trades)
        
        results = {
            'strategy': 'ICT Smart Money Concepts',
            'symbol': symbol,
            'timeframe': timeframe,
            'date_range': f'{start_date} - {end_date}',
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'trades': trades
        }
        
        # Save results
        with open('ict_strategy_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        
        print('ICT Smart Money Concepts strategy completed successfully!')
        print(f'Total Trades: {total_trades}')
        print(f'Win Rate: {win_rate:.1f}%')
        print(f'Total P&L: {total_pnl:.2f}%')

if __name__ == "__main__":
    main()`,
      
      "BOS + FVG Strategy": `import pandas as pd
import numpy as np
import ta
from datetime import datetime, timedelta
import requests
import json

def get_alpaca_data(symbol, start_date, end_date, timeframe):
    """Fetch data from Alpaca API"""
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        
        headers = {
            'APCA-API-KEY-ID': api_key, 
            'APCA-API-SECRET-KEY': api_secret
        }
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe
        }
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def identify_break_of_structure(data):
    """Identify Break of Structure (BOS)"""
    data['swing_high'] = data['high'].rolling(5).max()
    data['swing_low'] = data['low'].rolling(5).min()
    
    # Bullish BOS: Price breaks above previous swing high
    data['bullish_bos'] = data['close'] > data['swing_high'].shift(1)
    
    # Bearish BOS: Price breaks below previous swing low
    data['bearish_bos'] = data['close'] < data['swing_low'].shift(1)
    
    return data

def identify_fair_value_gaps(data):
    """Identify Fair Value Gaps (FVG)"""
    data['gap_up'] = data['low'] > data['high'].shift(1)
    data['gap_down'] = data['high'] < data['low'].shift(1)
    
    # FVG levels
    data['fvg_high'] = data['high'].shift(1)
    data['fvg_low'] = data['low'].shift(1)
    
    return data

def bos_fvg_strategy(data):
    """BOS + FVG Strategy"""
    trades = []
    position = None
    
    for i in range(20, len(data)):
        current = data.iloc[i]
        
        # Entry conditions
        if position is None:
            # Long entry: Bullish BOS + price returns to FVG
            if (current['bullish_bos'] and 
                current['low'] <= current['fvg_high'] and 
                current['close'] > current['open']):
                position = {
                    'type': 'long',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['low'] * 0.985,  # 1.5% below entry
                    'take_profit': current['close'] * 1.03  # 3% above entry
                }
            
            # Short entry: Bearish BOS + price returns to FVG
            elif (current['bearish_bos'] and 
                  current['high'] >= current['fvg_low'] and 
                  current['close'] < current['open']):
                position = {
                    'type': 'short',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['high'] * 1.015,  # 1.5% above entry
                    'take_profit': current['close'] * 0.97  # 3% below entry
                }
        
        # Exit conditions
        elif position is not None:
            if position['type'] == 'long':
                if current['low'] <= position['stop_loss'] or current['high'] >= position['take_profit']:
                    exit_price = position['stop_loss'] if current['low'] <= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (exit_price - position['entry_price']) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price <= position['entry_price'] else 'win'
                    })
                    position = None
            
            elif position['type'] == 'short':
                if current['high'] >= position['stop_loss'] or current['low'] <= position['take_profit']:
                    exit_price = position['stop_loss'] if current['high'] >= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (position['entry_price'] - exit_price) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price >= position['entry_price'] else 'win'
                    })
                    position = None
    
    return trades

def main():
    """Main function"""
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    
    # Get data
    data = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if data is None:
        return
    
    # Apply BOS and FVG analysis
    data = identify_break_of_structure(data)
    data = identify_fair_value_gaps(data)
    
    # Run strategy
    trades = bos_fvg_strategy(data)
    
    # Calculate performance
    if trades:
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['type'] == 'win'])
        win_rate = (winning_trades / total_trades) * 100
        total_pnl = sum(t['pnl'] for t in trades)
        
        results = {
            'strategy': 'BOS + FVG Strategy',
            'symbol': symbol,
            'timeframe': timeframe,
            'date_range': f'{start_date} - {end_date}',
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'trades': trades
        }
        
        # Save results
        with open('bos_fvg_strategy_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        
        print('BOS + FVG Strategy completed successfully!')
        print(f'Total Trades: {total_trades}')
        print(f'Win Rate: {win_rate:.1f}%')
        print(f'Total P&L: {total_pnl:.2f}%')

if __name__ == "__main__":
    main()`,
      
      "Trendline Breakout": `import pandas as pd
import numpy as np
import ta
from datetime import datetime, timedelta
import requests
import json

def get_alpaca_data(symbol, start_date, end_date, timeframe):
    """Fetch data from Alpaca API"""
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        
        headers = {
            'APCA-API-KEY-ID': api_key, 
            'APCA-API-SECRET-KEY': api_secret
        }
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe
        }
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_trendlines(data):
    """Calculate trendlines using linear regression"""
    data['volume_ma'] = data['volume'].rolling(20).mean()
    data['price_ma'] = data['close'].rolling(20).mean()
    
    # Simple trendline calculation
    data['trend_up'] = data['close'] > data['price_ma']
    data['trend_down'] = data['close'] < data['price_ma']
    
    return data

def identify_breakouts(data):
    """Identify trendline breakouts"""
    data['breakout_up'] = (data['close'] > data['high'].shift(1)) & (data['volume'] > data['volume_ma'])
    data['breakout_down'] = (data['close'] < data['low'].shift(1)) & (data['volume'] > data['volume_ma'])
    
    return data

def trendline_breakout_strategy(data):
    """Trendline Breakout Strategy"""
    trades = []
    position = None
    
    for i in range(20, len(data)):
        current = data.iloc[i]
        
        # Entry conditions
        if position is None:
            # Long entry: Upward breakout with volume confirmation
            if current['breakout_up'] and current['trend_up']:
                position = {
                    'type': 'long',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['low'] * 0.985,  # 1.5% below entry
                    'take_profit': current['close'] * 1.03  # 3% above entry
                }
            
            # Short entry: Downward breakout with volume confirmation
            elif current['breakout_down'] and current['trend_down']:
                position = {
                    'type': 'short',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['high'] * 1.015,  # 1.5% above entry
                    'take_profit': current['close'] * 0.97  # 3% below entry
                }
        
        # Exit conditions
        elif position is not None:
            if position['type'] == 'long':
                if current['low'] <= position['stop_loss'] or current['high'] >= position['take_profit']:
                    exit_price = position['stop_loss'] if current['low'] <= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (exit_price - position['entry_price']) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price <= position['entry_price'] else 'win'
                    })
                    position = None
            
            elif position['type'] == 'short':
                if current['high'] >= position['stop_loss'] or current['low'] <= position['take_profit']:
                    exit_price = position['stop_loss'] if current['high'] >= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (position['entry_price'] - exit_price) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price >= position['entry_price'] else 'win'
                    })
                    position = None
    
    return trades

def main():
    """Main function"""
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    
    # Get data
    data = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if data is None:
        return
    
    # Apply trendline analysis
    data = calculate_trendlines(data)
    data = identify_breakouts(data)
    
    # Run strategy
    trades = trendline_breakout_strategy(data)
    
    # Calculate performance
    if trades:
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['type'] == 'win'])
        win_rate = (winning_trades / total_trades) * 100
        total_pnl = sum(t['pnl'] for t in trades)
        
        results = {
            'strategy': 'Trendline Breakout',
            'symbol': symbol,
            'timeframe': timeframe,
            'date_range': f'{start_date} - {end_date}',
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'trades': trades
        }
        
        # Save results
        with open('trendline_breakout_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        
        print('Trendline Breakout strategy completed successfully!')
        print(f'Total Trades: {total_trades}')
        print(f'Win Rate: {win_rate:.1f}%')
        print(f'Total P&L: {total_pnl:.2f}%')

if __name__ == "__main__":
    main()`
    };
    
    return strategyTemplates[strategyName] || `# ${strategyName} Strategy Code\n# Generated strategy code would go here`;
  };

  // Convert saved strategies to the format expected by the UI
  const strategies: Strategy[] = [
    // Default strategies
    {
      id: "1",
      name: "ICT Smart Money Concepts",
      description: "Advanced institutional trading concepts focusing on order blocks, fair value gaps, and market structure shifts.",
      winRate: 72,
      avgPnL: 285,
      totalTrades: 156,
      isPremium: false,
      complexity: "Advanced",
      timeframe: "15M - 1H"
    },
    {
      id: "2", 
      name: "BOS + FVG Strategy",
      description: "Break of Structure combined with Fair Value Gap entries for high-probability setups.",
      winRate: 68,
      avgPnL: 220,
      totalTrades: 89,
      isPremium: false,
      complexity: "Intermediate",
      timeframe: "5M - 30M"
    },
    {
      id: "3",
      name: "Trendline Breakout",
      description: "Classic technical analysis approach using trendline breaks with volume confirmation.",
      winRate: 65,
      avgPnL: 180,
      totalTrades: 234,
      isPremium: false,
      complexity: "Beginner",
      timeframe: "1H - 4H"
    },
    {
      id: "4",
      name: "Supply & Demand Zones",
      description: "Professional zone-based trading with institutional order flow analysis.",
      winRate: 78,
      avgPnL: 350,
      totalTrades: 67,
      isPremium: true,
      complexity: "Advanced",
      timeframe: "4H - Daily"
    },
    {
      id: "5",
      name: "Fibonacci Retracement Pro",
      description: "Advanced Fibonacci techniques with confluence analysis and multiple timeframe confirmation.",
      winRate: 71,
      avgPnL: 265,
      totalTrades: 123,
      isPremium: true,
      complexity: "Intermediate",
      timeframe: "1H - 4H"
    },
    // Add saved strategies
    ...savedStrategies.map((savedStrategy) => ({
      id: savedStrategy.id,
      name: savedStrategy.strategy_name,
      description: savedStrategy.description,
      winRate: 64.5, // Default win rate for saved strategies
      avgPnL: 220, // Default P&L for saved strategies
      totalTrades: 62, // Default trade count for saved strategies
      isPremium: false,
      complexity: "Intermediate" as const,
      timeframe: savedStrategy.timeframe || "1Min"
    }))
  ];

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case "Beginner": return "bg-success";
      case "Intermediate": return "bg-warning";
      case "Advanced": return "bg-destructive";
      default: return "bg-muted";
    }
  };

  const getWinRateColor = (winRate: number) => {
    if (winRate >= 70) return "text-success";
    if (winRate >= 60) return "text-warning";
    return "text-destructive";
  };


  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Strategy Lab</h1>
          <p className="text-muted-foreground">Discover and test advanced trading strategies</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button 
            onClick={() => {
              // TODO: Implement view all strategies functionality
              alert('View All Strategies functionality will be implemented');
            }}
            variant="outline"
          >
            <BarChart3 className="h-4 w-4 mr-2" />
            View All
          </Button>
          <Button 
            onClick={loadSavedStrategies}
            variant="outline"
            disabled={isLoading}
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
            {isLoading ? 'Loading...' : 'Refresh'}
          </Button>
          <Button 
            onClick={() => setActiveTab(activeTab === 'strategies' ? 'tester' : 'strategies')}
            className="bg-gradient-primary"
          >
            {activeTab === 'strategies' ? (
              <>
                <TestTube className="h-4 w-4 mr-2" />
                Strategy Tester
              </>
            ) : (
              <>
                <BarChart3 className="h-4 w-4 mr-2" />
                View Strategies
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 bg-muted p-1 rounded-lg">
        <button
          onClick={() => setActiveTab('strategies')}
          className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'strategies'
              ? 'bg-background text-foreground shadow-sm'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <BarChart3 className="h-4 w-4 mr-2 inline" />
          Strategy Library
        </button>
        <button
          onClick={() => setActiveTab('tester')}
          className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'tester'
              ? 'bg-background text-foreground shadow-sm'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <TestTube className="h-4 w-4 mr-2 inline" />
          Strategy Tester
        </button>
      </div>

      {/* Content based on active tab */}
      {activeTab === 'strategies' ? (
        <>
          {/* Strategy Stats Overview */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total Strategies</p>
              <p className="text-2xl font-bold text-foreground">{strategies.length}</p>
            </div>
            <BarChart3 className="h-6 w-6 text-primary" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Avg Win Rate</p>
              <p className="text-2xl font-bold text-success">
                {Math.round(strategies.reduce((acc, s) => acc + s.winRate, 0) / strategies.length)}%
              </p>
            </div>
            <Target className="h-6 w-6 text-success" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Avg P&L</p>
              <p className="text-2xl font-bold text-profit">
                ${Math.round(strategies.reduce((acc, s) => acc + s.avgPnL, 0) / strategies.length)}
              </p>
            </div>
            <TrendingUp className="h-6 w-6 text-profit" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-secondary">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Premium Available</p>
              <p className="text-2xl font-bold text-primary">
                {strategies.filter(s => s.isPremium).length}
              </p>
            </div>
            <Crown className="h-6 w-6 text-primary" />
          </div>
        </Card>
      </div>

      {/* Strategies Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {strategies.map((strategy) => (
          <Card 
            key={strategy.id} 
            className={`p-6 hover:shadow-medium transition-all duration-200 ${
              strategy.isPremium ? "border-primary/50 bg-gradient-to-br from-primary/5 to-transparent" : ""
            }`}
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="text-lg font-semibold text-foreground">{strategy.name}</h3>
                  {strategy.isPremium && (
                    <Badge className="bg-primary">
                      <Lock className="h-3 w-3 mr-1" />
                      Premium
                    </Badge>
                  )}
                </div>
                <p className="text-sm text-muted-foreground mb-3">
                  {strategy.description}
                </p>
              </div>
            </div>

            {/* Strategy Details */}
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-xs text-muted-foreground">Complexity</p>
                <Badge className={getComplexityColor(strategy.complexity)}>
                  {strategy.complexity}
                </Badge>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Timeframe</p>
                <p className="text-sm font-medium">{strategy.timeframe}</p>
              </div>
            </div>

            {/* Performance Metrics */}
            <div className="space-y-3 mb-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-muted-foreground">Win Rate</span>
                  <span className={`text-sm font-bold ${getWinRateColor(strategy.winRate)}`}>
                    {strategy.winRate}%
                  </span>
                </div>
                <Progress value={strategy.winRate} className="h-2" />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-xs text-muted-foreground">Avg P&L</p>
                  <p className="text-lg font-bold text-profit">${strategy.avgPnL}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Total Trades</p>
                  <p className="text-lg font-bold text-foreground">{strategy.totalTrades}</p>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-3">
              {strategy.isPremium ? (
                <>
                  <Button className="flex-1 bg-gradient-primary">
                    <Crown className="h-4 w-4 mr-2" />
                    Unlock Premium
                  </Button>
                  <Button variant="outline" size="icon">
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                </>
              ) : (
                <>
                  <Button 
                    className="flex-1 bg-gradient-primary"
                    onClick={() => {
                      // Create strategy data for the results page with real strategy code
                      const getStrategyMetrics = (strategyName: string) => {
                        const metrics = {
                          "ICT Smart Money Concepts": {
                            totalReturn: 3.8,
                            maxDrawdown: -1.2,
                            sharpeRatio: 2.1,
                            avgWin: 0.52,
                            avgLoss: -0.35,
                            profitFactor: 2.4
                          },
                          "BOS + FVG Strategy": {
                            totalReturn: 2.9,
                            maxDrawdown: -1.5,
                            sharpeRatio: 1.7,
                            avgWin: 0.48,
                            avgLoss: -0.42,
                            profitFactor: 2.0
                          },
                          "Trendline Breakout": {
                            totalReturn: 2.2,
                            maxDrawdown: -1.27,
                            sharpeRatio: 1.85,
                            avgWin: 0.45,
                            avgLoss: -0.38,
                            profitFactor: 2.1
                          }
                        };
                        return metrics[strategyName] || {
                          totalReturn: 2.2,
                          maxDrawdown: -1.27,
                          sharpeRatio: 1.85,
                          avgWin: 0.45,
                          avgLoss: -0.38,
                          profitFactor: 2.1
                        };
                      };

                      const metrics = getStrategyMetrics(strategy.name);
                      const strategyData = {
                        config: {
                          name: strategy.name,
                          symbol: "QQQ", // Default symbol
                          timeframe: strategy.timeframe,
                          startDate: "2025-01-01",
                          endDate: "2025-03-01",
                          riskPerTrade: 1,
                          description: strategy.description
                        },
                        results: {
                          totalTrades: strategy.totalTrades,
                          winningTrades: Math.round(strategy.totalTrades * strategy.winRate / 100),
                          losingTrades: strategy.totalTrades - Math.round(strategy.totalTrades * strategy.winRate / 100),
                          winRate: strategy.winRate,
                          totalReturn: metrics.totalReturn,
                          maxDrawdown: metrics.maxDrawdown,
                          sharpeRatio: metrics.sharpeRatio,
                          avgWin: metrics.avgWin,
                          avgLoss: metrics.avgLoss,
                          profitFactor: metrics.profitFactor,
                          trades: [] // Empty trades array for now
                        },
                        generatedCode: getStrategyCode(strategy.name)
                      };
                      onNavigateToResults?.(strategyData);
                    }}
                  >
                    <Zap className="h-4 w-4 mr-2" />
                    View Strategy
                  </Button>
                  <Button variant="outline" size="icon">
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                </>
              )}
              <Button 
                variant="outline" 
                size="icon"
                onClick={() => deleteStrategy(strategy.id)}
                className="text-destructive hover:text-destructive hover:bg-destructive/10"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </Card>
        ))}
      </div>
        </>
      ) : (
        <StrategyTesterModule onStrategyGenerated={(strategyData) => {
          console.log('🎯 StrategiesModule received strategy data:', strategyData);
          console.log('🔄 Calling onNavigateToResults callback...');
          onNavigateToResults?.(strategyData);
          console.log('✅ onNavigateToResults callback completed');
        }} />
      )}


    </div>
  );
};