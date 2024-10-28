import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract articles from a given page
def extract_articles(page_url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(page_url)    
    
    # Check for a successful response
    if response.status_code != 200:
        print(f"Failed to retrieve page: {page_url} (Status Code: {response.status_code})")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    
    # Find all article elements based on the updated structure
    for item in soup.find_all('div', class_='o-teaser__content'):
        title_tag = item.find('a', class_='js-teaser-heading-link')
        data_tag = item.find('p', class_='o-teaser__standfirst')

        # Check if title and data are found
        if title_tag and data_tag:
            title = title_tag.text.strip()
            data = data_tag.text.strip()
            articles.append({'Title': title, 'Data': data})
        else:
            print("Missing title or data for item:", item)

    return articles

# Main function to handle pagination
def scrape_all_articles(base_url, total_pages):
    all_articles = []
    
    for page_num in range(1, total_pages + 1):
        print(f"Scraping page {page_num}...")
        page_url = f"{base_url}?page={page_num}"  # Update this according to the pagination structure
        articles = extract_articles(page_url)
        
        if not articles:  # Print the response text if no articles were found
            print(f"No articles found on page: {page_url}")
        
        all_articles.extend(articles)
        
        if len(all_articles) >= 350:  # Stop if we have collected enough articles
            break
            
    return all_articles[:350]  # Return only the first 350 articles

# Base URL for the articles (ensure it is correct)
base_url = 'https://www.ft.com/markets'  # Replace with the actual URL
total_pages = 50  # Set the number of pages you want to scrape

# Execute scraping
all_articles = scrape_all_articles(base_url, total_pages)

# Convert to DataFrame
df = pd.DataFrame(all_articles)

# Display the first few articles
print(df.tail())

# Save to Excel if desired
df.to_excel('extracted_articles.xlsx', index=False)
print("Articles saved to 'extracted_articles.xlsx'")
