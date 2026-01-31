-- Uniswap V3: USDC-ETH 0.05% Pool Analysis
-- Copy and paste this into https://dune.com/queries/new to get REAL data for free.

WITH swaps AS (
    SELECT
        block_time AS timestamp,
        tx_hash,
        CASE 
            WHEN token_a_symbol = 'USDC' THEN amount0_adjusted 
            ELSE amount1_adjusted 
        END AS amount_usdc,
        -- Approximate Gas Cost (Gas Used * Gas Price in ETH * ETH Price)
        (t.gas_used * t.gas_price / 1e18) * p.price AS gas_cost_usd,
        '0.05%' AS fee_tier
    FROM uniswap_v3_ethereum.pair_event_swap s
    JOIN ethereum.transactions t ON s.tx_hash = t.hash
    LEFT JOIN prices.usd p ON p.minute = date_trunc('minute', block_time) AND p.symbol = 'WETH'
    WHERE pool = '0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640' -- USDC/ETH 0.05%
    AND block_time > NOW() - INTERVAL '30' day -- Last 30 Days (Dune Free Tier limit often likes smaller chunks for CSV export)
)

SELECT * FROM swaps
ORDER BY timestamp DESC
LIMIT 100000 -- Download limit for free users; Run multiple times for more days if needed.
