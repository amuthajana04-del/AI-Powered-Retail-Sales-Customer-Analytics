from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CSV_DIR = Path("Dataset")
OUTPUT_DIR = Path("Screenshots")


def load_dataset():
    """Load the Superstore dataset from CSV file."""
    file_path = CSV_DIR / "Cleaned_Superstore.csv"
    df = pd.read_csv(file_path)
    return df


def validate_dataset(df):
    """Validate dataset integrity and structure."""
    required_columns = ["Product ID", "Product Name", "Category", "Sub-Category", 
                       "Sales", "Profit", "Quantity", "Region", "Segment", "Customer ID"]
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    if df.empty:
        raise ValueError("Dataset is empty")
    
    if df.isnull().sum().sum() > 0:
        df = df.dropna()
    
    print("✓ Dataset validated successfully")
    return df


def top_selling_products(df, n=10):
    """Calculate top N selling products by quantity and revenue."""
    top_qty = df.groupby("Product Name").agg({
        "Quantity": "sum",
        "Sales": "sum",
        "Profit": "sum"
    }).sort_values("Quantity", ascending=False).head(n)
    
    return top_qty


def top_profitable_products(df, n=10):
    """Calculate top N profitable products."""
    top_profit = df.groupby("Product Name").agg({
        "Profit": "sum",
        "Sales": "sum",
        "Quantity": "sum"
    }).sort_values("Profit", ascending=False).head(n)
    
    return top_profit


def region_wise_analysis(df):
    """Analyze best products by region."""
    region_products = df.groupby(["Region", "Product Name"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum"
    }).reset_index()
    
    top_per_region = region_products.sort_values(["Region", "Sales"], ascending=[True, False]).groupby("Region").head(5)
    
    return top_per_region


def category_wise_analysis(df):
    """Analyze performance by category."""
    category_perf = df.groupby("Category").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Customer ID": "nunique"
    }).sort_values("Profit", ascending=False)
    
    return category_perf


def customer_segment_analysis(df):
    """Analyze customer segments and their preferences."""
    segment_stats = df.groupby("Segment").agg({
        "Sales": ["sum", "mean"],
        "Profit": ["sum", "mean"],
        "Quantity": "sum",
        "Customer ID": "nunique"
    }).round(2)
    
    return segment_stats


def business_insights(df, top_products, top_profitable, region_analysis, category_analysis, segment_analysis):
    """Generate actionable business insights."""
    insights = []
    
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
    
    insights.append(f"Total Sales: ${total_sales:,.2f}")
    insights.append(f"Total Profit: ${total_profit:,.2f}")
    insights.append(f"Profit Margin: {profit_margin:.2f}%")
    
    best_product = top_products.index[0]
    insights.append(f"Best Selling Product: {best_product}")
    
    best_profitable = top_profitable.index[0]
    insights.append(f"Most Profitable Product: {best_profitable}")
    
    best_category = category_analysis.index[0]
    insights.append(f"Best Performing Category: {best_category}")
    
    best_segment = segment_analysis[("Sales", "sum")].idxmax()
    insights.append(f"Highest Revenue Segment: {best_segment}")
    
    return insights

def generate_charts(df, top_selling, top_profitable, category_perf):
    """Generate 4 visualizations for business analysis."""
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Chart 1: Top Selling Products
    top_selling.head(10)["Sales"].sort_values().plot(
        kind="barh", ax=axes[0, 0], color="skyblue"
    )
    axes[0, 0].set_title("Top 10 Selling Products by Revenue", fontsize=12, fontweight="bold")
    axes[0, 0].set_xlabel("Sales ($)")
    
    # Chart 2: Top Profitable Products
    top_profitable.head(10)["Profit"].sort_values().plot(
        kind="barh", ax=axes[0, 1], color="lightgreen"
    )
    axes[0, 1].set_title("Top 10 Profitable Products", fontsize=12, fontweight="bold")
    axes[0, 1].set_xlabel("Profit ($)")
    
    # Chart 3: Category Sales
    category_perf["Sales"].plot(
        kind="bar", ax=axes[1, 0], color="coral"
    )
    axes[1, 0].set_title("Sales by Category", fontsize=12, fontweight="bold")
    axes[1, 0].set_ylabel("Sales ($)")
    axes[1, 0].tick_params(axis="x", rotation=45)
    
    # Chart 4: Customer Segment Distribution
    segment_sales = df.groupby("Segment")["Sales"].sum()
    axes[1, 1].pie(segment_sales, labels=segment_sales.index, autopct="%1.1f%%", startangle=90)
    axes[1, 1].set_title("Sales Distribution by Customer Segment", fontsize=12, fontweight="bold")
    
    plt.tight_layout()
    output_path = Path("Screenshots") / "product_analysis_charts.png"
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"✓ Charts saved to {output_path}")
    plt.close()

def save_reports(top_selling, top_profitable, region_analysis, category_analysis, segment_analysis):
    """Save all analysis results to CSV files."""
    output_dir = Path("Dataset")
    output_dir.mkdir(exist_ok=True)
    
    top_selling.to_csv(output_dir / "top_selling_products.csv")
    top_profitable.to_csv(output_dir / "top_profitable_products.csv")
    region_analysis.to_csv(output_dir / "region_wise_analysis.csv", index=False)
    category_analysis.to_csv(output_dir / "category_analysis.csv")
    segment_analysis.to_csv(output_dir / "segment_analysis.csv")
    
    print("✓ Reports saved to Dataset/ directory")


def print_summary(insights, top_selling, top_profitable):
    """Print executive summary to console."""
    print("\n" + "="*60)
    print("PRODUCT RECOMMENDATION & ANALYTICS REPORT")
    print("="*60)
    
    print("\n📊 BUSINESS INSIGHTS:")
    for insight in insights:
        print(f"  • {insight}")
    
    print("\n🏆 TOP 5 SELLING PRODUCTS:")
    for idx, (product, row) in enumerate(top_selling.head(5).iterrows(), 1):
        print(f"  {idx}. {product} - Sales: ${row['Sales']:,.2f}, Qty: {row['Quantity']:.0f}")
    
    print("\n💰 TOP 5 PROFITABLE PRODUCTS:")
    for idx, (product, row) in enumerate(top_profitable.head(5).iterrows(), 1):
        print(f"  {idx}. {product} - Profit: ${row['Profit']:,.2f}, Sales: ${row['Sales']:,.2f}")
    
    print("\n" + "="*60 + "\n")


def main():
    """Main execution function orchestrating all analyses."""
    df = load_dataset()
    df = validate_dataset(df)
    
    top_selling = top_selling_products(df)
    top_profitable = top_profitable_products(df)
    region_analysis = region_wise_analysis(df)
    category_analysis = category_wise_analysis(df)
    segment_analysis = customer_segment_analysis(df)
    
    insights = business_insights(df, top_selling, top_profitable, region_analysis, category_analysis, segment_analysis)
    
    generate_charts(df, top_selling, top_profitable, category_analysis)
    save_reports(top_selling, top_profitable, region_analysis, category_analysis, segment_analysis)
    print_summary(insights, top_selling, top_profitable)


if __name__ == "__main__":
    main()