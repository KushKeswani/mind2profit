import json
import pandas as pd
from datetime import datetime

def export_trades_for_comparison():
    """Export Python backtest trades in a readable format for comparison"""
    
    # Load the backtest results
    try:
        with open("backtest_results.json", "r") as f:
            data = json.load(f)
        trades = data.get("trades", [])
    except FileNotFoundError:
        print("❌ backtest_results.json not found. Run the backtest first.")
        return
    
    print("📋 Python Backtest Trades for Comparison")
    print("=" * 80)
    print(f"Strategy: {data.get('strategy', 'Unknown')}")
    print(f"Symbol: {data.get('symbol', 'Unknown')}")
    print(f"Total Trades: {len(trades)}")
    print(f"Win Rate: {data.get('win_rate', 0)}%")
    print(f"Average Return: {data.get('avg_return', 0)}%")
    print("=" * 80)
    print()
    
    # Create a detailed trade list
    print("📊 DETAILED TRADE LIST:")
    print("-" * 80)
    print(f"{'#':<3} {'Entry Time':<20} {'Exit Time':<20} {'Entry Price':<12} {'Exit Price':<12} {'PnL %':<8} {'Status':<10}")
    print("-" * 80)
    
    for i, trade in enumerate(trades, 1):
        entry_time = pd.to_datetime(trade['entry_time']).strftime("%Y-%m-%d %H:%M")
        exit_time = pd.to_datetime(trade['exit_time']).strftime("%Y-%m-%d %H:%M")
        entry_price = f"${trade['entry_price']:.2f}"
        exit_price = f"${trade['exit_price']:.2f}"
        pnl = trade['pnl_percent']
        status = "WIN" if pnl > 0 else "LOSS"
        
        print(f"{i:<3} {entry_time:<20} {exit_time:<20} {entry_price:<12} {exit_price:<12} {pnl:>6.2f}% {status:<10}")
    
    print("-" * 80)
    
    # Summary statistics
    wins = [t for t in trades if t['pnl_percent'] > 0]
    losses = [t for t in trades if t['pnl_percent'] < 0]
    
    print()
    print("📈 SUMMARY STATISTICS:")
    print("-" * 40)
    print(f"Total Trades: {len(trades)}")
    print(f"Winning Trades: {len(wins)} ({len(wins)/len(trades)*100:.1f}%)")
    print(f"Losing Trades: {len(losses)} ({len(losses)/len(trades)*100:.1f}%)")
    print(f"Average Win: {sum([t['pnl_percent'] for t in wins])/len(wins):.2f}%" if wins else "Average Win: N/A")
    print(f"Average Loss: {sum([t['pnl_percent'] for t in losses])/len(losses):.2f}%" if losses else "Average Loss: N/A")
    print(f"Largest Win: {max([t['pnl_percent'] for t in trades]):.2f}%")
    print(f"Largest Loss: {min([t['pnl_percent'] for t in trades]):.2f}%")
    
    # Save to a text file for easy copying
    with open("python_trades_comparison.txt", "w") as f:
        f.write("PYTHON BACKTEST TRADES FOR COMPARISON\n")
        f.write("=" * 80 + "\n")
        f.write(f"Strategy: {data.get('strategy', 'Unknown')}\n")
        f.write(f"Symbol: {data.get('symbol', 'Unknown')}\n")
        f.write(f"Total Trades: {len(trades)}\n")
        f.write(f"Win Rate: {data.get('win_rate', 0)}%\n")
        f.write(f"Average Return: {data.get('avg_return', 0)}%\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("DETAILED TRADE LIST:\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'#':<3} {'Entry Time':<20} {'Exit Time':<20} {'Entry Price':<12} {'Exit Price':<12} {'PnL %':<8} {'Status':<10}\n")
        f.write("-" * 80 + "\n")
        
        for i, trade in enumerate(trades, 1):
            entry_time = pd.to_datetime(trade['entry_time']).strftime("%Y-%m-%d %H:%M")
            exit_time = pd.to_datetime(trade['exit_time']).strftime("%Y-%m-%d %H:%M")
            entry_price = f"${trade['entry_price']:.2f}"
            exit_price = f"${trade['exit_price']:.2f}"
            pnl = trade['pnl_percent']
            status = "WIN" if pnl > 0 else "LOSS"
            
            f.write(f"{i:<3} {entry_time:<20} {exit_time:<20} {entry_price:<12} {exit_price:<12} {pnl:>6.2f}% {status:<10}\n")
        
        f.write("-" * 80 + "\n\n")
        
        f.write("SUMMARY STATISTICS:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Trades: {len(trades)}\n")
        f.write(f"Winning Trades: {len(wins)} ({len(wins)/len(trades)*100:.1f}%)\n")
        f.write(f"Losing Trades: {len(losses)} ({len(losses)/len(trades)*100:.1f}%)\n")
        f.write(f"Average Win: {sum([t['pnl_percent'] for t in wins])/len(wins):.2f}%\n" if wins else "Average Win: N/A\n")
        f.write(f"Average Loss: {sum([t['pnl_percent'] for t in losses])/len(losses):.2f}%\n" if losses else "Average Loss: N/A\n")
        f.write(f"Largest Win: {max([t['pnl_percent'] for t in trades]):.2f}%\n")
        f.write(f"Largest Loss: {min([t['pnl_percent'] for t in trades]):.2f}%\n")
    
    print()
    print("✅ Trade details saved to 'python_trades_comparison.txt'")
    print("📋 You can now compare this with your TradingView Pine Script results")
    print()
    print("🔍 COMPARISON INSTRUCTIONS:")
    print("1. Copy the trade list above or from the saved file")
    print("2. Compare with your TradingView Pine Script trade list")
    print("3. Check if entry/exit times and prices match")
    print("4. Verify PnL percentages are the same")

if __name__ == "__main__":
    export_trades_for_comparison() 