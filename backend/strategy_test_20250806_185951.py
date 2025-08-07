"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 18:59:51
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

def get_data(symbol, start_date, end_date, api_key, api_secret):
    base_url = 'https://paper-api.alpaca.markets/v2/stocks/' + symbol + '/bars?'
    params = {
        'timeframe': '1Min',
        'start': start_date,
        'end': end_date
    }
    headers = {
        'APCA-API-KEY-ID': api_key,
        'APCA-API-SECRET-KEY': api_secret
    }
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_indicators(df, short_ma, long_ma):
    try:
        df['short_ma'] = df['close'].rolling(window=short_ma).mean()
        df['long_ma'] = df['close'].rolling(window=long_ma).mean()
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def generate_trades(df):
    trades = []
    in_position = False
    for i in range(len(df)):
        if df.iloc[i]['short_ma'] > df.iloc[i]['long_ma'] and not in_position:
            if i > 0:
                entry_price = df.iloc[i]['close']
                stop_loss = entry_price * 0.99  # 1% risk
                position_size = calculate_position_size(entry_price, stop_loss)
                trades.append({
                    'entry_time': df.index[i],
                    'entry_price': entry_price,
                    'position_size': position_size,
                    'status': 'open'
                })
                in_position = True
        elif df.iloc[i]['short_ma'] < df.iloc[i]['long_ma'] and in_position:
            exit_price = df.iloc[i]['close']
            pnl = (exit_price - trades[-1]['entry_price']) * trades[-1]['position_size']
            trades[-1]['exit_time'] = df.index[i]
            trades[-1]['exit_price'] = exit_price
            trades[-1]['pnl'] = pnl
            trades[-1]['status'] = 'closed'
            in_position = False
    return trades

def calculate_position_size(entry_price, stop_loss, risk_percent=0.01):
    try:
        account_balance = 100000  # Assume initial balance
        risk_amount = account_balance * risk_percent
        position_size = risk_amount / (entry_price - stop_loss)
        return int(position_size)
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0

def run_backtest(symbol, start_date, end_date, api_key, api_secret):
    df = get_data(symbol, start_date, end_date, api_key, api_secret)
    if df is None:
        return None
    df = calculate_indicators(df, 20, 50)
    if df is None:
        return None
    trades = generate_trades(df)
    return trades

def main():
    try:
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        trades = run_backtest(symbol, start_date, end_date, api_key, api_secret)
        if trades:
            with open('backtest_results.json', 'w') as f:
                json.dump(trades, f, default=str)
            print("Backtest results exported to backtest_results.json")
        else:
            print("No trades generated")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()