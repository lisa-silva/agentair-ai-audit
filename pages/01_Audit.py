import google.generativeai as genai
from utils.storage import save_audit
import streamlit as st
from utils.scraper import fetch_website_content, extract_text
from utils.analyzer import check_schema_markup, check_entity_coverage, calculate_visibility_score, generate_recommendations
from utils.pdf_generator import generate_pdf
import os

st.set_page_config(page_title="AgentAir AI Audit", layout="centered")

st.title("🔍 AgentAir AI Visibility Audit")
st.markdown("Enter a business website to see how visible it is to AI search (Siri, Gemini, ChatGPT).")

with st.form("audit_form"):
    business_name = st.text_input("Business Name", placeholder="e.g., Joe's Plumbing")
    url = st.text_input("Website URL", placeholder="https://example.com")
    submitted = st.form_submit_button("Run Audit")

if submitted and url:
    with st.spinner("Analyzing website..."):
        soup, error = fetch_website_content(url)
        
        if error:
            st.error(f"Failed to fetch website: {error}")
        else:
            text = extract_text(soup)
            schema_result = check_schema_markup(soup)
            
            # ═══════════════════════════════════════════════════════════════
            # DYNAMIC AI KEYWORD ENGINE
            # ═══════════════════════════════════════════════════════════════
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                prompt = f"""
                You are an expert SEO analyst. The user is auditing a business named "{business_name}".
                Identify their likely industry. 
                Generate a list of exactly 8 highly relevant keywords, core services, or trust signals that MUST be on their website for AI to understand them.
                Return ONLY a comma-separated list of words. No intro, no bullet points, no extra text.
                """
                response = model.generate_content(prompt)
                
                entities = [word.strip().lower() for word in response.text.split(',')]
                
                if len(entities) < 4:
                    entities = ["services", "about us", "contact", "pricing", "reviews", "team", "location", "guarantee"]
                    
            except Exception as e:
                st.error(f"🚨 AI Engine Error: {e}")
                entities = ["services", "about us", "contact", "pricing", "reviews", "team", "location", "guarantee"]
            # ═══════════════════════════════════════════════════════════════
            entity_coverage = check_entity_coverage(text, entities)
            
            score = calculate_visibility_score(schema_result, entity_coverage, len(text))
            recommendations = generate_recommendations(schema_result, entity_coverage)
            
            st.success("Audit complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("AI Visibility Score", f"{score}/100")
            with col2:
                st.metric("Schema Detected", "Yes" if schema_result["found"] else "No")
            
            st.subheader("📋 Key Findings")
            for entity, found in entity_coverage.items():
                st.write(f"{entity}: {'✅' if found else '❌'}")
            
            st.subheader("💡 Recommendations")
            for rec in recommendations:
                st.write(f"• {rec}")
            # Save the audit
            save_audit(business_name, url, score, recommendations)  
            st.success("✅ Audit saved to dashboard!")  
            pdf_file = generate_pdf(business_name, url, score, recommendations)
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download PDF Report", f, file_name=f"{business_name}_audit.pdf")
