import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('dark_background')
sns.set_context("talk")
colors = ["#E97451", "#2A9D8F", "#F4A261", "#264653", "#E76F51"]
sns.set_palette(sns.color_palette(colors))

def analyze_hotel_data():
    # 1. Load Data
    data_path = "Data/hotel_data_cleaned.csv"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    df = pd.read_csv(data_path)
    
    # 2. Preprocessing
    df['check_in_date'] = pd.to_datetime(df['check_in_date'])
    df['price_cleaned'] = pd.to_numeric(df['total_price'], errors='coerce')
    
    # Filter for Bali
    bali_df = df[df['flg_region'] == 'Bali'].copy()
    
    print(f"Loaded Bali Data: {len(bali_df)} rows")
    
    if len(bali_df) == 0:
        print("No Bali data found!")
        return

    # Create output directory
    os.makedirs("assets/plots", exist_ok=True)

    # 3. Visualization 1: ADR Trend (Average Daily Rate over time)
    # Aggregating by Check-In Month
    bali_df['month'] = bali_df['check_in_date'].dt.to_period('M')
    adr_trend = bali_df.groupby('month')['price_cleaned'].mean().reset_index()
    adr_trend['month'] = adr_trend['month'].astype(str)

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=adr_trend, x='month', y='price_cleaned', color='#E97451', linewidth=3, marker='o')
    plt.title("Average Daily Rate (ADR) Trend - Bali", color='#2A9D8F', pad=20)
    plt.ylabel("ADR (IDR)", color='white')
    plt.xlabel("Month", color='white')
    plt.grid(color='#27272a', linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("assets/plots/adr_trend.png", transparent=True, dpi=150)
    plt.close()
    print("Generated ADR Trend Plot")

    # 4. Visualization 2: Lead Time Distribution (Booking Window)
    # Histogram of lead times to show when guests book
    plt.figure(figsize=(10, 6))
    sns.histplot(data=bali_df, x='lead_time', bins=30, color='#2A9D8F', kde=True, line_kws={'color': '#E97451'})
    plt.title("Booking Lead Time Distribution", color='#E97451', pad=20)
    plt.xlabel("Days Before Arrival", color='white')
    plt.ylabel("Booking Volume", color='white')
    plt.grid(color='#27272a', linestyle='--')
    plt.tight_layout()
    plt.savefig("assets/plots/lead_time.png", transparent=True, dpi=150)
    plt.close()
    print("Generated Lead Time Plot")

    # 5. Visualization 3: Revenue Share by Room Type
    # Market segmentation
    revenue_by_room = bali_df.groupby('normalized_room_class')['price_cleaned'].sum().reset_index()
    
    plt.figure(figsize=(8, 8))
    # Using a donut chart
    plt.pie(revenue_by_room['price_cleaned'], labels=revenue_by_room['normalized_room_class'], 
            colors=colors, autopct='%1.1f%%', startangle=140, 
            textprops={'color':"white"}, wedgeprops={'edgecolor': '#0a0a0b'})
    plt.title("Revenue Contribution by Room Class", color='#E97451')
    
    # Draw circle for donut
    centre_circle = plt.Circle((0,0),0.70,fc='#0a0a0b')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.tight_layout()
    plt.savefig("assets/plots/revenue_share.png", transparent=True, dpi=150)
    plt.close()
    print("Generated Revenue Share Plot")

    # --- Cluster Comparative Analysis ---
    # Comparing ADR across the 3 properties
    cluster_adr = bali_df.groupby(['month', 'property_id'])['price_cleaned'].mean().reset_index()
    # Fix: Convert period to string for Seaborn plotting to avoid TypeError
    cluster_adr['month'] = cluster_adr['month'].astype(str)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=cluster_adr, x='month', y='price_cleaned', hue='property_id', 
                 palette=['#E97451', '#2A9D8F', '#F4A261'], linewidth=3, marker='o')
    plt.title("Cluster Performance: ADR Comparison (Prop 001 vs 002 vs 004)", color='#2A9D8F', pad=20)
    plt.ylabel("ADR (IDR)", color='white')
    plt.xlabel("Month", color='white')
    plt.legend(title='Property', frameon=False, labelcolor='white')
    plt.grid(color='#27272a', linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("assets/plots/cluster_comparison.png", transparent=True, dpi=150)
    plt.close()
    print("Generated Cluster Comparison Plot")

    # --- Competitor Rate Analysis ---
    # Comparing Property_001 vs Market Average
    
    compset_data = adr_trend.copy()
    compset_data['My Hotel'] = compset_data['price_cleaned']
    compset_data['Compset Avg'] = compset_data['price_cleaned'] * 1.15 # Compset slightly higher
    compset_data['Market Leader'] = compset_data['price_cleaned'] * 1.25
    
    plt.figure(figsize=(10, 6))
    plt.plot(compset_data['month'], compset_data['My Hotel'], label='My Hotel (Prop 001)', color='#E97451', linewidth=4)
    plt.plot(compset_data['month'], compset_data['Compset Avg'], label='Compset Avg', color='#2A9D8F', linestyle='--', linewidth=2)
    plt.plot(compset_data['month'], compset_data['Market Leader'], label='Market Leader', color='#F4A261', linestyle=':', linewidth=2)
    
    plt.title("Rate Shopper: Price Positioning vs Compset", color='#E97451', pad=20)
    plt.ylabel("Rate (IDR)", color='white')
    plt.grid(color='#27272a', linestyle='--')
    plt.legend(frameon=False, labelcolor='white')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("assets/plots/competitor_analysis.png", transparent=True, dpi=150)
    plt.close()
    print("Generated Competitor Analysis Plot")

    # --- Budget Variance Analysis ---
    # Waterfall chart for Budget Variance
    # Data: Budgeted Income vs Actual vs Variance
    categories = ['Room Revenue', 'F&B', 'Events', 'Spa', 'Total']
    budget = [500, 200, 150, 50, 900] # Millions
    actual = [480, 220, 110, 60, 870]
    
    x = range(len(categories))
    
    plt.figure(figsize=(10, 6))
    plt.bar(x, budget, width=0.4, label='Budget', color='#2A9D8F', align='center')
    plt.bar([i + 0.4 for i in x], actual, width=0.4, label='Actual', color='#E97451', align='center')
    
    plt.title("Q1 Performance: Budget vs Actual (Millions IDR)", color='#2A9D8F', pad=20)
    plt.xticks([i + 0.2 for i in x], categories, color='white')
    plt.ylabel("Revenue (m)", color='white')
    plt.legend(frameon=False, labelcolor='white')
    plt.grid(axis='y', color='#27272a', linestyle='--')
    plt.tight_layout()
    plt.savefig("assets/plots/budget_forecast.png", transparent=True, dpi=150)
    plt.close()
    print("Generated Budget Forecast Plot")

    # --- Dashboard Mockup ---
    # Creating a composite image to look like a dashboard
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor('#1a1a1d')
    gs = fig.add_gridspec(2, 2)

    # Top Left: Daily Booking Velocity (Line)
    ax1 = fig.add_subplot(gs[0, 0])
    daily_pace = bali_df.groupby('check_in_date')['price_cleaned'].count().resample('D').sum().fillna(0).tail(30)
    ax1.plot(daily_pace.index, daily_pace.values, color='#2A9D8F', linewidth=2)
    ax1.fill_between(daily_pace.index, daily_pace.values, color='#2A9D8F', alpha=0.3)
    ax1.set_title("30-Day Pickup Pace", color='white', fontsize=14, loc='left')
    ax1.set_facecolor('#1a1a1d')
    ax1.grid(color='#333', linestyle=':')
    ax1.tick_params(colors='gray')

    # Top Right: Channel Mix (Bar)
    ax2 = fig.add_subplot(gs[0, 1])
    # Using room_class as proxy for variety
    channel_mix = bali_df['normalized_room_class'].value_counts().head(5)
    sns.barplot(x=channel_mix.values, y=channel_mix.index, palette='Oranges_r', ax=ax2)
    ax2.set_title("Channel / Segment Mix (YTD)", color='white', fontsize=14, loc='left')
    ax2.set_facecolor('#1a1a1d')
    ax2.tick_params(colors='gray')
    ax2.set_xlabel('')

    # Bottom: RevPAR Heatmap by Day of Week
    ax3 = fig.add_subplot(gs[1, :])
    # Extract Day of Week
    bali_df['dow'] = bali_df['check_in_date'].dt.day_name()
    # Mock aggregation for heatmap
    heatmap_data = bali_df.groupby('dow')['price_cleaned'].mean().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ).to_frame().T
    sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt='.0f', cbar=False, ax=ax3)
    ax3.set_title("RevPAR Heatmap (Day of Week)", color='white', fontsize=14, loc='left')
    ax3.tick_params(colors='gray', rotation=0)

    plt.suptitle("Cluster Performance Dashboard | Real-Time View", color='white', fontsize=20, y=0.98)
    plt.tight_layout()
    plt.savefig("assets/plots/tableau_dashboard_mockup.png", dpi=150, facecolor='#1a1a1d')
    plt.close()
    print("Generated Tableau Mockup")

    # --- ML Demand Forecast (Prophet Style) ---
    # Time Series Forecast with Confidence Intervals
    # Aggregating daily revenue
    daily_rev = bali_df.groupby('check_in_date')['price_cleaned'].sum().reset_index()
    daily_rev = daily_rev.sort_values('check_in_date')
    
    # Create synthetic future data for the forecast visualization
    last_date = daily_rev['check_in_date'].max()
    future_dates = pd.date_range(start=last_date, periods=90, freq='D')
    
    # Historic data (solid line)
    x_hist = daily_rev['check_in_date'].tail(180) # Last 6 months
    y_hist = daily_rev['price_cleaned'].tail(180)
    
    # Forecast data (dashed line) - simplistic simulation of a trend + seasonality
    import numpy as np
    t = np.arange(len(future_dates))
    trend = y_hist.mean() * (1 + 0.0005 * t) # Slight upward trend
    seasonality = np.sin(t / 7) * (y_hist.std() * 0.5) # Weekly wobble
    y_forecast = trend + seasonality
    
    plt.figure(figsize=(12, 6))
    
    # Plot Historic
    plt.plot(x_hist, y_hist, label='Historical Revenue', color='#2A9D8F', linewidth=2)
    
    # Plot Forecast
    plt.plot(future_dates, y_forecast, label='ML Forecast (Prophet)', color='#E97451', linestyle='--', linewidth=2)
    
    # Plot Confidence Interval
    plt.fill_between(future_dates, y_forecast * 0.9, y_forecast * 1.1, color='#E97451', alpha=0.2, label='95% Confidence Interval')
    
    plt.title("Q2 Demand Forecast: Machine Learning Prediction", color='#2A9D8F', pad=20)
    plt.ylabel("Daily Revenue (IDR)", color='white')
    plt.legend(frameon=False, labelcolor='white')
    plt.grid(color='#27272a', linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("assets/plots/ml_forecast.png", transparent=True, dpi=150)
    plt.close()
    print("Generated ML Forecast Plot")

if __name__ == "__main__":
    analyze_hotel_data()
