import os
from google import genai
import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. Setup Client (GitHub will 'inject' the API Key here later)
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def run_sentiment_check(ticker_symbol):
    # Fetch free news from yfinance
    ticker = yf.Ticker(ticker_symbol)
    news = ticker.news[:5]
    
    headlines = [n['title'] for n in news]
    
    prompt = f"Analyze these headlines for {ticker_symbol} and give a sentiment score (-1 to 1). Be concise: {headlines}"
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents=prompt
    )
    
    # Create a simple data row
    new_data = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Ticker": ticker_symbol,
        "Score": response.text.strip()
    }
    return new_data

# Run for your main watch list
stocks = ["NVDA", "CRWD", "KO"]
results = [run_sentiment_check(s) for s in stocks]

# Save to a CSV file (This creates a historical record)
df = pd.DataFrame(results)
df.to_csv("sentiment_history.csv", mode='a', header=not os.path.exists("sentiment_history.csv"), index=False)
print("Analysis complete and saved to sentiment_history.csv")
