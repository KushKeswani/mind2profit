"""
Generated Strategy: Bollinger Bands Strategy
Description: Buy when price touches lower band, sell when it reaches middle band. Use 20-period with 2 standard deviations.
Generated: 2025-08-05 18:05:01
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

# Set Alpaca API credentials
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def get_historical_data(symbol, start_date, end_date):
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
        response = requests.get(base_url + 'stocks/' + symbol + '/bars', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_bollinger_bands(df, window=20, std_dev=2):
    df['close'] = pd.to_numeric(df['close'])
    df['bb_middle'] = df['close'].rolling(window).mean()
    df['bb_std'] = df['close'].rolling(window).std()
    df['bb_lower'] = df['bb_middle'] - std_dev * df['bb_std']
    df['bb_upper'] = df['bb_middle'] + std_dev * df['bb_std']
    return df

def calculate_position_size(current_price, risk_amount, stop_loss):
    position_size = risk_amount / (stop_loss / current_price)
    return position_size

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    window = 20
    std_dev = 2
    risk_per_trade = 0.01  # 1.0%
    
    df = get_historical_data(symbol, start_date, end_date)
    if df is None:
        return
    
    df = df.drop(columns=['exchange'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = calculate_bollinger_bands(df, window, std_dev)
    
    trades = []
    position = None
    
    for index, row in df.iterrows():
        if position is None:
            if row['close'] <= row['bb_lower']:
                position = {
                    'entry_price': row['close'],
                    'entry_time': row['timestamp'],
                    'position_size': calculate_position_size(row['close'], 1000 * risk_per_trade, row['close'] - row['bb_lower'])
                }
                trades.append({'type': 'buy', **position})
        else:
            if row['close'] >= row['bb_middle']:
                position['exit_price'] = row['close']
                position['exit_time'] = row['timestamp']
                position['pnl'] = position['exit_price'] - position['entry_price']
                position['shares'] = position['position_size']
                trades.append(position)
                position = None
    
    total_pnl = sum(t['pnl'] for t in trades if 'pnl' in t)
    win_rate = sum(1 for t in trades if t.get('pnl', 0) > 0) / len(trades) if trades else 0
    
    results = {
        'trades': trades,
        'total_pnl': total_pnl,
        'win_rate': win_rate,
        'parameters': {
            'symbol': symbol,
            'window': window,
            'std_dev': std_dev,
            'risk_per_trade': risk_per_trade
        }
    }
    
    with open('bollinger_bands_results.json', 'w') as f:
        json.dump(results, f, default=str)
    
    print('Backtest completed. Results saved to bollinger_bands_results.json')

if __name__ == "__main__":
    main()