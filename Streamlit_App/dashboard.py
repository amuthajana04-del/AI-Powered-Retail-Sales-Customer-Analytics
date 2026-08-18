import joblib
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Powered Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# PROFESSIONAL DASHBOARD HEADER
# ==========================================================

st.markdown(
    """
    <div style="
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(90deg, #0f172a, #1e3a8a);
        color: white;
        text-align: center;
        margin-bottom: 25px;
    ">
        <h1 style="margin-bottom: 5px;">
            🤖 AI Powered Retail Sales & Customer Analytics
        </h1>
        <p style="font-size: 18px; margin: 0;">
            Intelligent Sales • Customer • Product Analytics Dashboard
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Load Dataset
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Dataset/Cleaned_Superstore.csv")

df = load_data()
# ==========================================================
# SIDEBAR PROJECT INFORMATION
# ==========================================================

st.sidebar.markdown("---")

st.sidebar.title("🤖 AI Retail Analytics")

st.sidebar.info(
    """
    **Project Modules**

    📊 Sales Analytics  
    🔮 Sales Prediction  
    👥 Customer Segmentation  
    🛍️ Product Recommendation
    """
)

st.sidebar.markdown("---")

st.sidebar.write(
    "Developed by **S. Janagarajan**"
)
# ==========================
# Sidebar Filters
# ==========================

st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

segment = st.sidebar.multiselect(
    "Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)

# Apply Filters
df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment))
]

st.success("✅ Dataset Loaded Successfully")

# -------------------------------
# Charts
# -------------------------------
col1, col2 = st.columns(2)

# Sales by Category
with col1:

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=".2s",
        title="📊 Sales by Category"
    )

    fig1.update_layout(
        xaxis_title="Category",
        yaxis_title="Sales ($)"
    )

    st.plotly_chart(fig1, use_container_width=True)

# Sales by Region
with col2:

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        hole=0.45,
        title="🌍 Sales by Region"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# KPI Cards
st.markdown("---")

st.subheader("📈 Sales Trend by Order Date")

# Convert Order Date to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Monthly Sales
monthly_sales = (
    df.groupby(
        pd.Grouper(
            key="Order Date",
            freq="ME"
        )
    )["Sales"]
    .sum()
    .reset_index()
)
monthly_sales["Month"] = range(len(monthly_sales))
fig4 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig4, use_container_width=True)
# -------------------------------
st.markdown("---")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = len(df)
total_customers = df["Customer ID"].nunique()
st.subheader("📈 Business Performance Overview")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "💰 Total Sales",
    f"${total_sales:,.0f}"
)

kpi2.metric(
    "📈 Total Profit",
    f"${total_profit:,.0f}"
)

kpi3.metric(
    "🛒 Total Orders",
    f"{total_orders:,}"
)

kpi4.metric(
    "👥 Total Customers",
    f"{total_customers:,}"
)
# ============================================================
# TOP 10 SELLING PRODUCTS
# ============================================================

st.markdown("---")
st.subheader("🏆 Top 10 Selling Products")

top_products = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig_sales = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    color_continuous_scale="Blues",
    title="Top 10 Products by Sales"
)

fig_sales.update_layout(
    height=550,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig_sales, use_container_width=True)

# ============================================================
# TOP 10 PROFITABLE PRODUCTS
# ============================================================

st.markdown("---")
st.subheader("💰 Top 10 Profitable Products")

top_profit = (
    df.groupby("Product Name")["Profit"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig_profit = px.bar(
    top_profit,
    x="Profit",
    y="Product Name",
    orientation="h",
    color="Profit",
    color_continuous_scale="Viridis",
    title="Top 10 Products by Profit"
)

fig_profit.update_layout(
    height=550,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig_profit, use_container_width=True)

# ============================================================
# DOWNLOAD REPORTS
# ============================================================

st.markdown("---")
st.subheader("📥 Download Analysis Reports")

download1, download2 = st.columns(2)

with download1:

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Full Dataset",
        data=csv,
        file_name="Retail_Sales_Data.csv",
        mime="text/csv"
    )

with download2:

    csv2 = top_products.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Top Products",
        data=csv2,
        file_name="Top_Products.csv",
        mime="text/csv"
    )

# ============================================================
# SALES BY SEGMENT
# ============================================================

st.markdown("---")
st.subheader("👥 Sales by Segment")

segment_sales = (
    df.groupby("Segment")["Sales"]
      .sum()
      .reset_index()
)

fig_segment = px.bar(
    segment_sales,
    x="Segment",
    y="Sales",
    color="Segment",
    text_auto=".2s",
    title="Sales by Customer Segment"
)

st.plotly_chart(fig_segment, use_container_width=True)

# ============================================================
# PROFIT BY CATEGORY
# ============================================================

st.markdown("---")
st.subheader("📈 Profit by Category")

profit_category = (
    df.groupby("Category")["Profit"]
      .sum()
      .reset_index()
)

fig_profit_category = px.pie(
    profit_category,
    names="Category",
    values="Profit",
    hole=0.5,
    title="Profit Distribution by Category"
)

st.plotly_chart(fig_profit_category, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================
# ============================================================
# CUSTOMER SEGMENT DISTRIBUTION
# ============================================================

st.markdown("---")
st.subheader("👥 Customer Segment Distribution")

segment_count = (
    df.groupby("Segment")["Customer ID"]
      .nunique()
      .reset_index(name="Customers")
)

fig_segment = px.pie(
    segment_count,
    names="Segment",
    values="Customers",
    hole=0.5,
    title="Customer Distribution by Segment"
)

st.plotly_chart(fig_segment, use_container_width=True)
# ============================================================
# AI SALES PREDICTION
# ============================================================

st.markdown("---")
st.subheader("🤖 AI Sales Prediction")

model = joblib.load("trained_models/sales_prediction_model.pkl")

st.write("Predict next month sales using the trained Machine Learning model.")

if st.button("🔮 Predict Next Month Sales"):

    next_month = monthly_sales["Month"].max() + 1

    prediction = model.predict(
        pd.DataFrame({
            "Month": [next_month]
        })
    )

    st.success(
        f"💰 Predicted Next Month Sales: ${prediction[0]:,.2f}"
    )
    # ============================================================
# ACTUAL VS PREDICTED SALES
# ============================================================

st.markdown("---")
st.subheader("📊 Actual vs Predicted Sales")

prediction_values = model.predict(
    monthly_sales[["Month"]]
)

comparison_df = monthly_sales.copy()

comparison_df["Predicted Sales"] = prediction_values

fig_prediction = px.line(
    comparison_df,
    x="Order Date",
    y=["Sales", "Predicted Sales"],
    markers=True,
    title="Actual Sales vs Predicted Sales"
)

fig_prediction.update_layout(
    xaxis_title="Order Date",
    yaxis_title="Sales ($)",
    legend_title="Sales Type"
)

st.plotly_chart(
    fig_prediction,
    use_container_width=True
)
# ============================================================
# REGION WISE PROFIT
# ============================================================

st.markdown("---")
st.subheader("🌍 Profit by Region")

region_profit = (
    df.groupby("Region")["Profit"]
      .sum()
      .reset_index()
)

fig_region = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    color="Region",
    text_auto=".2s",
    title="Profit by Region"
)

st.plotly_chart(fig_region, use_container_width=True)
#======================================================
# CUSTOMER SEGMENTATION
# ==========================================================

st.markdown("---")
st.subheader("👥 Customer Segmentation")

# Load customer segmentation results
segment_file = "Dataset/customer_segments.csv"

try:
    segment_df = pd.read_csv(segment_file)

    st.success("✅ Customer Segmentation Data Loaded")

    # ------------------------------------------------------
    # Segment Summary
    # ------------------------------------------------------

    segment_summary = (
        segment_df
        .groupby("Customer Segment")
        .agg(
            Customers=("Customer Name", "count"),
            Average_Sales=("Sales", "mean"),
            Average_Profit=("Profit", "mean")
        )
        .reset_index()
    )

    # ------------------------------------------------------
    # Customer Count by Segment
    # ------------------------------------------------------

    st.markdown("### 👥 Customers by Segment")

    fig_segment_count = px.bar(
        segment_summary,
        x="Customer Segment",
        y="Customers",
        color="Customer Segment",
        text_auto=True,
        title="Customer Distribution by Segment"
    )

    st.plotly_chart(
        fig_segment_count,
        use_container_width=True
    )

    # ------------------------------------------------------
    # Sales by Customer Segment
    # ------------------------------------------------------

    st.markdown("### 💰 Sales by Customer Segment")

    segment_sales = (
        segment_df
        .groupby("Customer Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig_segment_sales = px.pie(
        segment_sales,
        names="Customer Segment",
        values="Sales",
        hole=0.5,
        title="Sales Distribution by Customer Segment"
    )

    st.plotly_chart(
        fig_segment_sales,
        use_container_width=True
    )

    # ------------------------------------------------------
    # Segment Details
    # ------------------------------------------------------

    st.markdown("### 📊 Segment Performance")

    st.dataframe(
        segment_summary,
        use_container_width=True
    )

except FileNotFoundError:

    st.warning(
        "⚠️ Customer segmentation data not found. "
        "Run Models/customer_segmentation.py first."
    )

 # ==========================================================
# PRODUCT RECOMMENDATION
# ==========================================================

st.markdown("---")
st.subheader("🛍️ Product Recommendation & Analytics")

try:
    top_selling_df = pd.read_csv(
        "Dataset/top_selling_products.csv"
    )

    top_profitable_df = pd.read_csv(
        "Dataset/top_profitable_products.csv"
    )

    st.success("✅ Product Analysis Reports Loaded")

except FileNotFoundError:
    st.warning(
        "⚠️ Product analysis reports not found. "
        "Run Models/product_recommendation.py first."
    )
# ----------------------------------------------------------
# TOP 10 SELLING PRODUCTS
# ----------------------------------------------------------

st.markdown("### 🏆 Top 10 Selling Products")

top_selling_display = (
    top_selling_df
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_recommend_sales = px.bar(
    top_selling_display.sort_values("Sales"),
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    title="Top 10 Products by Sales"
)

st.plotly_chart(
    fig_recommend_sales,
    use_container_width=True
)
# ==========================================================
# SMART PRODUCT RECOMMENDATION
# ==========================================================

st.markdown("### ⭐ Smart Product Recommendation")

recommend_category = st.selectbox(
    "Select a Category",
    ["All Categories"] + sorted(df["Category"].dropna().unique().tolist())
)

# Filter products based on selected category
if recommend_category == "All Categories":
    recommendation_df = df.copy()
else:
    recommendation_df = df[
        df["Category"] == recommend_category
    ].copy()

# Product-level analysis
recommendation = (
    recommendation_df
    .groupby(["Product Name", "Category", "Sub-Category"])
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

# Recommendation score
recommendation["Score"] = (
    recommendation["Sales"].rank(pct=True) * 0.5
    + recommendation["Profit"].rank(pct=True) * 0.3
    + recommendation["Quantity"].rank(pct=True) * 0.2
)

# Top 5 recommended products
recommended_products = (
    recommendation
    .sort_values("Score", ascending=False)
    .head(5)
)

st.markdown("#### 🏆 Recommended Products")

st.dataframe(
    recommended_products[
        [
            "Product Name",
            "Category",
            "Sub-Category",
            "Sales",
            "Profit",
            "Quantity"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

if not recommended_products.empty:

    best_product = recommended_products.iloc[0]

    st.success(
        f"⭐ **Top Recommendation:** "
        f"{best_product['Product Name']} | "
        f"Sales: ${best_product['Sales']:,.2f} | "
        f"Profit: ${best_product['Profit']:,.2f}"
    )
    # ==========================================================
# RECOMMENDATION CHART
# ==========================================================

st.markdown("#### 📊 Recommended Products Comparison")

fig_recommendation = px.bar(
    recommended_products.sort_values("Score"),
    x="Score",
    y="Product Name",
    orientation="h",
    color="Score",
    title="Top Recommended Products",
    text_auto=".2f"
)

fig_recommendation.update_layout(
    xaxis_title="Recommendation Score",
    yaxis_title="Product",
    height=450
)

st.plotly_chart(
    fig_recommendation,
    use_container_width=True
)
# ==========================================================
# RECOMMENDATION REASONS
# ==========================================================

st.markdown("#### 💡 Why These Products Are Recommended?")

reason_df = recommended_products[
    [
        "Product Name",
        "Sales",
        "Profit",
        "Quantity",
        "Score"
    ]
].copy()

reason_df["Reason"] = reason_df.apply(
    lambda row:
        "🔥 High Sales & Strong Profit"
        if row["Sales"] >= recommended_products["Sales"].median()
        and row["Profit"] >= recommended_products["Profit"].median()
        else
        "📈 Good Sales Performance"
        if row["Sales"] >= recommended_products["Sales"].median()
        else
        "💰 Strong Profit Performance"
        if row["Profit"] >= recommended_products["Profit"].median()
        else
        "📦 Good Quantity Sold",
    axis=1
)

st.dataframe(
    reason_df[
        [
            "Product Name",
            "Sales",
            "Profit",
            "Quantity",
            "Score",
            "Reason"
        ]
    ],
    use_container_width=True,
    hide_index=True
)
 # ==========================================================
 # FOOTER
 # ==========================================================

st.markdown("---")

st.caption("🚀 AI Powered Retail Sales & Customer Analytics Dashboard")
