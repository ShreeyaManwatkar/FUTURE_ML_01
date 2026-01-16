import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")
 
df['Order Date'] = pd.to_datetime(df['Order Date'])
df = df.dropna()
df = df.sort_values('Order Date')


monthly_sales = df.resample('M', on='Order Date')['Sales'].sum().asfreq('M')

train = monthly_sales[:-6]
test = monthly_sales[-6:]

model = ExponentialSmoothing(
    train,
    trend='add',
    seasonal='add',
    seasonal_periods=12
)
fitted_model = model.fit()

test_forecast = fitted_model.forecast(6)

mae = mean_absolute_error(test, test_forecast)
mape = np.mean(np.abs((test - test_forecast) / test)) * 100

print("MAE:", mae)
print("MAPE:", mape)
print("Monthly Sales Mean:", monthly_sales.mean())

# Visualization
plt.figure(figsize=(10,5))
plt.plot(train.index, train, label='Training Data')
plt.plot(test.index, test, label='Actual Sales')
plt.plot(test.index, test_forecast, label='Forecasted Sales')
plt.title("Actual vs Forecasted Sales")
plt.xlabel("Date")
plt.ylabel("Sales (₹)")
plt.legend()
plt.show()

# Future forecast
future_forecast = fitted_model.forecast(12)

plt.figure(figsize=(12,6))
plt.plot(monthly_sales, label='Historical Sales')
plt.plot(future_forecast, label='Forecasted Sales', linestyle='--')
plt.title("Monthly Sales Forecast for Business Planning")
plt.xlabel("Time")
plt.ylabel("Sales (₹)")
plt.legend()
plt.grid(True)
plt.show()