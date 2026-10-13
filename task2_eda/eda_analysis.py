
from pathlib import Path

import pandas as pd


def main():
    project_folder = Path(__file__).resolve().parent.parent
    data_file = project_folder / "data" / "scraped_products.csv"
    results_folder = project_folder / "results"
    results_folder.mkdir(parents=True, exist_ok=True)

    if not data_file.exists():
        print(f"Dataset not found: {data_file}")
        return

    df = pd.read_csv(data_file)

    required_columns = [
        "product_name",
        "price_gbp",
        "availability",
        "rating",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Missing required columns:", missing_columns)
        return

    df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")
    df["rating"] = df["rating"].astype(str).str.title()

    valid_df = df.dropna(subset=required_columns).copy()
    valid_df = valid_df[valid_df["price_gbp"] >= 0]

    report_lines = [
        "E-COMMERCE DATA ANALYTICS - EDA REPORT",
        "=" * 45,
        "",
        "DATASET OVERVIEW",
        f"Total rows loaded: {len(df)}",
        f"Valid rows analyzed: {len(valid_df)}",
        f"Number of columns: {len(df.columns)}",
        f"Duplicate product names: {df['product_name'].duplicated().sum()}",
        f"Missing values by column:\n{df.isnull().sum().to_string()}",
        "",
        "PRICE ANALYSIS (GBP)",
        valid_df["price_gbp"].describe().round(2).to_string(),
        "",
        "PRICE RANGE",
        f"Below £20: {(valid_df['price_gbp'] < 20).sum()}",
        f"£20 to £39.99: {((valid_df['price_gbp'] >= 20) & (valid_df['price_gbp'] < 40)).sum()}",
        f"£40 and above: {(valid_df['price_gbp'] >= 40).sum()}",
        "",
        "PRODUCT RATINGS",
        valid_df["rating"].value_counts().to_string(),
        "",
        "AVERAGE PRICE BY RATING",
        valid_df.groupby("rating")["price_gbp"].mean().sort_values().round(2).to_string(),
        "",
        "AVAILABILITY",
        valid_df["availability"].value_counts().to_string(),
        "",
        "INTERPRETATION",
        "This dataset contains book catalogue listings, not sales transactions.",
        "Listed prices and ratings do not establish sales, revenue, or customer behavior.",
    ]

    report = "\n".join(report_lines)
    report_file = results_folder / "eda_report.txt"
    report_file.write_text(report, encoding="utf-8")

    print(report)
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    main()