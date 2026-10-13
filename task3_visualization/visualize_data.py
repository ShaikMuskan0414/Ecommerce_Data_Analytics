from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_FOLDER / "data" / "scraped_products.csv"
OUTPUT_FOLDER = PROJECT_FOLDER / "results"

RATING_ORDER = ["One", "Two", "Three", "Four", "Five"]


def main():
    if not DATA_FILE.exists():
        print(f"Dataset not found: {DATA_FILE}")
        return

    df = pd.read_csv(DATA_FILE)

    required_columns = ["product_name", "price_gbp", "availability", "rating"]
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        print("Missing columns:", missing_columns)
        return

    df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")
    df = df.dropna(subset=required_columns)
    df = df[df["price_gbp"] >= 0]

    if df.empty:
        print("No valid data available for visualization.")
        return

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    # Chart 1: Distribution of book prices
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.hist(df["price_gbp"], bins=10, edgecolor="black")
    ax.axvline(
        df["price_gbp"].mean(),
        linestyle="--",
        linewidth=2,
        label=f"Mean: £{df['price_gbp'].mean():.2f}",
    )
    ax.set_title("Distribution of Book Prices", fontsize=14, pad=12)
    ax.set_xlabel("Listed price (£)")
    ax.set_ylabel("Number of books")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_FOLDER / "price_distribution.png", dpi=300)
    plt.close(fig)

    # Chart 2: Number of books by rating
    rating_counts = (
        df["rating"].str.title().value_counts()
        .reindex(RATING_ORDER, fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(rating_counts.index, rating_counts.values, edgecolor="black")
    ax.bar_label(bars, padding=3)
    ax.set_title("Number of Books by Rating", fontsize=14, pad=12)
    ax.set_xlabel("Star rating")
    ax.set_ylabel("Number of books")
    ax.set_ylim(0, max(rating_counts.max() * 1.2, 1))
    fig.tight_layout()
    fig.savefig(OUTPUT_FOLDER / "products_by_rating.png", dpi=300)
    plt.close(fig)

    # Chart 3: Five most expensive books
    top_five = df.nlargest(5, "price_gbp").sort_values("price_gbp")

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top_five["product_name"], top_five["price_gbp"],
                   edgecolor="black")
    ax.bar_label(bars, fmt="£%.2f", padding=4)
    ax.set_title("Five Most Expensive Books", fontsize=14, pad=12)
    ax.set_xlabel("Listed price (£)")
    ax.set_ylabel("Book title")
    ax.set_xlim(0, top_five["price_gbp"].max() * 1.2)
    fig.tight_layout()
    fig.savefig(OUTPUT_FOLDER / "top_five_expensive.png", dpi=300)
    plt.close(fig)

    # Chart 4: Availability
    availability_counts = df["availability"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(availability_counts.index, availability_counts.values,
                  edgecolor="black")
    ax.bar_label(bars, padding=3)
    ax.set_title("Book Availability in the Catalogue", fontsize=14, pad=12)
    ax.set_xlabel("Availability status")
    ax.set_ylabel("Number of books")
    ax.set_ylim(0, max(availability_counts.max() * 1.2, 1))
    fig.tight_layout()
    fig.savefig(OUTPUT_FOLDER / "product_availability.png", dpi=300)
    plt.close(fig)

    # Chart 5: Average listed price by rating
    average_price = (
        df.assign(rating=df["rating"].str.title())
        .groupby("rating")["price_gbp"]
        .mean()
        .reindex(RATING_ORDER)
        .dropna()
    )

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(average_price.index, average_price.values,
                  edgecolor="black")
    ax.bar_label(bars, fmt="£%.2f", padding=3)
    ax.set_title("Average Listed Price by Star Rating", fontsize=14, pad=12)
    ax.set_xlabel("Star rating")
    ax.set_ylabel("Average listed price (£)")
    ax.set_ylim(0, average_price.max() * 1.2)
    fig.tight_layout()
    fig.savefig(OUTPUT_FOLDER / "average_price_by_rating.png", dpi=300)
    plt.close(fig)

    print("Visualization completed successfully!")
    print(f"Books analyzed: {len(df)}")
    print(f"Charts saved in: {OUTPUT_FOLDER}")
    print("Created 5 high-resolution charts:")
    for filename in [
        "price_distribution.png",
        "products_by_rating.png",
        "top_five_expensive.png",
        "product_availability.png",
        "average_price_by_rating.png",
    ]:
        print(f"- {filename}")


if __name__ == "__main__":
    main()
