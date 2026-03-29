import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
  data = yf.download(ticker, period="3mo", interval="1d")

   # 🔥 Fix MultiIndex properly
  if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # 🔥 Ensure required columns exist
  required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
  data = data[[col for col in required_cols if col in data.columns]]


  return data  