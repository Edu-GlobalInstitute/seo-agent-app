import streamlit as st
import json
from researcher import execute_autonomous_research
from analyzer import generate_ultimate_json
from seo_metrics import get_realtime_click_data # NEW IMPORT

st.set_page_config(page_title="Edu Global: Traffic Engine", layout="wide")

st.title("🚀 Edu Global: Real-Time Traffic & Content Engine")

with st.form("enterprise_form"):
    topic = st.text_input("Target Topic (e.g., AP Calculus BC Exam Prep):")
    zone = st.text_input("Target Audience/Zone (e.g., High School Students in the US):")
    submit = st.form_submit_button("Execute Traffic-Optimized Analysis")

if submit and topic and zone:
    with st.status("Executing Traffic & Competitor Analysis...", expanded=True) as status:
        
        st.write("📈 Phase 1: Pulling Real-Time Google Click Data (SerpApi)...")
        seo_intelligence, questions = get_realtime_click_data(topic)
        
        st.write("🔍 Phase 2: Auto-Crawling Competitor Infrastructure...")
        links, scraped_data = execute_autonomous_research(topic, zone)
        
        st.write("🧠 Phase 3: Engineering Click-Optimized HTML & JSON...")
        
        try:
            # Pass BOTH competitor data AND real-time SEO traffic data to the AI
            data = generate_ultimate_json(topic, zone, scraped_data, seo_intelligence)
            status.update(label="Workflow Complete!", state="complete", expanded=False)
            
            st.success("✅ High-CTR Content Engineered Successfully!")
            
            tab_strat, tab_content, tab_meta = st.tabs(["📊 Traffic Strategy", "📄 HTML Article", "🔍 SEO Metadata"])
            
            with tab_strat:
                st.info("**Traffic Acquisition Strategy:**\n\n" + data["strategic_analysis"]["competitor_traffic_gap"])
            with tab_content:
                st.code(data["article_html"], language="html")
                with st.expander("Preview Visual Render"):
                    st.markdown(data["article_html"], unsafe_allow_html=True)
            with tab_meta:
                st.write(f"**Meta Title:** {data['seo_metadata']['meta_title']}")
                st.write(f"**Targeted Keywords:** {data['seo_metadata']['target_keywords']}")
                st.json(data) # Raw JSON download available here

        except Exception as e:
            st.error(f"System Error: {e}")
