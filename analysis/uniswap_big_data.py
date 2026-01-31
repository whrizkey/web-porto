import pandas as pd
import matplotlib.pyplot as plt

# File Path
DATA_FILE = 'Data/uniswap_large_transactions.csv'

def analyze_large_data():
    print(f"Loading Big Data from {DATA_FILE}...")
    
    # OPTIMIZATION: Read useful columns only to save memory if needed
    cols = ['timestamp', 'amount_usd', 'fee_tier', 'gas_cost_usd']
    df = pd.read_csv(DATA_FILE, usecols=cols)
    
    # Convert Time
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print(f"Loaded {len(df):,} rows.")
    
    # 1. Volume Analysis by Tier
    # Group by Fee Tier and sum volume
    volume_by_tier = df.groupby('fee_tier')['amount_usd'].sum()
    print("\nTotal Volume by Tier:")
    print(volume_by_tier.apply(lambda x: f"${x:,.0f}"))
    
    # 2. Profitability Analysis (Simulated)
    # Revenue = Volume * Tier (e.g. 0.05% = 0.0005)
    # We map the tier string to a float
    tier_map = {'0.05%': 0.0005, '0.3%': 0.0030, '1.0%': 0.0100}
    df['fee_rate'] = df['fee_tier'].map(tier_map)
    df['revenue_generated'] = df['amount_usd'] * df['fee_rate']
    
    # Group by Month and Tier
    df['month'] = df['timestamp'].dt.to_period('M')
    monthly_rev = df.groupby(['month', 'fee_tier'])['revenue_generated'].sum().unstack()
    
    # Visualization: Monthly Revenue Trend
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = {'0.05%': '#2a9d8f', '0.3%': '#e9c46a', '1.0%': '#e76f51'}
    
    monthly_rev.plot(kind='bar', stacked=True, ax=ax, color=[colors.get(x, '#fff') for x in monthly_rev.columns])
    
    ax.set_title(f'Monthly Protocol Revenue ({len(df)/1_000_000:.1f}M Transactions)', color='white', fontsize=14, pad=20)
    ax.set_ylabel('Revenue (USD)', color='#a0a0a0')
    ax.set_xlabel('Month', color='#a0a0a0')
    
    # Remove junk
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#404040')
    ax.spines['left'].set_color('#404040')
    
    plt.tight_layout()
    output_path = 'assets/plots/web3_big_data.png'
    plt.savefig(output_path, dpi=150, facecolor='#0a0a0b')
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    analyze_large_data()
