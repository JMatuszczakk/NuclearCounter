import requests
from datetime import datetime, timedelta
import os
import csv

def get_ukraine_news(api_key):
    # Base URL for NewsAPI
    base_url = "https://newsapi.org/v2/everything"

    # Parameters for the API request
    params = {
        "apiKey": api_key,
        "q": "Ukraine",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,  # Maximum allowed by NewsAPI
        "from": (datetime.now() - timedelta(days=30)).isoformat()  # Last 30 days
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        news_data = response.json()

        if news_data["status"] == "ok":
            articles = news_data["articles"]
            print(f"Found {len(articles)} articles about Ukraine.")
            
            # Create a CSV file
            filename = f"ukraine_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                # Write the header
                csvwriter.writerow(['Title', 'Source', 'Published At', 'URL', 'Content'])
                
                # Write the data
                for article in articles:
                    csvwriter.writerow([
                        article['title'],
                        article['source']['name'],
                        article['publishedAt'],
                        article['url'],
                        article.get('content', 'N/A')  # Use 'N/A' if content is missing
                    ])
            
            print(f"Data has been saved to {filename}")
        else:
            print(f"Error: {news_data['status']}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    api_key = os.environ.get('NEWSAPI_KEY')
    if not api_key:
        print("Error: NEWSAPI_KEY environment variable not set")
    else:
        get_ukraine_news(api_key)