"""
Generated Strategy: Bollinger Bands Strategy
Description: Buy when price touches lower Bollinger Band, sell when it reaches upper band
Generated: 2025-08-05 18:06:07
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
        endpoint = f'stocks/{symbol}/bars?timeframe=1Min&start={start_date}&end={end_date}'
        
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        
        response = requests.get(base_url + endpoint, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_position_size(risk_amount, stop_loss):
    try:
        position_size = risk_amount / stop_loss
        return position_size
    except:
        return 0

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    risk_per_trade = 0.01  # 1.0%
    
    # Fetch historical data
    data = get_historical_data(symbol, start_date, end_date)
    if data is None:
        return
    
    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    # Calculate Bollinger Bands
    df['bb_lower'], df['bb_middle'], df['bb_upper'] = ta.volatility.BollingerBands(
        close=df['close'],
        window=20,
        window_dev=2
    ).bollinger_lband(), ta.volatility.BollingerBands(
        close=df['close'],
        window=20,
        window_dev=2
    ).bollinger_mavg(), ta.volatility.BollingerBands(
        close=df['close'],
        window=20,
        window_dev=2
    ).bollinger_hband()
    
    # Initialize trade list
    trades = []
    
    # Strategy execution
    position = None
    for index, row in df.iterrows():
        if position is None:
            # Buy signal: price touches lower band
            if row['close'] <= row['bb_lower']:
                position = {
                    'entry_time': index,
                    'entry_price': row['close'],
                    'quantity': None
                }
                
                # Calculate position size based on risk
                stop_loss = row['entry_price'] - row['bb_lower']
                position_size = calculate_position_size(risk_per_trade * 100000, stop_loss)
                position['quantity'] = position_size
        
        else:
            # Sell signal: price reaches upper band
            if row['close'] >= row['bb_upper']:
                position['exit_time'] = index
                position['exit_price'] = row['close']
                position['profit'] = position['exit_price'] - position['entry_price']
                trades.append(position)
                position = None
    
    # Calculate performance metrics
    total_profit = sum(trade['profit'] for trade in trades)
    num_trades = len(trades)
    try:
        sharpe_ratio = (total_profit / num_trades) / (sum(abs(t['profit']) for t in trades) / num_trades)
    except:
        sharpe_ratio = 0
    
    # Prepare results for JSON
    results = {
        'trades': trades,
        'total_profit': total_profit,
        'num_trades': num_trades,
        'sharpe_ratio': sharpe_ratio
    }
    
    # Export to JSON
    with open('bollinger_bands_strategy_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()