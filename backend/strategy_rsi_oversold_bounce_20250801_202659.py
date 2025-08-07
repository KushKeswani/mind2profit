"""
Generated Strategy: RSI Oversold Bounce
Description: Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target. Use 14-period RSI with 30/50 levels.
Generated: 2025-08-01 20:26:59
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

# Configure Alpaca API
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def fetch_data(symbol, start_date, end_date):
    try:
        # Set up API headers
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        
        # Fetch minute data
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        
        bar_url = f'{ALPACA_BASE_URL}/v2/stocks/{symbol}/bars?timeframe=1Min&start={start.isoformat()}&end={end.isoformat()}'
        response = requests.get(bar_url, headers=headers)
        
        if response.status_code != 200:
            raise ValueError(f'Failed to fetch data: {response.text}')
            
        data = response.json()
        df = pd.DataFrame([{
            'timestamp': datetime.strptime(bar['timestamp'], '%Y-%m-%dT%H:%M:%SZ'),
            'open': float(bar['open']),
            'high': float(bar['high']),
            'low': float(bar['low']),
            'close': float(bar['close']),
            'volume': int(bar['volume'])
        } for bar in data['bars']])
        
        df.set_index('timestamp', inplace=True)
        return df
    
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        # Calculate RSI
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        df['rsi_signal'] = df['rsi'].shift(1)
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def strategy_logic(df):
    try:
        trades = []
        position = False
        buy_price = 0
        profit_target = 0.02  # 2% profit target
        
        for i in range(len(df)):
            current_row = df.iloc[i]
            
            if not position and current_row['rsi'] < 30:
                # Buy signal
                position = True
                buy_price = current_row['close']
                buy_time = current_row.name
                
            elif position:
                # Check for sell conditions
                if current_row['rsi'] >= 50 or (current_row['close'] - buy_price)/buy_price >= profit_target:
                    sell_price = current_row['close']
                    sell_time = current_row.name
                    profit = (sell_price - buy_price) / buy_price * 100
                    
                    trades.append({
                        'buy_time': str(buy_time),
                        'sell_time': str(sell_time),
                        'buy_price': buy_price,
                        'sell_price': sell_price,
                        'profit': profit
                    })
                    
                    position = False
                    buy_price = 0
                    
        return trades
    except Exception as e:
        print(f'Error executing strategy: {e}')
        return []

def analyze_results(trades):
    try:
        if not trades:
            return {'trades': [], 'performance': {}}
            
        total_profit = sum(t['profit'] for t in trades)
        num_trades = len(trades)
        avg_profit = total_profit / num_trades if num_trades > 0 else 0
        win_rate = sum(1 for t in trades if t['profit'] > 0) / num_trades * 100 if num_trades > 0 else 0
        
        performance = {
            'total_profit': total_profit,
            'num_trades': num_trades,
            'avg_profit': avg_profit,
            'win_rate': win_rate
        }
        
        return {'trades': trades, 'performance': performance}
    except Exception as e:
        print(f'Error analyzing results: {e}')
        return {'trades': [], 'performance': {}}

def export_to_json(results, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        return True
    except Exception as e:
        print(f'Error exporting to JSON: {e}')
        return False

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        filename = 'rsi_oversold_bounce_results.json'
        
        # Validate dates
        if not (start_date and end_date):
            print('Invalid date range')
            return
            
        # Fetch data
        df = fetch_data(symbol, start_date, end_date)
        if df is None or df.empty:
            print('No data fetched')
            return
            
        # Calculate indicators
        df = calculate_indicators(df)
        if df is None or 'rsi' not in df.columns:
            print('Indicators calculation failed')
            return
            
        # Execute strategy
        trades = strategy_logic(df)
        if not trades:
            print('No trades generated')
            return
            
        # Analyze results
        results = analyze_results(trades)
        
        # Export to JSON
        if export_to_json(results, filename):
            print(f'Results exported to {filename}')
            
    except Exception as e:
        print(f'Critical error: {e}')

if __name__ == '__main__':
    main()