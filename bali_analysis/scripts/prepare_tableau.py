"""
Bali Hotel Analysis: Generate Tableau-ready CSV
Prepares cleaned data for Tableau Public visualization
"""

import pandas as pd
import os

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CLEANED_DATA = os.path.join(PROJECT_ROOT, '02_cleaned_data', 'hotel_data_cleaned.csv')
TABLEAU_OUTPUT = os.path.join(PROJECT_ROOT, '04_tableau', 'bali_revenue_tableau.csv')

def prepare_tableau_export():
    """Create Tableau-optimized CSV"""
    print("📊 Preparing Tableau-ready export...")
    
    # Load cleaned data
    df = pd.read_csv(CLEANED_DATA)
    
    # Tableau optimization
    # 1. Clean column names (no spaces, camelCase)
    df.columns = df.columns.str.replace(' ', '_').str.lower()
    
    # 2. Ensure date is in YYYY-MM-DD format
    if 'arrival_date' in df.columns:
        df['arrival_date'] = pd.to_datetime(df['arrival_date']).dt.strftime('%Y-%m-%d')
    
    # 3. Add calculated fields for Tableau
    if 'adr' in df.columns:
        df['revenue'] = df['adr'] * df.get('nights', 1)
    
    # 4. Sort by date
    if 'arrival_date' in df.columns:
        df = df.sort_values('arrival_date')
    
    # Save
    df.to_csv(TABLEAU_OUTPUT, index=False)
    
    print(f"✅ Tableau file saved: {TABLEAU_OUTPUT}")
    print(f"📊 Records: {len(df):,}")
    print(f"📅 Date range: {df['arrival_date'].min()} to {df['arrival_date'].max()}")
    print("\n💡 Import this into Tableau Public for interactive dashboards!")
    
    return df

if __name__ == "__main__":
    prepare_tableau_export()
