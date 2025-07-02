import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from column_selection import final_preprocessed_df  # Assuming this is the preprocessed DataFrame from the previous step



print("--- Sales Trend Analysis for February 2024 ---")

# --- Part 1: Weekly Sales Trend Line Graph ---

# Determine the starting ISO week number for February 2024 in the dataset
min_sale_week = final_preprocessed_df['SaleWeek'].min()

# Create a 'RelativeWeek' column for plotting (Week 1, Week 2, etc. within the month)
final_preprocessed_df['RelativeWeek'] = final_preprocessed_df['SaleWeek'] - min_sale_week + 1

# Aggregate total sales by the new 'RelativeWeek'
weekly_sales = final_preprocessed_df.groupby('RelativeWeek')['TotalPrice'].sum().reset_index()

# Ensure the weeks are sorted for proper plotting order
weekly_sales = weekly_sales.sort_values(by='RelativeWeek')

plt.figure(figsize=(10, 6)) # Adjusted figure size for weekly data
sns.lineplot(
    data=weekly_sales,
    x='RelativeWeek',
    y='TotalPrice',
    marker='o', # Add markers for each data point
    color='skyblue', # Single color for a single line
    linewidth=2
)

plt.title('Weekly Sales Trend for February 2024')
plt.xlabel('Week Number (within month)')
plt.ylabel('Total Sales')
plt.xticks(weekly_sales['RelativeWeek'].unique()) # Ensure only actual week numbers are shown
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

print("\n--- Part 2: Fast-Moving and Slow-Moving Items ---")

# Group by ProductName and sum TotalPrice to get total sales for each product
sales_by_product = final_preprocessed_df.groupby('ProductName')['TotalPrice'].sum().sort_values(ascending=False)

print("\nTop 10 Fast-Moving Products (February 2024):")
print(sales_by_product.head(10))

print("\nTop 10 Slow-Moving Products (February 2024):")
print(sales_by_product.tail(10))

print("\nCombined sales trend analysis complete.")
