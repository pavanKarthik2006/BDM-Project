import pandas as pd
from column_selection import final_preprocessed_df

# Assuming 'final_preprocessed_df' is already available from the data preprocessing steps,
# containing 'TotalPrice', 'Quantity', 'Price', and 'Discount' columns
# for the filtered data of February 2024.

print("--- Financial Overview Calculations for February 2024 ---")

# 1. Calculate Total Revenue (Sales)
total_revenue_feb2024 = final_preprocessed_df['TotalPrice'].sum()
print(f"\nTotal Revenue (Sales) for February 2024: ₹{total_revenue_feb2024:,.2f}")

# 2. Calculate Total Cost of Goods Sold (COGS)
# Recalculate 'CostOfGoodsSold' column if it's not already present or for accuracy,
# using 'Price' as the cost per unit from the merged data.
# This ensures consistency with the analysis methods described.
final_preprocessed_df['CostOfGoodsSold'] = final_preprocessed_df['Quantity'] * final_preprocessed_df['Price'] * (1 - final_preprocessed_df['Discount'])
total_cogs_feb2024 = final_preprocessed_df['CostOfGoodsSold'].sum()
print(f"Total Cost of Goods Sold (COGS) for February 2024: ₹{total_cogs_feb2024:,.2f}")

# 3. Calculate Total Profit
total_profit_feb2024 = total_revenue_feb2024 - total_cogs_feb2024
print(f"Total Profit for February 2024: ₹{total_profit_feb2024:,.2f}")

# 4. Calculate Profit Margin Percentage
# Avoid division by zero if total_revenue_feb2024 is zero
profit_margin_percentage_feb2024 = (total_profit_feb2024 / total_revenue_feb2024) * 100 if total_revenue_feb2024 != 0 else 0
print(f"Profit Margin Percentage for February 2024: {profit_margin_percentage_feb2024:.2f}%")

print("\nFinancial calculations complete.")
