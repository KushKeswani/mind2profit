"""
Generated Strategy: Bollinger Bands Strategy
Description: Buy when price touches lower band, sell when it reaches middle band. Use 20-period with 2 standard deviations.
Generated: 2025-08-06 19:03:11
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API keys
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def get_bollinger_bands(data, period=20, std_dev=2):
    data['tp'] = (data['high'] + data['low'] + data['close']) / 3
    data['ma'] = data['tp'].rolling(window=period).mean()
    data['std'] = data['tp'].rolling(window=period).std()
    data['upper_band'] = data['ma'] + std_dev * data['std']
    data['lower_band'] = data['ma'] - std_dev * data['std']
    return data

def get_historical_data(symbol, start_date, end_date):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': '1Min',
            'limit': 10000
        }
        response = requests.get(base_url + 'stocks/v2/historic/prices', headers=headers, params=params)
        if response.status_code == 200:
            data = json.loads(response.content)
            df = pd.DataFrame([x['close'] for x in data['prices']], index=pd.to_datetime([x['date'] for x in data['prices']]), columns=['close'])
            df = df.reset_index()
            df.columns = ['time', 'close']
            df['open'] = df['close'].rolling(window=1).apply(lambda x: x)
            df['high'] = df['close'].rolling(window=1).apply(lambda x: x)
            df['low'] = df['close'].rolling(window=1).apply(lambda x: x)
            return df
        return None
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_position_size(current_price, risk_amount, stop_loss):
    try:
        position_size = risk_amount / (stop_loss / current_price)
        return position_size
    except:
        return 0

def backtest_strategy(data, initial_capital=100000):
    try:
        data = get_bollinger_bands(data)
        trades = []
        position = 0
        capital = initial_capital
        risk_amount = 0.01 * capital
        
        for i in range(len(data)):
            if i < 20:
                continue
                
            current_price = data.iloc[i]['close']
            lower_band = data.iloc[i]['lower_band']
            middle_band = data.iloc[i]['ma']
            
            if position == 0 and current_price <= lower_band:
                position_size = calculate_position_size(current_price, risk_amount, current_price - lower_band)
                if position_size > 0:
                    position = position_size
                    capital -= position_size * current_price
                    trades.append({
                        'type': 'buy',
                        'price': current_price,
                        'size': position_size,
                        'time': data.iloc[i]['time']
                    })
                    
            elif position > 0 and current_price >= middle_band:
                position_size = position
                capital += position_size * current_price
                position = 0
                trades.append({
                    'type': 'sell',
                    'price': current_price,
                    'size': position_size,
                    'time': data.iloc[i]['time']
                })
                
        performance = {
            'total_profit': capital - initial_capital,
            'number_of_trades': len(trades),
            'win_rate': sum(1 for trade in trades if trade['type'] == 'sell') / (len(trades)/2) if trades else 0
        }
        
        return trades, performance
    except Exception as e:
        print(f'Error in backtest: {e}')
        return None, None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        data = get_historical_data(symbol, start_date, end_date)
        if data is not None:
            trades, performance = backtest_strategy(data)
            if trades and performance:
                results = {
                    'trades': trades,
                    'performance': performance
                }
                with open('backtest_results.json', 'w') as f:
                    json.dump(results, f)
                print('Backtest completed successfully')
            else:
                print('No trades executed')
        else:
            print('Failed to fetch data')
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == "__main__":
    main()