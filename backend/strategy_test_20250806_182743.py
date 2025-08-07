"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 18:27:43
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

def get_data(symbol, start_date, end_date, timeframe):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        
        headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe
        }
        
        response = requests.get(base_url + 'stocks/' + symbol + '/bars', params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame([x['close'] for x in data], index=pd.to_datetime([x['t'] for x in data]), columns=['close'])
            return df
        else:
            print(f"Error fetching data: {response.text}")
            return None
    except Exception as e:
        print(f"Error in get_data: {e}")
        return None

def calculate_indicators(df, short_ma, long_ma):
    try:
        df['short_ma'] = df['close'].rolling(window=short_ma).mean()
        df['long_ma'] = df['close'].rolling(window=long_ma).mean()
        return df
    except Exception as e:
        print(f"Error in calculate_indicators: {e}")
        return None

def calculate_position_size(account_balance, risk_percent, stop_loss):
    try:
        position_size = (account_balance * risk_percent) / stop_loss
        return position_size
    except Exception as e:
        print(f"Error in calculate_position_size: {e}")
        return 0

def generate_signals(df):
    try:
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0.0
        signals['position'] = 'flat'
        
        for i in range(1, len(df)):
            if df['short_ma'].iloc[i] > df['long_ma'].iloc[i] and df['short_ma'].iloc[i-1] < df['long_ma'].iloc[i-1]:
                signals['signal'].iloc[i] = 1.0
                signals['position'].iloc[i] = 'long'
            elif df['short_ma'].iloc[i] < df['long_ma'].iloc[i] and df['short_ma'].iloc[i-1] > df['long_ma'].iloc[i-1]:
                signals['signal'].iloc[i] = -1.0
                signals['position'].iloc[i] = 'short'
        
        return signals
    except Exception as e:
        print(f"Error in generate_signals: {e}")
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        short_ma = 20
        long_ma = 50
        risk_percent = 0.01
        
        df = get_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return
        
        df = calculate_indicators(df, short_ma, long_ma)
        if df is None:
            return
        
        signals = generate_signals(df)
        if signals is None:
            return
        
        account_balance = 100000.0
        position_size = calculate_position_size(account_balance, risk_percent, 0.01)
        
        trade_list = []
        for i in range(len(signals)):
            if signals['position'].iloc[i] != 'flat':
                trade = {
                    'timestamp': signals.index[i].strftime('%Y-%m-%dT%H:%M:%S'),
                    'symbol': symbol,
                    'position': signals['position'].iloc[i],
                    'size': position_size,
                    'price': df['close'].iloc[i]
                }
                trade_list.append(trade)
        
        results = {
            'symbol': symbol,
            'timeframe': timeframe,
            'start_date': start_date,
            'end_date': end_date,
            'total_trades': len(trade_list),
            'profit': sum([trade['size'] * (trade['price'] - trade['price'] * 0.001) for trade in trade_list]),
            'loss': sum([trade['size'] * (trade['price'] * 0.001 - trade['price']) for trade in trade_list]),
            'trades': trade_list
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=4)
            
        print("Backtest completed successfully. Results saved to backtest_results.json")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()