import google.generativeai as genai
import json
import re
import time
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# UPGRADED: Switched to gemini-2.5-flash for a fresh quota and smarter outputs
json_model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"})

def generate_ultimate_json(topic, zone, competitor_data, seo_intelligence):
    """
    Takes deep competitor scrapes AND real-time Google traffic data 
    to engineer an article mathematically optimized for clicks.
    Includes Auto-Retry for API Rate Limits.
    """
    
    prompt = f"""
    SYSTEM OVERRIDE: You are a strict, algorithmic data parser and SEO strategist. You MUST NOT invent generic marketing fluff. You MUST extract and inject the provided LIVE GOOGLE SEARCH DATA into all required fields.
    
    Target Topic: {topic}
    Target Audience: {zone}
    
    >>> START LIVE GOOGLE SEARCH DATA (MANDATORY TO USE THESE EXACT PHRASES) <<<
    {seo_intelligence}
    >>> END LIVE GOOGLE SEARCH DATA <<<
    
    >>> START COMPETITOR DATA <<<
    {competitor_data}
    >>> END COMPETITOR DATA <<<
    
    CRITICAL INSTRUCTIONS FOR JSON OUTPUT:
    1. seo_metadata.url_slug: Extract the #1 highest volume keyword from the LIVE GOOGLE SEARCH DATA. Replace spaces with hyphens. Do not invent this.
    2. seo_metadata.meta_title: Start the title with the EXACT primary keyword from the live data (Max 60 chars).
    3. seo_metadata.meta_description: MUST explicitly answer one of the 'People Also Ask' questions.
    4. seo_metadata.target_keywords: Output a single string containing EXACTLY 15 keywords, separated by commas. ALL 15 MUST come directly from the LIVE GOOGLE SEARCH DATA.
    5. article_html: Write a 1500+ word HTML article. You MUST use <h2> tags. Every <h2> tag MUST be an exact 'People Also Ask' question from the live data.
    6. linkedin_post: Write the post. At the very bottom, append EXACTLY 15 hashtags (#) created directly from the live keywords.
    7. instagram_caption: Write the caption. At the very bottom, append EXACTLY 20 hashtags (#) created directly from the live keywords.

    Output ONLY a valid JSON object. No markdown wrapping. No explanations. Just the JSON.

    {{
      "strategic_analysis": {{
        "competitor_traffic_gap": "Actionable breakdown of how this steals traffic based on competitor weaknesses."
      }},
      "seo_metadata": {{
        "url_slug": "exact-live-keyword-slug",
        "meta_title": "Exact Live Keyword | High CTR Title",
        "meta_description": "Answers a specific People Also Ask question directly to win the snippet.",
        "target_keywords": "live keyword 1, live keyword 2, live keyword 3, live keyword 4, live keyword 5, live keyword 6, live keyword 7, live keyword 8, live keyword 9, live keyword 10, live keyword 11, live keyword 12, live keyword 13, live keyword 14, live keyword 15"
      }},
      "article_html": "<h1>Main Title</h1>\\n<p>intro...</p>\\n<h2>[Exact PAA Question 1]</h2>\\n<p>...</p>\\n<h2>[Exact PAA Question 2]</h2>\\n<p>...</p>",
      "linkedin_post": "Viral Hook.\\n\\nInsight.\\n\\nSolution.\\n\\nHashtags: #LiveKW1 #LiveKW2 #LiveKW3 #LiveKW4 #LiveKW5 #LiveKW6 #LiveKW7 #LiveKW8 #LiveKW9 #LiveKW10 #LiveKW11 #LiveKW12 #LiveKW13 #LiveKW14 #LiveKW15",
      "instagram_caption": "Viral Hook.\\n\\nValue.\\n\\nCTA.\\n\\nHashtags: #LiveKW1 #LiveKW2 #LiveKW3 #LiveKW4 #LiveKW5 #LiveKW6 #LiveKW7 #LiveKW8 #LiveKW9 #LiveKW10 #LiveKW11 #LiveKW12 #LiveKW13 #LiveKW14 #LiveKW15 #LiveKW16 #LiveKW17 #LiveKW18 #LiveKW19 #LiveKW20"
    }}
    """
    
    # PERFECTED: Auto-Retry System (Exponential Backoff)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = json_model.generate_content(prompt).text
            
            # Bulletproof JSON cleaner
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                raise ValueError("Agent Pipeline Error: Could not format final JSON.")
                
        except Exception as e:
            error_msg = str(e)
            # If we hit a Google Quota limit, don't crash. Wait and try again.
            if "429" in error_msg or "Quota" in error_msg:
                if attempt < max_retries - 1:
                    sleep_time = (attempt + 1) * 5  # Will wait 5s, then 10s
                    st.toast(f"Google Speed Limit hit. Auto-retrying in {sleep_time} seconds...", icon="⏳")
                    time.sleep(sleep_time)
                    continue
            # If it's a different error or we used all retries, throw the error to the UI
            raise e
