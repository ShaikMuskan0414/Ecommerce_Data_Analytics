# E-Commerce Data Analytics

## Project Overview
This project demonstrates an e-commerce data analysis workflow using Python. It covers web scraping, exploratory data analysis, data visualization, and sentiment analysis.

## Technologies Used
- Python
- Requests
- BeautifulSoup
- Pandas
- Matplotlib
- Seaborn
- VADER Sentiment Analysis

## Task 1: Web Scraping
Collected 60 book listings from Books to Scrape, a practice website. Extracted product names, prices in GBP, availability, and ratings.

Output: `data/scraped_products.csv`

## Task 2: Exploratory Data Analysis
Analyzed the scraped dataset to examine missing values, duplicate records, price statistics, ratings, availability, and the most and least expensive products.

Key findings:
- Total products analyzed: 60
- Average listed price: approximately £35.00
- Missing values: 0
- Duplicate rows: 0
- All 60 listings were marked in stock.

## Task 3: Data Visualization
Created the following charts:
- Product price distribution
- Number of products by rating
- Five most expensive books
- Product availability

The chart images are stored in the `results/` folder.

## Task 4: Sentiment Analysis
Used VADER sentiment analysis to classify ten sample review sentences as positive, negative, or neutral.

Outputs:
- `data/sample_sentiment_results.csv`
- `results/sentiment_analysis.png`

Note: These are sample review sentences, not real customer reviews.

## Project Structure
- `task1_web_scraping/` - Web scraping code
- `task2_eda/` - Exploratory data analysis
- `task3_visualization/` - Data visualization code
- `task4_sentiment_analysis/` - Sentiment analysis code
- `data/` - CSV datasets
- `results/` - Generated charts
- `requirements.txt` - Python dependencies

## How to Run
1. Install Python 3.
2. Open Terminal in the project directory.
3. Create a virtual environment:

   `python3 -m venv venv`

4. Activate it:

   `source venv/bin/activate`

5. Install dependencies:

   `python -m pip install -r requirements.txt`

6. Run the scripts from their respective task folders.

## Limitations
The scraped dataset contains book listings rather than real e-commerce sales transactions. The analysis therefore does not measure actual revenue or purchasing behavior. Sentiment analysis uses sample sentences and may misclassify ambiguous text.

## Future Improvements
- Analyze a real, documented e-commerce sales dataset.
- Use appropriately sourced customer reviews.
- Expand the visualizations and business insights.
- Evaluate and improve sentiment classification.
