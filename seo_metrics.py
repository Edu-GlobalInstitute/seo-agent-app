import requests
import streamlit as st

def get_realtime_click_data(topic):
    """
    Connects to SerpApi (Google Search API) to extract 'People Also Ask' 
    and 'Related Searches'. These are the exact phrases driving real-time clicks.
    """
    try:
        # You will need a free API key from serpapi.com
        api_key = st.secrets.get("SERPAPI_KEY", "")
        if not api_key:
            return "No SEO API Key provided. Relying on baseline AI knowledge.", []

        url = f"https://serpapi.com/search.json?q={topic}&hl=en&gl=us&api_key={api_key}"
        response = requests.get(url)
        data = response.json()

        seo_intelligence = "REAL-TIME GOOGLE SEARCH INTENT DATA:\n"
        high_click_questions = []

        # 1. Extract what people are actively asking (Massive CTR driver)
        if "related_questions" in data:
            seo_intelligence += "\nTarget these 'People Also Ask' questions for maximum clicks:\n"
            for q in data["related_questions"]:
                question = q.get("question")
                seo_intelligence += f"- {question}\n"
                high_click_questions.append(question)

        # 2. Extract trending related searches
        if "related_searches" in data:
            seo_intelligence += "\nInclude these high-volume related keywords:\n"
            for rs in data["related_searches"]:
                seo_intelligence += f"- {rs.get('query')}\n"

        return seo_intelligence, high_click_questions

    except Exception as e:
        print(f"SEO API Error: {e}")
        return "SEO Intelligence unavailable.", []
