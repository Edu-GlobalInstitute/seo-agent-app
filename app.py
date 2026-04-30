import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Pro SEO Agent", page_icon="🚀", layout="wide")

# Securely grab the API key from Streamlit's secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def research_and_scrape(query):
    links = []
    scraped_data = ""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))
            for res in results:
                links.append(res['href'])
                
        for url in links:
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = " ".join([p.text for p in soup.find_all('p')])
                scraped_data += f"\nSource: {url}\n{text[:1500]}\n"
            except:
                continue
    except Exception as e:
        st.error(f"Search error: {e}")
        
    return links, scraped_data

st.title("🚀 Pro AI SEO Agent")
st.markdown("Enter a topic to conduct deep internet research and generate optimized content.")

with st.form("agent_form"):
    topic = st.text_input("Target Topic (e.g., Data Science Courses):")
    zone = st.text_input("Target Audience/Zone (e.g., Professionals in London):")
    submit = st.form_submit_button("Run Deep Research")

if submit and topic and zone:
    st.info("Agent is scouring the web for top-performing competitors...")
    links, competitor_data = research_and_scrape(f"{topic} {zone}")
    
    if links:
        st.success("Research Complete! Found top competitor data.")
        st.write("**Sources Analyzed:**")
        for link in links:
            st.write(f"- {link}")
            
        st.info("Drafting perfect content based on keyword gaps...")
        prompt = f"""
        You are an elite SEO expert. Topic: "{topic}", Zone: "{zone}".
        Here is the text scraped from top competitors: {competitor_data}
        
        Analyze this data, find keyword gaps, and output:
        1. PERFECT SEO ARTICLE: Highly optimized, H1/H2/H3 tags.
        2. LINKEDIN POST: Title, Description, Keywords (comma-separated).
        3. INSTAGRAM CAPTION: Engaging caption with hashtags.
        """
        response = model.generate_content(prompt)
        
        st.markdown("---")
        st.subheader("✅ Your Perfect Outcome")
        st.markdown(response.text)
    else:
        st.error("Could not fetch competitor data. Please try another topic.")
