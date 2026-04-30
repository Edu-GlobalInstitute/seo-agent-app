import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Edu Global SEO Agent", page_icon="🚀", layout="wide")

# Securely grab the API key
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def research_and_scrape(query):
    links = []
    scraped_data = ""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            for res in results:
                links.append(res['href'])
                
        for url in links:
            try:
                response = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = " ".join([p.text for p in soup.find_all('p')])
                if len(text) > 100:
                    scraped_data += f"\nSource: {url}\n{text[:1000]}\n"
            except:
                continue
    except Exception:
        pass
        
    return links, scraped_data

st.title("🚀 Edu Global: AI SEO Agent")
st.markdown("Enter a topic to generate highly optimized, high-converting content.")

with st.form("agent_form"):
    topic = st.text_input("Target Topic (e.g., International Math Olympiad Prep):")
    zone = st.text_input("Target Audience/Zone (e.g., High School Students in India):")
    submit = st.form_submit_button("Generate Perfect Content")

if submit and topic and zone:
    st.info("Agent is attempting live web research...")
    links, competitor_data = research_and_scrape(f"{topic} {zone}")
    
    if links and competitor_data:
        st.success("Live Research Complete! Found top competitor data.")
        prompt = f"""
        You are an elite SEO expert and elite Social Media Manager for 'Edu Global Institute'. Topic: "{topic}", Zone: "{zone}".
        Here is the text scraped from live top competitors: {competitor_data}
        
        Analyze this data, find keyword gaps, and output exactly these three things:
        
        1. PERFECT SEO ARTICLE: Write a highly optimized article. OUTPUT THIS STRICTLY IN HTML FORMAT. Use ONLY body tags (<h1>, <h2>, <p>, <ul>, <li>, <strong>). Do NOT include <html>, <head>, or <body> tags. Wrap the HTML inside a code block so it is easy to copy.
        
        2. PERFECT LINKEDIN POST: Create a highly engaging, professional LinkedIn post ready to publish. Format it EXACTLY like this:
        **Title (The Hook):** [Write a scroll-stopping, attention-grabbing opening line with 1-2 emojis]
        **Description (The Body):** [Write an engaging, value-driven post in 3-4 short, punchy paragraphs. Use bullet points for readability. Speak directly to the pain points of the target audience. End with a strong Call to Action to enroll or contact Edu Global Institute.]
        **Keywords:** [Provide 10-15 highly relevant SEO keywords and hashtags, separated ONLY by commas, e.g., #EduGlobal, StudyAbroad, OlympiadPrep]
        
        3. INSTAGRAM CAPTION: Engaging caption with hashtags. Output in plain text.
        """
    else:
        st.warning("⚠️ Live search blocked by cloud security. Falling back to Elite AI Knowledge Base...")
        prompt = f"""
        You are an elite SEO expert and elite Social Media Manager for the 'Edu Global Institute'. 
        Target Topic: "{topic}"
        Target Audience/Zone: "{zone}"
        
        Using your vast internal knowledge of current SEO trends, output exactly these three things:
        
        1. PERFECT SEO ARTICLE: Write a highly optimized article. OUTPUT THIS STRICTLY IN HTML FORMAT. Use ONLY body tags (<h1>, <h2>, <p>, <ul>, <li>, <strong>). Do NOT include <html>, <head>, or <body> tags. Wrap the HTML inside a code block so it is easy to copy.
        
        2. PERFECT LINKEDIN POST: Create a highly engaging, professional LinkedIn post ready to publish. Format it EXACTLY like this:
        **Title (The Hook):** [Write a scroll-stopping, attention-grabbing opening line with 1-2 emojis]
        **Description (The Body):** [Write an engaging, value-driven post in 3-4 short, punchy paragraphs. Use bullet points for readability. Speak directly to the pain points of the target audience. End with a strong Call to Action to enroll or contact Edu Global Institute.]
        **Keywords:** [Provide 10-15 highly relevant SEO keywords and hashtags, separated ONLY by commas, e.g., #EduGlobal, StudyAbroad, OlympiadPrep]
        
        3. INSTAGRAM CAPTION: Engaging caption targeting the demographic with hashtags. Output in plain text.
        """

    st.info("Drafting perfect content...")
    try:
        response = model.generate_content(prompt)
        st.markdown("---")
        st.subheader("✅ Your Perfect Outcome")
        st.markdown(response.text)
    except Exception as e:
        st.error(f"AI Generation Error: {e}")
