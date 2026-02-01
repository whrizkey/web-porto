"""
DeFi Protocol Analysis: Step 3 - Analysis & Visualization
Creates publication-quality charts for the portfolio
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CLEANED_DATA = os.path.join(PROJECT_ROOT, '02_cleaned_data', 'defillama_tvl_cleaned.csv')
VIZ_DIR = os.path.join(PROJECT_ROOT, '03_visualizations')

# Set style
plt.style.use('dark_background')

def load_data():
    """Load cleaned data"""
    return pd.read_csv(CLEANED_DATA)

def create_top10_chart(df):
    """Bar chart of top 10 protocols"""
    top10 = df.head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['#2a9d8f' if i == 0 else '#e9c46a' if i < 3 else '#a0a0a0' 
              for i in range(len(top10))]
    
    ax.barh(top10['name'], top10['tvl_billions'], color=colors)
    
    ax.set_xlabel('Total Value Locked (Billions USD)', color='#a0a0a0')
    ax.set_title('Top 10 DeFi Protocols by TVL', color='white', fontsize=14, pad=20)
    
    # Style
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#404040')
    ax.spines['left'].set_color('#404040')
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, 'top10_protocols.png'), dpi=150, facecolor='#0a0a0b')
    print("✅ Created: top10_protocols.png")
    plt.close()

def create_category_chart(df):
    """Pie chart of categories"""
    category_tvl = df.groupby('category')['tvl_billions'].sum().sort_values(ascending=False)
    
    # Top 5 + Others
    top_categories = category_tvl.head(5)
    others = pd.Series({'Other': category_tvl[5:].sum()})
    plot_data = pd.concat([top_categories, others])
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['#2a9d8f', '#e9c46a', '#e76f51', '#f4a261', '#264653', '#a0a0a0']
    
    wedges, texts, autotexts = ax.pie(plot_data, labels=plot_data.index, autopct='%1.1f%%',
                                        colors=colors, textprops={'color': 'white'})
    
    ax.set_title('DeFi TVL Distribution by Category', color='white', fontsize=14, pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, 'category_distribution.png'), dpi=150, facecolor='#0a0a0b')
    print("✅ Created: category_distribution.png")
    plt.close()

def create_chain_comparison(df):
    """Multi-chain vs single-chain protocols"""
    multi_chain_tvl = df[df['is_multi_chain']]['tvl_billions'].sum()
    single_chain_tvl = df[~df['is_multi_chain']]['tvl_billions'].sum()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data = pd.Series({
        f'Multi-Chain\n({df["is_multi_chain"].sum()} protocols)': multi_chain_tvl,
        f'Single-Chain\n({(~df["is_multi_chain"]).sum()} protocols)': single_chain_tvl
    })
    
    colors = ['#2a9d8f', '#e9c46a']
    ax.bar(data.index, data.values, color=colors, width=0.6)
    
    ax.set_ylabel('Total Value Locked (Billions USD)', color='#a0a0a0')
    ax.set_title('Multi-Chain vs Single-Chain Protocols', color='white', fontsize=14, pad=20)
    
    # Style
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#404040')
    ax.spines['left'].set_color('#404040')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ_DIR, 'chain_comparison.png'), dpi=150, facecolor='#0a0a0b')
    print("✅ Created: chain_comparison.png")
    plt.close()

if __name__ == "__main__":
    print("📊 Creating visualizations...")
    df = load_data()
    
    create_top10_chart(df)
    create_category_chart(df)
    create_chain_comparison(df)
    
    print("\n✅ All visualizations complete!")
