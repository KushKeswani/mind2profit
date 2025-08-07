"""
Generated Strategy: test
Description: Moving average crossover strategy
Generated: 2025-08-02 23:31:13
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
        
        start_date = start_date + 'T00:00:00-05:00'
        end_date = end_date + 'T23:59:59-05:00'
        
        params = {
            'symbol': symbol,
            'timeframe': timeframe,
            'start': start_date,
            'end': end_date,
            'limit': 10000
        }
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df, short_ma, long_ma):
    try:
        df['short_ma'] = df['close'].rolling(window=short_ma).mean()
        df['long_ma'] = df['close'].rolling(window=long_ma).mean()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def generate_trades(df):
    try:
        trades = []
        active_trade = None
        
        for i in range(len(df)):
            if df['short_ma'].iloc[i] > df['long_ma'].iloc[i] and active_trade is None:
                active_trade = {
                    'entry_time': df['timestamp'].iloc[i],
                    'entry_price': df['close'].iloc[i],
                    'position_size': None
                }
            elif df['short_ma'].iloc[i] < df['long_ma'].iloc[i] and active_trade is not None:
                active_trade['exit_time'] = df['timestamp'].iloc[i]
                active_trade['exit_price'] = df['close'].iloc[i]
                trades.append(active_trade)
                active_trade = None
                
        if active_trade:
            active_trade['exit_time'] = df['timestamp'].iloc[-1]
            active_trade['exit_price'] = df['close'].iloc[-1]
            trades.append(active_trade)
            
        return trades
    except Exception as e:
        print(f'Error generating trades: {e}')
        return []

def calculate_position_size(account_balance, risk_per_trade, stop_loss):
    try:
        position_size = (account_balance * risk_per_trade) / stop_loss
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def run_backtest(symbol, start_date, end_date, timeframe, short_ma, long_ma, risk_per_trade):
    try:
        df = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return None
            
        df = calculate_indicators(df, short_ma, long_ma)
        if df is None:
            return None
            
        trades = generate_trades(df)
        if not trades:
            return None
            
        account_balance = 100000  # Initial account balance
        position_size = calculate_position_size(account_balance, risk_per_trade, 0.01)
        
        results = {
            'trades': [],
            'total_return': 0,
            'number_of_trades': 0,
            'win_rate': 0
        }
        
        for trade in trades:
            results['trades'].append({
                'entry_time': str(trade['entry_time']),
                'entry_price': trade['entry_price'],
                'exit_time': str(trade['exit_time']),
                'exit_price': trade['exit_price'],
                'position_size': position_size
            })
            
            results['total_return'] += (trade['exit_price'] - trade['entry_price']) / trade['entry_price']
            results['number_of_trades'] += 1
            
        results['win_rate'] = sum(1 for trade in trades if trade['exit_price'] > trade['entry_price']) / len(trades)
        
        return results
    except Exception as e:
        print(f'Error running backtest: {e}')
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        short_ma = 20
        long_ma = 50
        risk_per_trade = 0.01
        
        results = run_backtest(symbol, start_date, end_date, timeframe, short_ma, long_ma, risk_per_trade)
        
        if results:
            with open('backtest_results.json', 'w') as f:
                json.dump(results, f, indent=4)
            print('Backtest results exported to backtest_results.json')
        else:
            print('Backtest failed')
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == "__main__":
    main()