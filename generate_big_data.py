import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta

# Configuration
NUM_ROWS = 1_000_000 # 1 Million transactions
START_DATE = datetime(2025, 1, 1)

def generate_large_dataset():
    print(f"Generating {NUM_ROWS:,} transactions... (This might take a moment)")
    
    # 1. Generate Dates (Random distribution over 1 year)
    # We use numpy to generate random seconds offset
    offsets = np.random.randint(0, 31536000, NUM_ROWS) # Seconds in a year
    dates = [START_DATE + timedelta(seconds=int(x)) for x in offsets]
    dates.sort() # Sort by time
    
    # 2. Generate Amounts (Log-normal distribution to simulate real crypto: many small, few whales)
    amounts = np.random.lognormal(mean=7, sigma=2, size=NUM_ROWS)
    # Clip to realistic ranges ($10 to $10M)
    amounts = np.clip(amounts, 10, 10_000_000)
    
    # 3. Generate Fee Tiers (Weighted: 0.05% matches high volume)
    fee_tiers = np.random.choice(['0.05%', '0.3%', '1.0%'], size=NUM_ROWS, p=[0.7, 0.25, 0.05])
    
    # 4. Generate Gas Costs (Ethereum gas fluctuates)
    gas_costs = np.random.normal(5, 2, size=NUM_ROWS) # Avg $5 gas
    gas_costs = np.clip(gas_costs, 1, 50)
    
    # 5. Create DataFrame
    df = pd.DataFrame({
        'transaction_hash': [str(uuid.uuid4()) for _ in range(NUM_ROWS)], # Unique IDs
        'timestamp': dates,
        'amount_usd': amounts,
        'fee_tier': fee_tiers,
        'gas_cost_usd': gas_costs,
        'slippage_impact': np.random.uniform(0.0001, 0.005, NUM_ROWS) # Random slippage
    })
    
    # Save to CSV
    filename = 'Data/uniswap_large_transactions.csv'
    print(f"Saving to {filename}...")
    df.to_csv(filename, index=False)
    print("Done! Dataset ready.")

if __name__ == "__main__":
    generate_large_dataset()
