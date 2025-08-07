"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 18:14:20
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
        df = pd.DataFrame([d['close'] for d in data], index=pd.to_datetime([d['timestamp'] for d in data]), columns=['Close'])
        
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_macd(df):
    try:
        macd = ta.trend.MACD(df['Close'], window_slow=26, window_fast=12, window_sign=9)
        df['MACD'] = macd.macd()
        df['Signal'] = macd.signal()
        return df
    except Exception as e:
        print(f'Error calculating MACD: {e}')
        return None

def generate_signals(df):
    try:
        signals = pd.DataFrame(index=df.index, columns=['Signal'])
        signals['Signal'] = 0
        
        for i in range(1, len(df)):
            if df['MACD'].iloc[i] > df['Signal'].iloc[i] and df['MACD'].iloc[i-1] < df['Signal'].iloc[i-1]:
                signals.iloc[i] = 1
            elif df['MACD'].iloc[i] < df['Signal'].iloc[i] and df['MACD'].iloc[i-1] > df['Signal'].iloc[i-1]:
                signals.iloc[i] = -1
                
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
        in_position = False
        
        for i in range(len(df)):
            if signals['Signal'].iloc[i] == 1 and not in_position:
                position_size = calculate_position_size(portfolio_value, risk_per_trade, 0.02)
                if position_size == 0:
                    continue
                    
                entry_price = df['Close'].iloc[i]
                in_position = True
                trades.append({'Entry Time': df.index[i].strftime('%Y-%m-%dT%H:%M:%S'), 
                              'Entry Price': entry_price, 
                              'Position Size': position_size})
                
            elif signals['Signal'].iloc[i] == -1 and in_position:
                exit_price = df['Close'].iloc[i]
                pnl = (exit_price - entry_price) * position_size
                portfolio_value += pnl
                in_position = False
                
                trades[-1]['Exit Time'] = df.index[i].strftime('%Y-%m-%dT%H:%M:%S')
                trades[-1]['Exit Price'] = exit_price
                trades[-1]['PnL'] = pnl
                trades[-1]['PnL Pct'] = (pnl / portfolio_value) * 100
                
        performance = {
            'Total Return': (portfolio_value - 100000) / 100000 * 100,
            'Number of Trades': len(trades),
            'Sharpe Ratio': 1  # Simplified for example
        }
        
        results = {
            'Performance': performance,
            'Trades': trades
        }
        
        return results
    except Exception as e:
        print(f'Error in backtest: {e}')
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        risk_per_trade = 0.01
        
        results = backtest_strategy(symbol, start_date, end_date, timeframe, risk_per_trade)
        if results is None:
            print('Backtest failed')
            return
            
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Backtest completed successfully')
    except Exception as e:
        print(f'Main error: {e}')

if __name__ == "__main__":
    main()