# Investment Data Pipeline & Market Analytics

## Overview
End-to-end investment data pipeline ingesting equity market data from Yahoo Finance API into MySQL across 3 relational tables (6,300+ rows across 25 stocks, 5 sectors).

## Tech Stack
- Python (Pandas, yfinance)
- MySQL (3 relational tables, joins, aggregations)
- Power BI (dashboard — coming soon)

## Key Insight
Detected 12% volatility spike in Healthcare sector (ABBV) during 2024, identified through SQL standard deviation analysis across 6,300 price records.

## Files
- `fetch_data.py` — fetches stock data from Yahoo Finance API
- `load_to_mysql.py` — cleans and loads data into MySQL
- `analysis.sql` — SQL queries for insight generation
- `stock_data.csv` — raw data backup