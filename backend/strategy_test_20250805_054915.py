"""
Generated Strategy: Test
Description: Simple moving average crossover
Generated: 2025-08-05 05:49:15
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
            'timeframe': timeframe
        }
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_position_size(account_balance, risk_percent, stop_loss_pips):
    try:
        risk_amount = account_balance * (risk_percent / 100)
        position_size = risk_amount / stop_loss_pips
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        risk_percent = 1.0
        
        data = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if data is None:
            return
            
        data['time'] = pd.to_datetime(data['time'])
        data.set_index('time', inplace=True)
        
        # Calculate indicators
        data['short_ma'] = data['close'].rolling(20).mean()
        data['long_ma'] = data['close'].rolling(50).mean()
        data['atr'] = ta.volatility.AverageTrueRange(data).average_true_range
        
        # Generate signals
        data['signal'] = 0
        data.loc[data['short_ma'] > data['long_ma'], 'signal'] = 1
        data.loc[data['short_ma'] < data['long_ma'], 'signal'] = -1
        
        # Calculate trades
        trades = []
        position_size = 0
        account_balance = 100000  # Initial account balance
        
        for i in range(1, len(data)):
            if data.iloc[i-1]['signal'] == 1 and data.iloc[i]['signal'] == 0:
                # Entry
                entry_price = data.iloc[i]['open']
                stop_loss = entry_price - data.iloc[i]['atr'][-1]
                position_size = calculate_position_size(account_balance, risk_percent, entry_price - stop_loss)
                
                if position_size > 0:
                    # Record trade
                    trades.append({
                        'entry_time': data.index[i].strftime('%Y-%m-%d %H:%M:%S'),
                        'entry_price': entry_price,
                        'position_size': position_size
                    })
                    
            elif data.iloc[i-1]['signal'] == -1 and data.iloc[i]['signal'] == 0:
                # Exit
                if trades and 'exit_price' not in trades[-1]:
                    exit_price = data.iloc[i]['open']
                    pl = (exit_price - trades[-1]['entry_price']) * trades[-1]['position_size']
                    account_balance += pl
                    
                    trades[-1]['exit_price'] = exit_price
                    trades[-1]['profit_loss'] = pl
                    
        # Calculate performance metrics
        total_profit = sum(t['profit_loss'] for t in trades if 'profit_loss' in t)
        max_drawdown = (account_balance - (account_balance * 0.8))  # Simplified drawdown calculation
        
        # Prepare results
        results = {
            'strategy': 'Simple Moving Average Crossover',
            'symbol': symbol,
            'timeframe': timeframe,
            'date_range': f'{start_date} - {end_date}',
            'risk_per_trade': risk_percent,
            'number_of_trades': len(trades),
            'total_profit': total_profit,
            'max_drawdown': max_drawdown,
            'trades': trades
        }
        
        # Export to JSON
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=4)
            
        print('Backtest completed successfully!')
        
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()