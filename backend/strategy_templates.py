# Strategy Templates for the Strategy Library

STRATEGY_TEMPLATES = {
    "ICT Smart Money Concepts": {
        "name": "ICT Smart Money Concepts",
        "description": "Advanced institutional trading concepts focusing on order blocks, fair value gaps, and market structure shifts.",
        "code": '''import pandas as pd
import numpy as np
import ta
from datetime import datetime, timedelta
import requests
import json

def get_alpaca_data(symbol, start_date, end_date, timeframe):
    """Fetch data from Alpaca API"""
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        
        headers = {
            'APCA-API-KEY-ID': api_key, 
            'APCA-API-SECRET-KEY': api_secret
        }
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

def identify_order_blocks(data):
    """Identify institutional order blocks"""
    data['high_prev'] = data['high'].shift(1)
    data['low_prev'] = data['low'].shift(1)
    
    # Bullish order blocks (after a strong move down)
    data['bullish_ob'] = (data['close'] > data['open']) & (data['high_prev'] > data['low_prev'])
    
    # Bearish order blocks (after a strong move up)
    data['bearish_ob'] = (data['close'] < data['open']) & (data['high_prev'] < data['low_prev'])
    
    return data

def identify_fair_value_gaps(data):
    """Identify fair value gaps"""
    data['gap_up'] = data['low'] > data['high'].shift(1)
    data['gap_down'] = data['high'] < data['low'].shift(1)
    
    return data

def identify_market_structure(data):
    """Identify market structure shifts"""
    data['higher_high'] = data['high'] > data['high'].shift(1)
    data['lower_low'] = data['low'] < data['low'].shift(1)
    
    return data

def ict_strategy(data):
    """ICT Smart Money Concepts Strategy"""
    trades = []
    position = None
    
    for i in range(20, len(data)):
        current = data.iloc[i]
        
        # Entry conditions
        if position is None:
            # Long entry: Price returns to bullish order block
            if current['bullish_ob'] and current['close'] > current['open']:
                position = {
                    'type': 'long',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['low'] * 0.985,  # 1.5% below entry
                    'take_profit': current['close'] * 1.03  # 3% above entry
                }
            
            # Short entry: Price returns to bearish order block
            elif current['bearish_ob'] and current['close'] < current['open']:
                position = {
                    'type': 'short',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['high'] * 1.015,  # 1.5% above entry
                    'take_profit': current['close'] * 0.97  # 3% below entry
                }
        
        # Exit conditions
        elif position is not None:
            if position['type'] == 'long':
                if current['low'] <= position['stop_loss'] or current['high'] >= position['take_profit']:
                    exit_price = position['stop_loss'] if current['low'] <= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (exit_price - position['entry_price']) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price <= position['entry_price'] else 'win'
                    })
                    position = None
            
            elif position['type'] == 'short':
                if current['high'] >= position['stop_loss'] or current['low'] <= position['take_profit']:
                    exit_price = position['stop_loss'] if current['high'] >= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (position['entry_price'] - exit_price) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price >= position['entry_price'] else 'win'
                    })
                    position = None
    
    return trades

def main():
    """Main function"""
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    
    # Get data
    data = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if data is None:
        return
    
    # Apply ICT analysis
    data = identify_order_blocks(data)
    data = identify_fair_value_gaps(data)
    data = identify_market_structure(data)
    
    # Run strategy
    trades = ict_strategy(data)
    
    # Calculate performance
    if trades:
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['type'] == 'win'])
        win_rate = (winning_trades / total_trades) * 100
        total_pnl = sum(t['pnl'] for t in trades)
        
        results = {
            'strategy': 'ICT Smart Money Concepts',
            'symbol': symbol,
            'timeframe': timeframe,
            'date_range': f'{start_date} - {end_date}',
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'trades': trades
        }
        
        # Save results
        with open('ict_strategy_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        
        print('ICT Smart Money Concepts strategy completed successfully!')
        print(f'Total Trades: {total_trades}')
        print(f'Win Rate: {win_rate:.1f}%')
        print(f'Total P&L: {total_pnl:.2f}%')

if __name__ == "__main__":
    main()'''
    },
    
    "BOS + FVG Strategy": {
        "name": "BOS + FVG Strategy",
        "description": "Break of Structure combined with Fair Value Gap entries for high-probability setups.",
        "code": '''import pandas as pd
import numpy as np
import ta
from datetime import datetime, timedelta
import requests
import json

def get_alpaca_data(symbol, start_date, end_date, timeframe):
    """Fetch data from Alpaca API"""
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        
        headers = {
            'APCA-API-KEY-ID': api_key, 
            'APCA-API-SECRET-KEY': api_secret
        }
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

def identify_break_of_structure(data):
    """Identify Break of Structure (BOS)"""
    data['swing_high'] = data['high'].rolling(5).max()
    data['swing_low'] = data['low'].rolling(5).min()
    
    # Bullish BOS: Price breaks above previous swing high
    data['bullish_bos'] = data['close'] > data['swing_high'].shift(1)
    
    # Bearish BOS: Price breaks below previous swing low
    data['bearish_bos'] = data['close'] < data['swing_low'].shift(1)
    
    return data

def identify_fair_value_gaps(data):
    """Identify Fair Value Gaps (FVG)"""
    data['gap_up'] = data['low'] > data['high'].shift(1)
    data['gap_down'] = data['high'] < data['low'].shift(1)
    
    # FVG levels
    data['fvg_high'] = data['high'].shift(1)
    data['fvg_low'] = data['low'].shift(1)
    
    return data

def bos_fvg_strategy(data):
    """BOS + FVG Strategy"""
    trades = []
    position = None
    
    for i in range(20, len(data)):
        current = data.iloc[i]
        
        # Entry conditions
        if position is None:
            # Long entry: Bullish BOS + price returns to FVG
            if (current['bullish_bos'] and 
                current['low'] <= current['fvg_high'] and 
                current['close'] > current['open']):
                position = {
                    'type': 'long',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['low'] * 0.985,  # 1.5% below entry
                    'take_profit': current['close'] * 1.03  # 3% above entry
                }
            
            # Short entry: Bearish BOS + price returns to FVG
            elif (current['bearish_bos'] and 
                  current['high'] >= current['fvg_low'] and 
                  current['close'] < current['open']):
                position = {
                    'type': 'short',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['high'] * 1.015,  # 1.5% above entry
                    'take_profit': current['close'] * 0.97  # 3% below entry
                }
        
        # Exit conditions
        elif position is not None:
            if position['type'] == 'long':
                if current['low'] <= position['stop_loss'] or current['high'] >= position['take_profit']:
                    exit_price = position['stop_loss'] if current['low'] <= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (exit_price - position['entry_price']) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price <= position['entry_price'] else 'win'
                    })
                    position = None
            
            elif position['type'] == 'short':
                if current['high'] >= position['stop_loss'] or current['low'] <= position['take_profit']:
                    exit_price = position['stop_loss'] if current['high'] >= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (position['entry_price'] - exit_price) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price >= position['entry_price'] else 'win'
                    })
                    position = None
    
    return trades

def main():
    """Main function"""
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    
    # Get data
    data = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if data is None:
        return
    
    # Apply BOS and FVG analysis
    data = identify_break_of_structure(data)
    data = identify_fair_value_gaps(data)
    
    # Run strategy
    trades = bos_fvg_strategy(data)
    
    # Calculate performance
    if trades:
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['type'] == 'win'])
        win_rate = (winning_trades / total_trades) * 100
        total_pnl = sum(t['pnl'] for t in trades)
        
        results = {
            'strategy': 'BOS + FVG Strategy',
            'symbol': symbol,
            'timeframe': timeframe,
            'date_range': f'{start_date} - {end_date}',
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'trades': trades
        }
        
        # Save results
        with open('bos_fvg_strategy_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        
        print('BOS + FVG Strategy completed successfully!')
        print(f'Total Trades: {total_trades}')
        print(f'Win Rate: {win_rate:.1f}%')
        print(f'Total P&L: {total_pnl:.2f}%')

if __name__ == "__main__":
    main()'''
    },
    
    "Trendline Breakout": {
        "name": "Trendline Breakout",
        "description": "Classic technical analysis approach using trendline breaks with volume confirmation.",
        "code": '''import pandas as pd
import numpy as np
import ta
from datetime import datetime, timedelta
import requests
import json

def get_alpaca_data(symbol, start_date, end_date, timeframe):
    """Fetch data from Alpaca API"""
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        
        headers = {
            'APCA-API-KEY-ID': api_key, 
            'APCA-API-SECRET-KEY': api_secret
        }
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

def calculate_trendlines(data):
    """Calculate trendlines using linear regression"""
    data['volume_ma'] = data['volume'].rolling(20).mean()
    data['price_ma'] = data['close'].rolling(20).mean()
    
    # Simple trendline calculation
    data['trend_up'] = data['close'] > data['price_ma']
    data['trend_down'] = data['close'] < data['price_ma']
    
    return data

def identify_breakouts(data):
    """Identify trendline breakouts"""
    data['breakout_up'] = (data['close'] > data['high'].shift(1)) & (data['volume'] > data['volume_ma'])
    data['breakout_down'] = (data['close'] < data['low'].shift(1)) & (data['volume'] > data['volume_ma'])
    
    return data

def trendline_breakout_strategy(data):
    """Trendline Breakout Strategy"""
    trades = []
    position = None
    
    for i in range(20, len(data)):
        current = data.iloc[i]
        
        # Entry conditions
        if position is None:
            # Long entry: Upward breakout with volume confirmation
            if current['breakout_up'] and current['trend_up']:
                position = {
                    'type': 'long',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['low'] * 0.985,  # 1.5% below entry
                    'take_profit': current['close'] * 1.03  # 3% above entry
                }
            
            # Short entry: Downward breakout with volume confirmation
            elif current['breakout_down'] and current['trend_down']:
                position = {
                    'type': 'short',
                    'entry_price': current['close'],
                    'entry_time': current.name,
                    'stop_loss': current['high'] * 1.015,  # 1.5% above entry
                    'take_profit': current['close'] * 0.97  # 3% below entry
                }
        
        # Exit conditions
        elif position is not None:
            if position['type'] == 'long':
                if current['low'] <= position['stop_loss'] or current['high'] >= position['take_profit']:
                    exit_price = position['stop_loss'] if current['low'] <= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (exit_price - position['entry_price']) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price <= position['entry_price'] else 'win'
                    })
                    position = None
            
            elif position['type'] == 'short':
                if current['high'] >= position['stop_loss'] or current['low'] <= position['take_profit']:
                    exit_price = position['stop_loss'] if current['high'] >= position['stop_loss'] else position['take_profit']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': current.name,
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'pnl': (position['entry_price'] - exit_price) / position['entry_price'] * 100,
                        'type': 'loss' if exit_price >= position['entry_price'] else 'win'
                    })
                    position = None
    
    return trades

def main():
    """Main function"""
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    
    # Get data
    data = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if data is None:
        return
    
    # Apply trendline analysis
    data = calculate_trendlines(data)
    data = identify_breakouts(data)
    
    # Run strategy
    trades = trendline_breakout_strategy(data)
    
    # Calculate performance
    if trades:
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['type'] == 'win'])
        win_rate = (winning_trades / total_trades) * 100
        total_pnl = sum(t['pnl'] for t in trades)
        
        results = {
            'strategy': 'Trendline Breakout',
            'symbol': symbol,
            'timeframe': timeframe,
            'date_range': f'{start_date} - {end_date}',
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'trades': trades
        }
        
        # Save results
        with open('trendline_breakout_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        
        print('Trendline Breakout strategy completed successfully!')
        print(f'Total Trades: {total_trades}')
        print(f'Win Rate: {win_rate:.1f}%')
        print(f'Total P&L: {total_pnl:.2f}%')

if __name__ == "__main__":
    main()'''
    }
} 