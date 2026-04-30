import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import json

st.set_page_config(page_title="Edu Global SEO Agent PRO", page_icon="🏆", layout="wide")

# Securely grab the API key
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# Pointing to the most advanced available API endpoint for this generation
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
            # Pulling slightly more results for deeper research
            results = list(ddgs.text(query, max_results=4))
            for res in results:
                links.append(res['href'])
                
        for url in links:
            try:
                response = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = " ".join([p.text for p in soup.find_all('p')])
                if len(text) > 150:
                    scraped_data += f"\nSource: {url}\n{text[:1200]}\n"
            except:
                continue
    except Exception:
        pass
        
    return links, scraped_data

st.title("🏆 Edu Global: Elite SEO & Content Agent")
st.markdown("Generates hyper-optimized, student-focused content formatted in pure JSON.")

with st.form("agent_form"):
    topic = st.text_input("Target Topic (e.g., How to Crack the Math Olympiad):")
    zone = st.text_input("Target Audience/Zone (e.g., High School Students in India):")
    submit = st.form_submit_button("Generate Final Content")

if submit and topic and zone:
    st.info("Executing deep competitor research...")
    links, competitor_data = research_and_scrape(f"{topic} {zone}")
    
    # THE FINALIZED, PRO-LEVEL SYSTEM INSTRUCTION
    system_instruction = f"""
    You are an elite, top-1% SEO Expert and Student Content Strategist for 'Edu Global Institute'. 
    Topic: "{topic}", Target Audience: "{zone}".
    Competitor Data: {competitor_data if links else "Rely on elite internal knowledge."}
    
    CRITICAL INSTRUCTION: Your tone must be "Student-First". Do not sound like a boring corporate brochure. Sound inspiring, clear, authoritative, and deeply understanding of a student's academic stress and ambitions. Use simple, powerful language.

    You MUST output your response as a strictly valid JSON object using the exact keys below. 
    
    {{
      "seo_metadata": {{
        "meta_title": "Highly clickable SEO title, max 60 chars. Must include primary keyword.",
        "meta_description": "Compelling description to drive clicks, max 160 chars. Must include secondary keywords.",
        "target_keywords": "comma, separated, list, of, 15, highly, relevant, short, and, long, tail, seo, keywords"
      }},
      "article_html": "A deeply organized, 1000+ word article designed to rank #1. OUTPUT STRICTLY IN HTML BODY TAGS (<h1>, <h2>, <h3>, <p>, <ul>, <li>, <strong>, <em>). Do not use <html>, <head>, or <body> tags. Structure: H1 Title, engaging hook, highly readable short paragraphs, bulleted lists for scannability, semantic LSI keywords integrated naturally, and a strong, inspiring conclusion driving students to Edu Global Institute.",
      "linkedin_post": "**Title (The Hook):** [Scroll-stopping line with emojis]\\n\\n**Description:** [3-4 punchy paragraphs using bullet points. Speak to the ambition of the students or the parents. End with a strong CTA for Edu Global Institute.]\\n\\n**Keywords:** [10-15 comma-separated keywords/hashtags]",
      "instagram_caption": "[Engaging hook for students]\\n\\n[Relatable body copy that builds hype or offers a quick tip]\\n\\n[CTA to link in bio]\\n\\n[10 highly relevant hashtags]"
    }}
    """

    st.info("Engineering student-focused, SEO-perfect JSON data...")
    try:
        response = model.generate_content(system_instruction)
        data = json.loads(response.text)
        
        st.success("✅ Content Engineered Successfully!")
        st.markdown("---")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📄 HTML Article", "📱 Social Media", "🔍 SEO Metadata", "⚙️ Raw JSON"])
        
        with tab1:
            st.subheader("Student-Focused HTML Article")
            st.code(data["article_html"], language="html")
            with st.expander("Visual Preview"):
                st.markdown(data["article_html"], unsafe_allow_html=True)
                
        with tab2:
            st.subheader("LinkedIn Post")
            st.markdown(data["linkedin_post"])
            st.divider()
            st.subheader("Instagram Caption")
            st.markdown(data["instagram_caption"])
            
        with tab3:
            st.subheader("Optimized Metadata")
            st.write(f"**Meta Title:** {data['seo_metadata']['meta_title']}")
            st.write(f"**Meta Description:** {data['seo_metadata']['meta_description']}")
            st.write(f"**Keywords:** {data['seo_metadata']['target_keywords']}")
            
        with tab4:
            st.subheader("API-Ready JSON")
            st.json(data)
            
            # Simple download button for the JSON data
            json_string = json.dumps(data, indent=2)
            st.download_button(
                label="Download Full JSON",
                file_name="edu_global_content.json",
                mime="application/json",
                data=json_string
            )

    except json.JSONDecodeError:
        st.error("Data processing error. The AI failed to structure the JSON perfectly. Please re-run.")
    except Exception as e:
        st.error(f"System Error: {e}")
