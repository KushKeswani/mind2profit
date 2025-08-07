"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-06 18:20:11
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
API_SECRET = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, start_date, end_date):
    try:
        endpoint = f'{BASE_URL}/v2/data/{symbol}/bars?timeframe=1Min&start={start_date}&end={end_date}'
        headers = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')
        return None

def process_data(df):
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df['volume_ma20'] = df['volume'].rolling(20).mean()
        df['volume_ma50'] = df['volume'].rolling(50).mean()
        df['price_ma20'] = df['close'].rolling(20).mean()
        df['rsi'] = ta.momentum.RSI(df['close'], window=14)
        df['sma'] = ta.trend.SMA(df['close'], window=20)
        return df
    except Exception as e:
        print(f'Error processing data: {e}')
        return None

def calculate_position_size(portfolio_value, risk_per_trade, stop_loss_pips):
    try:
        position_size = (portfolio_value * risk_per_trade) / stop_loss_pips
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def generate_signals(df):
    try:
        signals = []
        for i in range(len(df)):
            if df['volume'][i] > df['volume_ma20'][i] and df['close'][i] > df['price_ma20'][i] and df['rsi'][i] < 30:
                signals.append({'type': 'buy', 'timestamp': df.index[i], 'price': df['close'][i]})
            elif df['volume'][i] < df['volume_ma20'][i] and df['close'][i] < df['price_ma20'][i] and df['rsi'][i] > 70:
                signals.append({'type': 'sell', 'timestamp': df.index[i], 'price': df['close'][i]})
        return signals
    except Exception as e:
        print(f'Error generating signals: {e}')
        return []

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        risk_per_trade = 0.01
        portfolio_value = 100000
        
        df = get_data(symbol, start_date, end_date)
        if df is None:
            return
            
        df = process_data(df)
        if df is None:
            return
            
        signals = generate_signals(df)
        if not signals:
            print('No trading signals generated')
            return
            
        trades = []
        position_size = calculate_position_size(portfolio_value, risk_per_trade, 10)
        
        for signal in signals:
            if signal['type'] == 'buy':
                trades.append({
                    'entry_time': signal['timestamp'].strftime('%Y-%m-%dT%H:%M:%S'),
                    'entry_price': signal['price'],
                    'position_size': position_size,
                    'risk_per_trade': risk_per_trade
                })
        
        results = {
            'trades': trades,
            'total_pnl': sum(t['position_size'] for t in trades),
            'number_of_trades': len(trades),
            'win_rate': len([t for t in trades if t['position_size'] > 0]) / len(trades) if trades else 0
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=4)
            
        print('Backtest results exported to backtest_results.json')
        
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()