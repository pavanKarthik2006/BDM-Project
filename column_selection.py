import pandas as pd

# --- Configuration ---
# Assuming the trimmed sales data for February 2024 has already been generated
# by the 'Generate Trimmed Sales Data for February 2024' immersive.
TRIMMED_SALES_FILE_PATH = r'C:\Users\Pavan\Downloads\archive (1)\trimmed_sales_feb_2024.csv'
PRODUCTS_FILE_PATH = r'C:\Users\Pavan\Downloads\archive (1)\products.csv'
CATEGORIES_FILE_PATH = r'C:\Users\Pavan\Downloads\archive (1)\categories.csv'

print("--- Step 1: Loading Trimmed Sales Data and Auxiliary Files ---")
try:
    trimmed_sales_df = pd.read_csv(TRIMMED_SALES_FILE_PATH)
    products_df = pd.read_csv(PRODUCTS_FILE_PATH)
    categories_df = pd.read_csv(CATEGORIES_FILE_PATH)
    print(f"Successfully loaded '{TRIMMED_SALES_FILE_PATH}', '{PRODUCTS_FILE_PATH}', and '{CATEGORIES_FILE_PATH}'.")
    print(f"Trimmed sales data size: {len(trimmed_sales_df)} rows.")
except FileNotFoundError as e:
    print(f"Error loading file: {e}. Please ensure all necessary CSV files are in the correct location.")
    exit()

# Ensure 'SalesDate' is datetime type for consistency, as it might become object after saving/loading CSV
trimmed_sales_df['SalesDate'] = pd.to_datetime(trimmed_sales_df['SalesDate'])
print(" 'SalesDate' column in trimmed_sales_df ensured as datetime format.")


print("\n--- Step 2: Merging with Product and Category Data & Recalculating TotalPrice ---")

# Keep only necessary columns from products_df before merging
products_relevant_cols = ['ProductID', 'ProductName', 'Price', 'CategoryID']
merged_df = pd.merge(trimmed_sales_df, products_df[products_relevant_cols], on='ProductID', how='left')

# Merge with categories_df on CategoryID to get CategoryName
categories_relevant_cols = ['CategoryID', 'CategoryName']
merged_df = pd.merge(merged_df, categories_df[categories_relevant_cols], on='CategoryID', how='left')

print("Products and Categories data merged with trimmed sales data.")

# Recalculate TotalPrice (important after merging with 'Price' from products_df)
# This uses the 'Price' from products.csv which is assumed to be the base price
merged_df['TotalPrice'] = merged_df['Quantity'] * merged_df['Price'] * (1 - merged_df['Discount'])
print("TotalPrice recalculated using merged product prices.")

# --- Feature Engineering (Time-based) ---
# Re-extract time-based features as they might be needed for consistency or re-calculation
merged_df['SaleYear'] = merged_df['SalesDate'].dt.year
merged_df['SaleMonth'] = merged_df['SalesDate'].dt.month_name()
merged_df['SaleWeekday'] = merged_df['SalesDate'].dt.day_name()
merged_df['SaleWeek'] = merged_df['SalesDate'].dt.isocalendar().week.astype(int)
print("Time-based features extracted.")


print("\n--- Step 3: Filtering Products and Categories for Indian Grocery Store Relevance ---")

# Define a list of product names to exclude that are not typically found in Indian grocery stores.
products_to_exclude = [
    'Barramundi', 'Creme De Banane - Marie', 'Shrimp - 31/40',
    'Orange - Canned, Mandarin', 'Cheese - Boursin, Garlic / Herbs',
    'Veal - Osso Bucco', 'Tomato - Tricolor Cherry', 'Grenadine',
    'Salmon - Atlantic, Skin On', 'Coffee - Irish Cream',
    'Crab - Dungeness, Whole', 'Sole - Dover, Whole, Fresh',
    'Sauce - Demi Glace', 'Seedlings - Mix, Organic',
    'Vanilla Beans', 'Bread Crumbs - Japanese Style'
]

# Define a list of categories to explicitly include as per your request
categories_to_include = [
    'Confections',
    'Produce',
    'Beverages',
    'Grain'
]

# Apply filters sequentially
# Filter out products not typically found in Indian grocery stores
filtered_by_product_exclusion = merged_df[~merged_df['ProductName'].isin(products_to_exclude)].copy()
print(f"Filtered by product exclusion. Rows remaining: {len(filtered_by_product_exclusion)}")

# Further filter by the specified categories
final_preprocessed_df = filtered_by_product_exclusion[
    filtered_by_product_exclusion['CategoryName'].isin(categories_to_include)
].copy()
print(f"Further filtered by category inclusion ({categories_to_include}). Final rows: {len(final_preprocessed_df)}")


print("\n--- Step 4: Remove Unnecessary Columns from the final filtered DataFrame ---")
# Only keep columns that are useful for the analysis (Sales Trend, Forecasting, Inventory Turnover, ABC Analysis)
columns_to_keep = [
    'ProductID', 'ProductName', 'CategoryID', 'CategoryName', 'Quantity', 'Discount', 'TotalPrice', 'SalesDate',
    'SaleYear', 'SaleMonth', 'SaleWeekday', 'SaleWeek', 'Price' # 'Price' is retained for COGS calculation in Inventory Turnover
]

final_preprocessed_df = final_preprocessed_df[columns_to_keep].copy()

print("\n--- Data Preprocessing Complete ---")
print("Final preprocessed DataFrame (final_preprocessed_df) ready for analysis.")
print("\nFirst 5 rows of final_preprocessed_df:")
print(final_preprocessed_df.head())
print("\nInformation about final_preprocessed_df:")
print(final_preprocessed_df.info())
