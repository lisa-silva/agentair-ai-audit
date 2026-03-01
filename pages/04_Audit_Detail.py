import streamlit as st
from utils.storage import get_audit_by_id

st.set_page_config(page_title="Audit Details", layout="centered")

# Back button
if st.button("← Back to Dashboard"):
    st.switch_page("pages/03_Dashboard.py")

# Get audit ID from session state
audit_id = st.session_state.get("selected_audit_id", None)

if not audit_id:
    st.error("No audit selected.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/03_Dashboard.py")
    st.stop()

# Load audit data
audit = get_audit_by_id(audit_id)

if not audit:
    st.error("Audit not found.")
    st.stop()

# Display audit details
st.title(f"🔍 {audit['business_name']}")
st.caption(f"Audited on {audit['timestamp'][:10]}")

col1, col2 = st.columns(2)
with col1:
    st.metric("AI Visibility Score", f"{audit['score']}/100")
with col2:
    st.markdown(f"**Website:** {audit['url']}")

st.markdown("---")
st.subheader("📋 Key Findings")

# Entity findings would need to be stored separately
# For now, show recommendations
st.subheader("💡 Recommendations")
for rec in audit['recommendations']:
    st.write(f"• {rec}")

st.markdown("---")

# Option to run a new audit or fix
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Run New Audit", use_container_width=True):
        st.switch_page("pages/01_Audit.py")
with col2:
    if st.button("🛠️ Fix These Issues", use_container_width=True):
        st.session_state.audit_business_name = audit['business_name']
        st.session_state.audit_website = audit['url']
        st.switch_page("pages/02_Schema_Fixer.py")