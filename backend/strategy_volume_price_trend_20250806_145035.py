"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-06 14:50:35
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
API_SECRET = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_historical_data(symbol, start_date, end_date):
    try:
        url = f'{BASE_URL}/v2/data/{symbol}/1min'
        params = {
            'start': start_date,
            'end': end_date,
            'limit': 10000
        }
        headers = {
            'APCA-API-KEY-ID': API_KEY,
            'APCA-API-SECRET-KEY': API_SECRET
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_vpt(data):
    try:
        df = pd.DataFrame(data['results'])
        df['time'] = pd.to_datetime(df['t'])
        df.set_index('time', inplace=True)
        df = df[['o', 'h', 'l', 'c', 'v']]
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df['vpt'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
        df['sma_20'] = df['close'].rolling(20).mean()
        df['buy_signal'] = df['vpt'] > df['sma_20']
        df['sell_signal'] = df['vpt'] < df['sma_20']
        return df
    except Exception as e:
        print(f'Error calculating VPT: {e}')
        return None

def calculate_position_size(initial_capital, risk_per_trade, current_price):
    try:
        position_size = (initial_capital * risk_per_trade) / current_price
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def generate_trades(df):
    try:
        trades = []
        position = 0
        for i in range(len(df)):
            if df['buy_signal'].iloc[i] and position == 0:
                shares = calculate_position_size(100000, 0.01, df['close'].iloc[i])
                trades.append({
                    'type': 'buy',
                    'price': df['close'].iloc[i],
                    'time': df.index[i].strftime('%Y-%m-%dT%H:%M:%S'),
                    'shares': shares
                })
                position = 1
            elif df['sell_signal'].iloc[i] and position == 1:
                shares = calculate_position_size(100000, 0.01, df['close'].iloc[i])
                trades.append({
                    'type': 'sell',
                    'price': df['close'].iloc[i],
                    'time': df.index[i].strftime('%Y-%m-%dT%H:%M:%S'),
                    'shares': shares
                })
                position = 0
        return trades
    except Exception as e:
        print(f'Error generating trades: {e}')
        return []

def main():
    try:
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        symbol = 'QQQ'
        
        data = get_historical_data(symbol, start_date, end_date)
        if data is None:
            return
            
        df = calculate_vpt(data)
        if df is None:
            return
            
        trades = generate_trades(df)
        if not trades:
            print('No trades generated')
            return
            
        performance = {
            'total_profit': sum((trade['price'] * trade['shares']) if trade['type'] == 'sell' else (-trade['price'] * trade['shares']) for trade in trades),
            'number_of_trades': len(trades),
            'win_rate': sum(1 for trade in trades if trade['type'] == 'sell' and trade['price'] > trades[trades.index(trade)-1]['price']) / (len(trades)/2)
        }
        
        results = {
            'performance': performance,
            'trades': trades
        }
        
        with open('strategy_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Results exported to strategy_results.json')
        
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()