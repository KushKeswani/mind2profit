import requests
import pandas as pd
import ta  # pip install ta
import json
from datetime import datetime, timedelta

# Replace with your Alpaca paper keys
API_KEY = "PK0F1YSWGZYNHF1VKOY5"
SECRET_KEY = "ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB"
DATA_URL = "https://data.alpaca.markets/v2"

def validate_data_quality(df):
    """Validate the quality of the fetched data"""
    print(f"📊 Data Validation:")
    print(f"   - Total rows: {len(df)}")
    print(f"   - Date range: {df.index.min()} to {df.index.max()}")
    print(f"   - Missing values: {df.isnull().sum().sum()}")
    print(f"   - Price range: ${df['c'].min():.2f} - ${df['c'].max():.2f}")
    print(f"   - Volume range: {df['v'].min():.0f} - {df['v'].max():.0f}")
    
    # Check for suspicious patterns
    suspicious = []
    if len(df) < 100:
        suspicious.append("Very few data points")
    if df['c'].std() < 0.1:
        suspicious.append("Very low price volatility")
    if df['v'].mean() < 100:
        suspicious.append("Very low volume")
    
    if suspicious:
        print(f"   ⚠️  Suspicious patterns: {', '.join(suspicious)}")
    else:
        print(f"   ✅ Data quality looks good")
    
    return len(suspicious) == 0

def validate_trade_logic(trades, df):
    """Validate that trades follow the intended logic"""
    print(f"\n🔍 Trade Logic Validation:")
    
    valid_trades = 0
    invalid_trades = 0
    
    for i, trade in enumerate(trades):
        entry_time = pd.to_datetime(trade['entry_time'])
        exit_time = pd.to_datetime(trade['exit_time'])
        
        # Get the data around the trade
        trade_data = df[entry_time:exit_time]
        
        if len(trade_data) == 0:
            print(f"   ❌ Trade {i+1}: No data found for trade period")
            invalid_trades += 1
            continue
        
        # Check entry conditions
        entry_row = df.loc[entry_time]
        if 'rsi' not in entry_row or pd.isna(entry_row['rsi']):
            print(f"   ❌ Trade {i+1}: No RSI data at entry")
            invalid_trades += 1
            continue
        
        # Verify RSI entry condition
        if entry_row['rsi'] >= 30:
            print(f"   ❌ Trade {i+1}: RSI at entry ({entry_row['rsi']:.1f}) >= 30")
            invalid_trades += 1
            continue
        
        # Verify price movement
        actual_pnl = (trade['exit_price'] - trade['entry_price']) / trade['entry_price'] * 100
        if abs(actual_pnl - trade['pnl_percent']) > 0.01:
            print(f"   ❌ Trade {i+1}: PnL mismatch (calc: {actual_pnl:.2f}%, stored: {trade['pnl_percent']:.2f}%)")
            invalid_trades += 1
            continue
        
        valid_trades += 1
    
    print(f"   ✅ Valid trades: {valid_trades}")
    print(f"   ❌ Invalid trades: {invalid_trades}")
    return valid_trades, invalid_trades

def fetch_1min_data(symbol="QQQ", start="2025-01-27", end="2025-08-01"):
    url = f"{DATA_URL}/stocks/{symbol}/bars"
    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY
    }
    params = {
        "start": start + "T09:30:00-04:00",
        "end": end + "T16:00:00-04:00",
        "timeframe": "1Min",
        "limit": 10000
    }
    
    print(f"🔗 Fetching data for {symbol} from {start} to {end}...")
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    data = r.json().get("bars", [])
    df = pd.DataFrame(data)
    if df.empty:
        raise Exception("No data returned.")
    df['t'] = pd.to_datetime(df['t'])
    df.set_index('t', inplace=True)
    return df

def backtest_rsi_strategy(df):
    print(f"\n📈 Running RSI strategy backtest...")
    df['rsi'] = ta.momentum.RSIIndicator(close=df['c'], window=14).rsi()
    
    in_trade = False
    entry_price = 0
    trades = []

    for i in range(15, len(df)):
        row = df.iloc[i]
        if not in_trade and row['rsi'] < 30:
            in_trade = True
            entry_price = row['c']
            entry_time = row.name
        elif in_trade:
            change_pct = (row['c'] - entry_price) / entry_price * 100
            if change_pct >= 3 or change_pct <= -2 or row['rsi'] > 50:
                trades.append({
                    "entry_time": str(entry_time),
                    "exit_time": str(row.name),
                    "entry_price": round(entry_price, 2),
                    "exit_price": round(row['c'], 2),
                    "pnl_percent": round(change_pct, 2),
                    "entry_rsi": round(row['rsi'], 1) if 'rsi' in row else None,
                    "exit_rsi": round(row['rsi'], 1) if 'rsi' in row else None
                })
                in_trade = False
    
    print(f"   📊 Found {len(trades)} trades")
    return trades

def analyze_results(trades):
    total = len(trades)
    wins = [t for t in trades if t['pnl_percent'] > 0]
    win_rate = round(len(wins) / total * 100, 2) if total else 0
    avg_return = round(sum(t['pnl_percent'] for t in trades) / total, 2) if total else 0
    
    # Additional statistics
    max_win = max([t['pnl_percent'] for t in trades]) if trades else 0
    max_loss = min([t['pnl_percent'] for t in trades]) if trades else 0
    avg_win = round(sum([t['pnl_percent'] for t in wins]) / len(wins), 2) if wins else 0
    losses = [t for t in trades if t['pnl_percent'] < 0]
    avg_loss = round(sum([t['pnl_percent'] for t in losses]) / len(losses), 2) if losses else 0
    
    return {
        "strategy": "RSI Oversold Bounce",
        "symbol": "QQQ",
        "total_trades": total,
        "win_rate": win_rate,
        "avg_return": avg_return,
        "max_win": round(max_win, 2),
        "max_loss": round(max_loss, 2),
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "trades": trades
    }

def export_trades_for_pinescript(trades):
    """Export trade details in a format suitable for Pine Script verification"""
    print(f"\n📅 Trade Times for Pine Script Verification:")
    print("=" * 60)
    print("// Copy these times to your Pine Script for verification")
    print("// Format: [entry_time, exit_time, entry_price, exit_price, pnl_percent]")
    print("trades = [")
    
    for i, trade in enumerate(trades):
        entry_time = pd.to_datetime(trade['entry_time'])
        exit_time = pd.to_datetime(trade['exit_time'])
        
        # Convert to TradingView format (timestamp in milliseconds)
        entry_timestamp = int(entry_time.timestamp() * 1000)
        exit_timestamp = int(exit_time.timestamp() * 1000)
        
        print(f"    [{entry_timestamp}, {exit_timestamp}, {trade['entry_price']}, {trade['exit_price']}, {trade['pnl_percent']}], // Trade {i+1}")
    
    print("]")
    print("\n// Pine Script code to verify trades:")
    print("// for i = 0 to array.size(trades) - 1")
    print("//     trade = trades[i]")
    print("//     entry_time = trade[0]")
    print("//     exit_time = trade[1]")
    print("//     entry_price = trade[2]")
    print("//     exit_price = trade[3]")
    print("//     pnl = trade[4]")
    print("//     if time >= entry_time and time <= exit_time")
    print("//         label.new(bar_index, high, str.tostring(pnl) + '%')")
    
    # Also save to a separate file for easy copying
    with open("trade_times_for_pinescript.txt", "w") as f:
        f.write("// Trade Times for Pine Script Verification\n")
        f.write("// Format: [entry_time, exit_time, entry_price, exit_price, pnl_percent]\n")
        f.write("trades = [\n")
        
        for i, trade in enumerate(trades):
            entry_time = pd.to_datetime(trade['entry_time'])
            exit_time = pd.to_datetime(trade['exit_time'])
            entry_timestamp = int(entry_time.timestamp() * 1000)
            exit_timestamp = int(exit_time.timestamp() * 1000)
            
            f.write(f"    [{entry_timestamp}, {exit_timestamp}, {trade['entry_price']}, {trade['exit_price']}, {trade['pnl_percent']}], // Trade {i+1}\n")
        
        f.write("]\n")
        f.write("\n// Pine Script verification code:\n")
        f.write("// for i = 0 to array.size(trades) - 1\n")
        f.write("//     trade = trades[i]\n")
        f.write("//     entry_time = trade[0]\n")
        f.write("//     exit_time = trade[1]\n")
        f.write("//     entry_price = trade[2]\n")
        f.write("//     exit_price = trade[3]\n")
        f.write("//     pnl = trade[4]\n")
        f.write("//     if time >= entry_time and time <= exit_time\n")
        f.write("//         label.new(bar_index, high, str.tostring(pnl) + '%')\n")
    
    print(f"\n✅ Trade times saved to 'trade_times_for_pinescript.txt'")
    print(f"📁 You can copy the times from the file above or from the console output")

if __name__ == "__main__":
    symbol = "QQQ"  # QQQ tracks Nasdaq 100, similar to NQ futures
    start_date = "2025-01-27"
    end_date = "2025-08-01"

    print("🚀 Starting RSI Backtest with Validation")
    print("=" * 50)
    
    # Fetch and validate data
    df = fetch_1min_data(symbol, start_date, end_date)
    data_valid = validate_data_quality(df)
    
    if not data_valid:
        print("❌ Data quality issues detected. Proceeding with caution...")
    
    # Run backtest
    trades = backtest_rsi_strategy(df)
    
    # Validate trades
    valid_trades, invalid_trades = validate_trade_logic(trades, df)
    
    # Export trade times for Pine Script verification
    export_trades_for_pinescript(trades)
    
    # Analyze results
    results = analyze_results(trades)
    
    # Print summary
    print(f"\n📋 Final Results:")
    print(f"   Strategy: {results['strategy']}")
    print(f"   Symbol: {results['symbol']}")
    print(f"   Total Trades: {results['total_trades']}")
    print(f"   Win Rate: {results['win_rate']}%")
    print(f"   Avg Return: {results['avg_return']}%")
    print(f"   Max Win: {results['max_win']}%")
    print(f"   Max Loss: {results['max_loss']}%")
    print(f"   Avg Win: {results['avg_win']}%")
    print(f"   Avg Loss: {results['avg_loss']}%")
    
    # Save results
    with open("backtest_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Backtest complete with validation. Results saved to backtest_results.json")
    
    if invalid_trades > 0:
        print(f"⚠️  Warning: {invalid_trades} trades failed validation")
    else:
        print("✅ All trades passed validation") 