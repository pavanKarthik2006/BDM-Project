import pandas as pd
from datetime import timedelta
import calendar

# --- Configuration ---
# IMPORTANT: Use the correct path to your large sales dataset file
SALES_FILE_PATH = r'C:\Users\Pavan\Downloads\archive (1)\sales.csv' 

# --- Target Month and Year ---
TARGET_YEAR = 2024
TARGET_MONTH = 2 # February

# --- Data Loading ---
try:
    sales_df = pd.read_csv(SALES_FILE_PATH)
    print(f"Successfully loaded '{SALES_FILE_PATH}'. Initial dataset size: {len(sales_df)} rows.")
except FileNotFoundError:
    print(f"Error: The file '{SALES_FILE_PATH}' was not found. Please check the path and filename.")
    exit()

# --- Data Cleaning: Convert 'SalesDate' to datetime ---
if 'SalesDate' in sales_df.columns:
    initial_rows = len(sales_df)
    sales_df.dropna(subset=['SalesDate'], inplace=True)
    if len(sales_df) < initial_rows:
        print(f"Removed {initial_rows - len(sales_df)} rows with missing 'SalesDate'.")

    sales_df['SalesDate'] = pd.to_datetime(sales_df['SalesDate'])
    print(" 'SalesDate' column converted to datetime format.")

    # --- Shift SalesDate year from 2018 to 2024 ---
    # This assumes the original data primarily contains years around 2018.
    # It will add 6 years to all dates to effectively shift them from 2018 to 2024.
    sales_df['SalesDate'] = sales_df['SalesDate'] + pd.DateOffset(years=TARGET_YEAR - 2018)
    print(f"Sales dates shifted from 2018 to {TARGET_YEAR} for analysis purposes.")

else:
    print("Error: 'SalesDate' column not found in the sales data. Please check your dataset.")
    exit()

# --- Define the 1-month period based on the TARGET_YEAR and TARGET_MONTH ---
num_days_in_month = calendar.monthrange(TARGET_YEAR, TARGET_MONTH)[1]
start_date_of_period = pd.Timestamp(TARGET_YEAR, TARGET_MONTH, 1)
end_date_of_period = pd.Timestamp(TARGET_YEAR, TARGET_MONTH, num_days_in_month) + timedelta(days=1)

print(f"\nTargeting data from: {start_date_of_period.strftime('%Y-%m-%d')}")
print(f"To: {(end_date_of_period - timedelta(days=1)).strftime('%Y-%m-%d')} (a full month period).")

# --- Trim the DataFrame ---
trimmed_sales_df = sales_df[
    (sales_df['SalesDate'] >= start_date_of_period) &
    (sales_df['SalesDate'] < end_date_of_period)
].copy()

print(f"\nData trimming complete. Trimmed dataset size: {len(trimmed_sales_df)} rows for the target month.")
if not trimmed_sales_df.empty:
    print(f"Date range of trimmed data: {trimmed_sales_df['SalesDate'].min()} to {trimmed_sales_df['SalesDate'].max()}")
else:
    print("No data found within the specified month. Please verify your target month and year, and ensure data exists for that period.")
    exit()

# --- Save the trimmed data to a new CSV file ---
output_filename = f"trimmed_sales_feb_{TARGET_YEAR}.csv"
trimmed_sales_df.to_csv(output_filename, index=False)
print(f"\nTrimmed sales data saved to '{output_filename}'.")

# Display head of the saved file for verification
print(f"\nHead of the saved '{output_filename}':")
print(pd.read_csv(output_filename).head())
