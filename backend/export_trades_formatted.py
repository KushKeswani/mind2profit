import json
import pandas as pd
from datetime import datetime

def export_trades_formatted():
    """Export trades in the exact format requested"""
    
    # Load the backtest results
    try:
        with open("backtest_results.json", "r") as f:
            data = json.load(f)
        trades = data.get("trades", [])
    except FileNotFoundError:
        print("❌ backtest_results.json not found. Run the backtest first.")
        return
    
    # Position size for dollar calculations (adjust as needed)
    position_size = 100000  # $100,000 position size
    
    print("📋 Python Backtest Trades (Formatted)")
    print("=" * 80)
    print(f"Strategy: {data.get('strategy', 'Unknown')}")
    print(f"Symbol: {data.get('symbol', 'Unknown')}")
    print(f"Total Trades: {len(trades)}")
    print(f"Win Rate: {data.get('win_rate', 0)}%")
    print(f"Average Return: {data.get('avg_return', 0)}%")
    print(f"Position Size: ${position_size:,}")
    print("=" * 80)
    print()
    
    # Export trades in the requested format
    print("📊 TRADES:")
    print("-" * 80)
    
    for i, trade in enumerate(trades, 1):
        entry_price = trade['entry_price']
        exit_price = trade['exit_price']
        pnl_percent = trade['pnl_percent']
        
        # Calculate dollar amount
        dollar_amount = (position_size * pnl_percent) / 100
        
        # Format the trade line
        trade_line = f"- Trade {i}: Entry ${entry_price:.2f} -> Exit ${exit_price:.2f} | {pnl_percent:+.2f}% | ${dollar_amount:+,.2f}"
        print(trade_line)
    
    print("-" * 80)
    
    # Summary statistics
    wins = [t for t in trades if t['pnl_percent'] > 0]
    losses = [t for t in trades if t['pnl_percent'] < 0]
    
    total_pnl = sum([t['pnl_percent'] for t in trades])
    total_dollar_pnl = (position_size * total_pnl) / 100
    
    print()
    print("📈 SUMMARY:")
    print("-" * 40)
    print(f"Total Trades: {len(trades)}")
    print(f"Winning Trades: {len(wins)} ({len(wins)/len(trades)*100:.1f}%)")
    print(f"Losing Trades: {len(losses)} ({len(losses)/len(trades)*100:.1f}%)")
    print(f"Total P&L: {total_pnl:+.2f}% | ${total_dollar_pnl:+,.2f}")
    print(f"Largest Win: {max([t['pnl_percent'] for t in trades]):.2f}%")
    print(f"Largest Loss: {min([t['pnl_percent'] for t in trades]):.2f}%")
    
    # Save to file
    with open("trades_formatted.txt", "w") as f:
        f.write("PYTHON BACKTEST TRADES (FORMATTED)\n")
        f.write("=" * 80 + "\n")
        f.write(f"Strategy: {data.get('strategy', 'Unknown')}\n")
        f.write(f"Symbol: {data.get('symbol', 'Unknown')}\n")
        f.write(f"Total Trades: {len(trades)}\n")
        f.write(f"Win Rate: {data.get('win_rate', 0)}%\n")
        f.write(f"Average Return: {data.get('avg_return', 0)}%\n")
        f.write(f"Position Size: ${position_size:,}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("TRADES:\n")
        f.write("-" * 80 + "\n")
        
        for i, trade in enumerate(trades, 1):
            entry_price = trade['entry_price']
            exit_price = trade['exit_price']
            pnl_percent = trade['pnl_percent']
            dollar_amount = (position_size * pnl_percent) / 100
            
            trade_line = f"- Trade {i}: Entry ${entry_price:.2f} -> Exit ${exit_price:.2f} | {pnl_percent:+.2f}% | ${dollar_amount:+,.2f}\n"
            f.write(trade_line)
        
        f.write("-" * 80 + "\n\n")
        
        f.write("SUMMARY:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Trades: {len(trades)}\n")
        f.write(f"Winning Trades: {len(wins)} ({len(wins)/len(trades)*100:.1f}%)\n")
        f.write(f"Losing Trades: {len(losses)} ({len(losses)/len(trades)*100:.1f}%)\n")
        f.write(f"Total P&L: {total_pnl:+.2f}% | ${total_dollar_pnl:+,.2f}\n")
        f.write(f"Largest Win: {max([t['pnl_percent'] for t in trades]):.2f}%\n")
        f.write(f"Largest Loss: {min([t['pnl_percent'] for t in trades]):.2f}%\n")
    
    print()
    print("✅ Trades saved to 'trades_formatted.txt'")
    print("📋 Ready for comparison with TradingView results")

if __name__ == "__main__":
    export_trades_formatted() 