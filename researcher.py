from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

def execute_deep_research(topic, zone):
    """Scrapes general top competitors and gathers deep context."""
    links = []
    scraped_data = ""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # 1. Broad Search for the topic
    search_query = f"{topic} {zone}"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(search_query, max_results=5))
            for res in results:
                links.append(res['href'])
                
        # Scrape the text
        for url in links:
            try:
                response = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract paragraphs and headers for deeper context
                text = " ".join([p.text for p in soup.find_all(['p', 'h2', 'h3'])])
                if len(text) > 200:
                    scraped_data += f"\n--- Source: {url} ---\n{text[:1500]}\n"
            except:
                continue
    except Exception as e:
        print(f"Research warning: {e}")
        
    return links, scraped_data
