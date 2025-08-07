"""
Generated Strategy: Bollinger Bands Strategy
Description: Buy when price touches lower band, sell when it reaches middle band. Use 20-period with 2 standard deviations.
Generated: 2025-08-06 18:33:24
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

# Set Alpaca API credentials
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_historical_data(symbol, start_date, end_date):
    try:
        endpoint = f'{BASE_URL}/v2/data/{symbol}/bars?timeframe=1Min&start={start_date}&end={end_date}'
        headers = {'APCA-API-KEY-ID': ALPACA_API_KEY, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY}
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_bollinger_bands(df, period=20, std_dev=2):
    df['bb_middle'] = df['close'].rolling(window=period).mean()
    df['bb_upper'] = df['bb_middle'] + std_dev*df['close'].rolling(window=period).std()
    df['bb_lower'] = df['bb_middle'] - std_dev*df['close'].rolling(window=period).std()
    return df

def generate_signals(df):
    df['buy_signal'] = 0
    df['sell_signal'] = 0
    df['buy_signal'][(df['close'] <= df['bb_lower']) & (df['close'].shift(1) > df['bb_lower'].shift(1))] = 1
    df['sell_signal'][(df['close'] >= df['bb_middle']) & (df['close'].shift(1) < df['bb_middle'].shift(1))] = 1
    return df

def calculate_position_size(portfolio_value, risk_percent, stop_loss):
    position_size = (portfolio_value * risk_percent) / stop_loss
    return position_size

def backtest_strategy():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        df = get_historical_data(symbol, start_date, end_date)
        if df is None:
            return None
            
        df = calculate_bollinger_bands(df)
        df = generate_signals(df)
        
        initial_capital = 100000
        portfolio_value = initial_capital
        risk_per_trade = 0.01
        
        trades = []
        position = 0
        entry_price = 0
        
        for index, row in df.iterrows():
            if row['buy_signal'] == 1 and position == 0:
                entry_price = row['close']
                stop_loss = entry_price - row['close'].rolling(window=20).std().iloc[-1]
                position_size = calculate_position_size(portfolio_value, risk_per_trade, abs(stop_loss))
                position = position_size
                trades.append({
                    'type': 'buy',
                    'timestamp': index.isoformat(),
                    'price': entry_price,
                    'size': position_size
                })
            elif row['sell_signal'] == 1 and position > 0:
                exit_price = row['close']
                profit = (exit_price - entry_price) * position
                portfolio_value += profit
                trades.append({
                    'type': 'sell',
                    'timestamp': index.isoformat(),
                    'price': exit_price,
                    'size': position_size
                })
                position = 0
        
        results = {
            'trades': trades,
            'initial_capital': initial_capital,
            'final_capital': portfolio_value,
            'total_trades': len(trades),
            'profit': portfolio_value - initial_capital
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        return results
    except Exception as e:
        print(f'Error in backtest: {e}')
        return None

def main():
    results = backtest_strategy()
    if results:
        print('Backtest completed successfully')
        print(f'Profit: ${results["profit"]:.2f}')
        print(f'Total Trades: {results["total_trades"]}')
    else:
        print('Backtest failed')

if __name__ == "__main__":
    main()