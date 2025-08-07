from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

app = FastAPI(title="Manual Backtesting API", version="1.0.0")

# Alpaca API Configuration
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY', 'PK0F1YSWGZYNHF1VKOY5')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY', 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB')
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'

class ManualBacktestRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    timeframe: str = "1Min"  # 1Min, 5Min, 15Min, 1Hour, 1Day
    strategy_type: str  # "moving_average", "macd", "rsi", "bollinger_bands", "custom"
    strategy_params: Dict[str, Any]
    initial_capital: float = 10000
    position_size: float = 0.1  # Percentage of capital per trade

class BacktestResult(BaseModel):
    success: bool
    symbol: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    total_return_pct: float
    max_drawdown: float
    max_drawdown_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    avg_win: float
    avg_loss: float
    profit_factor: float
    sharpe_ratio: float
    trades: List[Dict[str, Any]]
    equity_curve: List[Dict[str, Any]]
    error: Optional[str] = None

def get_alpaca_historical_data(symbol: str, start_date: str, end_date: str, timeframe: str = "1Min"):
    """Fetch historical data from Alpaca API"""
    try:
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        
        params = {
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe,
            'limit': 10000
        }
        
        # Use the correct endpoint for historical data
        url = f"{ALPACA_BASE_URL}/v2/stocks/{symbol}/bars"
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Alpaca API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if 'bars' not in data or not data['bars']:
            raise Exception("No data returned from Alpaca API")
        
        # Convert to DataFrame
        bars = data['bars']
        df = pd.DataFrame(bars)
        df['t'] = pd.to_datetime(df['t'])
        df.set_index('t', inplace=True)
        
        # Rename columns to standard format
        df.rename(columns={
            'o': 'Open',
            'h': 'High', 
            'l': 'Low',
            'c': 'Close',
            'v': 'Volume',
            'n': 'TradeCount',
            'vw': 'VWAP'
        }, inplace=True)
        
        return df
        
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")

def calculate_indicators(df: pd.DataFrame, strategy_params: Dict[str, Any]) -> pd.DataFrame:
    """Calculate technical indicators based on strategy type"""
    df = df.copy()
    
    strategy_type = strategy_params.get('strategy_type', 'moving_average')
    
    if strategy_type == 'moving_average':
        short_period = strategy_params.get('short_period', 10)
        long_period = strategy_params.get('long_period', 20)
        
        df['SMA_short'] = df['Close'].rolling(window=short_period).mean()
        df['SMA_long'] = df['Close'].rolling(window=long_period).mean()
        
    elif strategy_type == 'macd':
        fast_period = strategy_params.get('fast_period', 12)
        slow_period = strategy_params.get('slow_period', 26)
        signal_period = strategy_params.get('signal_period', 9)
        
        df['EMA_fast'] = df['Close'].ewm(span=fast_period).mean()
        df['EMA_slow'] = df['Close'].ewm(span=slow_period).mean()
        df['MACD'] = df['EMA_fast'] - df['EMA_slow']
        df['MACD_signal'] = df['MACD'].ewm(span=signal_period).mean()
        df['MACD_histogram'] = df['MACD'] - df['MACD_signal']
        
    elif strategy_type == 'rsi':
        period = strategy_params.get('period', 14)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
    elif strategy_type == 'bollinger_bands':
        period = strategy_params.get('period', 20)
        std_dev = strategy_params.get('std_dev', 2)
        
        df['BB_middle'] = df['Close'].rolling(window=period).mean()
        df['BB_std'] = df['Close'].rolling(window=period).std()
        df['BB_upper'] = df['BB_middle'] + (df['BB_std'] * std_dev)
        df['BB_lower'] = df['BB_middle'] - (df['BB_std'] * std_dev)
    
    return df

def generate_signals(df: pd.DataFrame, strategy_params: Dict[str, Any]) -> pd.DataFrame:
    """Generate buy/sell signals based on strategy"""
    df = df.copy()
    strategy_type = strategy_params.get('strategy_type', 'moving_average')
    
    # Initialize signal column
    df['Signal'] = 0  # 0 = hold, 1 = buy, -1 = sell
    
    if strategy_type == 'moving_average':
        # Buy when short MA crosses above long MA
        df['Signal'] = np.where(df['SMA_short'] > df['SMA_long'], 1, 0)
        df['Signal'] = np.where(df['SMA_short'] < df['SMA_long'], -1, df['Signal'])
        
    elif strategy_type == 'macd':
        # Buy when MACD crosses above signal line
        df['Signal'] = np.where(df['MACD'] > df['MACD_signal'], 1, 0)
        df['Signal'] = np.where(df['MACD'] < df['MACD_signal'], -1, df['Signal'])
        
    elif strategy_type == 'rsi':
        oversold = strategy_params.get('oversold', 30)
        overbought = strategy_params.get('overbought', 70)
        
        # Buy when RSI crosses above oversold
        df['Signal'] = np.where(df['RSI'] > oversold, 1, 0)
        df['Signal'] = np.where(df['RSI'] < overbought, -1, df['Signal'])
        
    elif strategy_type == 'bollinger_bands':
        # Buy when price touches lower band, sell when it touches upper band
        df['Signal'] = np.where(df['Close'] <= df['BB_lower'], 1, 0)
        df['Signal'] = np.where(df['Close'] >= df['BB_upper'], -1, df['Signal'])
    
    return df

def run_backtest(df: pd.DataFrame, initial_capital: float, position_size: float) -> Dict[str, Any]:
    """Run the actual backtest simulation"""
    capital = initial_capital
    position = 0
    trades = []
    equity_curve = []
    
    for i in range(1, len(df)):
        current_price = df['Close'].iloc[i]
        signal = df['Signal'].iloc[i]
        timestamp = df.index[i]
        
        # Execute trades based on signals
        if signal == 1 and position == 0:  # Buy signal
            shares = int((capital * position_size) / current_price)
            if shares > 0:
                position = shares
                trade_value = shares * current_price
                capital -= trade_value
                trades.append({
                    'timestamp': timestamp.isoformat(),
                    'action': 'BUY',
                    'shares': shares,
                    'price': current_price,
                    'value': trade_value,
                    'capital': capital
                })
                
        elif signal == -1 and position > 0:  # Sell signal
            trade_value = position * current_price
            capital += trade_value
            trades.append({
                'timestamp': timestamp.isoformat(),
                'action': 'SELL',
                'shares': position,
                'price': current_price,
                'value': trade_value,
                'capital': capital
            })
            position = 0
        
        # Calculate current equity
        current_equity = capital + (position * current_price)
        equity_curve.append({
            'timestamp': timestamp.isoformat(),
            'equity': current_equity,
            'capital': capital,
            'position_value': position * current_price
        })
    
    # Close any remaining position at the end
    if position > 0:
        final_price = df['Close'].iloc[-1]
        trade_value = position * final_price
        capital += trade_value
        trades.append({
            'timestamp': df.index[-1].isoformat(),
            'action': 'SELL',
            'shares': position,
            'price': final_price,
            'value': trade_value,
            'capital': capital
        })
    
    # Calculate performance metrics
    final_capital = capital
    total_return = final_capital - initial_capital
    total_return_pct = (total_return / initial_capital) * 100
    
    # Calculate drawdown
    equity_values = [point['equity'] for point in equity_curve]
    peak = max(equity_values)
    max_drawdown = 0
    for equity in equity_values:
        drawdown = (peak - equity) / peak * 100
        max_drawdown = max(max_drawdown, drawdown)
    
    # Calculate trade statistics
    buy_trades = [t for t in trades if t['action'] == 'BUY']
    sell_trades = [t for t in trades if t['action'] == 'SELL']
    
    total_trades = len(sell_trades)
    winning_trades = 0
    losing_trades = 0
    total_profit = 0
    total_loss = 0
    
    for i in range(len(buy_trades)):
        if i < len(sell_trades):
            buy_price = buy_trades[i]['price']
            sell_price = sell_trades[i]['price']
            profit = sell_price - buy_price
            
            if profit > 0:
                winning_trades += 1
                total_profit += profit
            else:
                losing_trades += 1
                total_loss += abs(profit)
    
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    avg_win = (total_profit / winning_trades) if winning_trades > 0 else 0
    avg_loss = (total_loss / losing_trades) if losing_trades > 0 else 0
    profit_factor = (total_profit / total_loss) if total_loss > 0 else float('inf')
    
    return {
        'initial_capital': initial_capital,
        'final_capital': final_capital,
        'total_return': total_return,
        'total_return_pct': total_return_pct,
        'max_drawdown': max_drawdown,
        'max_drawdown_pct': max_drawdown,
        'total_trades': total_trades,
        'winning_trades': winning_trades,
        'losing_trades': losing_trades,
        'win_rate': win_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'profit_factor': profit_factor,
        'trades': trades,
        'equity_curve': equity_curve
    }

@app.post("/manual-backtest", response_model=BacktestResult)
async def manual_backtest(request: ManualBacktestRequest):
    """Run a manual backtest with user-defined parameters"""
    try:
        # Fetch historical data
        df = get_alpaca_historical_data(
            request.symbol, 
            request.start_date, 
            request.end_date, 
            request.timeframe
        )
        
        if df.empty:
            raise HTTPException(status_code=400, detail="No data available for the specified period")
        
        # Calculate indicators
        df = calculate_indicators(df, request.strategy_params)
        
        # Generate signals
        df = generate_signals(df, request.strategy_params)
        
        # Run backtest
        results = run_backtest(df, request.initial_capital, request.position_size)
        
        return BacktestResult(
            success=True,
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital,
            **results
        )
        
    except Exception as e:
        return BacktestResult(
            success=False,
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital,
            final_capital=request.initial_capital,
            total_return=0,
            total_return_pct=0,
            max_drawdown=0,
            max_drawdown_pct=0,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0,
            avg_win=0,
            avg_loss=0,
            profit_factor=0,
            trades=[],
            equity_curve=[],
            error=str(e)
        )

@app.get("/available-symbols")
async def get_available_symbols():
    """Get list of available symbols for backtesting"""
    # This would typically fetch from Alpaca's assets endpoint
    # For now, return common symbols
    return {
        "stocks": ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NVDA", "NFLX"],
        "etfs": ["SPY", "QQQ", "IWM", "VTI", "VOO", "TQQQ", "SQQQ"],
        "futures": ["NQ", "ES"],  # Note: These require paid data
        "note": "Futures (NQ, ES) require paid Alpaca data subscription"
    }

@app.get("/strategy-templates")
async def get_strategy_templates():
    """Get available strategy templates for manual backtesting"""
    return {
        "moving_average": {
            "name": "Moving Average Crossover",
            "description": "Buy when short MA crosses above long MA",
            "parameters": {
                "short_period": {"type": "int", "default": 10, "min": 5, "max": 50},
                "long_period": {"type": "int", "default": 20, "min": 10, "max": 200}
            }
        },
        "macd": {
            "name": "MACD Crossover",
            "description": "Buy when MACD crosses above signal line",
            "parameters": {
                "fast_period": {"type": "int", "default": 12, "min": 5, "max": 50},
                "slow_period": {"type": "int", "default": 26, "min": 10, "max": 100},
                "signal_period": {"type": "int", "default": 9, "min": 5, "max": 50}
            }
        },
        "rsi": {
            "name": "RSI Strategy",
            "description": "Buy when RSI is oversold, sell when overbought",
            "parameters": {
                "period": {"type": "int", "default": 14, "min": 5, "max": 50},
                "oversold": {"type": "int", "default": 30, "min": 10, "max": 40},
                "overbought": {"type": "int", "default": 70, "min": 60, "max": 90}
            }
        },
        "bollinger_bands": {
            "name": "Bollinger Bands",
            "description": "Buy at lower band, sell at upper band",
            "parameters": {
                "period": {"type": "int", "default": 20, "min": 10, "max": 50},
                "std_dev": {"type": "float", "default": 2.0, "min": 1.0, "max": 3.0}
            }
        }
    }
