"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-06 13:31:09
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API keys
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def get_data(symbol, start_date, end_date):
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

def calculate_indicators(df):
    try:
        df['volume_ma'] = df['volume'].rolling(20).mean()
        df['price_ma'] = df['close'].rolling(50).mean()
        df['macd'], df['macd_signal'], df['macd_hist'] = ta.momentum.macd(df['close'], window_slow=26, window_fast=12, window_sign=9)
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def generate_signals(df):
    try:
        signals = []
        for i in range(len(df)):
            if df['volume'][i] > df['volume_ma'][i] and df['close'][i] > df['price_ma'][i] and df['macd'][i] > df['macd_signal'][i]:
                signals.append({'timestamp': df.index[i], 'type': 'buy'})
            elif df['volume'][i] < df['volume_ma'][i] and df['close'][i] < df['price_ma'][i] and df['macd'][i] < df['macd_signal'][i]:
                signals.append({'timestamp': df.index[i], 'type': 'sell'})
        return signals
    except Exception as e:
        print(f"Error generating signals: {e}")
        return None

def calculate_position_size(df, risk_percent):
    try:
        initial_capital = 100000
        position_size = []
        for i in range(len(df)):
            atr = df['high'].rolling(14).max() - df['low'].rolling(14).min()
            stop_loss = df['close'][i] - atr[i]
            position_size.append((initial_capital * risk_percent) / (df['close'][i] - stop_loss))
        return position_size
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        risk_percent = 0.01
        
        df = get_data(symbol, start_date, end_date)
        if df is None:
            return
            
        df = calculate_indicators(df)
        if df is None:
            return
            
        signals = generate_signals(df)
        if signals is None:
            return
            
        position_size = calculate_position_size(df, risk_percent)
        if position_size is None:
            return
        
        trades = []
        for i in range(len(signals)):
            if signals[i]['type'] == 'buy':
                next_sell = next((signals[j] for j in range(i+1, len(signals)) if signals[j]['type'] == 'sell'), None)
                if next_sell:
                    profit = df.loc[next_sell['timestamp']]['close'] - df.loc[signals[i]['timestamp']]['close']
                    trades.append({
                        'entry_time': signals[i]['timestamp'],
                        'exit_time': next_sell['timestamp'],
                        'profit': profit,
                        'size': position_size[i]
                    })
        
        results = {
            'trades': trades,
            'total_profit': sum(t['profit'] for t in trades),
            'num_trades': len(trades),
            'win_rate': sum(1 for t in trades if t['profit'] > 0) / len(trades) if len(trades) > 0 else 0
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print("Backtest completed successfully!")
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()