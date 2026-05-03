import google.generativeai as genai
import json
import re
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
json_model = genai.GenerativeModel('gemini-2.0-flash', generation_config={"response_mime_type": "application/json"})

def generate_ultimate_json(topic, zone, competitor_data, seo_intelligence):
    """
    Takes deep competitor scrapes AND real-time Google traffic data 
    to engineer an article mathematically optimized for clicks.
    """
    
    prompt = f"""
    You are an elite SEO Growth Hacker and Copywriter. 
    Target Topic: {topic} | Target Audience: {zone}
    
    REAL-TIME GOOGLE TRAFFIC DATA (You MUST target these exactly): 
    {seo_intelligence}
    
    COMPETITOR DEEP CRAWL (Find their weak spots): 
    {competitor_data}
    
    YOUR MISSION: Write an article that steals our competitors' clicks. 
    1. The Meta Title must trigger intense curiosity (Click-Through-Rate optimization).
    2. The HTML Article MUST include an H2 section explicitly answering the 'People Also Ask' questions from the Google data above to win the Google Featured Snippet.
    3. Output STRICTLY valid JSON.

    {{
      "strategic_analysis": {{
        "competitor_traffic_gap": "Why competitors are losing clicks and how this article captures them."
      }},
      "seo_metadata": {{
        "url_slug": "short-keyword-rich-slug",
        "meta_title": "Curiosity-Driven SEO Title (Max 60 chars) - Must drive massive clicks",
        "meta_description": "Punchy description promising a specific answer (Max 160 chars)",
        "target_keywords": "15 high-volume keywords based on the live SEO data"
      }},
      "article_html": "A 1500+ word HTML article. You MUST use <h2> tags for the 'People Also Ask' questions. Structure for maximum readability (short paragraphs, bullet points). Output ONLY HTML body tags.",
      "linkedin_post": "A highly controversial or insight-led post designed to go viral. Start with a hook that shatters a common belief.",
      "instagram_caption": "Engaging hook with 10 optimized hashtags."
    }}
    """
    
    response = json_model.generate_content(prompt).text
    
    # Bulletproof JSON cleaner
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    else:
        raise ValueError("Agent Pipeline Error: Could not format final JSON.")
