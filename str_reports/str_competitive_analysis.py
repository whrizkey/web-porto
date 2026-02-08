import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set portfolio design style
plt.style.use('dark_background')
sns.set_context("talk")
colors = ["#E97451", "#2A9D8F", "#F4A261", "#264653", "#E76F51"]
sns.set_palette(sns.color_palette(colors))

# Create output directory
os.makedirs("visualizations", exist_ok=True)

def load_data(market):
    """Load all datasets for a market"""
    daily = pd.read_csv(f"data/{market}_daily_2024_2025.csv")
    monthly = pd.read_csv(f"data/{market}_monthly_2024_2025.csv")
    quarterly = pd.read_csv(f"data/{market}_quarterly_2024_2025.csv")
    
    daily['date'] = pd.to_datetime(daily['date'])
    
    return daily, monthly, quarterly

def plot_absolute_performance(monthly, market):
    """Chart 1: Occupancy, ADR, RevPAR trends"""
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.patch.set_facecolor('#0a0a0b')
    
    monthly_2025 = monthly[monthly['year'] == 2025].copy()
    monthly_2025['month_label'] = pd.Categorical(monthly_2025['month_name'], 
                                                  categories=['January', 'February', 'March', 'April', 'May', 'June',
                                                             'July', 'August', 'September', 'October', 'November', 'December'],
                                                  ordered=True)
    monthly_2025 = monthly_2025.sort_values('month_label')
    
    # Occupancy
    axes[0].plot(monthly_2025['month_label'], monthly_2025['occupancy'], 
                color='#2A9D8F', linewidth=3, marker='o', markersize=8)
    axes[0].axhline(y=monthly_2025['occupancy'].mean(), color='#E97451', 
                   linestyle='--', linewidth=2, label=f"Avg: {monthly_2025['occupancy'].mean():.1f}%")
    axes[0].set_title(f"{market.title()} - Occupancy % (2025)", color='white', fontsize=16, pad=15)
    axes[0].set_ylabel("Occupancy %", color='white')
    axes[0].legend(frameon=False, labelcolor='white')
    axes[0].grid(color='#27272a', linestyle='--', alpha=0.3)
    axes[0].set_facecolor('#0a0a0b')
    
    # ADR
    axes[1].plot(monthly_2025['month_label'], monthly_2025['adr']/1000000, 
                color='#E97451', linewidth=3, marker='o', markersize=8)
    axes[1].axhline(y=monthly_2025['adr'].mean()/1000000, color='#2A9D8F', 
                   linestyle='--', linewidth=2, label=f"Avg: {monthly_2025['adr'].mean()/1000000:.1f}M IDR")
    axes[1].set_title(f"{market.title()} - Average Daily Rate (2025)", color='white', fontsize=16, pad=15)
    axes[1].set_ylabel("ADR (M IDR)", color='white')
    axes[1].legend(frameon=False, labelcolor='white')
    axes[1].grid(color='#27272a', linestyle='--', alpha=0.3)
    axes[1].set_facecolor('#0a0a0b')
    
    # RevPAR
    axes[2].plot(monthly_2025['month_label'], monthly_2025['revpar']/1000000, 
                color='#F4A261', linewidth=3, marker='o', markersize=8)
    axes[2].axhline(y=monthly_2025['revpar'].mean()/1000000, color='#2A9D8F', 
                   linestyle='--', linewidth=2, label=f"Avg: {monthly_2025['revpar'].mean()/1000000:.1f}M IDR")
    axes[2].set_title(f"{market.title()} - Revenue Per Available Room (2025)", color='white', fontsize=16, pad=15)
    axes[2].set_ylabel("RevPAR (M IDR)", color='white')
    axes[2].set_xlabel("Month", color='white')
    axes[2].legend(frameon=False, labelcolor='white')
    axes[2].grid(color='#27272a', linestyle='--', alpha=0.3)
    axes[2].set_facecolor('#0a0a0b')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"visualizations/{market}_absolute_performance.png", dpi=150, facecolor='#0a0a0b')
    plt.close()
    print(f"✓ Created {market}_absolute_performance.png")

def plot_str_indices(monthly, market):
    """Chart 2: STR Indices (MPI, ARI, RGI)"""
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor('#0a0a0b')
    
    monthly_2025 = monthly[monthly['year'] == 2025].copy()
    monthly_2025['month_label'] = pd.Categorical(monthly_2025['month_name'], 
                                                  categories=['January', 'February', 'March', 'April', 'May', 'June',
                                                             'July', 'August', 'September', 'October', 'November', 'December'],
                                                  ordered=True)
    monthly_2025 = monthly_2025.sort_values('month_label')
    
    x = np.arange(len(monthly_2025))
    width = 0.25
    
    ax.bar(x - width, monthly_2025['mpi'], width, label='MPI (Occupancy Index)', color='#2A9D8F')
    ax.bar(x, monthly_2025['ari'], width, label='ARI (Rate Index)', color='#E97451')
    ax.bar(x + width, monthly_2025['rgi'], width, label='RGI (Revenue Index)', color='#F4A261')
    
    ax.axhline(y=100, color='white', linestyle='--', linewidth=2, alpha=0.5, label='Fair Share (100)')
    
    ax.set_title(f"{market.title()} - STR Index Performance vs Competitive Set (2025)", 
                color='white', fontsize=16, pad=15)
    ax.set_ylabel("Index Value", color='white')
    ax.set_xlabel("Month", color='white')
    ax.set_xticks(x)
    ax.set_xticklabels(monthly_2025['month_label'], rotation=45)
    ax.legend(frameon=False, labelcolor='white')
    ax.grid(axis='y', color='#27272a', linestyle='--', alpha=0.3)
    ax.set_facecolor('#0a0a0b')
    
    # Add text annotation
    avg_rgi = monthly_2025['rgi'].mean()
    status = "Underperforming" if avg_rgi < 100 else "Outperforming"
    ax.text(0.98, 0.95, f"Avg RGI: {avg_rgi:.1f} ({status})", 
           transform=ax.transAxes, fontsize=12, color='#E97451',
           verticalalignment='top', horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='#1a1a1d', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(f"visualizations/{market}_str_indices.png", dpi=150, facecolor='#0a0a0b')
    plt.close()
    print(f"✓ Created {market}_str_indices.png")

def plot_yoy_comparison(monthly, market):
    """Chart 3: Year-over-Year Comparison"""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor('#0a0a0b')
    
    monthly_2024 = monthly[monthly['year'] == 2024].copy()
    monthly_2025 = monthly[monthly['year'] == 2025].copy()
    
    # Sort both by month
    monthly_2024 = monthly_2024.sort_values('month')
    monthly_2025 = monthly_2025.sort_values('month')
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    x = np.arange(len(months))
    width = 0.35
    
    # Occupancy YoY
    axes[0].bar(x - width/2, monthly_2024['occupancy'], width, label='2024', color='#264653', alpha=0.8)
    axes[0].bar(x + width/2, monthly_2025['occupancy'], width, label='2025', color='#2A9D8F')
    axes[0].set_title("Occupancy % YoY", color='white', fontsize=14)
    axes[0].set_ylabel("Occupancy %", color='white')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(months, rotation=45)
    axes[0].legend(frameon=False, labelcolor='white')
    axes[0].grid(axis='y', color='#27272a', linestyle='--', alpha=0.3)
    axes[0].set_facecolor('#0a0a0b')
    
    # ADR YoY
    axes[1].bar(x - width/2, monthly_2024['adr']/1000000, width, label='2024', color='#264653', alpha=0.8)
    axes[1].bar(x + width/2, monthly_2025['adr']/1000000, width, label='2025', color='#E97451')
    axes[1].set_title("ADR (M IDR) YoY", color='white', fontsize=14)
    axes[1].set_ylabel("ADR (M IDR)", color='white')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(months, rotation=45)
    axes[1].legend(frameon=False, labelcolor='white')
    axes[1].grid(axis='y', color='#27272a', linestyle='--', alpha=0.3)
    axes[1].set_facecolor('#0a0a0b')
    
    # RevPAR YoY
    axes[2].bar(x - width/2, monthly_2024['revpar']/1000000, width, label='2024', color='#264653', alpha=0.8)
    axes[2].bar(x + width/2, monthly_2025['revpar']/1000000, width, label='2025', color='#F4A261')
    axes[2].set_title("RevPAR (M IDR) YoY", color='white', fontsize=14)
    axes[2].set_ylabel("RevPAR (M IDR)", color='white')
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(months, rotation=45)
    axes[2].legend(frameon=False, labelcolor='white')
    axes[2].grid(axis='y', color='#27272a', linestyle='--', alpha=0.3)
    axes[2].set_facecolor('#0a0a0b')
    
    fig.suptitle(f"{market.title()} - Year-over-Year Performance (2024 vs 2025)", 
                color='white', fontsize=16, y=1.02)
    
    plt.tight_layout()
    plt.savefig(f"visualizations/{market}_yoy_comparison.png", dpi=150, facecolor='#0a0a0b')
    plt.close()
    print(f"✓ Created {market}_yoy_comparison.png")

def plot_day_of_week(daily, market):
    """Chart 4: Day-of-Week Performance"""
    daily_2025 = daily[daily['year'] == 2025].copy()
    
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_avg = daily_2025.groupby('day_of_week')[['occupancy', 'adr', 'revpar']].mean()
    dow_avg = dow_avg.reindex(dow_order)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#0a0a0b')
    
    # Occupancy by DOW
    axes[0].bar(range(7), dow_avg['occupancy'], color='#2A9D8F')
    axes[0].set_title(f"{market.title()} - Occupancy by Day of Week (2025)", color='white', fontsize=14)
    axes[0].set_ylabel("Average Occupancy %", color='white')
    axes[0].set_xticks(range(7))
    axes[0].set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=45)
    axes[0].grid(axis='y', color='#27272a', linestyle='--', alpha=0.3)
    axes[0].set_facecolor('#0a0a0b')
    
    # RevPAR by DOW
    axes[1].bar(range(7), dow_avg['revpar']/1000000, color='#F4A261')
    axes[1].set_title(f"{market.title()} - RevPAR by Day of Week (2025)", color='white', fontsize=14)
    axes[1].set_ylabel("Average RevPAR (M IDR)", color='white')
    axes[1].set_xticks(range(7))
    axes[1].set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=45)
    axes[1].grid(axis='y', color='#27272a', linestyle='--', alpha=0.3)
    axes[1].set_facecolor('#0a0a0b')
    
    plt.tight_layout()
    plt.savefig(f"visualizations/{market}_day_of_week.png", dpi=150, facecolor='#0a0a0b')
    plt.close()
    print(f"✓ Created {market}_day_of_week.png")

def plot_segment_mix(monthly, market):
    """Chart 5: Segment Mix Analysis"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#0a0a0b')
    
    monthly_2025 = monthly[monthly['year'] == 2025].copy()
    monthly_2025 = monthly_2025.sort_values('month')
    
    # Segment mix percentages
    months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    axes[0].bar(months_short, monthly_2025['seg_transient_pct'], 
               label='Transient', color='#2A9D8F', alpha=0.9)
    axes[0].bar(months_short, monthly_2025['seg_group_pct'], 
               bottom=monthly_2025['seg_transient_pct'],
               label='Group', color='#E97451', alpha=0.9)
    axes[0].bar(months_short, monthly_2025['seg_contract_pct'], 
               bottom=monthly_2025['seg_transient_pct'] + monthly_2025['seg_group_pct'],
               label='Contract', color='#F4A261', alpha=0.9)
    
    axes[0].set_title(f"{market.title()} - Segment Mix % (2025)", color='white', fontsize=14)
    axes[0].set_ylabel("Percentage", color='white')
    axes[0].set_xlabel("Month", color='white')
    axes[0].legend(frameon=False, labelcolor='white')
    axes[0].set_facecolor('#0a0a0b')
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45)
    
    # Segment revenue contribution
    axes[1].bar(months_short, monthly_2025['revenue_transient']/1000000, 
               label='Transient', color='#2A9D8F', alpha=0.9)
    axes[1].bar(months_short, monthly_2025['revenue_group']/1000000, 
               bottom=monthly_2025['revenue_transient']/1000000,
               label='Group', color='#E97451', alpha=0.9)
    axes[1].bar(months_short, monthly_2025['revenue_contract']/1000000, 
               bottom=(monthly_2025['revenue_transient'] + monthly_2025['revenue_group'])/1000000,
               label='Contract', color='#F4A261', alpha=0.9)
    
    axes[1].set_title(f"{market.title()} - Revenue by Segment (2025)", color='white', fontsize=14)
    axes[1].set_ylabel("Revenue (M IDR)", color='white')
    axes[1].set_xlabel("Month", color='white')
    axes[1].legend(frameon=False, labelcolor='white')
    axes[1].set_facecolor('#0a0a0b')
    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    plt.savefig(f"visualizations/{market}_segment_mix.png", dpi=150, facecolor='#0a0a0b')
    plt.close()
    print(f"✓ Created {market}_segment_mix.png")

def plot_market_gaps(monthly, market):
    """Chart 6: Market vs CompSet Gap Analysis"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#0a0a0b')
    
    monthly_2025 = monthly[monthly['year'] == 2025].copy()
    monthly_2025 = monthly_2025.sort_values('month')
    
    months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    x = np.arange(len(months_short))
    
    # Occupancy comparison
    axes[0].plot(x, monthly_2025['occupancy'], marker='o', linewidth=3, 
                label='Your Property', color='#E97451', markersize=8)
    axes[0].plot(x, monthly_2025['compset_occupancy'], marker='s', linewidth=2, 
                label='Competitive Set', color='#2A9D8F', linestyle='--', markersize=6)
    axes[0].plot(x, monthly_2025['market_occupancy'], marker='^', linewidth=2, 
                label='Market', color='#F4A261', linestyle=':', markersize=6)
    
    axes[0].set_title(f"{market.title()} - Occupancy Gap Analysis (2025)", color='white', fontsize=14)
    axes[0].set_ylabel("Occupancy %", color='white')
    axes[0].set_xlabel("Month", color='white')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(months_short, rotation=45)
    axes[0].legend(frameon=False, labelcolor='white')
    axes[0].grid(color='#27272a', linestyle='--', alpha=0.3)
    axes[0].set_facecolor('#0a0a0b')
    
    # ADR comparison
    axes[1].plot(x, monthly_2025['adr']/1000000, marker='o', linewidth=3, 
                label='Your Property', color='#E97451', markersize=8)
    axes[1].plot(x, monthly_2025['compset_adr']/1000000, marker='s', linewidth=2, 
                label='Competitive Set', color='#2A9D8F', linestyle='--', markersize=6)
    axes[1].plot(x, monthly_2025['market_adr']/1000000, marker='^', linewidth=2, 
                label='Market', color='#F4A261', linestyle=':', markersize=6)
    
    axes[1].set_title(f"{market.title()} - ADR Gap Analysis (2025)", color='white', fontsize=14)
    axes[1].set_ylabel("ADR (M IDR)", color='white')
    axes[1].set_xlabel("Month", color='white')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(months_short, rotation=45)
    axes[1].legend(frameon=False, labelcolor='white')
    axes[1].grid(color='#27272a', linestyle='--', alpha=0.3)
    axes[1].set_facecolor('#0a0a0b')
    
    plt.tight_layout()
    plt.savefig(f"visualizations/{market}_market_gaps.png", dpi=150, facecolor='#0a0a0b')
    plt.close()
    print(f"✓ Created {market}_market_gaps.png")

def generate_insights(monthly, market):
    """Generate key insights for the analysis"""
    monthly_2025 = monthly[monthly['year'] == 2025]
    monthly_2024 = monthly[monthly['year'] == 2024]
    
    insights = {
        'avg_occupancy_2025': monthly_2025['occupancy'].mean(),
        'avg_adr_2025': monthly_2025['adr'].mean(),
        'avg_revpar_2025': monthly_2025['revpar'].mean(),
        'avg_rgi_2025': monthly_2025['rgi'].mean(),
        'avg_mpi_2025': monthly_2025['mpi'].mean(),
        'avg_ari_2025': monthly_2025['ari'].mean(),
        'yoy_occ_change': monthly_2025['occupancy'].mean() - monthly_2024['occupancy'].mean(),
        'yoy_adr_change_pct': ((monthly_2025['adr'].mean() / monthly_2024['adr'].mean()) - 1) * 100,
        'yoy_revpar_change_pct': ((monthly_2025['revpar'].mean() / monthly_2024['revpar'].mean()) - 1) * 100,
        'dominant_segment': 'Transient' if monthly_2025['seg_transient_pct'].mean() > 50 else 
                           'Group' if monthly_2025['seg_group_pct'].mean() > 50 else 'Mixed'
    }
    
    return insights

# Main execution
if __name__ == "__main__":
    print("\n" + "="*70)
    print("STR COMPETITIVE ANALYSIS - GENERATING VISUALIZATIONS")
    print("="*70)
    
    for market in ['jakarta', 'bali']:
        print(f"\n[{market.upper()}] Loading data...")
        daily, monthly, quarterly = load_data(market)
        
        print(f"[{market.upper()}] Generating visualizations...")
        plot_absolute_performance(monthly, market)
        plot_str_indices(monthly, market)
        plot_yoy_comparison(monthly, market)
        plot_day_of_week(daily, market)
        plot_segment_mix(monthly, market)
        plot_market_gaps(monthly, market)
        
        print(f"[{market.upper()}] Calculating insights...")
        insights = generate_insights(monthly, market)
        
        print(f"\n{market.upper()} KEY INSIGHTS:")
        print(f"  2025 Avg Occupancy: {insights['avg_occupancy_2025']:.1f}%")
        print(f"  2025 Avg ADR: {insights['avg_adr_2025']/1000000:.2f}M IDR")
        print(f"  2025 Avg RevPAR: {insights['avg_revpar_2025']/1000000:.2f}M IDR")
        print(f"  Avg RGI: {insights['avg_rgi_2025']:.1f} ({'Outperforming' if insights['avg_rgi_2025'] > 100 else 'Underperforming'})")
        print(f"  YoY Occupancy Change: {insights['yoy_occ_change']:+.1f}pp")
        print(f"  YoY ADR Change: {insights['yoy_adr_change_pct']:+.1f}%")
        print(f"  YoY RevPAR Change: {insights['yoy_revpar_change_pct']:+.1f}%")
        print(f"  Dominant Segment: {insights['dominant_segment']}")
    
    print("\n" + "="*70)
    print("✓ ANALYSIS COMPLETE - All visualizations saved to visualizations/")
    print("="*70)
