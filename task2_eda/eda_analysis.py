
import pandas as pd
from pathlib import Path

# Locate the scraped dataset
project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder / "data" / "scraped_products.csv"

df = pd.read_csv(csv_file)

print("===== DATASET OVERVIEW =====")
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\n===== FIRST FIVE PRODUCTS =====")
print(df.head())

print("\n===== COLUMN INFORMATION =====")
print(df.info())

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())

print("\n===== PRICE STATISTICS (GBP) =====")
print(df["price_gbp"].describe())

print("\n===== PRODUCTS BY RATING =====")
print(df["rating"].value_counts())

print("\n===== PRODUCT AVAILABILITY =====")
print(df["availability"].value_counts())

print("\n===== FIVE MOST EXPENSIVE PRODUCTS =====")
print(
    df.sort_values("price_gbp", ascending=False)[
        ["product_name", "price_gbp", "rating"]
    ].head()
)

print("\n===== FIVE LEAST EXPENSIVE PRODUCTS =====")
print(
    df.sort_values("price_gbp")[
        ["product_name", "price_gbp", "rating"]
    ].head()
)

print("\nEDA analysis completed!")