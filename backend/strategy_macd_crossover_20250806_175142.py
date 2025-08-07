"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 17:51:42
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

def get_alpaca_data(symbol, start_date, end_date, timeframe):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        
        headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe,
            'limit': 10000
        }
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_macd(df):
    try:
        macd = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd.macd()
        df['signal'] = macd.signal()
        return df
    except Exception as e:
        print(f"Error calculating MACD: {e}")
        return None

def generate_signals(df):
    try:
        signals = []
        for i in range(1, len(df)):
            prev_macd = df['macd'].iloc[i-1]
            curr_macd = df['macd'].iloc[i]
            prev_signal = df['signal'].iloc[i-1]
            curr_signal = df['signal'].iloc[i]
            
            if curr_macd > curr_signal and prev_macd <= prev_signal:
                signals.append({'timestamp': df.index[i], 'type': 'buy'})
            elif curr_macd < curr_signal and prev_macd >= prev_signal:
                signals.append({'timestamp': df.index[i], 'type': 'sell'})
        return signals
    except Exception as e:
        print(f"Error generating signals: {e}")
        return None

def calculate_position_size(portfolio_value, risk_per_trade, stop_loss_pct):
    try:
        risk_amount = portfolio_value * risk_per_trade
        stop_loss = portfolio_value * stop_loss_pct
        position_size = risk_amount / stop_loss
        return position_size
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0

def backtest_strategy():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        initial_capital = 100000
        risk_per_trade = 0.01
        
        df = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return None
            
        df = calculate_macd(df)
        if df is None:
            return None
            
        signals = generate_signals(df)
        if signals is None:
            return None
        
        portfolio_value = initial_capital
        position_size = 0
        trades = []
        stop_loss_pct = 0.02
        
        for signal in signals:
            timestamp = signal['timestamp']
            price = df.loc[timestamp, 'close']
            
            if signal['type'] == 'buy':
                shares = calculate_position_size(portfolio_value, risk_per_trade, stop_loss_pct)
                cost = shares * price
                portfolio_value -= cost
                position_size = shares
                trades.append({
                    'timestamp': timestamp.isoformat(),
                    'type': 'buy',
                    'price': price,
                    'shares': shares,
                    'cost': cost
                })
            else:
                if position_size > 0:
                    revenue = position_size * price
                    portfolio_value += revenue
                    position_size = 0
                    trades.append({
                        'timestamp': timestamp.isoformat(),
                        'type': 'sell',
                        'price': price,
                        'shares': shares,
                        'revenue': revenue
                    })
        
        total_return = (portfolio_value - initial_capital) / initial_capital
        num_trades = len(trades)
        if num_trades > 0:
            avg_return = total_return / num_trades
            sharpe_ratio = avg_return / (pd.Series([t['return'] for t in trades]).std())
        else:
            avg_return = 0
            sharpe_ratio = 0
            
        max_drawdown = (portfolio_value / initial_capital).rolling(window=5).min().min() - 1
        
        results = {
            'trades': trades,
            'performance': {
                'total_return': total_return,
                'num_trades': num_trades,
                'avg_return': avg_return,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown
            }
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        return results
    except Exception as e:
        print(f"Error in backtest: {e}")
        return None

def main():
    results = backtest_strategy()
    if results:
        print("Backtest completed successfully")
    else:
        print("Backtest failed")

if __name__ == "__main__":
    main()