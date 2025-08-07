"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 18:27:09
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
API_SECRET = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, start_date, end_date):
    try:
        headers = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': '1Min',
            'limit': 10000
        }
        response = requests.get(f'{BASE_URL}/v2/data', params=params, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json()['data'])
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['SMA_20'] = ta.momentum.SMAIndicator(df['close']).sma_indicator()
        df['SMA_50'] = ta.momentum.SMAIndicator(df['close'], window=50).sma_indicator()
        df['ATR'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
        df['RSI'] = ta.momentum.RSIIndicator(df['close']).rsi()
        df['MACD'] = ta.trend.MACD(df['close']).macd()
        df['BB_Middle'] = ta.volatility.BollingerBands(df['close']).bollinger_mavg()
        df['BB_Upper'] = ta.volatility.BollingerBands(df['close']).bollinger_hband()
        df['BB_Lower'] = ta.volatility.BollingerBands(df['close']).bollinger_lband()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def generate_signals(df):
    try:
        signals = []
        for i in range(len(df)):
            if df['SMA_20'].iloc[i] > df['SMA_50'].iloc[i] and df['SMA_20'].iloc[i-1] <= df['SMA_50'].iloc[i-1]:
                signals.append({'timestamp': df.index[i], 'type': 'buy'})
            elif df['SMA_20'].iloc[i] < df['SMA_50'].iloc[i] and df['SMA_20'].iloc[i-1] >= df['SMA_50'].iloc[i-1]:
                signals.append({'timestamp': df.index[i], 'type': 'sell'})
        return signals
    except Exception as e:
        print(f'Error generating signals: {e}')
        return []

def calculate_position_size(risk_percent, current_price, atr, equity):
    try:
        risk_amount = equity * risk_percent / 100
        position_size = risk_amount / (atr * current_price)
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        df = get_data(symbol, start_date, end_date)
        if df is None:
            return
            
        df = df.drop(columns=['exchange'])
        df.index = pd.to_datetime(df['timestamp'])
        df = df.drop(columns=['timestamp'])
        
        df = calculate_indicators(df)
        if df is None:
            return
            
        signals = generate_signals(df)
        
        trades = []
        position_size = 0
        equity = 100000  # Initial equity
        
        for signal in signals:
            try:
                timestamp = signal['timestamp']
                current_row = df.loc[timestamp]
                current_price = current_row['close']
                atr = current_row['ATR']
                
                position_size = calculate_position_size(1.0, current_price, atr, equity)
                
                if signal['type'] == 'buy':
                    trades.append({
                        'timestamp': timestamp.isoformat(),
                        'type': 'buy',
                        'price': current_price,
                        'size': position_size,
                        'risk': 1.0
                    })
                else:
                    trades.append({
                        'timestamp': timestamp.isoformat(),
                        'type': 'sell',
                        'price': current_price,
                        'size': position_size,
                        'risk': 1.0
                    })
            except Exception as e:
                print(f'Error processing signal: {e}')
                continue
        
        results = {
            'trades': trades,
            'strategy': 'test',
            'symbol': symbol,
            'timeframe': '1Min',
            'start_date': start_date,
            'end_date': end_date
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Backtest completed successfully')
        
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()