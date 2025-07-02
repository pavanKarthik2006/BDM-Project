import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Removed: from io import StringIO # Not needed if reading directly from file
# Removed: import file_content_fetcher # As per your request, not using file_content_fetcher

# --- Data Loading ---
# The user wants a visualization of ABC analysis results.
# Assuming 'abc_analysis_results_feb_2024.csv' is directly available in the environment's root.
# Local file paths like C:\Users\... cannot be accessed directly in this environment.
ABC_RESULTS_FILE_PATH = 'abc_analysis_results_feb_2024.csv'

abc_results_df = pd.DataFrame()
data_loaded_successfully = False

try:
    # Attempt to load data directly using pandas.read_csv
    abc_results_df = pd.read_csv(ABC_RESULTS_FILE_PATH)
    data_loaded_successfully = True
    print(f"ABC analysis results loaded successfully from '{ABC_RESULTS_FILE_PATH}'.")
except FileNotFoundError:
    print(f"Error: The file '{ABC_RESULTS_FILE_PATH}' was not found.")
    print("Please ensure the file is uploaded directly to the environment or its name is correct.")
except Exception as e:
    print(f"Error during file loading or parsing for ABC results: {e}. Cannot proceed without data.")

if not data_loaded_successfully or abc_results_df.empty:
    print("Failed to load ABC analysis data or DataFrame is empty. Exiting visualization.")
    exit() # Exit if ABC data is not available


# --- Summarize ABC categories for Visualization ---
# The loaded CSV should already contain 'ABC_Category' and 'TotalRevenue'
# Check if 'ProductID' column exists, otherwise, adapt the groupby if needed.
# Assuming 'ProductID' is consistently present based on previous ABC analysis code.
if 'ProductID' not in abc_results_df.columns:
    print("Warning: 'ProductID' column not found for ProductCount. Grouping by ABC_Category only.")
    abc_summary = abc_results_df.groupby('ABC_Category').agg(
        TotalRevenue=('TotalRevenue', 'sum')
    ).reset_index()
    # Add a dummy ProductCount if not available for consistency in later print, though not used in plot.
    abc_summary['ProductCount'] = abc_results_df.groupby('ABC_Category').size().reset_index(name='count')['count']
else:
    abc_summary = abc_results_df.groupby('ABC_Category').agg(
        ProductCount=('ProductID', 'count'),
        TotalRevenue=('TotalRevenue', 'sum')
    ).reset_index()

# Calculate PercentageOfTotalRevenue
total_overall_revenue = abc_summary['TotalRevenue'].sum()
if total_overall_revenue == 0:
    print("Warning: Total revenue is zero. Percentage of total revenue will be zero.")
    abc_summary['PercentageOfTotalRevenue'] = 0.0
else:
    abc_summary['PercentageOfTotalRevenue'] = (abc_summary['TotalRevenue'] / total_overall_revenue) * 100

print("\nABC Analysis Summary for Visualization:")
print(abc_summary)


# --- Visualization of ABC Analysis ---
plt.figure(figsize=(10, 6))
# Ensure the order of categories is A, B, C for consistent plotting
# Check if all categories (A, B, C) are present. If not, adjust order dynamically.
available_categories = abc_summary['ABC_Category'].unique()
plot_order = [cat for cat in ['A', 'B', 'C'] if cat in available_categories]

if not plot_order:
    print("No A, B, or C categories found in the data to plot.")
else:
    sns.barplot(x='ABC_Category', y='PercentageOfTotalRevenue', data=abc_summary,
                palette='viridis', order=plot_order)

    plt.title('ABC Analysis: Percentage of Total Revenue by Category (February 2024)')
    plt.xlabel('ABC Category')
    plt.ylabel('Percentage of Total Revenue (%)')
    plt.ylim(0, 100) # Ensure Y-axis goes from 0 to 100%

    # Add text labels for percentages on top of bars
    for index, row in abc_summary.iterrows():
        # Find the correct x-position for each category (A=0, B=1, C=2 in the `plot_order`)
        if row['ABC_Category'] in plot_order: # Ensure the category is in the actual plot
            x_pos = plot_order.index(row['ABC_Category'])
            plt.text(x_pos, row['PercentageOfTotalRevenue'] + 2, f"{row['PercentageOfTotalRevenue']:.2f}%",
                     color='black', ha="center")

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

print("\nABC Analysis visualization complete.")
