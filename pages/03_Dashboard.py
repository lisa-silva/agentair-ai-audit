import streamlit as st
import pandas as pd
from datetime import datetime
from utils.storage import load_all_audits
import plotly.express as px

st.set_page_config(page_title="AgentAir Dashboard", layout="wide")

# Back button
if st.button("← Back to Home"):
    st.switch_page("app.py")

st.title("📊 Your Audit Dashboard")
st.markdown("View all your past AI visibility audits.")

# Load all audits
audits = load_all_audits()

if not audits:
    st.info("No audits yet. Run your first audit to get started!")
    if st.button("🔍 Run an Audit Now"):
        st.switch_page("pages/01_Audit.py")
    st.stop()

# Convert to DataFrame for easy manipulation
df = pd.DataFrame(audits)
df['date'] = pd.to_datetime(df['timestamp']).dt.date

# Top metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Audits", len(audits))
with col2:
    avg_score = df['score'].mean()
    st.metric("Average Score", f"{avg_score:.0f}/100")
with col3:
    latest_score = df.iloc[0]['score'] if not df.empty else 0
    st.metric("Latest Score", f"{latest_score}/100")
with col4:
    businesses = df['business_name'].nunique()
    st.metric("Unique Businesses", businesses)

st.markdown("---")

# Score trend over time
if len(audits) > 1:
    st.subheader("📈 Score Trend")
    fig = px.line(df, x='timestamp', y='score', title='Visibility Scores Over Time',
                  labels={'timestamp': 'Date', 'score': 'Score'})
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Audit history table
st.subheader("📋 Audit History")

# Format for display
display_df = df[['date', 'business_name', 'url', 'score']].copy()
display_df.columns = ['Date', 'Business', 'Website', 'Score']

# Add view button for each row
for idx, row in display_df.iterrows():
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 1, 1])
        
        with col1:
            st.write(row['Date'])
        with col2:
            st.write(row['Business'])
        with col3:
            st.write(row['Website'])
        with col4:
            score_color = "🟢" if row['Score'] >= 70 else "🟡" if row['Score'] >= 40 else "🔴"
            st.write(f"{score_color} {row['Score']}")
        with col5:
            if st.button("View", key=f"view_{idx}"):
                st.session_state.selected_audit_id = audits[idx]['id']
                st.switch_page("pages/04_Audit_Detail.py")

# Export option
st.markdown("---")
if st.button("📥 Export All Audits as CSV"):
    csv = df.to_csv(index=False)
    st.download_button(
        "Download CSV",
        csv,
        file_name="agentair_audits.csv",
        mime="text/csv"
    )