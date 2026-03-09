import streamlit as st

# 1. PAGE CONFIG MUST BE VERY FIRST
st.set_page_config(
    page_title="AgentAir Suite",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════
# 2. THE GATEKEEPER — Access Key Authentication
# ═══════════════════════════════════════════════════════════════

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h1>⚡ AgentAir Intelligence Suite</h1>
        <p style="color: #888; font-size: 1.1rem; margin: 20px 0;">Enter your agency access key to begin</p>
    </div>
    """, unsafe_allow_html=True)
    
    access_key = st.text_input(
        "Access Key",
        type="password",
        placeholder="Enter your access key",
        label_visibility="collapsed"
    )
    
    if st.button("Unlock", use_container_width=True):
        if access_key == "ALIEN-2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Invalid access key. Check your email for the correct key.")
    
    st.stop() # Stops the rest of the app from loading if not unlocked

# ═══════════════════════════════════════════════════════════════
# 3. THE HUB (Runs only if unlocked)
# ═══════════════════════════════════════════════════════════════

st.title("🛡️ AgentAir Command Center")
st.markdown("Wholesale AI Search Infrastructure. Select a module below.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("🔍 Audit Tool")
        st.markdown("Run Parse-First schema audits on client domains.")
        if st.button("Run an Audit →", key="audit_btn", use_container_width=True):
            st.switch_page("pages/01_Audit.py")

with col2:
    with st.container(border=True):
        st.subheader("🛠️ Schema Fixer")
        st.markdown("Generate precise JSON-LD markup for local businesses.")
        if st.button("Fix Your Site →", key="schema_btn", use_container_width=True):
            st.switch_page("pages/02_Schema_Fixer.py")

# Dashboard link
col3, col4, col5 = st.columns([1, 2, 1])
with col4:
    if st.button("📊 View Agency Dashboard", use_container_width=True):
        st.switch_page("pages/03_Dashboard.py")
        
st.markdown("---")
st.caption("© 2026 AgentAir. Built for Marketing Agencies.")
