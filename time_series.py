import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns
from column_selection import final_preprocessed_df  # Assuming this is the preprocessed DataFrame from the previous step

# Suppress warnings from Prophet
import logging
logging.getLogger('prophet').setLevel(logging.WARNING)

# Assuming 'final_preprocessed_df' is available and preprocessed
# from the 'Preprocess Trimmed Sales Data (February 2024) for Indian Grocery Store Specifics' immersive.
# This DataFrame should contain 'SalesDate' and 'TotalPrice'.

print("--- Time Series Forecasting for February 2024 Sales ---")
print("Using the 'final_preprocessed_df' which is already filtered for February 2024,")
print("Indian grocery store products, and selected categories.")


# Step 1: Prepare the data for Prophet
# Aggregate TotalPrice by SalesDate to get daily sales
daily_sales = final_preprocessed_df.groupby('SalesDate')['TotalPrice'].sum().reset_index()

# Rename columns to 'ds' and 'y' as required by Prophet
daily_sales = daily_sales.rename(columns={'SalesDate': 'ds', 'TotalPrice': 'y'})

print("\nPrepared daily sales data for Prophet (first 5 rows):")
print(daily_sales.head())
print(f"Total days in dataset: {len(daily_sales)}")


# Step 2: Initialize and Fit Prophet Model
# Using daily_seasonality=True if there's enough data to detect daily patterns
# (though with only one month, it might be weak)
model = Prophet(seasonality_mode='additive', daily_seasonality=True)
model.fit(daily_sales)

print("\nProphet model fitted to the February 2024 daily sales data.")

# Step 3: Make Future DataFrame
# Forecast for the next 7 days (into March)
future = model.make_future_dataframe(periods=7, include_history=True) # include_history=True to plot actuals
print(f"\nFuture DataFrame created for {len(future)} periods (including history and next 7 days).")
print(future.tail(10)) # Show some of the future dates

# Step 4: Generate Forecasts
forecast = model.predict(future)

print("\nForecast generated (first 5 rows of forecast):")
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())
print("Forecast generated (last 5 rows of forecast - predictions):")
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# Step 5: Plot the Forecasts
fig1 = model.plot(forecast)
plt.title('Daily Sales Forecast for February 2024 and Next 7 Days')
plt.xlabel('Date')
plt.ylabel('Total Sales (₹)') # Updated label to reflect Rupees
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# Plot the components of the forecast (trend, daily seasonality)
fig2 = model.plot_components(forecast)
plt.show()


# Step 6: Acknowledge Limitations
print("\n--- Important Note on Forecast Limitations ---")
print("This forecast was generated using only one month (February 2024) of historical sales data.")
print("Due to this very limited dataset, the accuracy and reliability of these predictions are inherently low.")
print("Time series models perform best with more historical data to accurately identify long-term trends,")
print("yearly seasonality, and more robust weekly/daily patterns.")
print("These forecasts should be considered illustrative and not for critical business decision-making.")

print("\nTime Series Forecasting section complete.")
