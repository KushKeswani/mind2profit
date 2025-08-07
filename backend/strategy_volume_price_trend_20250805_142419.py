"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-05 14:24:19
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, start_date, end_date):
    try:
        endpoint = f'{BASE_URL}/v2/data/{symbol}/bars?timeframe=1Min&start={start_date}&end={end_date}'
        headers = {'APCA-API-KEY-ID': ALPACA_API_KEY, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY}
        response = requests.get(endpoint, headers=headers)
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['volume_sma'] = df['volume'].rolling(20).mean()
        df['price_change'] = df['close'].pct_change()
        df['volume_change'] = df['volume'].pct_change()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def generate_signals(df):
    try:
        signals = []
        for i in range(len(df)):
            if df['volume_change'][i] > 0.5 and df['price_change'][i] > 0:
                signals.append({'timestamp': df.index[i], 'type': 'buy'})
            elif df['volume_change'][i] < -0.5 and df['price_change'][i] < 0:
                signals.append({'timestamp': df.index[i], 'type': 'sell'})
        return signals
    except Exception as e:
        print(f'Error generating signals: {e}')
        return None

def calculate_position_size(portfolio_value, risk_per_trade, stop_loss):
    try:
        position_size = (portfolio_value * risk_per_trade) / stop_loss
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def backtest_strategy():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        initial_capital = 100000
        risk_per_trade = 0.01
        
        df = get_data(symbol, start_date, end_date)
        if df is None:
            return None
            
        df = calculate_indicators(df)
        if df is None:
            return None
        
        signals = generate_signals(df)
        if signals is None:
            return None
        
        trades = []
        position_size = 0
        portfolio_value = initial_capital
        
        for signal in signals:
            try:
                timestamp = signal['timestamp']
                row = df.loc[df.index == timestamp]
                if row.empty:
                    continue
                
                close_price = row['close'].values[0]
                volume = row['volume'].values[0]
                
                if signal['type'] == 'buy':
                    stop_loss = close_price - (close_price * 0.02)
                    position_size = calculate_position_size(portfolio_value, risk_per_trade, close_price - stop_loss)
                    shares = position_size / close_price
                    trades.append({
                        'timestamp': timestamp,
                        'type': 'buy',
                        'price': close_price,
                        'shares': shares,
                        'position_size': position_size
                    })
                    portfolio_value += (close_price - stop_loss) * shares
                elif signal['type'] == 'sell':
                    stop_loss = close_price + (close_price * 0.02)
                    position_size = calculate_position_size(portfolio_value, risk_per_trade, stop_loss - close_price)
                    shares = position_size / close_price
                    trades.append({
                        'timestamp': timestamp,
                        'type': 'sell',
                        'price': close_price,
                        'shares': shares,
                        'position_size': position_size
                    })
                    portfolio_value -= (stop_loss - close_price) * shares
            except Exception as e:
                print(f'Error executing trade: {e}')
                continue
        
        return {
            'trades': trades,
            'metrics': {
                'initial_capital': initial_capital,
                'final_capital': portfolio_value,
                'number_of_trades': len(trades),
                'profit_factor': portfolio_value - initial_capital
            }
        }
    except Exception as e:
        print(f'Error in backtest_strategy: {e}')
        return None

def export_to_json(results, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        return True
    except Exception as e:
        print(f'Error exporting to JSON: {e}')
        return False

def main():
    try:
        results = backtest_strategy()
        if results is not None:
            export_to_json(results, 'backtest_results.json')
            print('Backtest completed successfully')
        else:
            print('Backtest failed')
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == "__main__":
    main()