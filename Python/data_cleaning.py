import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# File Paths
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_DIR, "..", "Dataset", "Superstore.csv")
CLEANED_PATH = os.path.join(BASE_DIR, "..", "Dataset", "Cleaned_Superstore.csv")
REPORT_PATH = os.path.join(BASE_DIR, "..", "Report", "Data_Cleaning_Report.txt")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "..", "Screenshots")

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ==========================================
# Load Dataset
# ==========================================

print("=" * 60)
print("LOADING DATASET...")
print("=" * 60)

df = pd.read_csv(DATASET_PATH, encoding="latin1")

print("\nFirst 5 Rows")
print(df.head())

print("\nDataset Information")
print(df.info())

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows :", df.duplicated().sum())

# ==========================================
# Data Cleaning
# ==========================================

# Remove duplicates
df = df.drop_duplicates()

# Fill Missing Values
for col in df.columns:

    if pd.api.types.is_numeric_dtype(df[col]):

        df[col] = df[col].fillna(df[col].mean())

    else:

        mode = df[col].mode()

        if len(mode) > 0:
            df[col] = df[col].fillna(mode[0])
        else:
            df[col] = df[col].fillna("Unknown")

# Convert Dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# ==========================================
# Save Cleaned Dataset
# ==========================================

df.to_csv(CLEANED_PATH, index=False)

print("\n✅ Cleaned Dataset Saved")

# ==========================================
# Sales by Category
# ==========================================

category_sales = df.groupby("Category")["Sales"].sum()

plt.figure(figsize=(8,5))
category_sales.plot(kind="bar")

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(os.path.join(SCREENSHOT_DIR, "Sales_by_Category.png"))

plt.close()

# ==========================================
# Profit by Region
# ==========================================

region_profit = df.groupby("Region")["Profit"].sum()

plt.figure(figsize=(8,5))
region_profit.plot(kind="bar")

plt.title("Profit by Region")
plt.xlabel("Region")
plt.ylabel("Profit")

plt.tight_layout()

plt.savefig(os.path.join(SCREENSHOT_DIR, "Profit_by_Region.png"))

plt.close()

# ==========================================
# Monthly Sales
# ==========================================

monthly_sales = df.groupby(
    df["Order Date"].dt.to_period("M")
)["Sales"].sum()

plt.figure(figsize=(12,5))
monthly_sales.plot()

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(os.path.join(SCREENSHOT_DIR, "Monthly_Sales.png"))

plt.close()

# ==========================================
# Missing Values Chart
# ==========================================

missing = df.isnull().sum()

plt.figure(figsize=(10,4))
missing.plot(kind="bar")

plt.title("Missing Values")

plt.tight_layout()

plt.savefig(os.path.join(SCREENSHOT_DIR, "Missing_Values.png"))

plt.close()

# ==========================================
# Generate Report
# ==========================================

with open(REPORT_PATH, "w") as report:

    report.write("DATA CLEANING REPORT\n")
    report.write("="*50 + "\n\n")

    report.write(f"Total Records : {len(df)}\n")
    report.write(f"Total Columns : {len(df.columns)}\n\n")

    report.write("Missing Values\n")
    report.write("-----------------\n")
    report.write(str(df.isnull().sum()))

    report.write("\n\nCategory Sales\n")
    report.write("-----------------\n")
    report.write(str(category_sales))

    report.write("\n\nRegion Profit\n")
    report.write("-----------------\n")
    report.write(str(region_profit))

print("\n✅ Report Generated Successfully")
print("✅ Charts Generated Successfully")
print("✅ Data Cleaning Module Completed Successfully")