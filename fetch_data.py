import yfinance as yf
import pandas as pd

stocks = {
    "Technology": ["AAPL", "MSFT", "GOOGL", "NVDA", "META"],
    "Banking":    ["JPM", "BAC", "GS", "WFC", "C"],
    "Energy":     ["XOM", "CVX", "SLB", "COP", "BP"],
    "Healthcare": ["JNJ", "PFE", "UNH", "ABBV", "MRK"],
    "Retail":     ["AMZN", "WMT", "TGT", "COST", "HD"]
}

all_data = []

for sector, tickers in stocks.items():
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        raw = yf.download(ticker, start="2020-01-01", end="2025-01-01",
                  auto_adjust=True, progress=False)
        # Flatten multi-level columns
        raw.columns = raw.columns.get_level_values(0)
        raw = raw.reset_index()
        raw = raw.rename(columns={
            "Date":   "price_date",
            "Open":   "open_price",
            "Close":  "close_price",
            "High":   "high_price",
            "Low":    "low_price",
            "Volume": "volume"
        })
        raw["ticker"] = ticker
        raw["sector"] = sector
        raw = raw[["price_date","open_price","close_price",
                   "high_price","low_price","volume","ticker","sector"]]
        raw = raw.dropna()
        all_data.append(raw)

final_df = pd.concat(all_data, ignore_index=True)
print(f"\nTotal rows: {len(final_df)}")
print(f"Unique tickers: {final_df['ticker'].nunique()}")
print(final_df.head())

final_df.to_csv("stock_data.csv", index=False)
print("\nSaved to stock_data.csv")