"""
DeFi Protocol Analysis: Step 1 - Data Collection
Fetches current TVL data from DeFiLlama API (free, no auth required)
"""

import requests
import pandas as pd
from datetime import datetime
import os

# Get the project root directory (2 levels up from this script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# DeFiLlama API endpoint
API_URL = "https://api.llama.fi/protocols"

def fetch_protocol_data():
    """Fetch all protocol data from DeFiLlama"""
    print("Fetching data from DeFiLlama API...")
    
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        
        protocols = response.json()
        print(f"✅ Successfully fetched {len(protocols)} protocols")
        
        return protocols
    
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return []

def save_raw_data(protocols):
    """Save raw data to CSV"""
    # Extract key fields
    data = []
    for protocol in protocols:
        data.append({
            'name': protocol.get('name', 'Unknown'),
            'symbol': protocol.get('symbol', ''),
            'category': protocol.get('category', 'Other'),
            'chains': ', '.join(protocol.get('chains', [])),
            'tvl': protocol.get('tvl', 0),
            'change_1h': protocol.get('change_1h', None),
            'change_1d': protocol.get('change_1d', None),
            'change_7d': protocol.get('change_7d', None),
            'mcap': protocol.get('mcap', None),
            'url': protocol.get('url', ''),
            'description': protocol.get('description', '')
        })
    
    df = pd.DataFrame(data)
    
    # Sort by TVL descending
    df = df.sort_values('tvl', ascending=False)
    
    # Save to CSV
    filename = os.path.join(PROJECT_ROOT, '01_raw_data', 'defillama_tvl_raw.csv')
    df.to_csv(filename, index=False)
    
    print(f"✅ Raw data saved to: {filename}")
    print(f"📊 Total protocols: {len(df)}")
    print(f"💰 Total TVL: ${df['tvl'].sum():,.0f}")
    print(f"\nTop 5 Protocols by TVL:")
    print(df[['name', 'category', 'tvl']].head().to_string(index=False))
    
    return df

if __name__ == "__main__":
    protocols = fetch_protocol_data()
    
    if protocols:
        df = save_raw_data(protocols)
        print("\n✅ Data collection complete!")
    else:
        print("❌ Failed to fetch data")
