import streamlit as st
from modules.authentication import authenticate
from database.db_connection import query_df
from pathlib import Path

st.set_page_config(page_title="MediAnalytics Pro", page_icon="🏥", layout="wide")
st.markdown(Path("assets/style.css").read_text(), unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

with st.sidebar:
    st.markdown("# 🏥 MediAnalytics Pro")
    st.caption("Hospital operational intelligence")
    if st.session_state.user:
        st.success(f"{st.session_state.user['username']} · {st.session_state.user['role']}")
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        st.markdown("### Sign in")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", type="primary", use_container_width=True):
            try:
                user = authenticate(username, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            except Exception as exc:
                st.error(f"Database connection error: {exc}")

st.title("MediAnalytics Pro")
st.caption("HOSPITAL PATIENT DATA ANALYSIS & OPERATIONAL INTELLIGENCE")
if not st.session_state.user:
    st.info("Sign in to access the hospital analytics workspace.")
    st.markdown("Use the setup instructions in README.md to create your first administrator.")
    st.stop()

st.markdown("Use the navigation menu to open the modules.")
st.write("All records in this educational project should be synthetic. Do not enter real patient information.")
st.page_link("pages/1_Dashboard.py", label="Open Executive Dashboard", icon="📊")
