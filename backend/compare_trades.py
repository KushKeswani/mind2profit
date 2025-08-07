import json
import pandas as pd
from datetime import datetime

def load_python_trades():
    """Load trades from the Python backtest results"""
    try:
        with open("backtest_results.json", "r") as f:
            data = json.load(f)
        return data.get("trades", [])
    except FileNotFoundError:
        print("❌ backtest_results.json not found. Run the backtest first.")
        return []

def load_pinescript_trades():
    """Load trades from the Pine Script output file"""
    try:
        with open("trade_times_for_pinescript.txt", "r") as f:
            content = f.read()
        
        # Extract trades array from the file
        trades = []
        lines = content.split('\n')
        in_trades_array = False
        
        for line in lines:
            if 'trades = [' in line:
                in_trades_array = True
                continue
            elif ']' in line and in_trades_array:
                in_trades_array = False
                break
            elif in_trades_array and line.strip().startswith('['):
                # Parse trade line: [timestamp1, timestamp2, price1, price2, pnl]
                trade_str = line.strip().rstrip(',').rstrip('//').strip()
                trade_data = eval(trade_str)  # Safe for our controlled format
                
                entry_time = datetime.fromtimestamp(trade_data[0] / 1000)
                exit_time = datetime.fromtimestamp(trade_data[1] / 1000)
                
                trades.append({
                    "entry_time": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "entry_price": trade_data[2],
                    "exit_price": trade_data[3],
                    "pnl_percent": trade_data[4]
                })
        
        return trades
    except FileNotFoundError:
        print("❌ trade_times_for_pinescript.txt not found. Run the backtest first.")
        return []

def compare_trades(python_trades, pinescript_trades):
    """Compare Python and Pine Script trades"""
    print("🔍 Comparing Python vs Pine Script Trades")
    print("=" * 60)
    
    if not python_trades or not pinescript_trades:
        print("❌ No trades to compare")
        return
    
    print(f"📊 Python Trades: {len(python_trades)}")
    print(f"📊 Pine Script Trades: {len(pinescript_trades)}")
    print()
    
    # Convert to comparable format
    python_formatted = []
    for trade in python_trades:
        entry_time = pd.to_datetime(trade['entry_time'])
        exit_time = pd.to_datetime(trade['exit_time'])
        python_formatted.append({
            'entry_timestamp': int(entry_time.timestamp() * 1000),
            'exit_timestamp': int(exit_time.timestamp() * 1000),
            'entry_price': trade['entry_price'],
            'exit_price': trade['exit_price'],
            'pnl_percent': trade['pnl_percent']
        })
    
    pinescript_formatted = []
    for trade in pinescript_trades:
        entry_time = pd.to_datetime(trade['entry_time'])
        exit_time = pd.to_datetime(trade['exit_time'])
        pinescript_formatted.append({
            'entry_timestamp': int(entry_time.timestamp() * 1000),
            'exit_timestamp': int(exit_time.timestamp() * 1000),
            'entry_price': trade['entry_price'],
            'exit_price': trade['exit_price'],
            'pnl_percent': trade['pnl_percent']
        })
    
    # Find matching trades
    matches = 0
    mismatches = 0
    
    print("🔍 Trade Comparison:")
    print("-" * 60)
    
    for i, py_trade in enumerate(python_formatted):
        found_match = False
        
        for j, ps_trade in enumerate(pinescript_formatted):
            # Check if timestamps match (within 1 minute tolerance)
            entry_diff = abs(py_trade['entry_timestamp'] - ps_trade['entry_timestamp'])
            exit_diff = abs(py_trade['exit_timestamp'] - ps_trade['exit_timestamp'])
            
            if entry_diff < 60000 and exit_diff < 60000:  # 1 minute tolerance
                # Check if prices and PnL match
                price_match = (abs(py_trade['entry_price'] - ps_trade['entry_price']) < 0.01 and
                             abs(py_trade['exit_price'] - ps_trade['exit_price']) < 0.01)
                pnl_match = abs(py_trade['pnl_percent'] - ps_trade['pnl_percent']) < 0.01
                
                if price_match and pnl_match:
                    print(f"✅ Trade {i+1}: MATCH")
                    matches += 1
                    found_match = True
                    break
                else:
                    print(f"⚠️  Trade {i+1}: TIMESTAMP MATCH but data differs")
                    print(f"   Python: Entry=${py_trade['entry_price']}, Exit=${py_trade['exit_price']}, PnL={py_trade['pnl_percent']}%")
                    print(f"   Pine:   Entry=${ps_trade['entry_price']}, Exit=${ps_trade['exit_price']}, PnL={ps_trade['pnl_percent']}%")
                    mismatches += 1
                    found_match = True
                    break
        
        if not found_match:
            print(f"❌ Trade {i+1}: NO MATCH FOUND")
            print(f"   Python: Entry=${py_trade['entry_price']}, Exit=${py_trade['exit_price']}, PnL={py_trade['pnl_percent']}%")
            mismatches += 1
    
    print()
    print("📋 Summary:")
    print(f"   ✅ Matches: {matches}")
    print(f"   ❌ Mismatches: {mismatches}")
    print(f"   📊 Match Rate: {matches/(matches+mismatches)*100:.1f}%")
    
    if matches == len(python_formatted) and mismatches == 0:
        print("🎉 PERFECT MATCH! Python and Pine Script trades are identical.")
    elif matches > 0:
        print("✅ Good match rate. Minor differences may be due to data precision or timing.")
    else:
        print("❌ No matches found. Check if both scripts are using the same data and logic.")

def main():
    print("🔍 Trade Comparison Tool")
    print("=" * 60)
    
    # Load trades from both sources
    python_trades = load_python_trades()
    pinescript_trades = load_pinescript_trades()
    
    # Compare trades
    compare_trades(python_trades, pinescript_trades)

if __name__ == "__main__":
    main() 