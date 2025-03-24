import re
from typing import Dict, List, LiteralString

from bs4 import BeautifulSoup
import requests
from duckduckgo_search import DDGS # type: ignore
import contractions # type: ignore
from fastapi import FastAPI, APIRouter, HTTPException
from keybert import KeyBERT # type: ignore
from difflib import SequenceMatcher
from nltk.corpus import stopwords # type: ignore
import nltk # type: ignore
nltk.download('stopwords')

router = APIRouter()

# Static page fetching
def fetch_html(url: str) -> str:
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        #print(f"Error fetching URL {url}: {e}")
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

# Url Fetching
def obtain_keywords(search_query: str) -> str:
    '''
    response: str = client.models.generate_content(
        model = "gemini-2.0-flash",
        contents = [
            {"role": "system", "text": "You are an expert in content optimisation"},
            {"role": "user", "text": f"Optimize the following text for clarity and SEO: {search_query}"},
        ]
    )
    '''
    keyword_model = KeyBERT()
    keyword_list = keyword_model.extract_keywords(search_query, keyphrase_ngram_range = (1, 2), stop_words = 'english')
    response = " ".join(keyword[0] for keyword in keyword_list)
    return response

def is_similar(a, b, threshold=0.8):
    return SequenceMatcher(None, a, b).ratio() > threshold

def deduplicate_by_content(articles: List[Dict[str, str]], threshold=0.8) -> List[Dict[str, str]]:
    unique_articles = []
    for article in articles:
        if not any(
            is_similar(article.get('title', ''), a.get('title', ''), threshold) or
            is_similar(article.get('text', ''), a.get('text', ''), threshold)
            for a in unique_articles
        ):
            unique_articles.append(article)
    return unique_articles

def search_extract(search_keywords: str, search_region: str, search_moderation: str, search_time_frame: str):
    collected_articles = []
    max_attempts = 10
    attempt = 0
    
    while len(collected_articles) < 10 and attempt < max_attempts:
        attempt += 1
        results = DDGS().news(
            keywords=search_keywords,
            region=search_region,
            safesearch=search_moderation,
            timelimit=search_time_frame,
            max_results=30
        )
        if not results:
            if attempt == max_attempts:
                raise HTTPException(status_code=404, detail="No search results found.")
            continue
    #deduplicated_results = deduplicate_by_content(results)
    #return deduplicated_results
    for article in results:
        try:
            raw_html = fetch_html(article.get('url'))
            if not raw_html:
                continue
            base_text = html_to_text(raw_html)
            if not base_text:
                continue
            cleaned_text = clean_text(base_text)
            if not cleaned_text:
                continue
            article['text'] = cleaned_text
            collected_articles.append(article)
        except Exception as e:
            continue
    return collected_articles
        
@router.get("/search_ddg")
async def search_for_url(search_query: str, search_region: str, search_moderation: str, search_time: str):
    keywords = obtain_keywords(search_query)
    print(f"Extracted Keywords: {keywords}")

    search_results = list(search_extract(keywords, search_region, search_moderation, search_time))
    print(len(search_results))
    return {"results": search_results}
