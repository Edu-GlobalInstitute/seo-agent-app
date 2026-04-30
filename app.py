import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import json

st.set_page_config(page_title="Edu Global SEO Agent", page_icon="🚀", layout="wide")

# Securely grab the API key
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# Use the latest model and configure it to strictly output JSON
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    generation_config={"response_mime_type": "application/json"}
)

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

st.title("🚀 Edu Global: AI SEO Agent (API Edition)")
st.markdown("Generates deeply researched HTML articles, social posts, and pure JSON output.")

with st.form("agent_form"):
    topic = st.text_input("Target Topic (e.g., AP Calculus BC Exam Prep):")
    zone = st.text_input("Target Audience/Zone (e.g., International Students in UAE):")
    submit = st.form_submit_button("Generate JSON & Content")

if submit and topic and zone:
    st.info("Agent is attempting live web research...")
    links, competitor_data = research_and_scrape(f"{topic} {zone}")
    
    # Core instructions for the AI
    system_instruction = f"""
    You are an elite SEO expert and Social Media Manager for 'Edu Global Institute'. 
    Topic: "{topic}", Zone: "{zone}".
    Competitor Data (if any): {competitor_data if links else "Rely on elite internal knowledge."}
    
    You MUST output your response as a strictly valid JSON object using the exact keys below. 
    Do not add any markdown formatting (like ```json) outside the object. Just return the raw JSON object.

    {{
      "seo_metadata": {{
        "meta_title": "A highly clickable SEO title (under 60 characters)",
        "meta_description": "A compelling meta description to drive clicks (under 160 characters)",
        "target_keywords": "comma, separated, list, of, 10, highly, relevant, seo, keywords"
      }},
      "article_html": "A deeply organized, comprehensive, and amazing article. Use strictly HTML body tags (<h1>, <h2>, <h3>, <p>, <ul>, <li>, <strong>, <em>). Do not include <html>, <head>, or <body> tags. Structure it to be the absolute best guide on the internet.",
      "linkedin_post": "**Title (The Hook):** [Scroll-stopping line with emojis]\\n\\n**Description:** [3-4 punchy paragraphs using bullet points. Address pain points. Strong CTA for Edu Global Institute.]\\n\\n**Hashtags:** [#EduGlobal, #StudyAbroad, etc]",
      "instagram_caption": "Engaging, student-focused caption.\\n\\n[CTA]\\n\\n[Relevant Hashtags]"
    }}
    """

    st.info("Drafting perfect JSON content...")
    try:
        # Generate the content
        response = model.generate_content(system_instruction)
        
        # Parse the JSON
        data = json.loads(response.text)
        
        st.success("✅ Generation Complete!")
        st.markdown("---")
        
        # Create beautiful UI Tabs for the user to view the data
        tab1, tab2, tab3, tab4 = st.tabs(["📄 HTML Article", "📱 Social Media", "🔍 SEO Metadata", "⚙️ Raw JSON"])
        
        with tab1:
            st.subheader("Deeply Organized HTML Article")
            st.code(data["article_html"], language="html")
            with st.expander("Preview Article Visually"):
                st.markdown(data["article_html"], unsafe_allow_html=True)
                
        with tab2:
            st.subheader("LinkedIn Post")
            st.markdown(data["linkedin_post"])
            st.divider()
            st.subheader("Instagram Caption")
            st.markdown(data["instagram_caption"])
            
        with tab3:
            st.subheader("Website Metadata")
            st.write(f"**Meta Title:** {data['seo_metadata']['meta_title']}")
            st.write(f"**Meta Description:** {data['seo_metadata']['meta_description']}")
            st.write(f"**Keywords:** {data['seo_metadata']['target_keywords']}")
            
        with tab4:
            st.subheader("System-Ready JSON Data")
            st.json(data)

    except json.JSONDecodeError:
        st.error("The AI failed to format the output as perfect JSON. Please try again.")
    except Exception as e:
        st.error(f"Error: {e}")
