from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
from strategy_chatbot import StrategyChatbot
import os

app = FastAPI(title="Strategy Tester API", version="1.0.0")

# Initialize the strategy chatbot
chatbot = StrategyChatbot()

# File to store saved strategies
SAVED_STRATEGIES_FILE = "saved_strategies.json"
# File to store public strategies
PUBLIC_STRATEGIES_FILE = "public_strategies.json"

class StrategyRequest(BaseModel):
    strategy_name: str
    description: str
    symbol: str = "QQQ"
    start_date: str = "2025-01-01"
    end_date: str = "2025-03-01"
    timeframe: str = "1Min"
    risk_per_trade: float = 1.0

class SaveStrategyRequest(BaseModel):
    strategy_name: str
    description: str
    symbol: str
    start_date: str
    end_date: str
    timeframe: str
    risk_per_trade: float
    generated_code: str
    validation_results: Dict[str, Any]
    summary: Optional[Dict[str, Any]] = None

class StrategyResponse(BaseModel):
    success: bool
    strategy_name: str
    generated_code: Optional[str] = None
    validation_results: Optional[Dict[str, Any]] = None
    filename: Optional[str] = None
    summary: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class PublicStrategyRequest(BaseModel):
    uuid: str
    name: str
    description: str
    entryConditions: Dict[str, List[str]]
    riskManagement: Dict[str, str]
    explanation: str
    author: str
    createdAt: str
    performance: Dict[str, float]

def load_saved_strategies():
    """Load saved strategies from JSON file"""
    if os.path.exists(SAVED_STRATEGIES_FILE):
        try:
            with open(SAVED_STRATEGIES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading saved strategies: {e}")
            return []
    return []

def save_strategies_to_file(strategies):
    """Save strategies to JSON file"""
    try:
        with open(SAVED_STRATEGIES_FILE, 'w') as f:
            json.dump(strategies, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving strategies: {e}")
        return False

def load_public_strategies():
    """Load public strategies from JSON file"""
    if os.path.exists(PUBLIC_STRATEGIES_FILE):
        try:
            with open(PUBLIC_STRATEGIES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading public strategies: {e}")
            return []
    return []

def save_public_strategies_to_file(strategies):
    """Save public strategies to JSON file"""
    try:
        with open(PUBLIC_STRATEGIES_FILE, 'w') as f:
            json.dump(strategies, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving public strategies: {e}")
        return False

@app.post("/generate-strategy", response_model=StrategyResponse)
async def generate_strategy(request: StrategyRequest):
    """Generate Python backtesting code from strategy description"""
    
    try:
        # Create enhanced strategy description
        enhanced_description = f"""
        Strategy: {request.strategy_name}
        Symbol: {request.symbol}
        Timeframe: {request.timeframe}
        Date Range: {request.start_date} to {request.end_date}
        Risk Per Trade: {request.risk_per_trade}%
        
        Strategy Description:
        {request.description}
        
        Requirements:
        - Use {request.symbol} data from Alpaca API
        - Use {request.timeframe} timeframe
        - Test from {request.start_date} to {request.end_date}
        - Implement risk management with {request.risk_per_trade}% risk per trade
        - Include proper validation and error handling
        - Export results to JSON format
        - Generate formatted trade list
        - Calculate position sizing based on risk percentage
        """
        
        print(f"🔄 Generating strategy: {request.strategy_name}")
        
        # Generate the Python code
        generated_code = chatbot.generate_strategy_code(enhanced_description)
        
        if generated_code.startswith("Error"):
            raise HTTPException(status_code=500, detail=generated_code)
        
        # Validate the generated code
        validation_results = chatbot.validate_strategy_code(generated_code)
        
        # Save the strategy code
        filename = chatbot.save_strategy_code(
            generated_code, 
            request.strategy_name, 
            request.description
        )
        
        # Create strategy summary
        summary = chatbot.create_strategy_summary(
            request.strategy_name,
            request.description,
            validation_results
        )
        
        return StrategyResponse(
            success=True,
            strategy_name=request.strategy_name,
            generated_code=generated_code,
            validation_results=validation_results,
            filename=filename,
            summary=summary
        )
        
    except Exception as e:
        return StrategyResponse(
            success=False,
            strategy_name=request.strategy_name,
            error=str(e)
        )

@app.get("/strategy-templates")
async def get_strategy_templates():
    """Get predefined strategy templates"""
    
    templates = {
        "moving_average_crossover": {
            "name": "Moving Average Crossover",
            "description": "Buy when short SMA crosses above long SMA, sell when it crosses below",
            "parameters": {
                "short_period": 20,
                "long_period": 50,
                "symbol": "QQQ"
            }
        },
        "rsi_oversold_bounce": {
            "name": "RSI Oversold Bounce",
            "description": "Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target",
            "parameters": {
                "rsi_period": 14,
                "oversold_level": 30,
                "exit_level": 50,
                "profit_target": 3.0,
                "stop_loss": -2.0
            }
        },
        "macd_crossover": {
            "name": "MACD Crossover",
            "description": "Buy when MACD line crosses above signal line, sell when it crosses below",
            "parameters": {
                "fast_period": 12,
                "slow_period": 26,
                "signal_period": 9
            }
        },
        "bollinger_bands": {
            "name": "Bollinger Bands Strategy",
            "description": "Buy when price touches lower band, sell when it reaches middle band",
            "parameters": {
                "period": 20,
                "std_dev": 2
            }
        },
        "volume_price_trend": {
            "name": "Volume Price Trend",
            "description": "Buy on high volume price breakouts, sell on volume decline",
            "parameters": {
                "volume_threshold": 1.5,
                "price_threshold": 0.5
            }
        }
    }
    
    return {"templates": templates}

@app.post("/run-strategy")
async def run_strategy(request: dict):
    strategy_file = request.get("strategy_file")
    """Run a generated strategy file"""
    
    try:
        # Import and run the strategy
        import subprocess
        import sys
        import json
        import os
        
        result = subprocess.run([sys.executable, strategy_file], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            # Check if backtest_results.json was created
            results_file = "backtest_results.json"
            if os.path.exists(results_file):
                try:
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                    
                    # Parse the results into structured format
                    trades = results.get('trades', [])
                    performance = results.get('performance', {})
                    
                    # Calculate real metrics
                    total_trades = len(trades)
                    winning_trades = len([t for t in trades if t.get('pnl_percent', 0) > 0])
                    losing_trades = total_trades - winning_trades
                    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
                    
                    total_pnl = sum([t.get('pnl_percent', 0) for t in trades])
                    avg_win = sum([t.get('pnl_percent', 0) for t in trades if t.get('pnl_percent', 0) > 0]) / winning_trades if winning_trades > 0 else 0
                    avg_loss = sum([t.get('pnl_percent', 0) for t in trades if t.get('pnl_percent', 0) < 0]) / losing_trades if losing_trades > 0 else 0
                    
                    return {
                        "success": True,
                        "output": result.stdout,
                        "message": "Strategy executed successfully",
                        "results": {
                            "totalTrades": total_trades,
                            "winningTrades": winning_trades,
                            "losingTrades": losing_trades,
                            "winRate": round(win_rate, 2),
                            "totalReturn": round(total_pnl, 2),
                            # maxDrawdown and sharpeRatio will be calculated from trades later
                            "avgWin": round(avg_win, 2),
                            "avgLoss": round(avg_loss, 2),
                            "trades": trades
                        }
                    }
                except Exception as e:
                    return {
                        "success": True,
                        "output": result.stdout,
                        "message": "Strategy executed but couldn't parse results",
                        "error": str(e)
                    }
            else:
                return {
                    "success": True,
                    "output": result.stdout,
                    "message": "Strategy executed successfully (no results file found)"
                }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "message": "Strategy execution failed"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to run strategy"
        }

@app.get("/strategy-status/{strategy_name}")
async def get_strategy_status(strategy_name: str):
    """Get the status of a generated strategy"""
    
    # This would typically check a database or file system
    # For now, return a mock status
    return {
        "strategy_name": strategy_name,
        "status": "ready",
        "last_updated": datetime.now().isoformat(),
        "validation_passed": True,
        "ready_to_run": True
    }

@app.post("/save-strategy")
async def save_strategy(request: SaveStrategyRequest):
    """Save a strategy for later use"""
    
    try:
        strategies = load_saved_strategies()
        
        # Create strategy object
        strategy = {
            "id": f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "strategy_name": request.strategy_name,
            "description": request.description,
            "symbol": request.symbol,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "timeframe": request.timeframe,
            "risk_per_trade": request.risk_per_trade,
            "generated_code": request.generated_code,
            "validation_results": request.validation_results,
            "summary": request.summary,
            "saved_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat()
        }
        
        # Add to strategies list
        strategies.append(strategy)
        
        # Save to file
        if save_strategies_to_file(strategies):
            return {
                "success": True,
                "message": "Strategy saved successfully",
                "strategy_id": strategy["id"]
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save strategy")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving strategy: {str(e)}")

@app.get("/saved-strategies")
async def get_saved_strategies():
    """Get all saved strategies"""
    
    try:
        strategies = load_saved_strategies()
        return {
            "success": True,
            "strategies": strategies
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading strategies: {str(e)}")

@app.get("/saved-strategy/{strategy_id}")
async def get_saved_strategy(strategy_id: str):
    """Get a specific saved strategy by ID"""
    
    try:
        strategies = load_saved_strategies()
        strategy = next((s for s in strategies if s["id"] == strategy_id), None)
        
        if strategy:
            return {
                "success": True,
                "strategy": strategy
            }
        else:
            raise HTTPException(status_code=404, detail="Strategy not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading strategy: {str(e)}")

@app.delete("/saved-strategy/{strategy_id}")
async def delete_saved_strategy(strategy_id: str):
    """Delete a saved strategy"""
    
    try:
        strategies = load_saved_strategies()
        original_count = len(strategies)
        
        # Remove strategy with matching ID
        strategies = [s for s in strategies if s["id"] != strategy_id]
        
        if len(strategies) < original_count:
            if save_strategies_to_file(strategies):
                return {
                    "success": True,
                    "message": "Strategy deleted successfully"
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to delete strategy")
        else:
            raise HTTPException(status_code=404, detail="Strategy not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting strategy: {str(e)}")

@app.post("/public-strategies")
async def publish_strategy(request: PublicStrategyRequest):
    """Publish a strategy to the public library"""
    
    try:
        public_strategies = load_public_strategies()
        
        # Create public strategy object
        public_strategy = {
            "uuid": request.uuid,
            "name": request.name,
            "description": request.description,
            "entryConditions": request.entryConditions,
            "riskManagement": request.riskManagement,
            "explanation": request.explanation,
            "author": request.author,
            "createdAt": request.createdAt,
            "performance": request.performance,
            "published_at": datetime.now().isoformat()
        }
        
        # Add to public strategies list
        public_strategies.append(public_strategy)
        
        # Save to file
        if save_public_strategies_to_file(public_strategies):
            return {
                "success": True,
                "message": "Strategy published successfully",
                "strategy_uuid": public_strategy["uuid"]
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to publish strategy")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error publishing strategy: {str(e)}")

@app.get("/public-strategies")
async def get_public_strategies():
    """Get all public strategies"""
    
    try:
        public_strategies = load_public_strategies()
        return {
            "success": True,
            "strategies": public_strategies
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading public strategies: {str(e)}")

@app.get("/public-strategy/{strategy_uuid}")
async def get_public_strategy(strategy_uuid: str):
    """Get a specific public strategy by UUID"""
    
    try:
        public_strategies = load_public_strategies()
        strategy = next((s for s in public_strategies if s["uuid"] == strategy_uuid), None)
        
        if strategy:
            return {
                "success": True,
                "strategy": strategy
            }
        else:
            raise HTTPException(status_code=404, detail="Public strategy not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading public strategy: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 