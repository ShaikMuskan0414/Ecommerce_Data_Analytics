
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate the project and dataset
project_folder = Path(__file__).resolve().parent.parent
data_file = project_folder / "data" / "scraped_products.csv"

# Create a folder for chart images
output_folder = project_folder / "results"
output_folder.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(data_file)

# Chart 1: Distribution of product prices
plt.figure(figsize=(8, 5))
plt.hist(df["price_gbp"], bins=10, edgecolor="black")
plt.title("Distribution of Book Prices")
plt.xlabel("Price (£)")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.savefig(output_folder / "price_distribution.png")
plt.show()
plt.close()

# Chart 2: Number of products by rating
rating_order = ["One", "Two", "Three", "Four", "Five"]
rating_counts = (
    df["rating"].value_counts()
    .reindex(rating_order, fill_value=0)
)

plt.figure(figsize=(8, 5))
rating_counts.plot(kind="bar", edgecolor="black")
plt.title("Number of Products by Rating")
plt.xlabel("Rating")
plt.ylabel("Number of Products")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_folder / "products_by_rating.png")
plt.show()
plt.close()

# Chart 3: Five most expensive products
top_five = df.nlargest(5, "price_gbp").sort_values("price_gbp")

plt.figure(figsize=(10, 6))
plt.barh(top_five["product_name"], top_five["price_gbp"],
         edgecolor="black")
plt.title("Five Most Expensive Books")
plt.xlabel("Price (£)")
plt.ylabel("Book")
plt.tight_layout()
plt.savefig(output_folder / "top_five_expensive.png")
plt.show()
plt.close()

# Chart 4: Product availability
availability_counts = df["availability"].value_counts()

plt.figure(figsize=(7, 5))
availability_counts.plot(kind="bar", edgecolor="black")
plt.title("Product Availability")
plt.xlabel("Availability")
plt.ylabel("Number of Products")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_folder / "product_availability.png")
plt.show()
plt.close()

print("Visualization completed!")
print("Charts saved in:", output_folder)
print("Created 4 charts.")