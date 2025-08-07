"""
Generated Strategy: test
Description: test
Generated: 2025-08-02 23:19:45
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

# API Configuration
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'

def fetch_data(symbol, start_date, end_date):
    try:
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
        response = requests.get(f'{ALPACA_BASE_URL}/v2/data/historic/trades', headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError('No data returned from Alpaca API')
        df = pd.DataFrame(data['trades'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        # Calculate common technical indicators
        df['SMA_20'] = df['price'].rolling(window=20).mean()
        df['EMA_20'] = df['price'].ewm(span=20, adjust=False).mean()
        df['RSI'] = ta.momentum.RSIIndicator(df['price']).rsi()
        df['MACD'], df['MACD_signal'], df['MACD_hist'] = ta.trend.MACD(df['price']).macd(), ta.trend.MACD(df['price']).macd_signal(), ta.trend.MACD(df['price']).macd_hist()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def strategy_logic(df):
    try:
        signals = df.copy()
        signals['buy'] = False
        signals['sell'] = False
        
        # Example strategy logic (replace with actual strategy)
        signals.loc[(df['SMA_20'] > df['EMA_20']) & (df['RSI'] < 70), 'buy'] = True
        signals.loc[(df['SMA_20'] < df['EMA_20']) & (df['RSI'] > 30), 'sell'] = True
        
        return signals
    except Exception as e:
        print(f'Error in strategy logic: {e}')
        return None

def calculate_position_size(portfolio_value, risk_per_trade, stop_loss_price, current_price):
    try:
        risk_amount = portfolio_value * risk_per_trade
        position_size = risk_amount / (current_price - stop_loss_price)
        return int(position_size)
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def execute_trade(symbol, quantity, side):
    try:
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        data = {
            'symbol': symbol,
            'qty': quantity,
            'side': side,
            'type': 'market',
            'time_in_force': 'gtc'
        }
        response = requests.post(f'{ALPACA_BASE_URL}/v2/orders', headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f'Error executing trade: {e}')
        return None

def analyze_results(trades):
    try:
        total_profit = sum(t['pnl'] for t in trades)
        num_trades = len(trades)
        win_rate = sum(1 for t in trades if t['pnl'] > 0) / num_trades if num_trades > 0 else 0
        max_drawdown = max((max(trades[:i+1]['cumulative']) - trades[i]['cumulative']) for i in range(len(trades))) if trades else 0
        sharpe_ratio = total_profit / (max_drawdown * len(trades)) if max_drawdown != 0 else 0
        
        return {
            'total_profit': total_profit,
            'num_trades': num_trades,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio
        }
    except Exception as e:
        print(f'Error analyzing results: {e}')
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        risk_per_trade = 0.01
        
        # Fetch data
        df = fetch_data(symbol, start_date, end_date)
        if df is None:
            return
        
        # Calculate indicators
        df = calculate_indicators(df)
        if df is None:
            return
        
        # Generate signals
        signals = strategy_logic(df)
        if signals is None:
            return
        
        # Simulate trading
        trades = []
        position = 0
        portfolio_value = 100000  # Initial portfolio value
        
        for index, row in signals.iterrows():
            if row['buy'] and position == 0:
                # Calculate position size
                stop_loss_price = row['price'] * 0.99  # Example stop loss
                position_size = calculate_position_size(portfolio_value, risk_per_trade, stop_loss_price, row['price'])
                
                # Execute buy
                trade = execute_trade(symbol, position_size, 'buy')
                if trade:
                    position = 1
                    trades.append({
                        'entry_time': index,
                        'entry_price': row['price'],
                        'quantity': position_size,
                        'side': 'buy'
                    })
            
            elif row['sell'] and position == 1:
                # Execute sell
                trade = execute_trade(symbol, position_size, 'sell')
                if trade:
                    position = 0
                    exit_price = row['price']
                    pnl = (exit_price - trades[-1]['entry_price']) * position_size
                    trades[-1]['exit_time'] = index
                    trades[-1]['exit_price'] = exit_price
                    trades[-1]['pnl'] = pnl
        
        # Calculate cumulative returns
        cumulative = 0
        for trade in trades:
            cumulative += trade['pnl']
            trade['cumulative'] = cumulative
        
        # Analyze results
        results = analyze_results(trades)
        if results is None:
            return
        
        # Export results to JSON
        results_json = {
            'trades': trades,