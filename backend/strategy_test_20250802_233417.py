"""
Generated Strategy: test
Description: Moving average crossover strategy
Generated: 2025-08-02 23:34:17
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
        
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()
        
        url = f'{base_url}stocks/{symbol}/bars?timeframe={timeframe}&start={start_date}&end={end_date}'
        headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df, short_ma=20, long_ma=50):
    try:
        df['short_ma'] = df['close'].rolling(window=short_ma).mean()
        df['long_ma'] = df['close'].rolling(window=long_ma).mean()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def generate_signals(df):
    try:
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0
        signals.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
        signals.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1)
        return signals
    except Exception as e:
        print(f'Error generating signals: {e}')
        return None

def calculate_position_size(portfolio_value, risk_per_trade, current_price):
    try:
        risk_amount = portfolio_value * risk_per_trade
        position_size = risk_amount / current_price
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def backtest_strategy(symbol, start_date, end_date, timeframe, risk_per_trade):
    try:
        df = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return None
            
        df = calculate_indicators(df)
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
            current_price = df.iloc[i]['close']
            signal = signals.iloc[i]['signal']
            
            if signal == 1 and not in_position:
                position_size = calculate_position_size(portfolio_value, risk_per_trade, current_price)
                in_position = True
                entry_price = current_price
                trades.append({'type': 'entry', 'price': entry_price, 'timestamp': df.index[i]})
                
            elif signal == -1 and in_position:
                exit_price = current_price
                pnl = (exit_price - entry_price) * position_size
                portfolio_value += pnl
                in_position = False
                trades.append({'type': 'exit', 'price': exit_price, 'timestamp': df.index[i]})
                
        performance = {
            'total_trades': len(trades),
            'winning_trades': sum(1 for trade in trades if trade['type'] == 'exit' and trade['price'] > entry_price),
            'losing_trades': len(trades) // 2,
            'profit_percentage': (portfolio_value - 100000) / 100000 * 100
        }
        
        return {'trades': trades, 'performance': performance}
        
    except Exception as e:
        print(f'Error in backtest strategy: {e}')
        return None

def main():
    symbol = 'QQQ'
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 3, 1)
    timeframe = '1Min'
    risk_per_trade = 0.01
    
    results = backtest_strategy(symbol, start_date, end_date, timeframe, risk_per_trade)
    
    if results:
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print('Backtest results saved to backtest_results.json')
    else:
        print('Backtest failed')

if __name__ == "__main__":
    main()