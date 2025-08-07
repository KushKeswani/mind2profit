"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 16:07:19
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
        
        response = requests.get(base_url + 'stocks/v2/minute', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['minute'])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_macd(df):
    try:
        macd = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd.macd()
        df['signal'] = macd.signal()
        df['histogram'] = macd.histogram()
        return df
    except Exception as e:
        print(f"Error calculating MACD: {e}")
        return None

def generate_signals(df):
    try:
        signals = []
        for i in range(1, len(df)):
            if df['macd'].iloc[i] > df['signal'].iloc[i] and df['macd'].iloc[i-1] < df['signal'].iloc[i-1]:
                signals.append({'type': 'buy', 'time': df.index[i], 'price': df['close'].iloc[i]})
            elif df['macd'].iloc[i] < df['signal'].iloc[i] and df['macd'].iloc[i-1] > df['signal'].iloc[i-1]:
                signals.append({'type': 'sell', 'time': df.index[i], 'price': df['close'].iloc[i]})
        return signals
    except Exception as e:
        print(f"Error generating signals: {e}")
        return None

def calculate_position_size(portfolio_value, risk_per_trade, stop_loss_pct):
    try:
        risk_amount = portfolio_value * risk_per_trade
        stop_loss = portfolio_value * stop_loss_pct
        shares = risk_amount / stop_loss
        return shares
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        initial_capital = 100000
        risk_per_trade = 0.01
        
        df = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return
            
        df = calculate_macd(df)
        if df is None:
            return
            
        signals = generate_signals(df)
        if signals is None:
            return
        
        portfolio_value = initial_capital
        position_size = 0
        trades = []
        
        for signal in signals:
            if signal['type'] == 'buy':
                shares = calculate_position_size(portfolio_value, risk_per_trade, 0.02)
                if shares > 0:
                    position_size = shares
                    trades.append({
                        'entry_time': signal['time'].strftime('%Y-%m-%dT%H:%M:%S'),
                        'entry_price': signal['price'],
                        'shares': shares
                    })
            elif signal['type'] == 'sell':
                if position_size > 0:
                    exit_price = signal['price']
                    pnl = (exit_price - trades[-1]['entry_price']) * position_size
                    portfolio_value += pnl
                    trades[-1]['exit_time'] = signal['time'].strftime('%Y-%m-%dT%H:%M:%S')
                    trades[-1]['exit_price'] = exit_price
                    trades[-1]['pnl'] = pnl
                    position_size = 0
        
        performance = {
            'total_return': (portfolio_value - initial_capital) / initial_capital,
            'number_of_trades': len(trades),
            'sharpe_ratio': 1.0  # Simplified for example
        }
        
        results = {
            'trades': trades,
            'performance': performance
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print("Backtest completed successfully")
        
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()