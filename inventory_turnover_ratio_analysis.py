import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
import calendar
# Removed: import content_fetcher # As per user, this is not defined in the environment.

# --- Configuration for Data Loading and Preprocessing ---
# IMPORTANT: Assuming these files are directly accessible in the environment's root.
SALES_FILE_PATH = r'C:\Users\Pavan\Downloads\archive (1)\trimmed_sales_feb_2024.csv'
PRODUCTS_FILE_PATH = r'C:\Users\Pavan\Downloads\archive (1)\products.csv'
CATEGORIES_FILE_PATH = r'C:\Users\Pavan\Downloads\archive (1)\categories.csv'

TARGET_YEAR = 2024
TARGET_MONTH = 2 # February

sales_df = pd.DataFrame()
products_df = pd.DataFrame()
categories_df = pd.DataFrame()
data_loaded_successfully = False # Keep this for internal logic, but won't use file_content_fetcher

try:
    sales_df = pd.read_csv(SALES_FILE_PATH)
    products_df = pd.read_csv(PRODUCTS_FILE_PATH)
    categories_df = pd.read_csv(CATEGORIES_FILE_PATH)
    data_loaded_successfully = True
    print("Real data loaded successfully from provided files.")
except FileNotFoundError as e:
    print(f"Error: One or more data files not found. Please ensure '{SALES_FILE_PATH}', '{PRODUCTS_FILE_PATH}', and '{CATEGORIES_FILE_PATH}' are uploaded correctly.")
    print(f"Error details: {e}")
    # Do not exit, but mark as not loaded successfully to prevent further operations on empty DFs.
    data_loaded_successfully = False
except Exception as e:
    print(f"An unexpected error occurred during file loading: {e}.")
    data_loaded_successfully = False


# --- Exit if real data could not be loaded ---
if not data_loaded_successfully:
    print("Cannot proceed with analysis as data loading failed.")
    exit() # Exit the script if data loading was unsuccessful


# --- Date Processing and Trimming ---
if 'SalesDate' in sales_df.columns:
    sales_df.dropna(subset=['SalesDate'], inplace=True)
    # Convert 'SalesDate' to datetime, handling potential errors
    sales_df['SalesDate'] = pd.to_datetime(sales_df['SalesDate'], errors='coerce')
    sales_df.dropna(subset=['SalesDate'], inplace=True) # Remove rows where conversion failed

    # Apply TARGET_YEAR to all SalesDate entries to ensure they fall into the desired analysis year
    # Assuming original sales data might be from a different year (e.g., 2018 as in Kaggle dataset)
    # This aligns all sales to TARGET_YEAR for February.
    sales_df['SalesDate'] = sales_df['SalesDate'].apply(
        lambda x: x.replace(year=TARGET_YEAR) if pd.notna(x) else x
    )
    print(f"SalesDate processed and year shifted to {TARGET_YEAR}.")
else:
    print("Error: 'SalesDate' column not found in the sales data. Cannot proceed with date-based analysis.")
    exit()

num_days_in_month = calendar.monthrange(TARGET_YEAR, TARGET_MONTH)[1]
start_date_of_period = pd.Timestamp(TARGET_YEAR, TARGET_MONTH, 1)
end_date_of_period = pd.Timestamp(TARGET_YEAR, TARGET_MONTH, num_days_in_month) + timedelta(days=1)

trimmed_sales_df = sales_df[
    (sales_df['SalesDate'] >= start_date_of_period) &
    (sales_df['SalesDate'] < end_date_of_period)
].copy()
print(f"Data trimmed to {len(trimmed_sales_df)} rows for {calendar.month_name[TARGET_MONTH]} {TARGET_YEAR}.")

if trimmed_sales_df.empty:
    print("Warning: Trimmed sales DataFrame is empty for the target month. Check your data and target period.")
    print("This might happen if the original 'SalesDate' values are not conducive to being shifted to Feb 2024,")
    print("or if 'trimmed data.csv' itself is empty or doesn't cover Feb 2024.")
    exit() # Exit if no data for the target month after trimming


# --- Merging with Product and Category Data ---
products_relevant_cols = ['ProductID', 'ProductName', 'Price', 'CategoryID']
merged_df = pd.merge(trimmed_sales_df, products_df[products_relevant_cols], on='ProductID', how='left')

categories_relevant_cols = ['CategoryID', 'CategoryName']
merged_df = pd.merge(merged_df, categories_df[categories_relevant_cols], on='CategoryID', how='left')

# Check if 'Price' column exists after merge before calculating TotalPrice
if 'Price' not in merged_df.columns:
    print("Error: 'Price' column is missing after merging products data. Cannot calculate TotalPrice.")
    exit()

merged_df['TotalPrice'] = merged_df['Quantity'] * merged_df['Price'] * (1 - merged_df['Discount'])
print("TotalPrice calculated.")


# --- Feature Engineering (Time-based) ---
merged_df['SaleYear'] = merged_df['SalesDate'].dt.year
merged_df['SaleMonth'] = merged_df['SalesDate'].dt.month_name()
merged_df['SaleWeekday'] = merged_df['SalesDate'].dt.day_name()
merged_df['SaleWeek'] = merged_df['SalesDate'].dt.isocalendar().week.astype(int)


# --- Contextual Filtering (Indian Grocery Store Specifics) ---
products_to_exclude = [
    'Barramundi', 'Creme De Banane - Marie', 'Shrimp - 31/40',
    'Orange - Canned, Mandarin', 'Cheese - Boursin, Garlic / Herbs',
    'Veal - Osso Bucco', 'Tomato - Tricolor Cherry', 'Grenadine',
    'Salmon - Atlantic, Skin On', 'Coffee - Irish Cream',
    'Crab - Dungeness, Whole', 'Sole - Dover, Whole, Fresh',
    'Sauce - Demi Glace', 'Seedlings - Mix, Organic',
    'Vanilla Beans', 'Bread Crumbs - Japanese Style'
]
categories_to_include = ['Confections', 'Produce', 'Beverages', 'Grain']

filtered_by_product_exclusion = merged_df[~merged_df['ProductName'].isin(products_to_exclude)].copy()
final_preprocessed_df = filtered_by_product_exclusion[
    filtered_by_product_exclusion['CategoryName'].isin(categories_to_include)
].copy()

columns_to_keep_final = [
    'ProductID', 'ProductName', 'CategoryID', 'CategoryName', 'Quantity', 'Discount', 'TotalPrice', 'SalesDate',
    'SaleYear', 'SaleMonth', 'SaleWeekday', 'SaleWeek', 'Price' # Ensuring 'Price' is here for COGS
]
final_preprocessed_df = final_preprocessed_df[columns_to_keep_final].copy()

if final_preprocessed_df.empty:
    print("Final preprocessed DataFrame is empty after filtering. Cannot perform Inventory Turnover Analysis.")
    exit() # Exit if no data for analysis


print("\n--- Inventory Turnover Ratio Analysis ---")

# --- Define the assumed Gross Profit Margin for COGS calculation ---
# This needs to be consistent with the Financial Overview calculation.
assumed_cogs_percentage_of_revenue = 0.70 # This implies a 30% gross profit margin.

# Calculate Cost of Goods Sold (COGS) based on the assumed percentage of TotalPrice
final_preprocessed_df['CostOfGoodsSold'] = final_preprocessed_df['TotalPrice'] * assumed_cogs_percentage_of_revenue

# Calculate total COGS for the trimmed month (February 2024)
total_cogs = final_preprocessed_df['CostOfGoodsSold'].sum()
print(f"\nTotal Cost of Goods Sold (COGS) for February 2024: ₹{total_cogs:,.2f}")

# --- Output COGS by Category in a Table ---
cogs_by_category = final_preprocessed_df.groupby('CategoryName')['CostOfGoodsSold'].sum().sort_values(ascending=False).reset_index()
print("\nCost of Goods Sold (COGS) by Category (February 2024) - Table:")
print(cogs_by_category.to_string(index=False)) # Use to_string to ensure full table is printed


# --- Visualize COGS by Category as a Bar Chart ---
plt.figure(figsize=(12, 6))
sns.barplot(x='CategoryName', y='CostOfGoodsSold', data=cogs_by_category, palette='viridis')
plt.title('Cost of Goods Sold (COGS) by Product Category (February 2024)')
plt.xlabel('Category Name')
plt.ylabel('Total COGS (₹)') # Updated label to reflect Rupees
plt.xticks(rotation=45, ha='right') # Rotate labels for readability
plt.tight_layout()
plt.show()


# --- Limitation: Average Inventory Calculation ---
print("\nLimitation: Accurate Average Inventory cannot be calculated without actual inventory data.")
print("This analysis is based on the sales data for February 2024. To calculate a true Inventory Turnover Ratio,")
print("you would need beginning and ending inventory levels (in units or value) for the month of February.")
print("If inventory data were available, the formula would be: ")
print("Inventory Turnover = Total COGS / Average Inventory ( (Beginning Inventory + Ending Inventory) / 2 )")
print("\nWithout inventory data, we can only analyze components like COGS, but not the full turnover rate itself.")

print("\nInventory Turnover Ratio Analysis section complete.")
