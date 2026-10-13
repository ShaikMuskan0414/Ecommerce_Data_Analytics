import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
PAGES_TO_SCRAPE = 3
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EcommerceAnalytics/1.0)"
}


def scrape_page(session, page_number):
    """Scrape book listings from one catalogue page."""
    url = BASE_URL.format(page_number)
    print(f"Scraping page {page_number}: {url}")

    response = session.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for book in soup.select("article.product_pod"):
        try:
            title_element = book.select_one("h3 a")
            price_element = book.select_one(".price_color")
            availability_element = book.select_one(".availability")
            rating_element = book.select_one("p.star-rating")

            if not all([
                title_element,
                price_element,
                availability_element,
                rating_element,
            ]):
                print("Skipping a listing with missing fields.")
                continue

            title = title_element.get("title", "").strip()
            price_text = (
                price_element.get_text(strip=True)
                .replace("£", "")
                .replace("Â", "")
                .strip()
            )
            price = float(price_text)
            availability = availability_element.get_text(" ", strip=True)

            rating_classes = rating_element.get("class", [])
            rating = next(
                (item for item in rating_classes if item != "star-rating"),
                "Unknown",
            )

            if not title or price < 0:
                print("Skipping a listing with invalid data.")
                continue

            products.append({
                "product_name": title,
                "price_gbp": price,
                "availability": availability,
                "rating": rating.title(),
            })

        except (ValueError, TypeError) as error:
            print(f"Skipping invalid listing: {error}")

    return products


def main():
    """Scrape catalogue pages and save valid results."""
    all_products = []

    with requests.Session() as session:
        for page_number in range(1, PAGES_TO_SCRAPE + 1):
            try:
                all_products.extend(scrape_page(session, page_number))
            except requests.RequestException as error:
                print(f"Could not scrape page {page_number}: {error}")

            if page_number < PAGES_TO_SCRAPE:
                time.sleep(1)

    if not all_products:
        print("No products collected. Existing CSV was not changed.")
        return

    df = pd.DataFrame(all_products)
    df = df.drop_duplicates(subset=["product_name"])
    df = df.dropna(
        subset=["product_name", "price_gbp", "availability", "rating"]
    )
    df = df[df["product_name"].str.strip().ne("")]

    project_folder = Path(__file__).resolve().parent.parent
    data_folder = project_folder / "data"
    data_folder.mkdir(parents=True, exist_ok=True)

    csv_file = data_folder / "scraped_products.csv"
    df.to_csv(csv_file, index=False)

    print("\nScraping completed!")
    print(f"Total products saved: {len(df)}")
    print(f"Saved CSV: {csv_file}")
    print("\nFirst five products:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()
