"""
Generated Strategy: Test
Description: Test strategy
Generated: 2025-08-06 16:49:49
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API keys
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def fetch_data(symbol, start_date, end_date):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        
        params = {
            'symbol': symbol,
            'timeframe': '1Min',
            'start': start_date,
            'end': end_date
        }
        
        response = requests.get(base_url + 'stocks/' + symbol + '/bars', params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_position_size(risk_percent, capital, stop_loss_price, current_price):
    try:
        risk_amount = capital * risk_percent / 100
        position_size = risk_amount / (current_price - stop_loss_price)
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def generate_trades(df):
    try:
        trades = []
        capital = 100000  # Initial capital
        risk_percent = 1.0
        
        for i in range(len(df)):
            current_price = df.iloc[i]['close']
            
            # Strategy logic (example)
            if i > 0 and df.iloc[i]['close'] > df.iloc[i-1]['close']:
                # Entry signal
                stop_loss_price = current_price * 0.99
                position_size = calculate_position_size(risk_percent, capital, stop_loss_price, current_price)
                
                trade = {
                    'entry_time': df.index[i].strftime('%Y-%m-%dT%H:%M:%S'),
                    'entry_price': current_price,
                    'quantity': position_size,
                    'risk_amount': capital * risk_percent / 100
                }
                trades.append(trade)
                
                # Exit logic (example)
                if i < len(df)-1 and df.iloc[i+1]['close'] < current_price:
                    trade['exit_time'] = df.index[i+1].strftime('%Y-%m-%dT%H:%M:%S')
                    trade['exit_price'] = df.iloc[i+1]['close']
                    trade['pnl'] = (trade['exit_price'] - trade['entry_price']) * trade['quantity']
        
        return trades
    except Exception as e:
        print(f'Error generating trades: {e}')
        return []

def export_to_json(trades, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(trades, f, indent=2)
        return True
    except Exception as e:
        print(f'Error exporting to JSON: {e}')
        return False

def backtest_strategy():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        df = fetch_data(symbol, start_date, end_date)
        if df is None:
            return False
            
        # Add technical indicators
        df['sma_20'] = df['close'].rolling(20).mean()
        df['rsi'] = ta.momentum.RSI(df['close'], window=14)
        
        trades = generate_trades(df)
        if not trades:
            return False
            
        # Calculate summary statistics
        total_pnl = sum(t['pnl'] for t in trades if 'pnl' in t)
        num_trades = len(trades)
        
        # Add summary to results
        results = {
            'trades': trades,
            'summary': {
                'total_pnl': total_pnl,
                'num_trades': num_trades,
                'win_rate': sum(1 for t in trades if 'pnl' in t and t['pnl'] > 0) / num_trades if num_trades > 0 else 0
            }
        }
        
        export_to_json(results, 'backtest_results.json')
        return True
    except Exception as e:
        print(f'Error in backtest_strategy: {e}')
        return False

def main():
    if backtest_strategy():
        print('Backtest completed successfully')
    else:
        print('Backtest failed')

if __name__ == "__main__":
    main()