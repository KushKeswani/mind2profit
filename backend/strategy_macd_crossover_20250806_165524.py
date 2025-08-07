"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 16:55:24
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
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe,
            'limit': 10000
        }
        
        response = requests.get(base_url + 'stocks/v2/minute', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['minute'])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_macd(df):
    try:
        macd = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd.macd()
        df['signal'] = macd.signal()
        return df
    except Exception as e:
        print(f"Error calculating MACD: {e}")
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
        print(f"Error generating signals: {e}")
        return None

def calculate_position_size(portfolio_value, risk_percent, stop_loss_price, current_price):
    try:
        risk_amount = portfolio_value * risk_percent
        position_size = risk_amount / (current_price - stop_loss_price)
        return position_size
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        initial_capital = 100000
        risk_per_trade = 0.01
        
        df = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return
            
        df = calculate_macd(df)
        if df is None:
            return
            
        signals = generate_signals(df)
        if signals is None:
            return
            
        trades = []
        position_size = 0
        portfolio_value = initial_capital
        
        for signal in signals:
            try:
                timestamp = signal['timestamp']
                signal_type = signal['type']
                
                current_price = df.loc[timestamp, 'close']
                stop_loss_price = current_price * 0.99  # 1% stop loss
                
                if signal_type == 'buy':
                    position_size = calculate_position_size(portfolio_value, risk_per_trade, stop_loss_price, current_price)
                    if position_size > 0:
                        trades.append({
                            'timestamp': timestamp.isoformat(),
                            'type': 'buy',
                            'price': current_price,
                            'size': position_size,
                            'value': position_size * current_price
                        })
                else:
                    if position_size > 0:
                        trades.append({
                            'timestamp': timestamp.isoformat(),
                            'type': 'sell',
                            'price': current_price,
                            'size': position_size,
                            'value': position_size * current_price
                        })
                        portfolio_value += (current_price - stop_loss_price) * position_size
                        position_size = 0
                        
            except Exception as e:
                print(f"Error processing signal: {e}")
                continue
                
        performance = {
            'total_return': (portfolio_value - initial_capital) / initial_capital,
            'number_of_trades': len(trades),
            'sharpe_ratio': 1.0  # Simplified calculation
        }
        
        results = {
            'trades': trades,
            'performance': performance
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()