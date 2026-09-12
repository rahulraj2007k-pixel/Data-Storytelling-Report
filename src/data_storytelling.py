"""
Data Storytelling — Online Retail
Run from project root:
    python src/data_storytelling.py

Input:
    data/online_retail_II.xlsx (downloaded from UCI Online Retail dataset)
Output:
    outputs/charts/*.png
    outputs/cleaned_online_retail.csv
    outputs/analysis_summary.txt
    outputs/final_eda_dashboard.png
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "online_retail_II.xlsx"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"
OUT.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)

def load_data():
    if not DATA.exists():
        raise FileNotFoundError(
            "Place the legally sourced UCI Online Retail Excel file at "
            f"{DATA}"
        )
    df = pd.read_excel(DATA, engine="openpyxl")
    # UCI Online Retail II can contain multiple sheets/periods.
    if "Invoice" in df.columns:
        return df
    if "InvoiceNo" in df.columns:
        return df
    raise ValueError("Expected Online Retail transaction columns were not found.")

def clean_data(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    # Normalize common column naming variants.
    rename = {
        "InvoiceNo": "Invoice",
        "StockCode": "StockCode",
        "Description": "Description",
        "Quantity": "Quantity",
        "InvoiceDate": "InvoiceDate",
        "UnitPrice": "UnitPrice",
        "CustomerID": "CustomerID",
        "Country": "Country",
    }
    df = df.rename(columns=rename)

    before = len(df)
    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates()

    # Keep fields required for customer/product/revenue analysis.
    df = df.dropna(subset=["Description", "CustomerID"])
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce")
    df = df.dropna(subset=["Quantity", "UnitPrice", "InvoiceDate", "CustomerID"])

    # Sales-performance scope: positive quantities and prices.
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()

    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.month
    df["MonthName"] = df["InvoiceDate"].dt.month_name()
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()

    quality = {
        "original_rows": before,
        "duplicates_removed": duplicates,
        "cleaned_rows": len(df),
        "cleaned_columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
    }
    return df, quality

def make_charts(df):
    sns.set_theme(style="whitegrid")

    monthly = df.groupby("YearMonth", as_index=False)["Revenue"].sum()
    plt.figure(figsize=(10, 5))
    plt.plot(monthly["YearMonth"], monthly["Revenue"], marker="o")
    plt.xticks(rotation=60, ha="right")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue (£)")
    plt.tight_layout()
    plt.savefig(CHARTS/"01_monthly_revenue.png", dpi=180)
    plt.close()

    countries = df.groupby("Country")["Revenue"].sum().nlargest(10).sort_values()
    plt.figure(figsize=(9, 5))
    countries.plot(kind="barh")
    plt.title("Top 10 Countries by Revenue")
    plt.xlabel("Revenue (£)")
    plt.tight_layout()
    plt.savefig(CHARTS/"02_top_countries.png", dpi=180)
    plt.close()

    products = df.groupby("Description")["Revenue"].sum().nlargest(10).sort_values()
    plt.figure(figsize=(10, 6))
    products.plot(kind="barh")
    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Revenue (£)")
    plt.tight_layout()
    plt.savefig(CHARTS/"03_top_products.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df.sample(min(15000, len(df)), random_state=42),
                    x="Quantity", y="Revenue", alpha=0.35)
    plt.title("Quantity vs Revenue")
    plt.tight_layout()
    plt.savefig(CHARTS/"04_quantity_vs_revenue.png", dpi=180)
    plt.close()

    corr = df[["Quantity", "UnitPrice", "Revenue"]].corr()
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", vmin=-1, vmax=1)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(CHARTS/"05_correlation_heatmap.png", dpi=180)
    plt.close()

    dow = df.groupby("DayOfWeek")["Revenue"].sum().reindex(
        ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    )
    plt.figure(figsize=(9, 5))
    dow.plot(kind="bar")
    plt.title("Revenue by Day of Week")
    plt.ylabel("Revenue (£)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(CHARTS/"06_revenue_by_day.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df["UnitPrice"])
    plt.title("Unit Price Distribution")
    plt.xlabel("Unit Price (£)")
    plt.tight_layout()
    plt.savefig(CHARTS/"07_unit_price_boxplot.png", dpi=180)
    plt.close()

    # Dashboard
    total_revenue = df["Revenue"].sum()
    total_qty = df["Quantity"].sum()
    orders = df["Invoice"].nunique()
    customers = df["CustomerID"].nunique()
    products_n = df["StockCode"].nunique()
    aov = total_revenue / orders if orders else 0

    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, height_ratios=[0.65, 1.4, 1.4])
    fig.suptitle("Online Retail — Decision-Oriented Data Storytelling Dashboard",
                 fontsize=20, fontweight="bold")

    cards = [
        ("Revenue", f"£{total_revenue:,.2f}"),
        ("Quantity Sold", f"{total_qty:,.0f}"),
        ("Orders", f"{orders:,.0f}"),
        ("Customers", f"{customers:,.0f}"),
        ("Products", f"{products_n:,.0f}"),
        ("Average Order Value", f"£{aov:,.2f}"),
    ]
    for i, (label, value) in enumerate(cards):
        ax = fig.add_subplot(gs[0, i % 3])
        if i >= 3:
            ax = fig.add_subplot(gs[0, i % 3])
        ax.axis("off")
        ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=17, fontweight="bold")
        ax.text(0.5, 0.18, label, ha="center", va="center", fontsize=10)

    ax1 = fig.add_subplot(gs[1, :2])
    ax1.plot(monthly["YearMonth"], monthly["Revenue"], marker="o")
    ax1.set_title("Monthly Revenue")
    ax1.tick_params(axis="x", rotation=55)

    ax2 = fig.add_subplot(gs[1, 2])
    countries.sort_values().plot(kind="barh", ax=ax2)
    ax2.set_title("Top Countries")

    ax3 = fig.add_subplot(gs[2, :2])
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", vmin=-1, vmax=1, ax=ax3)
    ax3.set_title("Correlation")

    ax4 = fig.add_subplot(gs[2, 2])
    products.sort_values().plot(kind="barh", ax=ax4)
    ax4.set_title("Top Products")

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT/"final_eda_dashboard.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

def main():
    df = load_data()
    clean, quality = clean_data(df)
    clean.to_csv(OUT/"cleaned_online_retail.csv", index=False)
    make_charts(clean)

    summary = [
        "DATA STORYTELLING ANALYSIS SUMMARY",
        f"Original rows: {quality['original_rows']:,}",
        f"Duplicates removed: {quality['duplicates_removed']:,}",
        f"Cleaned rows: {quality['cleaned_rows']:,}",
        f"Cleaned columns: {quality['cleaned_columns']}",
        f"Missing values after cleaning: {quality['missing_values']}",
        f"Revenue: £{clean['Revenue'].sum():,.2f}",
        f"Quantity sold: {clean['Quantity'].sum():,.0f}",
        f"Orders: {clean['Invoice'].nunique():,}",
        f"Customers: {clean['CustomerID'].nunique():,}",
        f"Products: {clean['StockCode'].nunique():,}",
        f"Average order value: £{clean['Revenue'].sum()/clean['Invoice'].nunique():,.2f}",
    ]
    (OUT/"analysis_summary.txt").write_text("\n".join(summary), encoding="utf-8")
    print("\n".join(summary))
    print("\nCharts and dashboard saved under outputs/.")

if __name__ == "__main__":
    main()
