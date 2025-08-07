"""
Generated Strategy: Moving Average Crossover
Description: Buy when short SMA crosses above long SMA, sell when it crosses below. Use 20-period and 50-period simple moving averages.
Generated: 2025-08-06 18:28:58
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

def get_alpaca_data(symbol, start_date, end_date, api_key, api_secret):
    base_url = 'https://paper-api.alpaca.markets'
    endpoint = f'/v2/data/{symbol}/bars?timeframe=1Min&start={start_date}&end={end_date}'
    headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}
    try:
        response = requests.get(base_url + endpoint, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_smas(data, short_period, long_period):
    data['sma_short'] = data['close'].rolling(short_period).mean()
    data['sma_long'] = data['close'].rolling(long_period).mean()
    return data

def generate_signals(data):
    data['signal'] = 0
    data.loc[data['sma_short'] > data['sma_long'], 'signal'] = 1
    data.loc[data['sma_short'] < data['sma_long'], 'signal'] = -1
    return data

def calculate_position_size(portfolio_value, risk_per_trade, stop_loss):
    position_size = (portfolio_value * risk_per_trade) / stop_loss
    return position_size

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    short_period = 20
    long_period = 50
    risk_per_trade = 0.01
    initial_capital = 100000
    
    api_key = 'PK0F1YSWGZYNHF1VKOY5'
    api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
    
    data = get_alpaca_data(symbol, start_date, end_date, api_key, api_secret)
    if data is None:
        return
    
    data = calculate_smas(data, short_period, long_period)
    data = generate_signals(data)
    
    trades = []
    position_size = 0
    portfolio_value = initial_capital
    stop_loss_pct = 0.02
    
    for index, row in data.iterrows():
        if row['signal'] == 1:
            stop_loss = row['close'] * stop_loss_pct
            position_size = calculate_position_size(portfolio_value, risk_per_trade, stop_loss)
            trades.append({
                'entry_time': index,
                'entry_price': row['close'],
                'position_size': position_size,
                'type': 'buy'
            })
        elif row['signal'] == -1 and position_size > 0:
            exit_price = row['close']
            pnl = (exit_price - trades[-1]['entry_price']) * position_size
            portfolio_value += pnl
            trades[-1]['exit_time'] = index
            trades[-1]['exit_price'] = exit_price
            trades[-1]['pnl'] = pnl
            position_size = 0
    
    performance = {
        'total_return': (portfolio_value - initial_capital) / initial_capital,
        'number_of_trades': len(trades),
        'sharpe_ratio': (portfolio_value - initial_capital) / (sum([t['pnl'] for t in trades]) / len(trades))
    }
    
    results = {
        'trades': trades,
        'performance': performance
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, default=str)
    
    print('Backtest completed successfully!')

if __name__ == "__main__":
    main()