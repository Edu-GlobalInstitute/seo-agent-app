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
    SYSTEM OVERRIDE: You are an Elite Content Synthesizer, Skyscraper SEO Strategist, and Viral Copywriter. 
    You do not invent fluff. You analyze top-performing competitor articles and real-time search data to create an outcome that is mathematically 10x better than anything currently ranking.
    
    Target Topic: {topic}
    Target Audience: {zone}
    
    >>> START LIVE GOOGLE SEARCH DATA (MANDATORY SEO QUERIES) <<<
    {seo_intelligence}
    >>> END LIVE GOOGLE SEARCH DATA <<<
    
    >>> START TOP-PERFORMING COMPETITOR ARTICLES (ANALYZE & OUTPERFORM) <<<
    {competitor_data}
    >>> END COMPETITOR ARTICLES <<<
    
    CRITICAL 'SKYSCRAPER' INSTRUCTIONS FOR JSON OUTPUT:
    1. seo_metadata.url_slug: Extract the #1 highest-volume SHORT-TAIL keyword from the LIVE GOOGLE SEARCH DATA. Replace spaces with hyphens.
    2. seo_metadata.meta_title: Must be highly clickable and start with the exact primary keyword (Max 60 chars).
    3. seo_metadata.target_keywords: Output exactly 15 comma-separated keywords. You MUST include a strategic mix of broad SHORT-TAIL keywords and highly specific LONG-TAIL keywords extracted directly from the live data.
    4. article_html: This is your masterpiece. Read the competitor articles provided, identify their gaps, and write a 1500+ word HTML article that is significantly more comprehensive, authoritative, and readable. 
       - You MUST use <h2> tags for the exact 'People Also Ask' LONG-TAIL questions.
       - Use <h3> tags, bullet points, and bold text for readability.
       - Do not just summarize; provide unique, elite value for the {zone}.
    5. linkedin_post: Write a viral-engineered post that outperforms standard industry updates. 
       - Start with a pattern-interrupt hook.
       - Provide a counter-intuitive insight derived from your research.
       - At the bottom, append EXACTLY 15 hashtags based on the live keywords.
    6. instagram_caption: High-energy, value-driven caption ending with a strong CTA and EXACTLY 20 hashtags.

    Output ONLY a valid JSON object. No markdown wrapping. Just the JSON.

    {{
      "strategic_analysis": {{
        "competitor_traffic_gap": "Actionable breakdown of exactly what the top-performing competitor articles missed, and how our new Skyscraper article fills that gap to steal their readers."
      }},
      "seo_metadata": {{
        "url_slug": "short-tail-keyword-slug",
        "meta_title": "Primary Keyword | High CTR Title",
        "meta_description": "Answers a specific long-tail People Also Ask question directly to win the snippet.",
        "target_keywords": "short tail kw 1, short tail kw 2, long tail query 1, long tail query 2... (Exactly 15)"
      }},
      "article_html": "<h1>Main Title</h1>\\n<p>Elite intro capturing attention...</p>\\n<h2>[Exact Long-Tail PAA Question 1]</h2>\\n<p>Comprehensive answer that is 10x better than competitors...</p>\\n<h3>Actionable Step</h3>\\n<ul><li>...</li></ul>\\n<h2>[Exact Long-Tail PAA Question 2]</h2>\\n<p>...</p>",
      "linkedin_post": "Viral Hook.\\n\\nDeep Industry Insight.\\n\\nThe Superior Solution.\\n\\nHashtags: #LiveKW1 #LiveKW2 #LiveKW3 #LiveKW4 #LiveKW5 #LiveKW6 #LiveKW7 #LiveKW8 #LiveKW9 #LiveKW10 #LiveKW11 #LiveKW12 #LiveKW13 #LiveKW14 #LiveKW15",
      "instagram_caption": "Viral Hook.\\n\\nElite Value.\\n\\nCTA.\\n\\nHashtags: #LiveKW1 #LiveKW2 #LiveKW3 #LiveKW4 #LiveKW5 #LiveKW6 #LiveKW7 #LiveKW8 #LiveKW9 #LiveKW10 #LiveKW11 #LiveKW12 #LiveKW13 #LiveKW14 #LiveKW15 #LiveKW16 #LiveKW17 #LiveKW18 #LiveKW19 #LiveKW20"
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
