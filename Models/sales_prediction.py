import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# -------------------------------
# Create folders
# -------------------------------

os.makedirs("../Screenshots", exist_ok=True)
os.makedirs("./trained_models", exist_ok=True)

# -------------------------------
# Load Dataset
# -------------------------------

df = pd.read_csv("../Dataset/Cleaned_Superstore.csv", encoding="latin1")

print("="*50)
print("DATASET LOADED")
print("="*50)

print(df.head())

# -------------------------------
# Convert Date
# -------------------------------

df["Order Date"] = pd.to_datetime(df["Order Date"])

# -------------------------------
# Monthly Sales
# -------------------------------

monthly_sales = df.groupby(
    df["Order Date"].dt.to_period("M")
)["Sales"].sum().reset_index()

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

monthly_sales["Month"] = range(len(monthly_sales))

print("\nMonthly Sales")
print(monthly_sales.head())

# -------------------------------
# Model Training
# -------------------------------

X = monthly_sales[["Month"]]
y = monthly_sales["Sales"]

model = LinearRegression()

model.fit(X, y)

monthly_sales["Predicted Sales"] = model.predict(X)

# -------------------------------
# Metrics
# -------------------------------

mae = mean_absolute_error(y, monthly_sales["Predicted Sales"])
mse = mean_squared_error(y, monthly_sales["Predicted Sales"])
rmse = mse ** 0.5
r2 = r2_score(y, monthly_sales["Predicted Sales"])

print("\nMODEL PERFORMANCE")
print("="*40)

print("MAE :", round(mae,2))
print("MSE :", round(mse,2))
print("RMSE :", round(rmse,2))
print("R2 Score :", round(r2,4))

# -------------------------------
# Prediction Graph
# -------------------------------

plt.figure(figsize=(10,5))

plt.plot(
    monthly_sales["Order Date"],
    monthly_sales["Sales"],
    marker="o",
    label="Actual Sales"
)

plt.plot(
    monthly_sales["Order Date"],
    monthly_sales["Predicted Sales"],
    marker="o",
    label="Predicted Sales"
)

plt.xticks(rotation=45)

plt.title("Sales Prediction")

plt.xlabel("Month")

plt.ylabel("Sales")

plt.legend()

plt.tight_layout()

plt.savefig("../Screenshots/sales_prediction.png")

plt.show()

# -------------------------------
# Save Model
# -------------------------------

joblib.dump(
    model,
    "./trained_models/sales_prediction_model.pkl"
)

print("\nModel Saved Successfully")

# -------------------------------
# Future Prediction
# -------------------------------

future_month = [[len(monthly_sales)+1]]

future_prediction = model.predict(future_month)

print("\nNEXT MONTH SALES PREDICTION")

print(round(future_prediction[0],2))