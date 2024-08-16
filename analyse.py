import csv
import os
import requests
import json

def read_news(file_path):
    news_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            news = {
                'title': row[0],
                'source': row[1],
                'published_at': row[2],
                'url': row[3],
                'content': row[4]
            }
            news_list.append(news)
    return news_list

def analyze_news(news_list):
    api_url = "https://api.openai.com/v1/chat/completions"  # Replace with actual GPT API endpoint
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Concatenate all news content into one string
    combined_content = "\n\n".join([news['content'] for news in news_list])
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": 'Polymarket shows 7 percent chance of nuclear weapons detonation in 2024. Analyze the following news articles and predict potential nuclear threats. Answer only in DD/MM/YYYY with predicted time of start of nuclear conflict. today is 16/08/2024 DD/MM/YYYY. Before the Kursk incursion my prediction was 2 years. It is your job to make a new prediction It is imperative that you give the predicted date. Answer in json like Prediction: {"date": "01/10/2025"} f News follow:\n\n' + str(combined_content)}
        ],
        "max_tokens": 1500
    }
    
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        prediction = response.json()
        print(f"Prediction: {prediction['choices'][0]['message']['content']}\n")
        try:
            
            #the response from gpt looks loke this "Prediction: Prediction: {"date": "01/09/2026"}" so we need to parse it
            prediction = prediction['choices'][0]['message']['content'].split("Prediction: ")[1]
            prediction = json.loads(prediction)


            print(combined_content)
            print("__________________________")
            print("Based on the news articles, the following is predicted:")

            print(f"Predicted date: {prediction['date']}")

        except:
            print("Error: Could not parse prediction.")
            
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    news_file_path = 'news.csv'  # Path to your CSV file
    news_data = read_news(news_file_path)
    analyze_news(news_data)