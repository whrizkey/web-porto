"""
DeFi Protocol Analysis: Step 2 - Data Cleaning
Cleans and enriches the raw DeFiLlama data
"""

import pandas as pd
import os

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_DATA = os.path.join(PROJECT_ROOT, '01_raw_data', 'defillama_tvl_raw.csv')
CLEANED_DATA = os.path.join(PROJECT_ROOT, '02_cleaned_data', 'defillama_tvl_cleaned.csv')

def clean_data():
    """Load and clean the raw data"""
    print("📂 Loading raw data...")
    df = pd.read_csv(RAW_DATA)
    
    print(f"Original dataset: {len(df)} protocols")
    
    # 1. Remove protocols with TVL=0 or missing TVL
    df = df[df['tvl'] > 0]
    print(f"After removing zero TVL: {len(df)} protocols")
    
    # 2. Add derived columns
    # TVL in billions for readability
    df['tvl_billions'] = df['tvl'] / 1_000_000_000
    
    # Calculate market share %
    total_tvl = df['tvl'].sum()
    df['market_share_pct'] = (df['tvl'] / total_tvl) * 100
    
    # 3. Categorize chain count
    df['chain_count'] = df['chains'].apply(lambda x: len(x.split(', ')) if pd.notna(x) else 0)
    df['is_multi_chain'] = df['chain_count'] > 1
    
    # 4. Clean category names (standardize)
    df['category'] = df['category'].fillna('Other')
    df['category'] = df['category'].str.strip()
    
    # 5. Keep only top 100 protocols for analysis (manageable dataset)
    df_top = df.head(100).copy()
    
    print(f"✅ Keeping top 100 protocols by TVL")
    print(f"💰 Total TVL in dataset: ${df_top['tvl'].sum():,.0f}")
    print(f"📊 Coverage: {df_top['market_share_pct'].sum():.2f}% of total market")
    
    # Save cleaned data
    df_top.to_csv(CLEANED_DATA, index=False)
    print(f"\n✅ Cleaned data saved to: {CLEANED_DATA}")
    
    # Show some stats
    print("\n📈 Category Breakdown (Top 100):")
    category_stats = df_top.groupby('category')['tvl'].sum().sort_values(ascending=False).head()
    for cat, tvl in category_stats.items():
        print(f"  {cat}: ${tvl:,.0f}")
    
    return df_top

if __name__ == "__main__":
    df = clean_data()
    print("\n✅ Data cleaning complete!")
