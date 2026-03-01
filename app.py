import streamlit as st

st.set_page_config(
    page_title="AgentAir",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🛡️ AgentAir")
st.markdown("Welcome to AgentAir — your AI visibility toolkit.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("🔍 Audit Tool")
        st.markdown("Check if your website is visible to AI search.")
        if st.button("Run an Audit →", key="audit_btn", use_container_width=True):
            st.switch_page("pages/01_Audit.py")

with col2:
    with st.container(border=True):
        st.subheader("🛠️ Schema Fixer")
        st.markdown("Generate proper schema markup for your business.")
        if st.button("Fix Your Site →", key="schema_btn", use_container_width=True):
            st.switch_page("pages/02_Schema_Fixer.py")

st.markdown("---")

# Dashboard link
col3, col4, col5 = st.columns([1, 2, 1])
with col4:
    if st.button("📊 View Your Dashboard", use_container_width=True):
        st.switch_page("pages/03_Dashboard.py")

st.markdown("---")
st.caption("© 2026 AgentAir. Built for local businesses.")