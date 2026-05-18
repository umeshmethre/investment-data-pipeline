USE investment_pipeline;

-- Query 1: Volatility per stock
SELECT st.ticker,
       se.sector_name,
       ROUND(STDDEV(dp.close_price), 2) AS price_volatility,
       ROUND((STDDEV(dp.close_price) / AVG(dp.close_price)) * 100, 2) AS volatility_pct
FROM daily_prices dp
JOIN stocks st ON dp.stock_id = st.stock_id
JOIN sectors se ON st.sector_id = se.sector_id
GROUP BY st.ticker, se.sector_name
ORDER BY volatility_pct DESC;

-- Query 2: Average closing price per sector
SELECT se.sector_name,
       ROUND(AVG(dp.close_price), 2) AS avg_close_price
FROM daily_prices dp
JOIN stocks st ON dp.stock_id = st.stock_id
JOIN sectors se ON st.sector_id = se.sector_id
GROUP BY se.sector_name
ORDER BY avg_close_price DESC;

-- Query 3: Sector-wise total trading volume
SELECT se.sector_name,
       ROUND(SUM(dp.volume) / 1000000, 2) AS total_volume_millions
FROM daily_prices dp
JOIN stocks st ON dp.stock_id = st.stock_id
JOIN sectors se ON st.sector_id = se.sector_id
GROUP BY se.sector_name
ORDER BY total_volume_millions DESC;

-- Query 4: NVDA month-over-month volatility spike (KEY INSIGHT)
SELECT 
    st.ticker,
    DATE_FORMAT(dp.price_date, '%Y-%m') AS month,
    ROUND(AVG(dp.close_price), 2) AS avg_close,
    ROUND(
        (AVG(dp.close_price) - LAG(AVG(dp.close_price)) 
        OVER (PARTITION BY st.ticker ORDER BY DATE_FORMAT(dp.price_date, '%Y-%m')))
        / LAG(AVG(dp.close_price)) 
        OVER (PARTITION BY st.ticker ORDER BY DATE_FORMAT(dp.price_date, '%Y-%m')) * 100
    , 2) AS mom_change_pct
FROM daily_prices dp
JOIN stocks st ON dp.stock_id = st.stock_id
JOIN sectors se ON st.sector_id = se.sector_id
WHERE se.sector_name = 'Technology'
AND st.ticker = 'NVDA'
GROUP BY st.ticker, month
ORDER BY month;