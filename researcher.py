from firecrawl import FirecrawlApp
import streamlit as st
import time

def execute_deep_research(topic, zone, competitor_url=None):
    """
    Executes an enterprise-grade deep crawl of a specific competitor 
    or relies on AI knowledge if no URL is provided.
    """
    scraped_data = ""
    
    # We will pass the competitor URL from the Streamlit UI
    if competitor_url:
        try:
            # Securely grab the Firecrawl API key from Streamlit secrets
            app = FirecrawlApp(api_key=st.secrets["FIRECRAWL_API_KEY"])
            
            # Initiate the deep scrape
            scrape_result = app.scrape_url(
                competitor_url, 
                params={'formats': ['markdown']} # Markdown is perfect for Gemini to read
            )
            
            # Extract the raw, deep content
            if 'markdown' in scrape_result:
                raw_text = scrape_result['markdown']
                # Limit to first 4000 characters to keep it highly relevant
                scraped_data = f"\n--- DEEP CRAWL DATA FROM {competitor_url} ---\n{raw_text[:4000]}\n"
                return [competitor_url], scraped_data
            else:
                raise Exception("Could not extract markdown data.")
                
        except Exception as e:
            print(f"Deep Crawl Failed: {e}")
            return [], ""
    else:
        # If no competitor URL is provided, return empty to trigger the AI's internal knowledge
        return [], ""
