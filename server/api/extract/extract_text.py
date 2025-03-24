from bs4 import BeautifulSoup
from fastapi import APIRouter
#import html2text
import requests
import re
import contractions # type: ignore
from nltk.corpus import stopwords # type: ignore
import nltk # type: ignore
nltk.download('stopwords')

router = APIRouter()

def fetch_html(url: str) -> str:
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def html_to_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup(['a', 'script', 'style', 'meta', 'link', 'noscript', 'nav', 'header', 'footer', 'figure']):
        tag.decompose()
    tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    article_text = ' '.join(tag.get_text(strip=True) for tag in tags)
    return article_text

def clean_text(article_text):
    text = article_text.lower()
    text = text.encode('ascii', 'ignore').decode()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\w\s.,!?-]', '', text) # Remove unwanted characters, leave punctuation for analysis
    text = text.strip()
    text = contractions.fix(text)
    stop_words = set(stopwords.words('english'))
    cleaned_text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
    return cleaned_text

@router.get("/extract_txt")
async def extract_from_url(url):
    try:
        raw_html = fetch_html(url)
        if not raw_html:
            return { "text": "Scraped failed" }
    
        base_text = html_to_text(raw_html)
        '''print("------------------------------\n")
        print(base_text)
        print("\n------------------------------")'''
        if not base_text:
            return { "text": "Website uses JavaScript rendering or Shadow DOM" }
        cleaned_text = clean_text(base_text)
        if not cleaned_text:
            return { "text": "Failed to clean text" }
        return { "text": cleaned_text }
    except Exception as e:
        return { "text": str(e) }
