import bcrypt
import streamlit as st
from database.db_connection import query_df, execute

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except (ValueError, TypeError):
        return False

def authenticate(username, password):
    users = query_df(
        "SELECT user_id, username, password_hash, role FROM users WHERE username=:u AND active=1",
        {"u": username}
    )
    if users.empty or not verify_password(password, users.iloc[0]["password_hash"]):
        return None
    row = users.iloc[0]
    execute("INSERT INTO audit_logs(user_id, action) VALUES(:uid, :act)",
            {"uid": int(row.user_id), "act": "Successful login"})
    return {"user_id": int(row.user_id), "username": row.username, "role": row.role}

def require_role(*roles):
    user = st.session_state.get("user")
    if not user:
        st.warning("Please log in.")
        st.stop()
    if roles and user["role"] not in roles:
        st.error("You do not have permission to access this section.")
        st.stop()
