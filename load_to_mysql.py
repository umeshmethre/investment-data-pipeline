import pandas as pd
import mysql.connector

# ---- CONFIG ----
DB_USER = "root"
DB_PASS = "Sony@143"
DB_NAME = "investment_pipeline"
DB_HOST = "localhost"

# ---- LOAD & CLEAN CSV ----
df = pd.read_csv("stock_data.csv")
df = df[["price_date","open_price","close_price",
         "high_price","low_price","volume","ticker","sector"]]
df = df.dropna()
df["price_date"] = pd.to_datetime(df["price_date"]).dt.date
print(f"Clean rows to load: {len(df)}")

# ---- CONNECT ----
conn = mysql.connector.connect(
    host=DB_HOST, user=DB_USER,
    password=DB_PASS, database=DB_NAME,
    consume_results=True
)
cursor = conn.cursor()

# ---- INSERT SECTORS ----
sector_map = {}
for sector in df["sector"].unique():
    cursor.execute(
        "INSERT IGNORE INTO sectors (sector_name) VALUES (%s)", (sector,))
    conn.commit()
    cursor.execute(
        "SELECT sector_id FROM sectors WHERE sector_name = %s", (sector,))
    result = cursor.fetchone()
    sector_map[sector] = result[0]
print("Sectors done:", sector_map)

# ---- INSERT STOCKS ----
stock_map = {}
for _, row in df[["ticker","sector"]].drop_duplicates().iterrows():
    cursor.execute(
        "INSERT IGNORE INTO stocks (ticker, company_name, sector_id) VALUES (%s,%s,%s)",
        (row["ticker"], row["ticker"], sector_map[row["sector"]]))
    conn.commit()
    cursor.execute(
        "SELECT stock_id FROM stocks WHERE ticker = %s", (row["ticker"],))
    result = cursor.fetchone()
    stock_map[row["ticker"]] = result[0]
print(f"Stocks done: {len(stock_map)}")

# ---- INSERT DAILY PRICES ----
batch = []
for _, row in df.iterrows():
    batch.append((
        stock_map[row["ticker"]],
        row["price_date"],
        row["open_price"],
        row["close_price"],
        row["high_price"],
        row["low_price"],
        int(row["volume"])
    ))

cursor.executemany("""
    INSERT INTO daily_prices
    (stock_id, price_date, open_price, close_price, high_price, low_price, volume)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
""", batch)
conn.commit()
cursor.close()
conn.close()

print(f"\nTotal rows inserted: {len(batch)}")
print("All data loaded into MySQL successfully!")