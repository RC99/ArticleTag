import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_articles(url, total_articles=340):
    articles_list = []
    
    # Step 1: Send a GET request to the main page
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the main page. Status code: {response.status_code}")
        return articles_list

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all articles on the main page (first load)
    articles = soup.find_all(itemtype="http://schema.org/NewsArticle")

    # Extract up to the specified number of headlines and article bodies from the main page
    for article in articles:
        if len(articles_list) >= total_articles:
            break
        headline = article.find(itemprop="headline").get_text(strip=True)
        article_body = article.find(itemprop="articleBody").get_text(strip=True)
        
        # Store the extracted data
        articles_list.append({'headline': headline, 'body': article_body})

    # Step 2: Load more articles using the API
    page = 1
    while len(articles_list) < total_articles:
        page += 1
        # Construct the API URL for the next page
        api_url_with_page = f"https://inshorts.com/api/en/search/trending_topics/technology?page={page}&type=NEWS_CATEGORY"
        
        # Send a GET request to the API
        response = requests.get(api_url_with_page)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to load more articles from API. Status code: {response.status_code}")
            break
        
        # Parse the JSON response
        data = response.json()
        
        # Check if the 'data' key exists and contains 'suggested_news'
        if 'data' in data and 'suggested_news' in data['data']:
            for item in data['data']['suggested_news']:
                if len(articles_list) >= total_articles:
                    break
                # Ensure item is a dictionary and extract news_obj
                if isinstance(item, dict) and 'news_obj' in item:
                    news_obj = item['news_obj']
                    articles_list.append({
                        'headline': news_obj.get('title', 'No title found'),
                        'body': news_obj.get('content', 'No content found')
                    })
        else:
            print("No more articles found or unexpected response structure.")
            break

    return articles_list

# Example usage
url = "https://inshorts.com/en/read/technology"
#"https://inshorts.com/en/read/sports"  # Main page URL
scraped_articles = scrape_articles(url)

# Convert to a DataFrame
df = pd.DataFrame(scraped_articles)
df['Class'] = 'technology'

# Save to an Excel file
excel_file = 'scraped_articles_tech.xlsx'
df.to_excel(excel_file, index=False)

# Display the results
print(f"Scraped {len(scraped_articles)} articles and saved to '{excel_file}'.")

for i, article in enumerate(scraped_articles):
    print(f"Article {i + 1}:")
    print("Headline:", article['headline'])
    print("Article Body:", article['body'])
    print("-" * 40)
