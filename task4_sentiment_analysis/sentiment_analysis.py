
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pathlib import Path

# Locate project folders
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"
results_folder = project_folder / "results"

data_folder.mkdir(parents=True, exist_ok=True)
results_folder.mkdir(parents=True, exist_ok=True)

# Sample reviews for testing the workflow
# These are examples, not real customer feedback.
reviews = [
    {"review": "Excellent product, I really love it!"},
    {"review": "Very good quality and fast delivery."},
    {"review": "Amazing experience, highly recommended."},
    {"review": "The product is okay, nothing special."},
    {"review": "It is average and works as expected."},
    {"review": "The quality is poor and disappointing."},
    {"review": "Terrible product, I regret buying it."},
    {"review": "Delivery was slow and the product was damaged."},
    {"review": "Good value for money."},
    {"review": "Not worth the price."}
]

df = pd.DataFrame(reviews)

# Analyze sentiment
analyzer = SentimentIntensityAnalyzer()

def classify_sentiment(review):
    score = analyzer.polarity_scores(review)["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df["sentiment"] = df["review"].apply(classify_sentiment)

# Save results
output_csv = data_folder / "sample_sentiment_results.csv"
df.to_csv(output_csv, index=False)

print("===== SENTIMENT ANALYSIS RESULTS =====")
print(df.to_string(index=False))

print("\n===== SENTIMENT COUNTS =====")
sentiment_counts = df["sentiment"].value_counts()
print(sentiment_counts)

# Create chart
plt.figure(figsize=(7, 5))
sentiment_counts.plot(kind="bar", edgecolor="black")
plt.title("Sentiment Analysis of Sample Reviews")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)
plt.tight_layout()

chart_file = results_folder / "sentiment_analysis.png"
plt.savefig(chart_file)
plt.show()
plt.close()

print("\nSentiment analysis completed!")
print("CSV saved to:", output_csv)
print("Chart saved to:", chart_file)
print("Note: Results use sample reviews, not real customer feedback.")