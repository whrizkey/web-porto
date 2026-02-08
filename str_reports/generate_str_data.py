import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

def generate_daily_str_data(market, property_rooms, base_adr, base_occ, year=2025):
    """Generate daily STR data with segment mix"""
    
    property_name = f"Property_{market[:3].upper()}_001"
    
    # Generate all days in the year
    start_date = pd.Timestamp(f'{year}-01-01')
    end_date = pd.Timestamp(f'{year}-12-31')
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    
    for date in dates:
        # Seasonality factors
        month = date.month
        day_of_week = date.dayofweek  # 0=Monday, 6=Sunday
        
        if market == "Jakarta":
            # Corporate: Strong Mon-Thu, weaker Fri-Sun
            monthly_seasonal = [0.85, 0.88, 0.95, 1.00, 1.02, 0.92, 0.85, 0.87, 1.00, 1.05, 1.03, 0.82][month-1]
            dow_factor = [1.1, 1.1, 1.05, 1.0, 0.85, 0.70, 0.75][day_of_week]
            
            # Segment mix for corporate market
            seg_transient = np.random.normal(25, 5)  # Individual business travelers
            seg_group = np.random.normal(50, 8)      # MICE, corporate groups
            seg_contract = 100 - seg_transient - seg_group  # Corporate contracts
        else:  # Bali
            # Leisure: Strong Fri-Sun, consistent weekdays
            monthly_seasonal = [1.10, 1.08, 0.95, 0.92, 0.90, 1.05, 1.15, 1.18, 1.12, 0.95, 0.98, 1.15][month-1]
            dow_factor = [0.95, 0.95, 0.95, 1.0, 1.1, 1.2, 1.15][day_of_week]
            
            # Segment mix for resort market
            seg_transient = np.random.normal(75, 6)  # Leisure FIT
            seg_group = np.random.normal(15, 4)      # Tour groups, weddings
            seg_contract = 100 - seg_transient - seg_group  # OTA contracts
        
        # Constrain segments to realistic ranges
        seg_transient = np.clip(seg_transient, 10, 90)
        seg_group = np.clip(seg_group, 5, 80)
        seg_contract = 100 - seg_transient - seg_group
        
        # Daily occupancy
        occ = np.clip(base_occ * monthly_seasonal * dow_factor + np.random.normal(0, 5), 30, 100)
        rooms_sold = round(property_rooms * occ / 100)
        
        # Daily ADR (weighted by segment)
        base_daily_adr = base_adr * monthly_seasonal * dow_factor * np.random.normal(1, 0.03)
        
        # Segment ADR variations (transient pays more, contract pays less)
        adr_transient = round(base_daily_adr * 1.15, -3)
        adr_group = round(base_daily_adr * 0.90, -3)
        adr_contract = round(base_daily_adr * 0.85, -3)
        
        # Weighted average ADR
        adr = round((adr_transient * seg_transient + adr_group * seg_group + adr_contract * seg_contract) / 100, -3)
        revpar = round(adr * occ / 100, -3)
        
        # Revenue by segment
        total_revenue = adr * rooms_sold
        rev_transient = round(total_revenue * seg_transient / 100, -2)
        rev_group = round(total_revenue * seg_group / 100, -2)
        rev_contract = round(total_revenue * seg_contract / 100, -2)
        
        # CompSet (5-7 hotels average, slightly better)
        compset_occ = occ * np.random.normal(1.06, 0.02)
        compset_adr = adr * np.random.normal(1.09, 0.03)
        compset_revpar = round(compset_adr * compset_occ / 100, -3)
        
        # Market (all luxury hotels)
        market_occ = occ * np.random.normal(0.94, 0.04)
        market_adr = adr * np.random.normal(0.96, 0.05)
        market_revpar = round(market_adr * market_occ / 100, -3)
        
        # STR Indices
        mpi = round((occ / compset_occ) * 100, 1)
        ari = round((adr / compset_adr) * 100, 1)
        rgi = round((revpar / compset_revpar) * 100, 1)
        
        data.append({
            'date': date,
            'property_name': property_name,
            'market': market,
            'year': year,
            'month': month,
            'day_of_week': date.day_name(),
            'total_rooms': property_rooms,
            'rooms_sold': rooms_sold,
            'rooms_available': property_rooms,
            'occupancy': round(occ, 1),
            'adr': int(adr),
            'revpar': int(revpar),
            'compset_occupancy': round(compset_occ, 1),
            'compset_adr': int(compset_adr),
            'compset_revpar': int(compset_revpar),
            'market_occupancy': round(market_occ, 1),
            'market_adr': int(market_adr),
            'market_revpar': int(market_revpar),
            'mpi': mpi,
            'ari': ari,
            'rgi': rgi,
            'seg_transient_pct': round(seg_transient, 1),
            'seg_group_pct': round(seg_group, 1),
            'seg_contract_pct': round(seg_contract, 1),
            'adr_transient': int(adr_transient),
            'adr_group': int(adr_group),
            'adr_contract': int(adr_contract),
            'revenue_transient': int(rev_transient),
            'revenue_group': int(rev_group),
            'revenue_contract': int(rev_contract),
            'total_revenue': int(total_revenue)
        })
    
    return pd.DataFrame(data)

def aggregate_to_monthly(df):
    """Aggregate daily data to monthly with segment details"""
    
    monthly = df.groupby(['property_name', 'market', 'year', 'month']).agg({
        'total_rooms': 'first',
        'rooms_sold': 'sum',
        'rooms_available': 'sum',
        'total_revenue': 'sum',
        'revenue_transient': 'sum',
        'revenue_group': 'sum',
        'revenue_contract': 'sum',
        'compset_occupancy': 'mean',
        'compset_adr': 'mean',
        'market_occupancy': 'mean',
        'market_adr': 'mean'
    }).reset_index()
    
    # Calculate monthly metrics
    monthly['occupancy'] = round((monthly['rooms_sold'] / monthly['rooms_available']) * 100, 1)
    monthly['adr'] = round(monthly['total_revenue'] / monthly['rooms_sold'], -3).astype(int)
    monthly['revpar'] = round(monthly['adr'] * monthly['occupancy'] / 100, -3).astype(int)
    
    # Segment mix percentages
    monthly['seg_transient_pct'] = round((monthly['revenue_transient'] / monthly['total_revenue']) * 100, 1)
    monthly['seg_group_pct'] = round((monthly['revenue_group'] / monthly['total_revenue']) * 100, 1)
    monthly['seg_contract_pct'] = round((monthly['revenue_contract'] / monthly['total_revenue']) * 100, 1)
    
    # CompSet and Market
    monthly['compset_occupancy'] = monthly['compset_occupancy'].round(1)
    monthly['compset_adr'] = monthly['compset_adr'].round(-3).astype(int)
    monthly['compset_revpar'] = round(monthly['compset_adr'] * monthly['compset_occupancy'] / 100, -3).astype(int)
    
    monthly['market_occupancy'] = monthly['market_occupancy'].round(1)
    monthly['market_adr'] = monthly['market_adr'].round(-3).astype(int)
    monthly['market_revpar'] = round(monthly['market_adr'] * monthly['market_occupancy'] / 100, -3).astype(int)
    
    # STR Indices
    monthly['mpi'] = round((monthly['occupancy'] / monthly['compset_occupancy']) * 100, 1)
    monthly['ari'] = round((monthly['adr'] / monthly['compset_adr']) * 100, 1)
    monthly['rgi'] = round((monthly['revpar'] / monthly['compset_revpar']) * 100, 1)
    
    # Add month name
    monthly['month_name'] = pd.to_datetime(monthly['year'].astype(str) + '-' + monthly['month'].astype(str) + '-01').dt.strftime('%B')
    
    # Sort columns
    monthly = monthly[['property_name', 'market', 'year', 'month', 'month_name',
                      'total_rooms', 'rooms_sold', 'rooms_available', 'occupancy', 'adr', 'revpar',
                      'compset_occupancy', 'compset_adr', 'compset_revpar',
                      'market_occupancy', 'market_adr', 'market_revpar',
                      'mpi', 'ari', 'rgi',
                      'seg_transient_pct', 'seg_group_pct', 'seg_contract_pct',
                      'total_revenue', 'revenue_transient', 'revenue_group', 'revenue_contract']]
    
    return monthly

def aggregate_to_quarterly(df):
    """Aggregate daily data to quarterly"""
    df['quarter'] = df['date'].dt.quarter
    
    quarterly = df.groupby(['property_name', 'market', 'year', 'quarter']).agg({
        'total_rooms': 'first',
        'rooms_sold': 'sum',
        'rooms_available': 'sum',
        'total_revenue': 'sum',
        'revenue_transient': 'sum',
        'revenue_group': 'sum',
        'revenue_contract': 'sum',
        'compset_occupancy': 'mean',
        'compset_adr': 'mean',
        'market_occupancy': 'mean',
        'market_adr': 'mean'
    }).reset_index()
    
    # Calculate quarterly metrics
    quarterly['occupancy'] = round((quarterly['rooms_sold'] / quarterly['rooms_available']) * 100, 1)
    quarterly['adr'] = round(quarterly['total_revenue'] / quarterly['rooms_sold'], -3).astype(int)
    quarterly['revpar'] = round(quarterly['adr'] * quarterly['occupancy'] / 100, -3).astype(int)
    
    # Segment mix
    quarterly['seg_transient_pct'] = round((quarterly['revenue_transient'] / quarterly['total_revenue']) * 100, 1)
    quarterly['seg_group_pct'] = round((quarterly['revenue_group'] / quarterly['total_revenue']) * 100, 1)
    quarterly['seg_contract_pct'] = round((quarterly['revenue_contract'] / quarterly['total_revenue']) * 100, 1)
    
    # CompSet and Market
    quarterly['compset_occupancy'] = quarterly['compset_occupancy'].round(1)
    quarterly['compset_adr'] = quarterly['compset_adr'].round(-3).astype(int)
    quarterly['compset_revpar'] = round(quarterly['compset_adr'] * quarterly['compset_occupancy'] / 100, -3).astype(int)
    
    quarterly['market_occupancy'] = quarterly['market_occupancy'].round(1)
    quarterly['market_adr'] = quarterly['market_adr'].round(-3).astype(int)
    quarterly['market_revpar'] = round(quarterly['market_adr'] * quarterly['market_occupancy'] / 100, -3).astype(int)
    
    # STR Indices
    quarterly['mpi'] = round((quarterly['occupancy'] / quarterly['compset_occupancy']) * 100, 1)
    quarterly['ari'] = round((quarterly['adr'] / quarterly['compset_adr']) * 100, 1)
    quarterly['rgi'] = round((quarterly['revpar'] / quarterly['compset_revpar']) * 100, 1)
    
    quarterly['quarter_name'] = 'Q' + quarterly['quarter'].astype(str)
    
    return quarterly

# Generate data for BOTH 2024 and 2025
print("="*70)
print("GENERATING COMPLETE STR DATASET (2024-2025)")
print("="*70)

all_data = []

for year in [2024, 2025]:
    print(f"\n[{year}] Generating Jakarta data...")
    jakarta_daily = generate_daily_str_data(
        market="Jakarta",
        property_rooms=280,
        base_adr=3500000,
        base_occ=68,
        year=year
    )
    
    print(f"[{year}] Generating Bali data...")
    bali_daily = generate_daily_str_data(
        market="Bali",
        property_rooms=180,
        base_adr=5200000,
        base_occ=75,
        year=year
    )
    
    all_data.append((year, jakarta_daily, bali_daily))

# Combine years and create aggregates
print("\nCreating combined datasets...")
jakarta_daily_all = pd.concat([d[1] for d in all_data], ignore_index=True)
bali_daily_all = pd.concat([d[2] for d in all_data], ignore_index=True)

jakarta_monthly_all = aggregate_to_monthly(jakarta_daily_all)
bali_monthly_all = aggregate_to_monthly(bali_daily_all)

jakarta_quarterly_all = aggregate_to_quarterly(jakarta_daily_all)
bali_quarterly_all = aggregate_to_quarterly(bali_daily_all)

# Create output directory
os.makedirs("data", exist_ok=True)

# Save comprehensive reports
jakarta_daily_all.to_csv("data/jakarta_daily_2024_2025.csv", index=False)
bali_daily_all.to_csv("data/bali_daily_2024_2025.csv", index=False)

jakarta_monthly_all.to_csv("data/jakarta_monthly_2024_2025.csv", index=False)
bali_monthly_all.to_csv("data/bali_monthly_2024_2025.csv", index=False)

jakarta_quarterly_all.to_csv("data/jakarta_quarterly_2024_2025.csv", index=False)
bali_quarterly_all.to_csv("data/bali_quarterly_2024_2025.csv", index=False)

# Also save individual year files for convenience
for year, jkt, bal in all_data:
    aggregate_to_monthly(jkt).to_csv(f"data/jakarta_monthly_{year}.csv", index=False)
    aggregate_to_monthly(bal).to_csv(f"data/bali_monthly_{year}.csv", index=False)

print("\n" + "="*70)
print("DATASET SUMMARY")
print("="*70)
print(f"\n✓ Jakarta (280 rooms):")
print(f"  - Daily records: {len(jakarta_daily_all)} ({len(jakarta_daily_all)//365} years)")
print(f"  - Monthly records: {len(jakarta_monthly_all)}")
print(f"  - Quarterly records: {len(jakarta_quarterly_all)}")

print(f"\n✓ Bali (180 rooms):")
print(f"  - Daily records: {len(bali_daily_all)} ({len(bali_daily_all)//365} years)")
print(f"  - Monthly records: {len(bali_monthly_all)}")
print(f"  - Quarterly records: {len(bali_quarterly_all)}")

print("\n" + "="*70)
print("SEGMENT MIX SAMPLE - Jakarta 2025")
print("="*70)
sample_jkt = jakarta_monthly_all[jakarta_monthly_all['year'] == 2025][['month_name', 'seg_transient_pct', 'seg_group_pct', 'seg_contract_pct']].head(6)
print(sample_jkt.to_string(index=False))

print("\n" + "="*70)
print("YOY COMPARISON SAMPLE - Bali")
print("="*70)
yoy_sample = bali_monthly_all[bali_monthly_all['month'] == 1][['year', 'month_name', 'occupancy', 'adr', 'revpar', 'mpi', 'rgi']]
print(yoy_sample.to_string(index=False))

print("\n✓ All files saved to data/ directory")
print("\n" + "="*70)
print("FILES CREATED:")
print("="*70)
print("  Multi-year datasets:")
print("    - jakarta_daily_2024_2025.csv")
print("    - bali_daily_2024_2025.csv")
print("    - jakarta_monthly_2024_2025.csv")
print("    - bali_monthly_2024_2025.csv")
print("    - jakarta_quarterly_2024_2025.csv")
print("    - bali_quarterly_2024_2025.csv")
print("  Single-year datasets:")
print("    - jakarta_monthly_2024.csv / jakarta_monthly_2025.csv")
print("    - bali_monthly_2024.csv / bali_monthly_2025.csv")
print("="*70)
