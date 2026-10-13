
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
products = []

for page in range(1, 4):
    url = BASE_URL.format(page)
    print("Scraping page", page)

    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.select("article.product_pod"):
        title = book.h3.a["title"]
        price_text = book.select_one(".price_color").get_text(strip=True)
        availability = book.select_one(".availability").get_text(strip=True)

        rating_classes = book.select_one("p.star-rating").get("class", [])
        rating = next(
            (item for item in rating_classes if item != "star-rating"),
            "Unknown"
        )

        price = price_text.replace("£", "").replace("Â", "")

        products.append({
            "product_name": title,
            "price_gbp": float(price),
            "availability": availability,
            "rating": rating
        })

    time.sleep(1)

df = pd.DataFrame(products)

project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"
data_folder.mkdir(parents=True, exist_ok=True)

csv_file = data_folder / "scraped_products.csv"
df.to_csv(csv_file, index=False)

print("\nScraping completed!")
print("Total products:", len(df))
print("Saved CSV:", csv_file)
print("\nFirst five products:")
print(df.head())