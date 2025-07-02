import pandas as pd
from column_selection import final_preprocessed_df  



print("--- ABC Analysis ---")

# Group by ProductID and calculate total revenue for each product
# Ensure 'ProductName' is included if you want it in the ABC analysis results dataframe.
product_revenue = final_preprocessed_df.groupby(['ProductID', 'ProductName'])['TotalPrice'].sum().sort_values(ascending=False).reset_index()
product_revenue.columns = ['ProductID', 'ProductName', 'TotalRevenue']

# Calculate cumulative percentage of total revenue
product_revenue['CumulativeRevenue'] = product_revenue['TotalRevenue'].cumsum()
product_revenue['CumulativeRevenuePercentage'] = (product_revenue['CumulativeRevenue'] / product_revenue['TotalRevenue'].sum()) * 100

# Assign ABC categories
# A-items: Top 70% of revenue
# B-items: Next 20% of revenue (up to 90%)
# C-items: Remaining 10% of revenue (above 90%)
def assign_abc_category(percentage):
    if percentage <= 70:
        return 'A'
    elif percentage <= 90:
        return 'B'
    else:
        return 'C'

product_revenue['ABC_Category'] = product_revenue['CumulativeRevenuePercentage'].apply(assign_abc_category)

print("\nABC Analysis Results (Top 5 products):")
print(product_revenue.head()) # Display top few ABC categorized products

# Summarize ABC categories
abc_summary = product_revenue.groupby('ABC_Category').agg(
    ProductCount=('ProductID', 'count'),
    TotalRevenue=('TotalRevenue', 'sum'),
    PercentageOfTotalRevenue=('TotalRevenue', lambda x: (x.sum() / product_revenue['TotalRevenue'].sum()) * 100)
).reset_index()
print("\nABC Analysis Summary:")
print(abc_summary)

# Save the ABC analysis results to a CSV file
output_filename = 'abc_analysis_results_feb_2024.csv'
product_revenue.to_csv(output_filename, index=False)
print(f"\nABC analysis results saved to '{output_filename}'.")

print("\nABC Analysis section complete.")
