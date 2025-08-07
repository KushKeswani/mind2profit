"""
Generated Strategy: Test
Description: Test strategy
Generated: 2025-08-06 16:43:33
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API credentials
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def fetch_data(symbol, start_date, end_date):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        params = {
            'symbol': symbol,
            'timeframe': '1Min',
            'start': start_date,
            'end': end_date
        }
        response = requests.get(base_url + 'stocks/' + symbol + '/bars', headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['bars'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        else:
            print(f'Error fetching data: {response.text}')
            return None
    except Exception as e:
        print(f'Error in fetch_data: {e}')
        return None

def calculate_position_size(risk_amount, price):
    return risk_amount / price

def backtest_strategy(df, initial_capital, risk_percent):
    try:
        df['SMA_20'] = ta.momentum.SMAIndicator(df['close'], window=20).sma_indicator()
        df['SMA_50'] = ta.momentum.SMAIndicator(df['close'], window=50).sma_indicator()
        
        trades = []
        position = False
        equity = initial_capital
        risk_amount = initial_capital * risk_percent
        
        for index, row in df.iterrows():
            if pd.notnull(row['SMA_20']) and pd.notnull(row['SMA_50']):
                if row['SMA_20'] > row['SMA_50'] and not position:
                    position_size = calculate_position_size(risk_amount, row['close'])
                    position = True
                    trades.append({
                        'entry_time': row['timestamp'],
                        'entry_price': row['close'],
                        'position_size': position_size
                    })
                elif row['SMA_20'] < row['SMA_50'] and position:
                    position = False
                    exit_price = row['close']
                    pnl = (exit_price - trades[-1]['entry_price']) * trades[-1]['position_size']
                    equity += pnl
                    trades[-1]['exit_time'] = row['timestamp']
                    trades[-1]['exit_price'] = exit_price
                    trades[-1]['pnl'] = pnl
        
        return trades, equity
    except Exception as e:
        print(f'Error in backtest_strategy: {e}')
        return None, initial_capital

def calculate_metrics(trades, initial_equity, final_equity):
    try:
        total_trades = len(trades)
        wins = sum(1 for trade in trades if trade['pnl'] > 0)
        losses = total_trades - wins
        win_rate = wins / total_trades if total_trades > 0 else 0
        total_profit = final_equity - initial_equity
        max_drawdown = 0
        sharpe_ratio = ta.risk.SharpeRatio().calculate(final_equity)
        
        return {
            'total_trades': total_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio
        }
    except Exception as e:
        print(f'Error in calculate_metrics: {e}')
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        initial_capital = 100000
        risk_percent = 0.01
        
        df = fetch_data(symbol, start_date, end_date)
        if df is not None:
            trades, final_equity = backtest_strategy(df, initial_capital, risk_percent)
            if trades is not None:
                metrics = calculate_metrics(trades, initial_capital, final_equity)
                if metrics is not None:
                    results = {
                        'symbol': symbol,
                        'start_date': start_date,
                        'end_date': end_date,
                        'initial_capital': initial_capital,
                        'risk_percent': risk_percent,
                        'trades': trades,
                        'metrics': metrics
                    }
                    with open('backtest_results.json', 'w') as f:
                        json.dump(results, f, default=str)
                    print('Backtest completed successfully')
                else:
                    print('Error calculating metrics')
            else:
                print('Error running backtest')
        else:
            print('Error fetching data')
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == "__main__":
    main()