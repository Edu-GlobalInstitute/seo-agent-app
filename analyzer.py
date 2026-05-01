import google.generativeai as genai
import json
import re
import streamlit as st

# Securely grab the API key and configure the model
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    'gemini-2.5-flash', 
    generation_config={"response_mime_type": "application/json"}
)

def generate_ultimate_json(topic, zone, competitor_data):
    """Feeds the research to Gemini, cleans the output, and returns valid JSON."""
    
    system_instruction = f"""
    You are an elite SEO Strategist and Competitor Analyst for 'Edu Global Institute'. 
    Target Topic: "{topic}" | Target Audience: "{zone}".
    Scraped Market Data: {competitor_data if competitor_data else "Rely on elite internal knowledge of the EdTech market."}
    
    CRITICAL MISSION: We are competing against major players like Art of Problem Solving (AoPS), Cheenta Academy, The Little Scientist, Thinkus Academy, and RSI. 
    Analyze the data and your internal knowledge of these institutions. What are they doing to gain traffic and trust that we are not? How are they structuring their curriculum pitching? 
    
    You MUST output your response as a strictly valid JSON object. Everything must be genuine, highly accurate, and student/parent focused.

    {{
      "strategic_analysis": {{
        "competitor_comparison": "Deep analysis comparing Edu Global to AoPS, Cheenta, RSI, etc. What are they doing better?",
        "our_missing_gap": "Actionable advice on what Edu Global must implement immediately to steal their market share."
      }},
      "seo_metadata": {{
        "url_slug": "example-optimized-url-slug-with-dashes",
        "meta_title": "Highly clickable SEO title (max 60 chars)",
        "meta_description": "Compelling description to drive clicks (max 160 chars)",
        "target_keywords": "comma, separated, list, of, 15, elite, seo, keywords"
      }},
      "article_html": "A 1500+ word, deeply organized article. OUTPUT STRICTLY IN HTML BODY TAGS (<h1>, <h2>, <h3>, <p>, <ul>, <li>, <strong>). No <html> or <body> tags. Must be superior to competitors. Use semantic LSI keywords.",
      "linkedin_post": "**Title (The Hook):** [Scroll-stopping line with emojis]\\n\\n**Description:** [Punchy paragraphs using bullet points comparing the elite nature of our program vs standard ones. Strong CTA.]\\n\\n**Keywords:** [10-15 comma-separated keywords/hashtags]",
      "instagram_caption": "[Engaging hook]\\n\\n[Relatable, elite academic value proposition]\\n\\n[CTA to link in bio]\\n\\n[10 highly relevant hashtags]"
    }}
    """

    # 1. Generate the raw text response
    response = model.generate_content(system_instruction)
    raw_text = response.text
    
    # 2. BULLETPROOF CLEANER: Extract ONLY the JSON part
    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    
    if match:
        clean_json_string = match.group(0)
        return json.loads(clean_json_string) # Safely load the cleaned string
    else:
        raise ValueError("AI Output Error: Could not locate a valid JSON object in the response.")
