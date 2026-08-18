# ==========================================================
# AI-Powered Retail Sales & Customer Analytics
# Module: Customer Segmentation
# Algorithm: K-Means Clustering
# Author: S. Janagarajan
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
import joblib

from pathlib import Path

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "Dataset"
SCREENSHOT_DIR = BASE_DIR / "Screenshots"
MODEL_DIR = BASE_DIR / "Models" / "trained_models"

# Create folders if they don't exist

SCREENSHOT_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

# ==========================================================
# Load Dataset
# ==========================================================

print("=" * 60)
print("CUSTOMER SEGMENTATION USING K-MEANS")
print("=" * 60)

dataset_path = DATASET_DIR / "Cleaned_Superstore.csv"

df = pd.read_csv(dataset_path, encoding="latin1")

print("\nDataset Loaded Successfully!\n")

print(df.head())

print("\nDataset Shape :", df.shape)

# ==========================================================
# Customer Summary
# ==========================================================

customer_data = (
    df.groupby("Customer Name")
      .agg({
          "Sales": "sum",
          "Profit": "sum",
          "Quantity": "sum"
      })
      .reset_index()
)

print("\nCustomer Summary")

print(customer_data.head())

# ==========================================================
# Feature Selection
# ==========================================================

X = customer_data[["Sales", "Profit", "Quantity"]]

# ==========================================================
# Feature Scaling
# ==========================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)
# ==========================================================
# Train K-Means Model
# ==========================================================

print("\nTraining K-Means Model...")

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

customer_data["Cluster"] = kmeans.fit_predict(X_scaled)

print("K-Means Model Trained Successfully!")

# ==========================================================
# Automatic Cluster Naming
# ==========================================================

cluster_sales = (
    customer_data.groupby("Cluster")["Sales"]
    .mean()
    .sort_values()
)

cluster_order = cluster_sales.index.tolist()

cluster_labels = {
    cluster_order[0]: "Budget",
    cluster_order[1]: "Regular",
    cluster_order[2]: "Premium"
}

customer_data["Customer Segment"] = (
    customer_data["Cluster"]
    .map(cluster_labels)
)

print("\nCustomer Segments Assigned Successfully!")

# ==========================================================
# Display Segment Summary
# ==========================================================

print("\nCustomer Segment Count")
print("-" * 40)

print(
    customer_data["Customer Segment"]
    .value_counts()
)

print("\nAverage Sales by Segment")
print("-" * 40)

print(
    customer_data.groupby("Customer Segment")["Sales"]
    .mean()
)

print("\nAverage Profit by Segment")
print("-" * 40)

print(
    customer_data.groupby("Customer Segment")["Profit"]
    .mean()
)

# ==========================================================
# Save Customer Segments CSV
# ==========================================================

output_csv = DATASET_DIR / "customer_segments.csv"

customer_data.to_csv(
    output_csv,
    index=False
)

print("\nCustomer Segments CSV Saved Successfully!")

print(output_csv)
# ==========================================================
# Visualization
# ==========================================================

plt.figure(figsize=(12, 7))

colors = {
    "Budget": "red",
    "Regular": "blue",
    "Premium": "green"
}

for segment in customer_data["Customer Segment"].unique():

    data = customer_data[
        customer_data["Customer Segment"] == segment
    ]

    plt.scatter(
        data["Sales"],
        data["Profit"],
        label=segment,
        s=80,
        alpha=0.7,
        color=colors[segment]
    )

plt.title("Customer Segmentation using K-Means", fontsize=16)

plt.xlabel("Total Sales")

plt.ylabel("Total Profit")

plt.legend()

plt.grid(True)

plt.tight_layout()

chart_path = SCREENSHOT_DIR / "customer_segments.png"

plt.savefig(chart_path)

plt.show()

print("\nCustomer Segmentation Chart Saved Successfully!")

# ==========================================================
# Save Model
# ==========================================================

model_path = MODEL_DIR / "customer_segmentation_model.pkl"

joblib.dump(kmeans, model_path)

print("\nK-Means Model Saved Successfully!")

# ==========================================================
# Business Insights
# ==========================================================

print("\n" + "=" * 60)
print("BUSINESS INSIGHTS")
print("=" * 60)

segment_summary = customer_data.groupby("Customer Segment").agg(
    Total_Customers=("Customer Name", "count"),
    Average_Sales=("Sales", "mean"),
    Average_Profit=("Profit", "mean")
)

print(segment_summary)

top_customer = customer_data.sort_values(
    by="Sales",
    ascending=False
).iloc[0]

print("\nTop Customer")
print("-" * 40)

print(f"Customer Name : {top_customer['Customer Name']}")
print(f"Sales         : {top_customer['Sales']:.2f}")
print(f"Profit        : {top_customer['Profit']:.2f}")
print(f"Segment       : {top_customer['Customer Segment']}")

print("\nFiles Generated")
print("-" * 40)
print(f"CSV   : {output_csv}")
print(f"Chart : {chart_path}")
print(f"Model : {model_path}")

print("\nCustomer Segmentation Completed Successfully!")
print("=" * 60)