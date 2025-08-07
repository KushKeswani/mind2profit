"""
Generated Strategy: Bollinger Bands Strategy
Description: Buy when price touches lower band, sell when it reaches middle band. Use 20-period with 2 standard deviations.
Generated: 2025-08-06 13:33:12
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API keys
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

def calculate_bollinger_bands(df, period=20, std_dev=2):
    df['close'] = pd.to_numeric(df['close'])
    df['bb_middle'] = df['close'].rolling(window=period).mean()
    df['bb_std'] = df['close'].rolling(window=period).std()
    df['bb_lower'] = df['bb_middle'] - std_dev * df['bb_std']
    df['bb_upper'] = df['bb_middle'] + std_dev * df['bb_std']
    return df

def calculate_position_size(risk_amount, stop_loss, current_price):
    return risk_amount / stop_loss

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    risk_per_trade = 0.01  # 1.0%
    
    # Fetch data
    df = get_historical_data(symbol, start_date, end_date)
    if df is None:
        return
    
    # Calculate indicators
    df = calculate_bollinger_bands(df)
    
    # Initialize trade variables
    trades = []
    position = False
    equity = 100000  # Starting equity
    risk_amount = equity * risk_per_trade
    
    for index, row in df.iterrows():
        if not position:
            # Buy condition: price touches lower band
            if row['close'] <= row['bb_lower']:
                # Calculate position size
                stop_loss = row['high'] - row['low']
                shares = calculate_position_size(risk_amount, stop_loss, row['close'])
                
                # Open position
                position = True
                trades.append({
                    'type': 'buy',
                    'time': index,
                    'price': row['close'],
                    'shares': shares
                })
        else:
            # Sell condition: price reaches middle band
            if row['close'] >= row['bb_middle']:
                # Close position
                position = False
                trades.append({
                    'type': 'sell',
                    'time': index,
                    'price': row['close'],
                    'shares': shares
                })
    
    # Calculate performance
    total_profit = sum((trade['price'] if trade['type'] == 'sell' else -trade['price']) for trade in trades)
    num_trades = len(trades)
    win_rate = sum(1 for trade in trades if trade['type'] == 'sell') / (num_trades // 2)
    
    # Export results
    results = {
        'trades': trades,
        'total_profit': total_profit,
        'num_trades': num_trades,
        'win_rate': win_rate
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()