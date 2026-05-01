from firecrawl import FirecrawlApp
from duckduckgo_search import DDGS
import streamlit as st
import time

def execute_autonomous_research(topic, zone):
    """
    Autonomous Agent Workflow:
    Step 1: Automatically discover top competitors ranking for the keyword.
    Step 2: Deep crawl their exact website infrastructure and curriculum.
    """
    links = []
    scraped_data = ""
    # Creating a highly targeted search query
    search_query = f"{topic} {zone}"
    
    try:
        # --- STEP 1: AUTO-DISCOVERY ---
        # We use DuckDuckGo as a free, silent search engine to find the targets
        with DDGS() as ddgs:
            # Grab the top 3 ranking URLs
            results = list(ddgs.text(search_query, max_results=3))
            for res in results:
                links.append(res['href'])
                
        if not links:
            return [], "Search yielded no immediate competitors. Relying on AI internal data."

        # --- STEP 2: DEEP CRAWLING ---
        # Securely initialize Firecrawl using your API key from Streamlit Secrets
        app = FirecrawlApp(api_key=st.secrets["FIRECRAWL_API_KEY"])
        
        for url in links:
            try:
                # A 1-second delay prevents Firecrawl from being overwhelmed by rapid requests
                time.sleep(1) 
                
                # Execute the deep scrape, requesting markdown format (perfect for Gemini to read)
                scrape_result = app.scrape_url(
                    url, 
                    params={'formats': ['markdown']}
                )
                
                if 'markdown' in scrape_result:
                    raw_text = scrape_result['markdown']
                    # We grab the first 3000 characters of each site. 
                    # This captures their core strategy and syllabus without overloading the AI's brain.
                    scraped_data += f"\n--- DEEP CRAWL DATA FROM: {url} ---\n{raw_text[:3000]}\n"
            except Exception as e:
                # If one specific competitor's site blocks the crawler, skip it and move to the next
                print(f"Warning: Failed to deep crawl {url}: {e}")
                continue 
                
        return links, scraped_data

    except Exception as e:
        print(f"Critical Auto-Discovery Failure: {e}")
        # If the whole system fails, we gracefully return empty data so the AI falls back to its elite internal knowledge
        return [], ""
