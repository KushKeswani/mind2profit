"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 13:28:04
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
        
        start_date = start_date + 'T00:00:00'
        end_date = end_date + 'T23:59:59'
        
        url = f'{base_url}stocks/{symbol}/bars?timeframe={timeframe}&start={start_date}&end={end_date}'
        
        headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['bars'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            return df
        else:
            print(f'Error fetching data: {response.text}')
            return None
    except Exception as e:
        print(f'Error in get_alpaca_data: {e}')
        return None

def calculate_macd(df):
    try:
        macd = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd.macd()
        df['signal'] = macd.signal()
        return df
    except Exception as e:
        print(f'Error calculating MACD: {e}')
        return None

def generate_signals(df):
    try:
        signals = []
        for i in range(1, len(df)):
            prev_macd = df['macd'].iloc[i-1]
            curr_macd = df['macd'].iloc[i]
            prev_signal = df['signal'].iloc[i-1]
            curr_signal = df['signal'].iloc[i]
            
            if curr_macd > curr_signal and prev_macd <= prev_signal:
                signals.append({'timestamp': df.index[i], 'type': 'buy'})
            elif curr_macd < curr_signal and prev_macd >= prev_signal:
                signals.append({'timestamp': df.index[i], 'type': 'sell'})
        return signals
    except Exception as e:
        print(f'Error generating signals: {e}')
        return None

def calculate_position_size(portfolio_value, risk_per_trade, stop_loss_pct):
    try:
        risk_amount = portfolio_value * risk_per_trade
        stop_loss = portfolio_value * stop_loss_pct
        position_size = risk_amount / stop_loss
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def backtest_strategy(symbol, start_date, end_date, timeframe, risk_per_trade):
    try:
        df = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return None
            
        df = calculate_macd(df)
        if df is None:
            return None
            
        signals = generate_signals(df)
        if signals is None:
            return None
        
        portfolio_value = 100000
        position_size = 0
        trades = []
        wins = 0
        losses = 0
        
        for signal in signals:
            if signal['type'] == 'buy':
                shares = calculate_position_size(portfolio_value, risk_per_trade, 0.02)
                if shares > 0:
                    trades.append({
                        'timestamp': signal['timestamp'].strftime('%Y-%m-%dT%H:%M:%S'),
                        'type': 'buy',
                        'shares': int(shares),
                        'price': df.loc[signal['timestamp'], 'close']
                    })
            elif signal['type'] == 'sell':
                if position_size > 0:
                    trades.append({
                        'timestamp': signal['timestamp'].strftime('%Y-%m-%dT%H:%M:%S'),
                        'type': 'sell',
                        'shares': int(position_size),
                        'price': df.loc[signal['timestamp'], 'close']
                    })
        
        total_return = 1.0
        for trade in trades:
            if trade['type'] == 'buy':
                position_size = trade['shares']
            else:
                if position_size > 0:
                    profit = (trade['price'] - df.loc[trade['timestamp'] - timedelta(minutes=1), 'close']) / df.loc[trade['timestamp'] - timedelta(minutes=1), 'close']
                    total_return *= (1 + profit)
                    if profit > 0:
                        wins += 1
                    else:
                        losses += 1
                    position_size = 0
        
        sharpe_ratio = (total_return - 1) / (len(trades) ** 0.5) if len(trades) > 0 else 0
        
        results = {
            'trades': trades,
            'performance': {
                'total_return': total_return,
                'number_of_trades': len(trades),
                'win_rate': wins / (wins + losses) if (wins + losses) > 0 else 0,
                'sharpe_ratio': sharpe_ratio
            }
        }
        
        return results
    except Exception as e:
        print(f'Error in backtest_strategy: {e}')
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        risk_per_trade = 0.01
        
        results = backtest_strategy(symbol, start_date, end_date, timeframe, risk_per_trade)
        
        if results is not None:
            with open('backtest_results.json', 'w') as f:
                json.dump(results, f, default=str)
            print('Backtest results exported to backtest_results.json')
        else:
            print('Backtest failed')
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == "__main__":
    main()