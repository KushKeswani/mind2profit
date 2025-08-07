"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-06 13:34:19
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API credentials
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def fetch_data(symbol, start_date, end_date):
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
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['volume_ma'] = df['volume'].rolling(20).mean()
        df['price_ma'] = df['close'].rolling(20).mean()
        df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def backtest_strategy(df, risk_per_trade):
    try:
        trades = []
        position_size = 0
        equity = 100000
        risk_amount = equity * risk_per_trade
        
        for i in range(1, len(df)):
            current_row = df.iloc[i]
            prev_row = df.iloc[i-1]
            
            # Buy signal: Price breaks above previous high with increasing volume
            if current_row['high'] > prev_row['high'] and current_row['volume'] > prev_row['volume']:
                if position_size == 0:
                    # Calculate position size based on risk management
                    stop_loss = current_row['low'] * 0.99
                    position_size = risk_amount / (current_row['close'] - stop_loss)
                    position_size = int(position_size)
                    
                    # Record trade entry
                    trades.append({
                        'entry_time': current_row.name.isoformat(),
                        'entry_price': current_row['close'],
                        'shares': position_size,
                        'type': 'buy'
                    })
                    
            # Sell signal: Price drops below previous low with decreasing volume
            elif current_row['low'] < prev_row['low'] and current_row['volume'] < prev_row['volume']:
                if position_size > 0:
                    # Record trade exit
                    exit_price = current_row['close']
                    profit = (exit_price - trades[-1]['entry_price']) * position_size
                    equity += profit
                    
                    trades[-1]['exit_time'] = current_row.name.isoformat()
                    trades[-1]['exit_price'] = exit_price
                    trades[-1]['profit'] = profit
                    position_size = 0
                    
        return trades
    except Exception as e:
        print(f'Error executing backtest: {e}')
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        risk_per_trade = 0.01
        
        df = fetch_data(symbol, start_date, end_date)
        if df is None:
            return
            
        df = calculate_indicators(df)
        if df is None:
            return
            
        trades = backtest_strategy(df, risk_per_trade)
        if trades is None:
            return
            
        # Calculate performance metrics
        total_profit = sum(t['profit'] for t in trades if 'profit' in t)
        num_trades = len([t for t in trades if 'profit' in t])
        win_rate = len([t for t in trades if t.get('profit', 0) > 0]) / num_trades if num_trades > 0 else 0
        
        # Prepare results for JSON export
        results = {
            'symbol': symbol,
            'timeframe': '1Min',
            'start_date': start_date,
            'end_date': end_date,
            'total_profit': total_profit,
            'num_trades': num_trades,
            'win_rate': win_rate,
            'trades': trades
        }
        
        # Export to JSON
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Backtest completed successfully!')
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()