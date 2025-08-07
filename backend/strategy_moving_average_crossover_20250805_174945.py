"""
Generated Strategy: Moving Average Crossover
Description: Buy when short SMA crosses above long SMA, sell when it crosses below. Use 20-period and 50-period simple moving averages.
Generated: 2025-08-05 17:49:45
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
        
        response = requests.get(base_url + 'stocks/v2/ags', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_position_size(portfolio_value, risk_percent, stop_loss_pips):
    try:
        position_size = (portfolio_value * risk_percent) / stop_loss_pips
        return position_size
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0

def moving_average_crossover_strategy(data):
    try:
        data['sma_20'] = ta.momentum.SMA(data, window=20).SMA()
        data['sma_50'] = ta.momentum.SMA(data, window=50).SMA()
        data['atr'] = ta.volatility.AverageTrueRange(data, window=14).ATR()
        
        data['signal'] = 0
        data.loc[data['sma_20'] > data['sma_50'], 'signal'] = 1
        data.loc[data['sma_20'] < data['sma_50'], 'signal'] = -1
        
        return data
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def backtest_strategy(data, initial_capital):
    try:
        trades = []
        position = 0
        portfolio_value = initial_capital
        
        for i in range(len(data)):
            if i < 50:
                continue
                
            current_row = data.iloc[i]
            prev_row = data.iloc[i-1]
            
            if prev_row['signal'] == 1 and current_row['signal'] == 1:
                if position == 0:
                    position_size = calculate_position_size(portfolio_value, 0.01, current_row['atr'])
                    position = 1
                    entry_price = current_row['close']
                    trades.append({
                        'type': 'buy',
                        'date': current_row.name,
                        'price': entry_price,
                        'size': position_size
                    })
                    
            elif prev_row['signal'] == -1 and current_row['signal'] == -1:
                if position == 1:
                    exit_price = current_row['close']
                    profit = (exit_price - entry_price) * position_size
                    portfolio_value += profit
                    position = 0
                    trades.append({
                        'type': 'sell',
                        'date': current_row.name,
                        'price': exit_price,
                        'size': position_size
                    })
                    
        return trades
    except Exception as e:
        print(f"Error executing backtest: {e}")
        return None

def export_results_to_json(trades, results_file):
    try:
        with open(results_file, 'w') as f:
            json.dump(trades, f, indent=2)
        return True
    except Exception as e:
        print(f"Error exporting results: {e}")
        return False

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        initial_capital = 100000
        
        data = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if data is None:
            return
            
        data = moving_average_crossover_strategy(data)
        if data is None:
            return
            
        trades = backtest_strategy(data, initial_capital)
        if trades is None:
            return
            
        results_file = 'backtest_results.json'
        export_results_to_json(trades, results_file)
        
        print(f"Backtest completed successfully. Results saved to {results_file}")
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()