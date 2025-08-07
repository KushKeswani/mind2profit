import json
import re
from datetime import datetime
import requests
import pandas as pd
import ta

class StrategyChatbot:
    def __init__(self):
        self.api_key = "0097473bda6ba5d1b430afc0cefdcbd87820c51bbd6a64d6ce6cb33cc1ee9acc"
        self.together_url = "https://api.together.xyz/v1/chat/completions"
        
    def generate_strategy_code(self, strategy_description):
        """Generate Python backtesting code from strategy description"""
        
        system_prompt = """
You are an expert Python backtesting engineer. Generate complete, working Python code.

CRITICAL RULES:
1. Generate ONLY valid Python code - no explanations, no markdown
2. Use these exact imports: import requests, pandas as pd, ta, json, datetime
3. Use Alpaca API keys: PK0F1YSWGZYNHF1VKOY5 and ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB
4. Include try/except error handling
5. Use 'ta' library for technical indicators
6. Export results to JSON
7. Include main() function and if __name__ == "__main__" block
8. Keep code concise but complete

Return ONLY Python code, no explanations.
"""

        user_prompt = f"""
Create a complete Python backtesting script for:

{strategy_description}

Requirements:
- Use Alpaca API
- Include error handling
- Export to JSON
- Use 'ta' library
- Include main() function
- Return ONLY Python code
"""

        try:
            response = requests.post(
                self.together_url,
                json={
                    "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                                    "temperature": 0.2,
                "max_tokens": 4000
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                try:
                    code = response.json()["choices"][0]["message"]["content"]
                    
                    # Clean up the code - remove any markdown or thinking sections
                    if "```python" in code:
                        code = code.split("```python")[1].split("```")[0]
                    elif "```" in code:
                        code = code.split("```")[1]
                    
                    # Remove any thinking sections
                    if "<think>" in code:
                        code = code.split("<think>")[0] + code.split("</think>")[-1]
                    
                    return code.strip()
                except Exception as e:
                    return f"Error parsing response: {str(e)}"
            else:
                error_detail = response.text if response.text else "No error details"
                return f"Error generating code: {response.status_code} - {error_detail}"
                
        except Exception as e:
            return f"Error: {str(e)}"

    def validate_strategy_code(self, code):
        """Validate the generated strategy code"""
        validation_results = {
            "syntax_valid": False,
            "has_required_imports": False,
            "has_alpaca_api": False,
            "has_technical_indicators": False,
            "has_trade_logic": False,
            "has_error_handling": False,
            "issues": []
        }
        
        try:
            # Check for required imports
            if "import requests" in code and "import pandas" in code and "import ta" in code:
                validation_results["has_required_imports"] = True
            else:
                validation_results["issues"].append("Missing required imports (requests, pandas, ta)")
            
            # Check for Alpaca API usage
            if "alpaca" in code.lower() or "APCA-API-KEY" in code:
                validation_results["has_alpaca_api"] = True
            else:
                validation_results["issues"].append("Missing Alpaca API integration")
            
            # Check for technical indicators
            if "ta." in code or "RSI" in code or "MACD" in code or "SMA" in code:
                validation_results["has_technical_indicators"] = True
            else:
                validation_results["issues"].append("Missing technical indicators")
            
            # Check for trade logic
            if "trade" in code.lower() or "entry" in code.lower() or "exit" in code.lower():
                validation_results["has_trade_logic"] = True
            else:
                validation_results["issues"].append("Missing trade logic")
            
            # Check for error handling
            if "try:" in code and "except:" in code:
                validation_results["has_error_handling"] = True
            else:
                validation_results["issues"].append("Missing error handling")
            
            # Test syntax
            compile(code, '<string>', 'exec')
            validation_results["syntax_valid"] = True
            
        except SyntaxError as e:
            validation_results["issues"].append(f"Syntax error: {str(e)}")
        except Exception as e:
            validation_results["issues"].append(f"Validation error: {str(e)}")
        
        return validation_results

    def save_strategy_code(self, code, strategy_name, description):
        """Save the generated strategy code to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"strategy_{strategy_name.replace(' ', '_').lower()}_{timestamp}.py"
        
        # Add header comments
        header = f'''"""
Generated Strategy: {strategy_name}
Description: {description}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

'''
        
        full_code = header + code
        
        try:
            with open(filename, "w") as f:
                f.write(full_code)
            return filename
        except Exception as e:
            return f"Error saving file: {str(e)}"

    def create_strategy_summary(self, strategy_name, description, validation_results):
        """Create a summary of the generated strategy"""
        summary = {
            "strategy_name": strategy_name,
            "description": description,
            "generated_at": datetime.now().isoformat(),
            "validation": validation_results,
            "status": "ready" if validation_results["syntax_valid"] else "needs_fixes"
        }
        
        return summary

def main():
    """Main function to test the strategy chatbot"""
    chatbot = StrategyChatbot()
    
    print("🤖 Strategy Tester Chatbot")
    print("=" * 50)
    
    # Example strategy description
    strategy_description = """
    Create a moving average crossover strategy for QQQ:
    - Use 20-period and 50-period simple moving averages
    - Buy when 20 SMA crosses above 50 SMA
    - Sell when 20 SMA crosses below 50 SMA
    - Use 1-minute data from January 2025 to March 2025
    - Include proper risk management and position sizing
    """
    
    print("📝 Strategy Description:")
    print(strategy_description)
    print()
    
    print("🔄 Generating Python code...")
    generated_code = chatbot.generate_strategy_code(strategy_description)
    
    print("✅ Code generated successfully!")
    print()
    
    print("🔍 Validating code...")
    validation_results = chatbot.validate_strategy_code(generated_code)
    
    print("📊 Validation Results:")
    for key, value in validation_results.items():
        if key != "issues":
            status = "✅" if value else "❌"
            print(f"   {status} {key}: {value}")
    
    if validation_results["issues"]:
        print("\n⚠️  Issues found:")
        for issue in validation_results["issues"]:
            print(f"   - {issue}")
    
    print()
    print("💾 Saving strategy code...")
    filename = chatbot.save_strategy_code(generated_code, "Moving Average Crossover", strategy_description)
    print(f"✅ Saved to: {filename}")
    
    print()
    print("📋 Strategy Summary:")
    summary = chatbot.create_strategy_summary("Moving Average Crossover", strategy_description, validation_results)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main() 