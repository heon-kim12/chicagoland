import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

final_stats = pd.read_csv("final_stats.csv")
# -----------------------------------------------------
# Dashboard Title and Description
st.title("Home Purchase Recommendation Dashboard")
st.write("""
This dashboard provides a recommendation based on forecasted housing prices for the 20–30 miles tier with an income between **$60K–$100K** and a home-buying budget of **$220,000**, 
the dashboard below suggests locations where the forecasted 2025 average home price falls within your budget.
""")

# -----------------------------------------------------
# Sidebar Inputs for User Details
st.sidebar.header("Your Details")
income_range = st.sidebar.slider(
    "Select your income range ($)", 
    min_value=60000, 
    max_value=100000, 
    value=(60000, 100000), 
    step=5000
)
budget = st.sidebar.number_input(
    "Enter your home-buying budget ($)", 
    value=220000, 
    step=10000
)

# -----------------------------------------------------
# Recommend Locations Based on Forecasted 2025 Prices
recommended = final_stats[final_stats['mean_2025'] <= budget].sort_values(by='mean_2025')
st.subheader("Recommended Locations (Forecasted 2025 Prices)")
if not recommended.empty:
    st.write(f"Based on your budget of ${budget:,.0f}, the following locations have forecasted average home prices below your budget:")
    st.dataframe(recommended[['city', 'mean_2025']])
else:
    st.write("No locations were found with forecasted average prices below your budget.")

# -----------------------------------------------------
# Detailed Historical vs. Forecast Comparison for a Selected City
selected_city = st.selectbox(
    "Select a city to see a detailed historical vs. forecast comparison", 
    final_stats["city"].unique()
)
city_data = final_stats[final_stats["city"] == selected_city].iloc[0]

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(["2024 (Historical)", "2025 (Forecast)"],
       [city_data["mean_2024"], city_data["mean_2025"]],
       color=["blue", "orange"])
ax.set_ylabel("Housing Price ($)")
ax.set_title(f"Average Housing Price Comparison for {selected_city}")
# Format y-axis in dollar notation
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
st.pyplot(fig)
