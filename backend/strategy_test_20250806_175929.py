"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 17:59:29
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
            'timeframe': timeframe
        }
        
        response = requests.get(base_url + 'stocks/' + symbol + '/bars', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_position_size(portfolio_value, risk_per_trade, stop_loss_pct):
    try:
        position_size = portfolio_value * risk_per_trade
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    risk_per_trade = 0.01
    
    data = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if data is None:
        return
    
    data['datetime'] = pd.to_datetime(data['timestamp'])
    data.set_index('datetime', inplace=True)
    
    data['SMA_20'] = data['close'].rolling(20).mean()
    data['SMA_50'] = data['close'].rolling(50).mean()
    
    data['signal'] = 0
    data.loc[data['SMA_20'] > data['SMA_50'], 'signal'] = 1
    data.loc[data['SMA_20'] < data['SMA_50'], 'signal'] = -1
    
    trades = []
    position_size = calculate_position_size(100000, risk_per_trade, 0.02)
    
    for i in range(1, len(data)):
        if data.iloc[i-1]['signal'] == 1 and data.iloc[i]['signal'] == 0:
            trades.append({
                'type': 'sell',
                'price': data.iloc[i]['close'],
                'quantity': position_size / data.iloc[i]['close'],
                'timestamp': data.iloc[i]['timestamp']
            })
        elif data.iloc[i-1]['signal'] == -1 and data.iloc[i]['signal'] == 0:
            trades.append({
                'type': 'buy',
                'price': data.iloc[i]['close'],
                'quantity': position_size / data.iloc[i]['close'],
                'timestamp': data.iloc[i]['timestamp']
            })
    
    results = {
        'trades': trades,
        'performance': {
            'total_trades': len(trades),
            'profit': sum([trade['price'] * trade['quantity'] for trade in trades if trade['type'] == 'sell']) - sum([trade['price'] * trade['quantity'] for trade in trades if trade['type'] == 'buy']),
            'win_rate': len([trade for trade in trades if (trade['type'] == 'sell' and trade['price'] > 0) or (trade['type'] == 'buy' and trade['price'] > 0)]) / len(trades) if trades else 0
        }
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()