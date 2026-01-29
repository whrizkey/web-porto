import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# Set Portfolio Style
plt.style.use('dark_background')
sns.set_context("talk")
colors = ["#E97451", "#2A9D8F", "#F4A261", "#264653", "#E76F51"]
sns.set_palette(sns.color_palette(colors))

def extract_sqm(text):
    if pd.isna(text): return None
    # Look for patterns like "35sqm" or "35 sqm"
    match = re.search(r'(\d+)\s*sqm', text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

def analyze_hedonic_pricing():
    print("--- Starting Hedonic Pricing Analysis ---")
    
    # 1. Load Data
    try:
        df = pd.read_csv("Data/hotel_data_cleaned.csv")
    except FileNotFoundError:
        print("Error: Data file not found.")
        return

    # Basic Cleaning
    df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')
    df = df.dropna(subset=['total_price'])
    
    # Filter for realistic price range (exclude potential outliers/errors)
    df = df[df['total_price'] > 100000] 

    # 2. Feature Engineering (NLP on 'room_description' and 'inclusions_text')
    print("Extracting features from text...")
    
    # Combine text fields for easier searching
    df['full_text'] = (df['room_description'].fillna('') + " " + df['inclusions_text'].fillna('')).str.lower()
    
    # Binary Features (Attributes)
    df['has_breakfast'] = df['full_text'].apply(lambda x: 1 if any(w in x for w in ['breakfast', 'meal']) else 0)
    df['has_view'] = df['full_text'].apply(lambda x: 1 if any(w in x for w in ['view', 'ocean', 'sea', 'garden', 'pool']) else 0)
    df['is_suite'] = df['full_text'].apply(lambda x: 1 if 'suite' in x or 'villa' in x else 0)
    df['has_balcony'] = df['full_text'].apply(lambda x: 1 if any(w in x for w in ['balcony', 'terrace']) else 0)
    df['has_living_area'] = df['full_text'].apply(lambda x: 1 if 'living' in x else 0)
    df['has_club_access'] = df['full_text'].apply(lambda x: 1 if 'club' in x or 'executive' in x else 0)

    # Numeric Features
    df['sqm'] = df['room_description'].apply(extract_sqm)
    # Fill missing sqm with median of the room type or global median
    df['sqm'] = df['sqm'].fillna(df.groupby('room_class_name')['sqm'].transform('median'))
    df['sqm'] = df['sqm'].fillna(df['sqm'].median())
    
    # 3. Prepare Model Data
    features = ['sqm', 'has_breakfast', 'has_view', 'is_suite', 'has_balcony', 'has_living_area', 'has_club_access']
    target = 'total_price'
    
    X = df[features]
    y = df[target]
    
    # 4. Train Model (Linear Regression for Interpretability)
    model = LinearRegression()
    model.fit(X, y)
    
    # 5. Extract Coefficients (The "Price Tag")
    coef_df = pd.DataFrame({
        'Feature': features,
        'Value_IDR': model.coef_
    })
    coef_df = coef_df.sort_values(by='Value_IDR', ascending=False)
    
    print("\n--- Hedonic Pricing Results ---")
    print(f"Base Price (Intercept): IDR {model.intercept_:,.0f}")
    print(coef_df)
    
    # 6. Visualization
    plt.figure(figsize=(10, 6))
    
    # Color mapping: Green for positive value, Red for negative (if any)
    bar_colors = ['#2A9D8F' if x > 0 else '#E97451' for x in coef_df['Value_IDR']]
    
    sns.barplot(data=coef_df, x='Value_IDR', y='Feature', palette=bar_colors)
    
    plt.title("Hedonic Pricing: The Monetary Value of Features", color='white', pad=20)
    plt.xlabel("Price Premium (IDR)", color='white')
    plt.ylabel("Feature", color='white')
    plt.axvline(x=0, color='white', linestyle='--', linewidth=1)
    plt.grid(axis='x', color='#27272a', linestyle='--')
    
    # Format x-axis labels as Millions (Example: 0.5M)
    ax = plt.gca()
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:,.1f}M'.format(x/1000000) for x in vals])
    
    plt.tight_layout()
    plt.savefig("assets/plots/hedonic_valuation.png", transparent=True, dpi=150)
    print("\nPlot saved to assets/plots/hedonic_valuation.png")

if __name__ == "__main__":
    analyze_hedonic_pricing()
