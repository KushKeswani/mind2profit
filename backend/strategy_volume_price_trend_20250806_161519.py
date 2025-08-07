"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-06 16:15:19
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
            'start': start_date,
            'end': end_date,
            'timeframe': '1Min',
            'limit': 10000
        }
        response = requests.get(base_url + 'stocks/v2/historic/prices', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['prices'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['volume_ma20'] = df['volume'].rolling(20).mean()
        df['volume_ma50'] = df['volume'].rolling(50).mean()
        df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def generate_signals(df):
    try:
        signals = []
        prev_high = df['high'].shift(1)
        prev_low = df['low'].shift(1)
        prev_volume = df['volume'].shift(1)
        
        for i in range(1, len(df)):
            if df['close'][i] > prev_high[i-1] and df['volume'][i] > prev_volume[i-1]:
                signals.append({'timestamp': df['timestamp'][i], 'type': 'buy'})
            elif df['close'][i] < prev_low[i-1] and df['volume'][i] < prev_volume[i-1]:
                signals.append({'timestamp': df['timestamp'][i], 'type': 'sell'})
        return signals
    except Exception as e:
        print(f'Error generating signals: {e}')
        return None

def calculate_position_size(df, risk_percent):
    try:
        position_size = []
        for i in range(len(df)):
            atr = df['atr'][i]
            stop_loss = atr * 2
            position_size.append({
                'timestamp': df['timestamp'][i],
                'size': (10000 * risk_percent) / stop_loss
            })
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return None

def backtest_strategy():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        risk_percent = 0.01
        
        # Fetch data
        df = get_historical_data(symbol, start_date, end_date)
        if df is None:
            return None
        
        # Convert to pandas datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        # Calculate indicators
        df = calculate_indicators(df)
        if df is None:
            return None
        
        # Generate signals
        signals = generate_signals(df)
        if signals is None:
            return None
        
        # Calculate position sizes
        position_size = calculate_position_size(df, risk_percent)
        if position_size is None:
            return None
        
        # Create trade list
        trades = []
        for signal, size in zip(signals, position_size):
            trades.append({
                'timestamp': signal['timestamp'],
                'type': signal['type'],
                'size': size['size']
            })
        
        # Calculate performance metrics
        try:
            pnl = sum([trade['size'] * (df['close'][trade['timestamp']] * 
                                       (1 if trade['type'] == 'buy' else -1)) 
                      for trade in trades])
            sharpe_ratio = pnl / df['close'].std() * 252**0.5
        except Exception as e:
            print(f'Error calculating performance: {e}')
            return None
        
        # Prepare results
        results = {
            'trades': trades,
            'performance': {
                'total_pnl': pnl,
                'sharpe_ratio': sharpe_ratio,
                'risk_per_trade': risk_percent
            },
            'parameters': {
                'symbol': symbol,
                'timeframe': '1Min',
                'start_date': start_date,
                'end_date': end_date
            }
        }
        
        return results
    except Exception as e:
        print(f'Error in backtest: {e}')
        return None

def export_to_json(results, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        return True
    except Exception as e:
        print(f'Error exporting to JSON: {e}')
        return False

def main():
    results = backtest_strategy()
    if results:
        export_to_json(results, 'backtest_results.json')
        print('Backtest completed successfully')
    else:
        print('Backtest failed')

if __name__ == "__main__":
    main()