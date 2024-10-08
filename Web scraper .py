#This one scrapes the titles of articles from a news website

import requests
from bs4 import BeautifulSoup

url = 'https://example-news-website.com'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

for article in soup.find_all('h2', class_='article-title'):
    print(article.get_text())
