"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 18:19:42
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
        
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()
        
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe,
            'limit': 10000
        }
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame([d['close'] for d in data], index=pd.to_datetime([d['t'] for d in data]), columns=['close'])
        
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_position_size(account_balance, risk_percent, stop_loss_pips):
    try:
        risk_amount = account_balance * risk_percent / 100
        position_size = risk_amount / stop_loss_pips
        return position_size
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0

def main():
    symbol = 'QQQ'
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 3, 1)
    timeframe = '1Min'
    risk_percent = 1.0
    
    df = get_alpaca_data(symbol, start_date, end_date, timeframe)
    
    if df is None:
        print("Failed to retrieve data")
        return
    
    df['SMA_20'] = ta.momentum.SMAIndicator(df['close'], window=20).sma_indicator
    df['SMA_50'] = ta.momentum.SMAIndicator(df['close'], window=50).sma_indicator
    
    trades = []
    account_balance = 100000
    position_size = 0
    position = 0
    
    for i in range(len(df)):
        if i < 50:
            continue
            
        current_price = df['close'].iloc[i]
        sma_20 = df['SMA_20'].iloc[i]
        sma_50 = df['SMA_50'].iloc[i]
        
        if sma_20 > sma_50 and position <= 0:
            position = 1
            position_size = account_balance * 0.01
            entry_price = current_price
            trades.append({
                'type': 'buy',
                'entry': entry_price,
                'exit': None,
                'pnl': None
            })
        
        elif sma_20 < sma_50 and position >= 0:
            position = -1
            position_size = account_balance * 0.01
            entry_price = current_price
            trades.append({
                'type': 'sell',
                'entry': entry_price,
                'exit': None,
                'pnl': None
            })
    
    results = {
        'trades': trades,
        'performance': {
            'total_pnl': account_balance - 100000,
            'win_rate': len([t for t in trades if t['pnl'] > 0]) / len(trades) if trades else 0
        }
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f)
    
    print("Backtest completed. Results saved to backtest_results.json")

if __name__ == "__main__":
    main()