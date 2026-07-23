import pandas as pd
from sqlalchemy import create_engine

# ----------------------------
# Database Configuration
# ----------------------------

username = "root"
password = ""          # XAMPP default root password empty
host = "localhost"
port = "3306"
database = "retail_analytics"

# ----------------------------
# Connect Database
# ----------------------------

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# ----------------------------
# Load CSV
# ----------------------------

df = pd.read_csv("../Dataset/Cleaned_Superstore.csv", encoding="latin1")

print(df.head())

# ----------------------------
# Import into Database
# ----------------------------

df.to_sql(
    name="sales_data",
    con=engine,
    if_exists="replace",
    index=False
)

print("✅ Data Imported Successfully into MySQL!")