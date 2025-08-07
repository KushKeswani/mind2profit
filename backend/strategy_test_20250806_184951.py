"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 18:49:51
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
        
        headers = {
            'APCA-API-KEY-ID': api_key,
            'APCA-API-SECRET-KEY': api_secret
        }
        
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe,
            'limit': 10000
        }
        
        response = requests.get(base_url + 'stocks/v2/ags', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_indicators(df):
    try:
        df['short_ma'] = df['close'].rolling(20).mean()
        df['long_ma'] = df['close'].rolling(50).mean()
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def get_trade_signals(df):
    try:
        signals = []
        for i in range(len(df)):
            if df['short_ma'].iloc[i] > df['long_ma'].iloc[i] and df['short_ma'].iloc[i-1] <= df['long_ma'].iloc[i-1]:
                signals.append({'type': 'buy', 'price': df['close'].iloc[i], 'time': df.index[i]})
            elif df['short_ma'].iloc[i] < df['long_ma'].iloc[i] and df['short_ma'].iloc[i-1] >= df['long_ma'].iloc[i-1]:
                signals.append({'type': 'sell', 'price': df['close'].iloc[i], 'time': df.index[i]})
        return signals
    except Exception as e:
        print(f"Error generating signals: {e}")
        return None

def calculate_position_size(balance, risk, stop_loss):
    try:
        position_size = (balance * risk) / stop_loss
        return position_size
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0

def run_backtest():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        risk_per_trade = 0.01
        
        df = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return None
            
        df = calculate_indicators(df)
        if df is None:
            return None
            
        signals = get_trade_signals(df)
        if signals is None:
            return None
        
        initial_balance = 100000
        balance = initial_balance
        position_size = 0
        trades = []
        
        for signal in signals:
            if signal['type'] == 'buy':
                stop_loss = 0.02 * signal['price']
                position_size = calculate_position_size(balance, risk_per_trade, stop_loss)
                if position_size == 0:
                    continue
                    
                take_profit = signal['price'] + (signal['price'] * 0.03)
                trades.append({
                    'type': 'buy',
                    'entry': signal['price'],
                    'exit': take_profit,
                    'size': position_size,
                    'time': signal['time'].strftime('%Y-%m-%dT%H:%M:%S'),
                    'pl': (take_profit - signal['price']) * position_size
                })
                
                balance += (take_profit - signal['price']) * position_size
                
            elif signal['type'] == 'sell':
                stop_loss = signal['price'] * 0.02
                position_size = calculate_position_size(balance, risk_per_trade, stop_loss)
                if position_size == 0:
                    continue
                    
                take_profit = signal['price'] - (signal['price'] * 0.03)
                trades.append({
                    'type': 'sell',
                    'entry': signal['price'],
                    'exit': take_profit,
                    'size': position_size,
                    'time': signal['time'].strftime('%Y-%m-%dT%H:%M:%S'),
                    'pl': (signal['price'] - take_profit) * position_size
                })
                
                balance += (signal['price'] - take_profit) * position_size
                
        metrics = {
            'initial_balance': initial_balance,
            'final_balance': balance,
            'number_of_trades': len(trades),
            'win_rate': sum(1 for trade in trades if trade['pl'] > 0) / len(trades) if trades else 0,
            'average_pl': sum(trade['pl'] for trade in trades) / len(trades) if trades else 0
        }
        
        return {'trades': trades, 'metrics': metrics, 'parameters': {
            'symbol': symbol,
            'timeframe': timeframe,
            'start_date': start_date,
            'end_date': end_date,
            'risk_per_trade': risk_per_trade
        }}
    except Exception as e:
        print(f"Error running backtest: {e}")
        return None

def main():
    try:
        backtest_results = run_backtest()
        if backtest_results is None:
            print("Backtest failed")
            return
            
        with open('backtest_results.json', 'w') as f:
            json.dump(backtest_results, f, indent=4)
            
        print("Backtest completed successfully")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()