"""
Generated Strategy: RSI Oversold Bounce
Description: Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target. Use 14-period RSI with 30/50 levels.
Generated: 2025-08-01 21:09:17
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
        # Fetch 1-minute data in chunks
        bar_data = []
        current_start = start_date
        while current_start < end_date:
            current_end = min(current_start + timedelta(days=1), end_date)
            response = requests.get(
                f'{ALPACA_BASE_URL}/v2/{symbol}/bars?timeframe=1Min&start={current_start}&end={current_end}',
                headers={'APCA-API-KEY-ID': ALPACA_API_KEY, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY}
            )
            if response.status_code == 200:
                data = response.json()
                bar_data.extend(data['bars'])
                current_start = current_end
            else:
                print(f'Error fetching data: {response.text}')
                return None
        # Convert to DataFrame
        df = pd.DataFrame([{
            'timestamp': pd.to_datetime(bar['timestamp']),
            'open': float(bar['open']),
            'high': float(bar['high']),
            'low': float(bar['low']),
            'close': float(bar['close']),
            'volume': int(bar['volume'])
        } for bar in bar_data])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error in fetch_data: {str(e)}')
        return None

def calculate_indicators(df):
    try:
        # Calculate RSI with 14 periods
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        return df
    except Exception as e:
        print(f'Error in calculate_indicators: {str(e)}')
        return None

def strategy_logic(df):
    try:
        trades = []
        position = None
        entry_price = None
        for i in range(len(df)):
            if i < 14:
                continue  # Wait for RSI to be calculated
            current_row = df.iloc[i]
            
            # Buy signal: RSI crosses below 30
            if current_row['rsi'] < 30 and (df.iloc[i-1]['rsi'] >= 30 if i > 0 else True):
                if position is None:
                    position = 'long'
                    entry_price = current_row['close']
                    shares = calculate_position_size(entry_price, 0.01)
                    trades.append({
                        'type': 'buy',
                        'timestamp': current_row.name,
                        'price': entry_price,
                        'shares': shares
                    })
            
            # Sell signal: RSI crosses above 50 or reaches 2% profit
            if position == 'long':
                if current_row['rsi'] > 50 or (current_row['close'] / entry_price >= 1.02):
                    position = None
                    exit_price = current_row['close']
                    trades.append({
                        'type': 'sell',
                        'timestamp': current_row.name,
                        'price': exit_price,
                        'shares': shares
                    })
        return trades
    except Exception as e:
        print(f'Error in strategy_logic: {str(e)}')
        return None

def calculate_position_size(entry_price, risk_percent):
    try:
        # Calculate position size based on 1% risk
        # Assuming $100,000 portfolio
        portfolio_value = 100000
        risk_amount = portfolio_value * risk_percent
        position_size = risk_amount / entry_price
        return int(position_size)
    except Exception as e:
        print(f'Error in calculate_position_size: {str(e)}')
        return 0

def execute_trades(trades):
    try:
        executed_trades = []
        for trade in trades:
            try:
                if trade['type'] == 'buy':
                    # Execute buy order
                    response = requests.post(
                        f'{ALPACA_BASE_URL}/v2/orders',
                        headers={'APCA-API-KEY-ID': ALPACA_API_KEY, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY},
                        json={
                            'symbol': 'QQQ',
                            'qty': trade['shares'],
                            'side': 'buy',
                            'type': 'market',
                            'time_in_force': 'gtc'
                        }
                    )
                    executed_trades.append({
                        'type': 'buy',
                        'timestamp': trade['timestamp'],
                        'price': response.json()['filled_average_price'],
                        'shares': response.json()['filled_qty']
                    })
                elif trade['type'] == 'sell':
                    # Execute sell order
                    response = requests.post(
                        f'{ALPACA_BASE_URL}/v2/orders',
                        headers={'APCA-API-KEY-ID': ALPACA_API_KEY, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY},
                        json={
                            'symbol': 'QQQ',
                            'qty': trade['shares'],
                            'side': 'sell',
                            'type': 'market',
                            'time_in_force': 'gtc'
                        }
                    )
                    executed_trades.append({
                        'type': 'sell',
                        'timestamp': trade['timestamp'],
                        'price': response.json()['filled_average_price'],
                        'shares': response.json()['filled_qty']
                    })
            except Exception as e:
                print(f'Error executing trade: {str(e)}')
        return executed_trades
    except Exception as e:
        print(f'Error in execute_trades: {str(e)}')
        return None

def analyze_results(trades):
    try:
        total_pnl = 0
        win_rate = 0
        for i in range(0, len(trades), 2):
            if i+1 >= len(trades):
                break
            buy = trades[i]
            sell = trades[i+1]
            pnl = (float(sell['price']) - float(buy['price'])) / float(buy['price']) * 100
            total_pnl += pnl
            if pnl > 0:
                win_rate += 1
        win_rate = win_rate / (len(trades) // 2) if len(trades) > 0 else 0
        return {
            'total_pnl': total_pnl,
            'win_rate': win_rate,
            'number_of_trades': len(trades) // 2
        }
    except Exception as e:
        print(f'Error in analyze_results: {str(e)}')
        return None

def main():
    try:
        symbol = 'QQQ