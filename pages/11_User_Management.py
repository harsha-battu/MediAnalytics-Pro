import streamlit as st
from modules.authentication import require_role,hash_password
from database.db_connection import query_df,execute
require_role("Admin")
st.title("User Management")
with st.form("newuser"):
    username=st.text_input("Username")
    password=st.text_input("Temporary password",type="password")
    role=st.selectbox("Role",["Admin","Staff","Analyst"])
    if st.form_submit_button("Create user"):
        if len(password)<10: st.error("Use a password with at least 10 characters.")
        elif not username.strip(): st.error("Username is required.")
        else:
            try:
                execute("INSERT INTO users(username,password_hash,role) VALUES(:u,:p,:r)",
                        {"u":username.strip(),"p":hash_password(password),"r":role})
                st.success("User created.")
            except Exception as e: st.error(f"Could not create user: {e}")
try: st.dataframe(query_df("SELECT user_id,username,role,active,created_at FROM users"),use_container_width=True,hide_index=True)
except Exception as e: st.error(f"Database error: {e}")
