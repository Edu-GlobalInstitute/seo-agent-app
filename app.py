import streamlit as st
import json
# Import your custom modules
from researcher import execute_autonomous_research
from analyzer import generate_ultimate_json

st.set_page_config(page_title="Edu Global: Autonomous SEO Agent", page_icon="🚀", layout="wide")

st.title("🚀 Edu Global: Autonomous Competitor & Content Engine")
st.markdown("Zero-click architecture: Auto-discovers top competitors, deep-crawls their websites simultaneously, and engineers API-ready content.")

with st.form("enterprise_form"):
    topic = st.text_input("Target Topic (e.g., AP Calculus BC Exam Prep):")
    zone = st.text_input("Target Audience/Zone (e.g., High School Students in the US):")
    # Notice: No manual URL input needed anymore! The agent does it automatically.
    submit = st.form_submit_button("Execute Autonomous Analysis")

if submit and topic and zone:
    with st.status("Executing Multi-Level Agent Workflow...", expanded=True) as status:
        st.write("🔍 Phase 1: Auto-Discovering and Deep-Crawling Top Competitors...")
        
        # Calling the new autonomous function from researcher.py
        links, scraped_data = execute_autonomous_research(topic, zone)
        
        if links:
            st.write(f"✅ Phase 1 Complete: Successfully auto-crawled {len(links)} top ranking sites in parallel.")
        else:
            st.write("⚠️ Phase 1 Notice: Live crawl blocked or no targets found. Relying on elite internal AI market data.")
            
        st.write("🧠 Phase 2: Analyzing strategic gaps against competitors...")
        st.write("✍️ Phase 3: Engineering HTML, Socials, and Meta Data...")
        
        try:
            # Call the AI analyzer module 
            data = generate_ultimate_json(topic, zone, scraped_data)
            status.update(label="Workflow Complete!", state="complete", expanded=False)
            
            # --- UI DASHBOARD ---
            st.success("✅ Content Engineered Successfully!")
            st.markdown("---")
            
            tab_strat, tab_content, tab_social, tab_meta, tab_json = st.tabs([
                "📊 Competitor Strategy", "📄 HTML Article", "📱 Social Media", "🔍 SEO Metadata", "⚙️ Raw JSON"
            ])
            
            with tab_strat:
                st.subheader("Deep Competitor Gap Analysis")
                st.info("**Market Comparison:**\n\n" + data["strategic_analysis"]["competitor_comparison"])
                st.warning("**Actionable Missing Gap:**\n\n" + data["strategic_analysis"]["our_missing_gap"])

            with tab_content:
                st.subheader("Elite HTML Article (Body Only)")
                st.code(data["article_html"], language="html")
                with st.expander("Preview Visual Render"):
                    st.markdown(data["article_html"], unsafe_allow_html=True)
                    
            with tab_social:
                st.subheader("LinkedIn Post")
                st.markdown(data["linkedin_post"])
                st.divider()
                st.subheader("Instagram Caption")
                st.markdown(data["instagram_caption"])
                
            with tab_meta:
                st.subheader("Website Metadata")
                st.write(f"**URL Slug:** `/{data['seo_metadata']['url_slug']}`")
                st.write(f"**Meta Title:** {data['seo_metadata']['meta_title']}")
                st.write(f"**Meta Description:** {data['seo_metadata']['meta_description']}")
                st.write(f"**Keywords:** {data['seo_metadata']['target_keywords']}")
                
            with tab_json:
                st.subheader("System-Ready JSON Data")
                st.json(data)
                st.download_button(
                    label="Download Enterprise JSON",
                    file_name=f"edu_global_{data['seo_metadata']['url_slug']}.json",
                    mime="application/json",
                    data=json.dumps(data, indent=2)
                )

        except Exception as e:
            error_message = str(e)
            status.update(label="Error in Generation", state="error")
            
            if "429" in error_message or "Quota" in error_message:
                st.error("⏳ **Free Tier Speed Limit Reached!** Google's API requires a brief pause. Please wait exactly 60 seconds and click Generate again.")
            else:
                st.error(f"System Error: {e}")
                st.info("If you still see an error, the AI response might have been too long to parse perfectly. Try a slightly narrower topic.")
