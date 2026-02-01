"""
Web3 Uniswap Analysis: Generate cleaned data and Tableau export
"""

import pandas as pd
import os

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_DATA = os.path.join(PROJECT_ROOT, '01_raw_data', 'uniswap_sample_data.csv')
CLEANED_DATA = os.path.join(PROJECT_ROOT, '02_cleaned_data', 'uniswap_cleaned.csv')
TABLEAU_OUTPUT = os.path.join(PROJECT_ROOT, '04_tableau', 'uniswap_tableau.csv')

def clean_and_prepare():
    """Clean raw data and create Tableau export"""
    print("📂 Loading raw Uniswap data...")
    
    df = pd.read_csv(RAW_DATA)
    print(f"Original records: {len(df):,}")
    
    # Clean data
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.replace(' ', '_').str.lower()
    
    # Save cleaned version
    df_clean.to_csv(CLEANED_DATA, index=False)
    print(f"✅ Cleaned data saved: {CLEANED_DATA}")
    
    # Prepare Tableau version (aggregated)
    tableau_df = df_clean.copy()
    
    # Format dates if they exist
    if 'date' in tableau_df.columns:
        tableau_df['date'] = pd.to_datetime(tableau_df['date']).dt.strftime('%Y-%m-%d')
    
    # Save Tableau version
    tableau_df.to_csv(TABLEAU_OUTPUT, index=False)
    print(f"✅ Tableau file saved: {TABLEAU_OUTPUT}")
    print(f"📊 Records: {len(tableau_df):,}")
    
    return tableau_df

if __name__ == "__main__":
    clean_and_prepare()
    print("\n✅ Web3 data pipeline complete!")
