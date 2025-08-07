"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 18:00:27
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

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
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', params=params, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_indicators(df, short_ma, long_ma):
    try:
        df['short_ma'] = df['close'].rolling(window=short_ma).mean()
        df['long_ma'] = df['close'].rolling(window=long_ma).mean()
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def generate_signals(df):
    try:
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0
        signals.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
        signals.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1
        return signals
    except Exception as e:
        print(f"Error generating signals: {e}")
        return None

def calculate_position_size(account_balance, risk_percent, stop_loss):
    try:
        position_size = (account_balance * risk_percent) / stop_loss
        return position_size
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0

def backtest_strategy():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        short_ma = 20
        long_ma = 50
        risk_percent = 0.01
        
        df = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return
        
        df = calculate_indicators(df, short_ma, long_ma)
        if df is None:
            return
        
        signals = generate_signals(df)
        if signals is None:
            return
        
        trades = []
        position_size = 0
        account_balance = 100000  # Initial balance
        stop_loss = 0.02  # 2% stop loss
        
        for i in range(1, len(df)):
            if signals.iloc[i-1] == 1 and signals.iloc[i] == -1:
                # Sell signal
                entry_price = df.iloc[i]['close']
                position_size = calculate_position_size(account_balance, risk_percent, entry_price * stop_loss)
                if position_size == 0:
                    continue
                
                exit_price = df.iloc[i+20]['close']  # Assuming 20 periods to exit
                pnl = (exit_price - entry_price) * position_size
                account_balance += pnl
                
                trades.append({
                    'entry_date': df.iloc[i].name.isoformat(),
                    'entry_price': entry_price,
                    'exit_date': df.iloc[i+20].name.isoformat(),
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'position_size': position_size
                })
        
        results = {
            'trades': trades,
            'total_pnl': account_balance - 100000,
            'win_rate': sum(1 for trade in trades if trade['pnl'] > 0) / len(trades) if trades else 0
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        return results
    except Exception as e:
        print(f"Error in backtest: {e}")
        return None

def main():
    results = backtest_strategy()
    if results:
        print("Backtest completed successfully. Results saved to backtest_results.json")

if __name__ == "__main__":
    main()