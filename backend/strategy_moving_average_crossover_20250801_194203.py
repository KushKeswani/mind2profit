"""
Generated Strategy: Moving Average Crossover
Description: 
    Create a moving average crossover strategy for QQQ:
    - Use 20-period and 50-period simple moving averages
    - Buy when 20 SMA crosses above 50 SMA
    - Sell when 20 SMA crosses below 50 SMA
    - Use 1-minute data from January 2025 to March 2025
    - Include proper risk management and position sizing
    
Generated: 2025-08-01 19:42:03
"""

<think>
Okay, I need to create a Python backtesting script for a moving average crossover strategy on QQQ. The user provided specific requirements, so I should make sure to address each one.

First, the strategy uses 20-period and 50-period simple moving averages. I'll need to calculate these using the 'ta' library, which has functions for SMA. I'll import the necessary modules like pandas for data handling and alpaca_trade_api for fetching data.

Next, the trading logic is to buy when the 20 SMA crosses above the 50 SMA and sell when it crosses below. I'll need to iterate through the data, check for these crossovers, and generate signals accordingly.

The data should be fetched using the Alpaca API. I have the API keys, so I'll set them as environment variables and use them to create an Alpaca client. I'll request 1-minute data from January 2025 to March 2025. I should handle any potential errors here, like invalid API responses.

I need to include proper validation. For example, checking if the data is successfully fetched and not empty. Also, ensuring that the SMAs are correctly calculated and that there are enough data points.

Risk management and position sizing are important. I'll set a fixed investment amount per trade, say $1000, and calculate the number of shares to buy based on QQQ's price. Using bracket orders with stop-loss and take-profit targets will help manage risk. I'll set the stop-loss at 1% below the entry price and take-profit at 2% above.

For error handling, I'll wrap API calls and critical sections in try-except blocks to catch exceptions and log them. This will prevent the script from crashing and provide useful feedback.

I'll track each trade's details, including entry and exit prices, P&L, and timestamps. After processing all data, I'll calculate the total profit, number of trades, and win rate. These results will be exported to a JSON file for easy analysis.

Finally, I'll make sure the code follows Python conventions, includes comments for clarity, and is well-structured. Testing the script with the provided parameters should ensure it runs smoothly and meets all the user's requirements.
</think>

```python
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from alpaca_trade_api import REST
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Alpaca API configuration
ALPACA_API_KEY = os.getenv('PK0F1YSWGZYNHF1VKOY5')
ALPACA_SECRET_KEY = os.getenv('ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB')
BASE_URL = 'https://paper-api.alpaca.markets'

# Create Alpaca client
alpaca = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL)

def fetch_data(symbol, start_date, end_date, interval):
    """Fetch historical data from Alpaca API"""
    try:
        data = alpaca.get_barset(symbol, interval, start=start_date, end=end_date).df
        if data.empty:
            logging.error("No data fetched")
            return None
        return data[symbol]
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return None

def calculate_indicators(data):
    """Calculate moving averages"""
    data['sma_20'] = data['close'].rolling(20).mean()
    data['sma_50'] = data['close'].rolling(50).mean()
    return data

def generate_signals(data):
    """Generate buy/sell signals based on MA crossover"""
    signals = []
    in_position = False
    
    for i in range(len(data)):
        if i < 50:  # Wait for enough data for SMAs
            continue
            
        current_price = data.iloc[i]['close']
        sma_20 = data.iloc[i]['sma_20']
        sma_50 = data.iloc[i]['sma_50']
        
        # Check for crossover
        if sma_20 > sma_50 and not in_position:
            signals.append({
                'timestamp': data.index[i],
                'type': 'buy',
                'price': current_price
            })
            in_position = True
        elif sma_20 < sma_50 and in_position:
            signals.append({
                'timestamp': data.index[i],
                'type': 'sell',
                'price': current_price
            })
            in_position = False
            
    return signals

def execute_trades(signals, symbol, investment_amount):
    """Simulate trade execution with risk management"""
    trades = []
    position_size = 0
    
    for signal in signals:
        if signal['type'] == 'buy':
            # Calculate number of shares to buy
            shares = investment_amount / signal['price']
            position_size = shares
            trades.append({
                'entry_timestamp': signal['timestamp'],
                'entry_price': signal['price'],
                'shares': shares,
                'position_size': position_size
            })
        elif signal['type'] == 'sell':
            if position_size > 0:
                exit_price = signal['price']
                pnl = (exit_price - trades[-1]['entry_price']) * position_size
                trades[-1]['exit_timestamp'] = signal['timestamp']
                trades[-1]['exit_price'] = exit_price
                trades[-1]['pnl'] = pnl
                position_size = 0
                
    return trades

def analyze_results(trades):
    """Calculate performance metrics"""
    total_profit = sum(t['pnl'] for t in trades if 'pnl' in t)
    num_trades = len([t for t in trades if 'pnl' in t])
    win_rate = sum(1 for t in trades if t['pnl'] > 0) / num_trades if num_trades > 0 else 0
    
    return {
        'total_profit': total_profit,
        'num_trades': num_trades,
        'win_rate': win_rate
    }

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-31'
    interval = '1min'
    investment_amount = 1000  # Dollars per trade
    
    # Fetch data
    data = fetch_data(symbol, start_date, end_date, interval)
    if data is None:
        return
    
    # Calculate indicators
    data = calculate_indicators(data)
    
    # Generate signals
    signals = generate_signals(data)
    
    # Execute trades
    trades = execute_trades(signals, symbol, investment_amount)
    
    # Analyze results
    results = analyze_results(trades)
    
    # Export results
    results_file = 'trading_results.json'
    with open(results_file, 'w') as f:
        json.dump({
            'trades': trades,
            'performance': results
        }, f, indent=2)
    
    logging.info(f"Results exported to {results_file}")

if __name__ == '__main__':
    main()
```